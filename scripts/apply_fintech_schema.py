import os
from pathlib import Path
from urllib.parse import quote_plus

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


def read_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def mysql_server_url() -> str:
    user = os.getenv("MYSQL_USER", "root")
    password = quote_plus(os.getenv("MYSQL_PASSWORD", ""))
    host = os.getenv("MYSQL_HOST", "127.0.0.1")
    port = os.getenv("MYSQL_PORT", "3306")
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/"


def execute_sql_script(conn, sql_text: str) -> None:
    statements = [stmt.strip() for stmt in sql_text.split(";") if stmt.strip()]
    for statement in statements:
        conn.execute(text(statement))


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    read_dotenv(repo_root / ".env")

    db_name = os.getenv("MYSQL_DATABASE", "fintech")
    engine = create_engine(mysql_server_url(), future=True)

    root_db_scripts = [
        repo_root / "db" / "Collateral_Table.sql",
        repo_root / "db" / "repayments_table.sql",
        repo_root / "db" / "borrower_payback_status_table.sql",
    ]
    nested_schema = repo_root / "github" / "PeerLending" / "db" / "schema.sql"

    try:
        with engine.begin() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
            conn.execute(text(f"USE {db_name}"))

            # Parent tables required by foreign keys in your scripts.
            conn.execute(
                text(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INT AUTO_INCREMENT PRIMARY KEY,
                        email VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
            )
            conn.execute(
                text(
                    """
                    CREATE TABLE IF NOT EXISTS loans (
                        loan_id INT AUTO_INCREMENT PRIMARY KEY,
                        borrower_id INT NOT NULL,
                        principal_amount DECIMAL(12,2) NOT NULL,
                        status ENUM('open','closed','defaulted') DEFAULT 'open',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        CONSTRAINT fk_loans_borrower FOREIGN KEY (borrower_id) REFERENCES users(user_id)
                    )
                    """
                )
            )

            if nested_schema.exists():
                execute_sql_script(conn, nested_schema.read_text(encoding="utf-8"))

            for script in root_db_scripts:
                if script.exists():
                    execute_sql_script(conn, script.read_text(encoding="utf-8"))

            rows = conn.execute(
                text(
                    """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = :schema
                    ORDER BY table_name
                    """
                ),
                {"schema": db_name},
            ).fetchall()
    except SQLAlchemyError as exc:
        print("Failed to apply schema.")
        print("Check MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE in .env")
        print(f"Error: {exc}")
        raise SystemExit(1)

    print(f"Schema applied to '{db_name}'.")
    print("Tables now present:")
    for row in rows:
        print(f" - {row[0]}")


if __name__ == "__main__":
    main()