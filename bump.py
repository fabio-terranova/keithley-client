import os
import re
import sys
from pathlib import Path


def bump_version(version: str, part: str) -> str:
    major, minor, patch = map(int, version.split("."))
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        raise ValueError("Invalid part. Use 'major', 'minor', or 'patch'.")
    return f"{major}.{minor}.{patch}"


def update_pyproject(version: str):
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    content = re.sub(r'version\s*=\s*".*?"', f'version = "{version}"', content)
    pyproject_path.write_text(content)


def update_init(version: str):
    init_path = Path("src/keithley_client/__init__.py")
    content = init_path.read_text()
    content = re.sub(r'__version__\s*=\s*".*?"', f'__version__ = "{version}"', content)
    init_path.write_text(content)


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in {"major", "minor", "patch"}:
        print("Usage: python bump.py [major|minor|patch]")
        sys.exit(1)

    part = sys.argv[1]

    # Read current version from pyproject.toml
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    current_version = re.search(r'version\s*=\s*"(.*?)"', content).group(1)

    # Bump version
    new_version = bump_version(current_version, part)

    # Update files
    update_pyproject(new_version)
    update_init(new_version)

    print(f"Bumped version from {current_version} to {new_version}")

    # Commit changes
    os.system("git add pyproject.toml src/keithley_client/__init__.py")
    os.system(f'git commit -m "chore: bump version to {new_version}"')


if __name__ == "__main__":
    main()
