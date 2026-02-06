#!/usr/bin/env python3
import pathlib
import tomllib

# Prints the names of all device dependencies defined in pyproject.toml,
# (under [project.optional-dependencies]) separated by commas.
def main() -> None:
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    pyproject_path = repo_root / "pyproject.toml"

    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    extras = data.get("project", {}).get("optional-dependencies", {})

    # Preserve TOML order; include only non-empty lists
    names = [name for name, deps in extras.items() if deps]

    print(",".join(names))


if __name__ == "__main__":
    main()
