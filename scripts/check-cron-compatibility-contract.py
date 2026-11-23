#!/usr/bin/env python3
"""Protect the installed legacy scheduler's identity and stop-first handover."""

import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "infra-templates/container-crontab"
HISTORY_HASHES = {
    "docker-compose.yml": "5f08572688e0a080008572063eea55eeabc56273e05538194d17b148e48c6ab6",
    "rancher-compose.yml": "f869674f102b775ea981a57353a157f8c30959bf1cd1430a0cb21227b53f998f",
    "README.md": "80ebbc61def63a890dfcc6249fb80819da307550b513d5879a4d8e1c91f7d49a",
}


def main():
    for name, expected in HISTORY_HASHES.items():
        actual = hashlib.sha256((TEMPLATE / "3" / name).read_bytes()).hexdigest()
        assert actual == expected, (name, actual)

    config = (TEMPLATE / "config.yml").read_text(encoding="utf-8")
    assert "io.pasturestack.catalog.compatibility-only: 'true'" in config
    assert re.search(r"(?m)^version: v0\.6\.2$", config)
    compose = (TEMPLATE / "4/docker-compose.yml.tpl").read_text(encoding="utf-8")
    platform = (TEMPLATE / "4/rancher-compose.yml").read_text(encoding="utf-8")
    assert re.findall(r"(?m)^  ([a-z][a-z-]+):$", compose) == ["container-crontab"]
    assert re.findall(r"(?m)^([a-z][a-z-]+):$", platform) == ["container-crontab"]
    assert "image: ghcr.io/pasturestack/container-cron:v0.6.2" in compose
    assert "    restart: always\n" in compose
    assert "      - /var/run/docker.sock:/var/run/docker.sock\n" in compose
    assert "      io.rancher.scheduler.global: 'true'\n" in compose
    assert "io.rancher.container.hostname_override: container_name" in compose
    assert "    start_first: false\n" in platform
    assert "  upgrade_from: '>=v0.5.0 <v0.6.2'\n" in platform
    assert re.findall(r"(?m)^    - variable: (\w+)$", platform) == ["metrics", "debug"]
    assert platform.count("      type: enum\n") == 2
    assert platform.count("      default: false\n") == 2
    assert platform.count("        - true\n        - false\n") == 2
    assert '.Values.metrics "true"' in compose
    assert '.Values.debug "true"' in compose
    # Preserve the historical --rancher-mode service-state checks using the
    # maintained runtime's equivalent flag rather than changing execution mode.
    assert "    command: container-cron --metadata-mode{{" in compose
    for removed in ("--rancher-mode", "DOCKER_API_VERSION", "privileged: true"):
        assert removed not in compose, removed

    inventory = json.loads((ROOT / "catalog-images.json").read_text(encoding="utf-8"))
    legacy = inventory["legacyImages"]
    assert len(legacy) == 1
    assert legacy[0]["defaultForNewInstall"] is False
    assert legacy[0]["vulnerabilityScan"] == {"status": "unassessed-legacy"}
    published = next(item for item in inventory["images"]
                     if item["reference"] == "ghcr.io/pasturestack/container-cron:v0.6.2")
    assert published["publicationStatus"] == "published"
    assert published["publicationVerification"]["anonymousReadback"] is True
    assert published["vulnerabilityScan"]["critical"] == 0
    assert published["vulnerabilityScan"]["high"] == 0
    print("CRON_COMPATIBILITY_CONTRACT_OK history=3 target=4 service=container-crontab stop_first=true")


if __name__ == "__main__":
    main()
