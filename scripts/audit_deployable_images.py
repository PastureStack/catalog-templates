#!/usr/bin/env python3
"""Fail closed unless every enabled catalog image uses a reviewed version tag."""

from __future__ import annotations

import json
import hashlib
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
PROVENANCE_PATH = REPO_ROOT / "catalog-provenance.json"
IMAGE_PATTERN = re.compile(r"^\s*image:\s*(['\"]?)([^'\"#\s]+)\1\s*(?:#.*)?$")
DEFAULT_IMAGE_PATTERN = re.compile(r"^\s*default:\s*(['\"]?)(ghcr\.io/[^'\"#\s]+)\1\s*(?:#.*)?$")
LABEL_PATTERN = re.compile(r"^\s+(io\.[^:]+):\s*(['\"]?)(.*?)\2\s*$")
QUESTION_PATTERN = re.compile(r"^\s*-\s+variable:\s*(['\"]?)([A-Za-z0-9_]+)\1\s*$")
TEMPLATE_VERSION_PATTERN = re.compile(
    r"^version:\s*(['\"]?)([^'\"#\s]+)\1\s*$",
    re.MULTILINE,
)
CATALOG_VERSION_PATTERN = re.compile(
    r"^  version:\s*(['\"]?)([^'\"#\s]+)\1\s*$",
    re.MULTILINE,
)
VERSION_TAG_PATTERN = re.compile(
    r"^ghcr\.io/pasturestack/[a-z0-9][a-z0-9._-]*:"
    r"v?\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$"
)
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
EXPECTED_INFRA_TEMPLATE_COUNT = 22
EXPECTED_QUESTION_COUNT = 171
NON_TAIWAN_TERMS = (
    "審計",
    "日志",
    "軟件",
    "信息",
    "默認",
    "服務器",
    "文件夾",
    "網絡",
    "支持",
    "添加",
    "配置文件",
)
RETAINED_VERSION_LAYOUTS = {
    "network-diagnostics": ("1", "2"),
    "network-policy-manager": ("1", "2"),
    "secret-volume-driver": ("1", "2"),
}
RETAINED_VERSION_HASHES = {
    "infra-templates/network-diagnostics/1/README.md": "16e864645e5aa96e007d399b805d94576a4750a25e3bd27437fa2eecefe83baf",
    "infra-templates/network-diagnostics/1/docker-compose.yml.tpl": "875b3eb705b908510a3ebcfeecf3451a49fc03a3c32fd4010eb25622049def97",
    "infra-templates/network-diagnostics/1/rancher-compose.yml": "e881c61014e2fc2036e681fe1e0789e14ecb70299a55ae134a72bcd13a6a6dc1",
    "infra-templates/network-policy-manager/1/README.md": "0011d724fc562bb947eaf84855972a67e5a7dfdaff983ada005ba228b6bf7e28",
    "infra-templates/network-policy-manager/1/docker-compose.yml": "14def5ee298c2b7235ee37cbea701dd1d851e1c0ed889fc00643718d67ff37a7",
    "infra-templates/network-policy-manager/1/rancher-compose.yml": "1738f74873162f591c694914178627ecc9787d85bfea098558f3e11bf4d0d432",
    "infra-templates/secret-volume-driver/1/README.md": "4f629802043c2fa69b7dfbec29bbff2cfde16ce9c143c15d22bca2758037e6e9",
    "infra-templates/secret-volume-driver/1/docker-compose.yml": "77f1808a8fbaa48fd460418310323661b4c10f9a261cc3322610259e7b40ac90",
    "infra-templates/secret-volume-driver/1/rancher-compose.yml": "78bb7944972e51835c07627068ad31e932bff5dbfb1a3e33d80264935595dfdc",
}


def blocker(message: str, failures: list[str]) -> None:
    failures.append(message)


