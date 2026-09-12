<!-- SPDX-License-Identifier: MIT -->

# PastureStack Network Services

This version adds a single, selectable host firewall backend for Network Plugin Manager. It keeps Metadata Service and Internal DNS unchanged from version 3. The prepared template references published Network Plugin Manager `v0.8.15`; its official image manifest digest and source revision are recorded in `catalog-images.json`. The isolated three-backend rule-ownership gate passed, but the complete managed-service lifecycle gate still precedes deployment of this catalog candidate.

## Firewall backend

`FIREWALL_BACKEND` defaults to `auto`. It reads Docker's actual firewall driver: Docker's native `nftables` driver uses native nft rules, while Docker's `iptables` driver selects the frontend that owns Docker's active NAT chain. That may be `iptables-nft` or `iptables-legacy` on **any supported host**, including Ubuntu 26.04 and later. The OS release, installed executable, or unloaded kernel module alone never selects a backend. To pin one path, choose:

- `nftables`: Docker's native nftables firewall backend. This is **not** the same as the iptables-nft compatibility CLI.
- `iptables-nft`: xtables compatibility CLI backed by nf_tables, for Docker's iptables firewall driver.
- `iptables-legacy`: legacy xtables, only when the running Docker daemon actually owns the active rules through that frontend.

The manager refuses a mismatched or ambiguous selection and does not fall back, switch Docker's backend, or load legacy modules. An Ubuntu 26.04+ host already using `iptables-legacy` or `iptables-nft` must keep its live Docker path; do not turn on native nftables merely because the OS is new. A deliberate migration requires a separate host change, rollback point, and network lifecycle test.

This manager alone owns the host NAT and host-port `CATTLE_*` chains. Its
masquerade rules exclude destinations inside the managed overlay subnet in
all three backends; the IPsec host-XFRM router must not patch these chains.
Upgrade Network Services first and verify manager health on every host before
upgrading the matching IPsec Overlay version.

For Docker's native nftables driver, configure Docker itself with `"firewall-backend": "nftables"` and `"bridge-accept-fwmark": "0x1068/0x1068"` before upgrading this stack. Persist `net.ipv4.ip_forward=1` on the host and verify it remains enabled after a reboot: Docker's native nftables backend does not enable IPv4 forwarding for you. The mark allows Docker's bridge forwarding rules to accept the manager's published-host-port traffic; the template cannot configure the host daemon or kernel settings. Check and explicitly migrate any stale `iptables-nft` `FORWARD DROP` policy or previous platform hooks before switching Docker. The manager refuses that mixed state rather than changing the host's global firewall policy. Docker's native nftables backend remains an experimental Docker feature; qualify it against the installed Docker release before production use.

## Other configuration

- `DOCKER_BRIDGE`: host bridge for managed workload traffic.
- `DNS_RECURSER_TIMEOUT`, `TTL`: upstream DNS timeout and service-discovery cache time.
- `CPU_PERIOD`, `CPU_QUOTA`: Metadata Service CPU scheduling limits.
- `RELOAD_INTERVAL_LIMIT`, `ARP_SYNC_INTERVAL`: metadata reload and host ARP reconciliation intervals.

Network Plugin Manager still requires host networking, host PID visibility, the Docker socket, Docker state, kernel-module and runtime mounts, and the shared CNI volume. Metadata Service starts as root only to assign its link-local address, then drops to UID/GID 10001. Internal DNS shares its namespace. The `rancher-compose.yml` filename, `io.rancher.*` labels, `CATTLE_*` fallback variables, `/var/lib/rancher` CA path, and `rancher-cni-driver` volume are compatibility contracts, not a request to use legacy firewall rules.

These template files are MIT-licensed. The manager, metadata service, and internal DNS retain their Apache-2.0 licenses and bundled dependency notices. Verify image source and the recorded manifest digest in `catalog-images.json` before deployment.
