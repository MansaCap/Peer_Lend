import sys
import os
from pathlib import Path

# Base scaffold structure
STRUCTURE = {
    "config": ["settings.yaml", "schema.json", "secrets.yaml"],
    "src/api": ["__init__.py", "payback.py"],
    "src/services": ["__init__.py", "scoring.py"],
    "src/models": ["__init__.py", "borrower.py"],
    "src/utils": ["__init__.py", "config_loader.py"],
    "tests": ["test_payback.py", "test_utils.py"],
    "db/migrations": ["init.sql"],
    "db": ["schema.sql"],
    "docs": ["architecture.md", "api-spec.md"],
    "": ["main.py", "requirements.txt", "README.md", ".gitignore", "docker-compose.yaml"]
}

def create_scaffold(base_dir: Path):
    for folder, files in STRUCTURE.items():
        folder_path = base_dir / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        for file in files:
            file_path = folder_path / file
            if not file_path.exists():
                with open(file_path, "w") as f:
                    if file.endswith(".py"):
                        f.write("# " + file + "\n")
                    elif file.endswith(".yaml"):
                        f.write("# " + file + " configuration\n")
                    elif file.endswith(".json"):
                        f.write("{}\n")
                    elif file.endswith(".md"):
                        f.write("# " + file.replace(".md", "").title() + "\n")
                    elif file.endswith(".sql"):
                        f.write("-- SQL scaffold for " + file + "\n")
                    else:
                        f.write("")
                print(f"Created {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python init_project.py <ProjectName>")
        sys.exit(1)

    project_name = sys.argv[1]
    base_dir = Path(project_name)
    base_dir.mkdir(exist_ok=True)

    create_scaffold(base_dir)
    print(f"\n✅ Project scaffold created at {base_dir.resolve()}")
