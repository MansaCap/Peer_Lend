import uvicorn


def start() -> None:
    uvicorn.run(
        "peer_lending_backend.src.app.main:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
    )