def main() -> int:
    failures: list[str] = []
    data = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))

    for relative, expected_hash in RETAINED_VERSION_HASHES.items():
        retained_path = REPO_ROOT / relative
        if not retained_path.is_file():
            blocker(f"retained catalog file is missing: {relative}", failures)
            continue
        actual_hash = hashlib.sha256(retained_path.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            blocker(
                f"retained catalog file changed: {relative} "
                f"expected={expected_hash} actual={actual_hash}",
                failures,
            )

    if data.get("schemaVersion") != 1:
        blocker("catalog-images.json schemaVersion must be 1", failures)
    if provenance.get("schemaVersion") != 1:
        blocker("catalog-provenance.json schemaVersion must be 1", failures)
    if provenance.get("classification") != "upstream-first-party":
        blocker("catalog provenance must be classified as upstream-first-party", failures)
    if not COMMIT_PATTERN.fullmatch(str(provenance.get("preservedBoundary", ""))):
        blocker("catalog provenance must identify the full preserved boundary", failures)

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
    localized_question_count = 0
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

        question_files = sorted(root.glob("**/rancher-compose.yml"))
        for path in question_files:
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if "default:" not in line or "ghcr.io/" not in line:
                    continue
                match = DEFAULT_IMAGE_PATTERN.fullmatch(line)
                relative = path.relative_to(REPO_ROOT)
                if not match:
                    blocker(f"malformed default image at {relative}:{line_number}", failures)
                    continue
                reference = match.group(2)
                discovered.append((relative, line_number, reference))
                if not VERSION_TAG_PATTERN.fullmatch(reference):
                    blocker(f"default image must use a semantic version tag at {relative}:{line_number}: {reference}", failures)
                elif reference not in locked:
                    blocker(f"default image is absent from catalog-images.json at {relative}:{line_number}: {reference}", failures)

    infra_root = REPO_ROOT / "infra-templates"
    infra_configs = {
        path.parent.name: path
        for path in infra_root.glob("*/config.yml")
        if path.is_file()
    }
    provenance_entries = provenance.get("entries", {})
    if not isinstance(provenance_entries, dict):
        blocker("catalog-provenance.json entries must be an object", failures)
        provenance_entries = {}
    if set(infra_configs) != set(provenance_entries):
        missing = sorted(set(infra_configs) - set(provenance_entries))
        extra = sorted(set(provenance_entries) - set(infra_configs))
        blocker(
            f"catalog provenance folders differ: missing={missing} extra={extra}",
            failures,
        )
    if len(infra_configs) != EXPECTED_INFRA_TEMPLATE_COUNT:
        blocker(
            "expected exactly "
            f"{EXPECTED_INFRA_TEMPLATE_COUNT} reviewed infrastructure templates, "
            f"found {len(infra_configs)}",
            failures,
        )

    for folder, config_path in sorted(infra_configs.items()):
        config_text = config_path.read_text(encoding="utf-8")
        labels = {
            match.group(1): match.group(3)
            for line in config_text.splitlines()
            if (match := LABEL_PATTERN.fullmatch(line))
        }
        entry = provenance_entries.get(folder, {})
        source_path = str(entry.get("sourcePath", ""))
        origin_status = str(entry.get("originStatus", ""))
        if not source_path.startswith("infra-templates/"):
            blocker(f"invalid source path for {folder}: {source_path!r}", failures)
        if origin_status not in {"supported", "experimental", "first-party"}:
            blocker(f"invalid origin status for {folder}: {origin_status!r}", failures)

        expected_labels = {
            "io.pasturestack.catalog.origin": "upstream-first-party",
            "io.pasturestack.catalog.origin-template": Path(source_path).name,
            "io.pasturestack.catalog.origin-status": origin_status,
        }
        for key, expected in expected_labels.items():
            if labels.get(key) != expected:
                blocker(
                    f"provenance label {key} for {folder} must be {expected!r}",
                    failures,
                )
        for field in ("name", "description"):
            key = f"io.pasturestack.catalog.{field}.zh-tw"
            if not labels.get(key):
                blocker(f"missing Taiwan localization label {key} for {folder}", failures)

        version_dirs = sorted(
            (path for path in config_path.parent.iterdir()
             if path.is_dir() and path.name.isdigit() and any(path.iterdir())),
            key=lambda path: int(path.name),
        )
        if not version_dirs:
            blocker(f"no numeric version directory for {folder}", failures)
            continue
        actual_versions = tuple(path.name for path in version_dirs)
        retained_layout = RETAINED_VERSION_LAYOUTS.get(folder)
        if retained_layout and actual_versions != retained_layout:
            blocker(
                f"{folder} retained version layout differs: "
                f"expected={retained_layout} actual={actual_versions}",
                failures,
            )
        elif not retained_layout and len(version_dirs) != 1:
            blocker(
                f"{folder} must expose exactly one reviewed current version, "
                f"found {list(actual_versions)}",
                failures,
            )
        for version_dir in version_dirs:
            localized_readme = version_dir / "README.zh-TW.md"
            if not localized_readme.is_file():
                blocker(
                    f"missing Taiwan Traditional Chinese README for "
                    f"{folder}/{version_dir.name}",
                    failures,
                )
        current_dir = version_dirs[-1]
        readme_path = current_dir / "README.zh-TW.md"

        compose_path = current_dir / "rancher-compose.yml"
        if compose_path.is_file():
            compose_text = compose_path.read_text(encoding="utf-8")
            template_version = TEMPLATE_VERSION_PATTERN.search(config_text)
            catalog_version = CATALOG_VERSION_PATTERN.search(compose_text)
            if not template_version or not catalog_version:
                blocker(
                    f"missing template or .catalog version for {folder}",
                    failures,
                )
            elif template_version.group(2) != catalog_version.group(2):
                blocker(
                    f"template and .catalog versions differ for {folder}: "
                    f"{template_version.group(2)!r} != "
                    f"{catalog_version.group(2)!r}",
                    failures,
                )
            question_labels = {
                match.group(1)
                for line in compose_text.splitlines()
                if (match := LABEL_PATTERN.fullmatch(line))
            }
            variables = [
                match.group(2).lower()
                for line in compose_text.splitlines()
                if (match := QUESTION_PATTERN.fullmatch(line))
            ]
            localized_question_count += len(variables)
            for variable in variables:
                prefix = f"io.pasturestack.catalog.question.{variable}"
                for suffix in ("label.zh-tw", "description.zh-tw"):
                    key = f"{prefix}.{suffix}"
                    if key not in question_labels:
                        blocker(
                            f"missing Taiwan localization {key} in "
                            f"{compose_path.relative_to(REPO_ROOT)}",
                            failures,
                        )

        localized_files = [config_path]
        localized_files.extend(
            version_dir / "README.zh-TW.md"
            for version_dir in version_dirs
            if (version_dir / "README.zh-TW.md").is_file()
        )
        if compose_path.is_file():
            localized_files.append(compose_path)
        for localized_path in localized_files:
            localized_text = localized_path.read_text(encoding="utf-8")
            for term in NON_TAIWAN_TERMS:
                if term in localized_text:
                    blocker(
                        f"non-Taiwan term {term!r} in "
                        f"{localized_path.relative_to(REPO_ROOT)}",
                        failures,
                    )

    if localized_question_count != EXPECTED_QUESTION_COUNT:
        blocker(
            f"expected {EXPECTED_QUESTION_COUNT} localized questions, "
            f"found {localized_question_count}",
            failures,
        )

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
    print(f"infra_template_count={len(infra_configs)}")
    print(f"localized_question_count={localized_question_count}")
    print(f"deployable_image_blocker_count={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
