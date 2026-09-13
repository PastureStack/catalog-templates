#!/usr/bin/env python3
"""Guard the latest coupled firewall-backend Catalog templates."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "infra-templates"
CHOICES = ("auto", "nftables", "iptables-nft", "iptables-legacy")
TEMPLATES = ("network-services", "ipsec-overlay")
CNI_HOST_NAT = {
    "ipsec-overlay": "true",
    "vxlan-overlay-network": "true",
    "per-host-subnet-network": "{{ .Values.HOST_NAT }}",
    "layer-2-flat-network": "false",
}


def latest_version(template: str) -> str:
    versions = [int(path.name) for path in (ROOT / template).iterdir()
                if path.is_dir() and path.name.isdecimal()]
    if not versions:
        raise AssertionError(f"No numbered versions for {template}")
    return str(max(versions))


def read(template: str, filename: str) -> str:
    return (ROOT / template / latest_version(template) / filename).read_text(
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


def check_cni_ownership(template: str, expected_host_nat: str) -> None:
    # hostNat is consumed by Network Plugin Manager. The bridge CNI's ipMasq
    # is a different knob and would create a second host-NAT owner.
    compose = read(template, "docker-compose.yml.tpl")
    cni = compose.split("      cni_config:\n", 1)[1]
    assert f"          hostNat: {expected_host_nat}\n" in cni, template
    assert "ipMasq:" not in cni, template

    if template == "vxlan-overlay-network":
        router = compose.split("  vxlan-router:\n", 1)[1].split(
            "  cni-driver:\n", 1
        )[0]
        assert "    network_mode: container:vxlan-network\n" in router


def main() -> None:
    for template in TEMPLATES:
        check_question(template)

    manager = read("network-services", "docker-compose.yml.tpl")
    router = read("ipsec-overlay", "docker-compose.yml.tpl").split(
        "  overlay-router:\n", 1
    )[1].split("  connectivity-check:\n", 1)[0]
    assert "    - --firewall-backend\n    - '${FIREWALL_BACKEND}'\n" in manager
    assert "PASTURESTACK_FIREWALL_BACKEND: '${FIREWALL_BACKEND}'" in router
    assert "    - /var/run/docker.sock:/var/run/docker.sock:ro\n" in router
    for template, host_nat in CNI_HOST_NAT.items():
        check_cni_ownership(template, host_nat)
    print("FIREWALL_BACKEND_CATALOG_CONTRACT_OK")


if __name__ == "__main__":
    main()
