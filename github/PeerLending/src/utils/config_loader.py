import os
from dataclasses import dataclass
from urllib.parse import quote_plus
import tomllib


def _read_dotenv(path: str) -> None:
	"""Load simple KEY=VALUE pairs into environment without overriding existing values."""
	if not os.path.exists(path):
		return

	with open(path, "r", encoding="utf-8") as handle:
		for raw_line in handle:
			line = raw_line.strip()
			if not line or line.startswith("#") or "=" not in line:
				continue
			key, value = line.split("=", 1)
			key = key.strip()
			value = value.strip().strip('"').strip("'")
			if key and key not in os.environ:
				os.environ[key] = value


def _read_env_toml(path: str) -> None:
	"""Load TOML config into env vars without overriding existing values.

	Supported shapes:
	1) flat: MYSQL_HOST = "127.0.0.1"
	2) section: [mysql] host = "127.0.0.1"
	"""
	if not os.path.exists(path):
		return

	with open(path, "rb") as handle:
		data = tomllib.load(handle)

	mysql_section = data.get("mysql", {}) if isinstance(data, dict) else {}
	mapping = {
		"MYSQL_HOST": mysql_section.get("host", data.get("MYSQL_HOST") if isinstance(data, dict) else None),
		"MYSQL_PORT": mysql_section.get("port", data.get("MYSQL_PORT") if isinstance(data, dict) else None),
		"MYSQL_USER": mysql_section.get("user", data.get("MYSQL_USER") if isinstance(data, dict) else None),
		"MYSQL_PASSWORD": mysql_section.get("password", data.get("MYSQL_PASSWORD") if isinstance(data, dict) else None),
		"MYSQL_DATABASE": mysql_section.get("database", data.get("MYSQL_DATABASE") if isinstance(data, dict) else None),
	}

	for key, value in mapping.items():
		if value is None or key in os.environ:
			continue
		os.environ[key] = str(value)


@dataclass(frozen=True)
class AppConfig:
	host: str
	port: int
	user: str
	password: str
	database: str

	@property
	def sqlalchemy_url(self) -> str:
		encoded_password = quote_plus(self.password)
		return (
			f"mysql+pymysql://{self.user}:{encoded_password}@"
			f"{self.host}:{self.port}/{self.database}"
		)

	@property
	def masked_sqlalchemy_url(self) -> str:
		return f"mysql+pymysql://{self.user}:***@{self.host}:{self.port}/{self.database}"


def load_config() -> AppConfig:
	repo_root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".env"))
	repo_root_env_toml = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".env.toml"))
	_read_dotenv(repo_root_env)
	_read_env_toml(repo_root_env_toml)

	return AppConfig(
		host=os.getenv("MYSQL_HOST", "127.0.0.1"),
		port=int(os.getenv("MYSQL_PORT", "3306")),
		user=os.getenv("MYSQL_USER", "root"),
		password=os.getenv("MYSQL_PASSWORD", ""),
		database=os.getenv("MYSQL_DATABASE", "fintech"),
	)
