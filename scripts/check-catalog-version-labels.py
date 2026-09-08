#!/usr/bin/env python3
"""Validate user-facing Catalog version labels without parsing image tags."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CURRENT_VERSION = re.compile(r"v\d+\.\d+\.\d+")
BANNED_LABEL_PARTS = ("pasturestack", "windows-ltsc")


def _unquote(value: str) -> str:
    value = value.split("#", 1)[0].strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    return value


def _config_version(path: Path) -> str:
    match = re.search(r"(?m)^version:\s*(.+?)\s*$", path.read_text(encoding="utf-8"))
    if match is None:
        raise AssertionError(f"missing top-level version: {path.relative_to(ROOT)}")
    return _unquote(match.group(1))


def _catalog_version(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    catalog = re.search(r"(?ms)^\.catalog:\s*$\n(?P<body>(?:^[ \t]+.*(?:\n|$))*)", text)
    if catalog is None:
        raise AssertionError(f"missing .catalog block: {path.relative_to(ROOT)}")
    match = re.search(r"(?m)^\s+version:\s*(.+?)\s*$", catalog.group("body"))
    if match is None:
        raise AssertionError(f"missing .catalog.version: {path.relative_to(ROOT)}")
    return _unquote(match.group(1))


def main() -> None:
    templates = []
    for catalog_root in (ROOT / "infra-templates", ROOT / "project-templates"):
        templates.extend(path.parent for path in catalog_root.glob("*/config.yml"))

    if not templates:
        raise AssertionError("no Catalog templates found")

    for template in sorted(templates):
        config_version = _config_version(template / "config.yml")
        relative = template.relative_to(ROOT)
        if CURRENT_VERSION.fullmatch(config_version) is None:
            raise AssertionError(
                f"current version must be a plain vMAJOR.MINOR.PATCH label: "
                f"{relative}={config_version!r}")

        version_dirs = sorted(
            (path for path in template.iterdir()
             if (path.is_dir() and path.name.isdecimal()
                 and (path / "rancher-compose.yml").is_file())),
            key=lambda path: int(path.name))
        if not version_dirs:
            raise AssertionError(f"no numeric version directories: {relative}")

        labels = [
            _catalog_version(path / "rancher-compose.yml")
            for path in version_dirs
        ]
        if len(labels) != len(set(labels)):
            raise AssertionError(f"duplicate visible versions: {relative}={labels!r}")
        if labels[-1] != config_version:
            raise AssertionError(
                f"default version does not match latest directory: "
                f"{relative} config={config_version!r} latest={labels[-1]!r}")

        for label in labels:
            lowered = label.casefold()
            banned = [part for part in BANNED_LABEL_PARTS if part in lowered]
            if banned:
                raise AssertionError(
                    f"implementation detail in visible version: "
                    f"{relative}={label!r} banned={banned!r}")

    print(f"CATALOG_VERSION_LABELS_OK templates={len(templates)}")


if __name__ == "__main__":
    main()
