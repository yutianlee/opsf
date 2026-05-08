"""Check that a release tag matches the package version."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

TAG_PATTERN = re.compile(r"^v(?P<release>\d+\.\d+\.\d+)(?:-alpha\.(?P<alpha>\d+))?$")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("release_ref", help="Release tag or refs/tags/... ref to compare")
    parser.add_argument("--pyproject", default="pyproject.toml", help="Path to pyproject.toml")
    args = parser.parse_args()

    try:
        package_version = read_project_version(Path(args.pyproject))
        tag_version = pep440_from_release_ref(args.release_ref)
    except ValueError as exc:
        print(f"release version check failed: {exc}", file=sys.stderr)
        return 2

    if tag_version != package_version:
        print(
            "release version check failed: "
            f"tag {args.release_ref!r} maps to package version {tag_version!r}, "
            f"but pyproject.toml declares {package_version!r}",
            file=sys.stderr,
        )
        return 1

    print(f"release version check passed: {args.release_ref} -> {package_version}")
    return 0


def read_project_version(pyproject_path: Path) -> str:
    in_project = False
    for raw_line in pyproject_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            in_project = line == "[project]"
            continue
        if in_project:
            match = re.fullmatch(r'version\s*=\s*"([^"]+)"', line)
            if match:
                return match.group(1)
    raise ValueError(f"could not find [project] version in {pyproject_path}")


def pep440_from_release_ref(release_ref: str) -> str:
    tag = release_ref.removeprefix("refs/tags/")
    match = TAG_PATTERN.fullmatch(tag)
    if match is None:
        raise ValueError(
            f"release ref {release_ref!r} is not a supported tag; "
            "expected vX.Y.Z or vX.Y.Z-alpha.N"
        )
    version = match.group("release")
    alpha = match.group("alpha")
    if alpha is not None:
        return f"{version}a{alpha}"
    return version


if __name__ == "__main__":
    raise SystemExit(main())
