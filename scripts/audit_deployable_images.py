#!/usr/bin/env python3
"""Fail closed unless every enabled catalog image uses a reviewed version tag."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_ROOTS = (
    REPO_ROOT / "templates",
    REPO_ROOT / "infra-templates",
    REPO_ROOT / "project-templates",
)
LOCK_PATH = REPO_ROOT / "catalog-images.json"
IMAGE_PATTERN = re.compile(r"^\s*image:\s*(['\"]?)([^'\"#\s]+)\1\s*(?:#.*)?$")
VERSION_TAG_PATTERN = re.compile(
    r"^ghcr\.io/pasturestack/[a-z0-9][a-z0-9._-]*:"
    r"v?\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$"
)
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")


def blocker(message: str, failures: list[str]) -> None:
    failures.append(message)


def main() -> int:
    failures: list[str] = []
    data = json.loads(LOCK_PATH.read_text(encoding="utf-8"))

    if data.get("schemaVersion") != 1:
        blocker("catalog-images.json schemaVersion must be 1", failures)

    allowed_prefixes = tuple(data.get("allowedRegistryPrefixes", ()))
    if not allowed_prefixes:
        blocker("catalog-images.json must define allowedRegistryPrefixes", failures)

    locked: dict[str, dict[str, object]] = {}
    for item in data.get("images", ()):
        reference = item.get("reference", "")
        if not isinstance(reference, str) or not VERSION_TAG_PATTERN.fullmatch(reference):
            blocker(f"invalid locked image reference: {reference!r}", failures)
            continue
        if reference in locked:
            blocker(f"duplicate locked image reference: {reference}", failures)
        locked[reference] = item
        if not reference.startswith(allowed_prefixes):
            blocker(f"registry is not allowed: {reference}", failures)
        if reference.endswith(":latest") or "@" in reference:
            blocker(f"only semantic version tags are permitted: {reference}", failures)
        if not COMMIT_PATTERN.fullmatch(str(item.get("sourceCommit", ""))):
            blocker(f"sourceCommit must be a full SHA for: {reference}", failures)
        if not str(item.get("sourceRepository", "")).startswith("https://github.com/"):
            blocker(f"sourceRepository must be an HTTPS GitHub URL for: {reference}", failures)
        scan = item.get("vulnerabilityScan", {})
        if not isinstance(scan, dict) or scan.get("high") != 0 or scan.get("critical") != 0:
            blocker(f"HIGH and CRITICAL findings must both be zero for: {reference}", failures)

    discovered: list[tuple[Path, int, str]] = []
    template_count = 0
    for root in TEMPLATE_ROOTS:
        if not root.exists():
            continue
        template_count += sum(1 for path in root.glob("*/config.yml") if path.is_file())
        compose_files = sorted(root.glob("**/docker-compose.y*ml"))
        compose_files.extend(sorted(root.glob("**/docker-compose.y*ml.tpl")))
        for path in compose_files:
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if "image:" not in line:
                    continue
                match = IMAGE_PATTERN.fullmatch(line)
                relative = path.relative_to(REPO_ROOT)
                if not match:
                    blocker(f"dynamic or malformed image at {relative}:{line_number}", failures)
                    continue
                reference = match.group(2)
                discovered.append((relative, line_number, reference))
                if not VERSION_TAG_PATTERN.fullmatch(reference):
                    blocker(f"image must use a semantic version tag at {relative}:{line_number}: {reference}", failures)
                elif reference not in locked:
                    blocker(f"image is absent from catalog-images.json at {relative}:{line_number}: {reference}", failures)

    if template_count == 0:
        blocker("the current catalog must contain at least one reviewed template", failures)
    if not discovered:
        blocker("the current catalog contains no image references", failures)

    used = {reference for _, _, reference in discovered}
    for reference in sorted(set(locked) - used):
        blocker(f"unused image lock entry: {reference}", failures)

    for failure in failures:
        print(f"BLOCKER {failure}")
    print(f"template_count={template_count}")
    print(f"image_reference_count={len(discovered)}")
    print(f"locked_image_count={len(locked)}")
    print(f"deployable_image_blocker_count={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
