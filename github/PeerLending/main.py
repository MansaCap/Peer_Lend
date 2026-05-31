from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from src.utils.config_loader import load_config


config = load_config()
app = FastAPI(title="PeerLending API", version="0.1.0")


@app.get("/health")
def health() -> dict:
	return {
		"status": "ok",
		"database": config.database,
		"db_host": config.host,
		"db_port": config.port,
	}


@app.get("/health/db")
def health_db() -> dict:
	try:
		engine = create_engine(config.sqlalchemy_url, pool_pre_ping=True, future=True)
		with engine.connect() as conn:
			conn.execute(text("SELECT 1"))
		return {"status": "ok", "db_connection": "up"}
	except SQLAlchemyError as exc:
		raise HTTPException(status_code=503, detail=f"Database unavailable: {exc}") from exc
