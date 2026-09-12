#!/usr/bin/env python3
"""Guard the two coupled, current firewall-backend Catalog templates."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "infra-templates"
CHOICES = ("auto", "nftables", "iptables-nft", "iptables-legacy")
CURRENT_VERSIONS = {"network-services": "4", "ipsec-overlay": "5"}


def read(template: str, filename: str) -> str:
    return (ROOT / template / CURRENT_VERSIONS[template] / filename).read_text(
        encoding="utf-8"
    )


def check_question(template: str) -> None:
    text = read(template, "rancher-compose.yml")
    question = text.split("  - variable: FIREWALL_BACKEND\n", 1)[1].split(
        "  - variable:", 1
    )[0]
    assert "    default: auto\n" in question, template
    assert "    required: true\n" in question, template
    for choice in CHOICES:
        assert f"    - {choice}\n" in question, (template, choice)


def main() -> None:
    for template in ("network-services", "ipsec-overlay"):
        check_question(template)

    manager = read("network-services", "docker-compose.yml.tpl")
    router = read("ipsec-overlay", "docker-compose.yml.tpl").split(
        "  overlay-router:\n", 1
    )[1].split("  connectivity-check:\n", 1)[0]
    assert "    - --firewall-backend\n    - '${FIREWALL_BACKEND}'\n" in manager
    assert "PASTURESTACK_FIREWALL_BACKEND: '${FIREWALL_BACKEND}'" in router
    assert "    - /var/run/docker.sock:/var/run/docker.sock:ro\n" in router
    print("FIREWALL_BACKEND_CATALOG_CONTRACT_OK")


if __name__ == "__main__":
    main()
