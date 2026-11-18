#!/usr/bin/env python3
"""Copy the four portable skills to an explicit destination without overwriting."""

import argparse
import shutil
import sys
import tempfile
from pathlib import Path


SKILLS = (
    "cann-op-develop",
    "cann-op-review",
    "cann-op-env-check",
    "cann-op-submit",
)


def install(destination, dry_run=False):
    source = Path(__file__).resolve().parent
    destination = Path(destination).expanduser().resolve()
    if destination.exists() and not destination.is_dir():
        raise ValueError("Destination is not a directory: {}".format(destination))
    for name in SKILLS:
        origin = source / name
        if not (origin / "SKILL.md").is_file():
            raise ValueError("Incomplete source skill: {}".format(origin))
        if any(path.is_symlink() for path in origin.rglob("*")) or origin.is_symlink():
            raise ValueError("Source skills must contain regular files: {}".format(origin))
        target = destination / name
        if target.exists() or target.is_symlink():
            raise FileExistsError("Refusing to overwrite existing target: {}".format(target))
    if destination == source or source in destination.parents:
        raise ValueError("Destination must be outside this source package")
    for name in SKILLS:
        print("{} -> {}".format(source / name, destination / name))
    if dry_run:
        print("Dry run: no files written.")
        return
    destination.mkdir(parents=True, exist_ok=True)
    # Stage all copies before creating any final skill directory. mkdir below
    # refuses targets that appeared since preflight, including dangling links.
    created = []
    with tempfile.TemporaryDirectory(prefix=".cann-op-install-", dir=destination) as temp:
        staging = Path(temp)
        for name in SKILLS:
            shutil.copytree(source / name, staging / name)
        try:
            for name in SKILLS:
                target = destination / name
                target.mkdir()
                created.append(target)
                for child in (staging / name).iterdir():
                    child.rename(target / child.name)
        except OSError:
            for target in reversed(created):
                shutil.rmtree(target)
            raise
    print("Installed {} skills. Reload skills in your client.".format(len(SKILLS)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", required=True, help="Client skill directory")
    parser.add_argument("--dry-run", action="store_true", help="Check paths without writing")
    args = parser.parse_args()
    try:
        install(args.dest, args.dry_run)
    except (OSError, ValueError) as error:
        print("Installation failed: {}".format(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
