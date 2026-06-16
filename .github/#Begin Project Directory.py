"""Create the Peer_Lend project scaffold.

This helper is intentionally idempotent so it can be rerun safely when the
branch path changes or when future folders need to be recreated.
"""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DIRECTORIES = (
    PROJECT_ROOT / "Pulse",
    PROJECT_ROOT / "Ancla",
    PROJECT_ROOT / "api",
    PROJECT_ROOT / "db",
    PROJECT_ROOT / "docs",
    PROJECT_ROOT / "roadmap",
)


def build_scaffold() -> None:
    for directory in DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    build_scaffold()
    print("Project scaffold verified.")
