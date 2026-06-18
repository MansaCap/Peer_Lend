import uvicorn


def start() -> None:
    uvicorn.run("src.api:app", host="127.0.0.1", port=8001, reload=True)
