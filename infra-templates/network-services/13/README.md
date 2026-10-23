<!-- SPDX-License-Identifier: MIT -->

# PastureStack Network Services

Version 13 (visible version `v0.3.11`) uses the published Network Plugin Manager `v0.8.25`, Metadata Service `v0.10.6`, and Internal DNS `v0.17.13`. This dependency update retains version 12's firewall ownership, CNI convergence, Catalog questions, sidekicks and shared volumes. Earlier numeric revisions remain unchanged. Published source, image digests and runtime scan evidence are recorded in `catalog-images.json`.

The NPM25 and Metadata106 GitHub Releases report `immutable: false`; recorded OCI manifest digests and SBOM SHA256 values identify the verified content, not a GitHub release lock. Metadata106's full raw report retains 44 reviewed unfixed findings (38 Medium and 6 Low), not zero findings. Metadata106 preserves the platform's opaque `revision-hash` change tokens so existing long-poll clients observe updates without a protocol change.

## CNI configuration convergence

The manager preflights all desired CNI configurations and writes each through an atomic replacement with mode `0600`. Only after every desired configuration has been written successfully may it retire an obsolete platform configuration. The historical `10-rancher.conf` must have the exact name/type/IPAM triplet `rancher-cni-network` / `rancher-bridge` / `rancher-cni-ipam`; the current `10-pasturestack.conf` must have `pasturestack-cni-network` / `pasture-bridge` / `metadata-cni-ipam`. The same ownership check applies when the selected provider requires the historical configuration again.

Retirement renames the obsolete file with a `.pasturestack-retired` suffix, preserving its original bytes outside the CNI `.conf` / `.json` execution set. An existing retirement backup must be byte-identical; a conflicting backup causes an error. Unrelated administrator configurations are preserved. Malformed or partially matching platform configurations, symlinks, and unsafe metadata paths cause an explicit error. The manager never sweeps the configuration directory or removes CNI binary aliases as part of this migration.

Each component is a published security rebuild. Full-severity evidence is recorded separately from deployment acceptance; publication does not establish that an existing infrastructure stack has completed its managed upgrade.

## Provider and lifecycle convergence

The manager selects one eligible CNI provider per binary from the infrastructure-service metadata on the local host. The highest numeric OCI image version wins; an unversioned or nonnumeric development label cannot replace a numeric release, and ties use a deterministic immutable container-ID ordering. The generated wrapper stays bound to that exact provider and does not relist containers by service label at invocation time. It executes the provider's private `/opt/cni/bin` copy with a bounded compatibility fallback for older images. Wrapper replacement uses an exclusive temporary inode and atomic rename; content, file type, and mode drift are repaired without following a replacement symlink.

When platform metadata temporarily reports a host-port container before its primary address, the manager may read the exact running container's network namespace. It accepts only one IPv4 address inside that network's configured managed subnet and revalidates the same Docker container PID after the namespace read. Missing, ambiguous, out-of-subnet, or lifecycle-raced results fail closed and retain the last known-good host-port rules until metadata and CNI converge.

## Firewall backend

`FIREWALL_BACKEND` defaults to `auto`. It reads Docker's actual firewall driver: Docker's native `nftables` driver uses native nft rules, while Docker's `iptables` driver selects the frontend that owns Docker's active NAT chain. That may be `iptables-nft` or `iptables-legacy` on **any supported host**, including Ubuntu 26.04 and later. The OS release, installed executable, or unloaded kernel module alone never selects a backend. To pin one path, choose:

- `nftables`: Docker's native nftables firewall backend. This is **not** the same as the iptables-nft compatibility CLI.
- `iptables-nft`: xtables compatibility CLI backed by nf_tables, for Docker's iptables firewall driver.
- `iptables-legacy`: legacy xtables, only when the running Docker daemon actually owns the active rules through that frontend.

The manager refuses a mismatched or ambiguous selection and does not fall back, switch Docker's backend, or load legacy modules. An Ubuntu 26.04+ host already using `iptables-legacy` or `iptables-nft` must keep its live Docker path; do not turn on native nftables merely because the OS is new. A deliberate migration requires a separate host change, rollback point, and network lifecycle test.

This manager alone owns the host NAT and host-port `CATTLE_*` chains. Its
masquerade rules exclude destinations inside the managed overlay subnet in
all three backends; the IPsec host-XFRM router must not patch these chains.
For the per-host-subnet driver, the manager also excludes other active hosts'
validated subnets from masquerade and adds a bounded forwarding exception.
Inactive registrations are ignored; missing or overlapping labels on an active
host fail closed. This is a routed, unencrypted network; protect the host
transport separately.
Upgrade Network Services first and verify manager health on every host before
upgrading the matching IPsec Overlay version.

Shared-subnet ingress is enabled only when CNI metadata explicitly sets
`allowSharedSubnetIngress: true`, or for the legacy fixed-subnet contract that
already declares both `bridgeSubnet` and `hostNat: true`. It is rejected for
host-label-based subnets, where only validated active peer ranges are trusted.

For Docker's native nftables driver, configure Docker itself with `"firewall-backend": "nftables"` and `"bridge-accept-fwmark": "0x1068/0x1068"` before upgrading this stack. Persist `net.ipv4.ip_forward=1` on the host and verify it remains enabled after a reboot: Docker's native nftables backend does not enable IPv4 forwarding for you. The mark allows Docker's bridge forwarding rules to accept the manager's published-host-port traffic; the template cannot configure the host daemon or kernel settings. Check and explicitly migrate any stale `iptables-nft` `FORWARD DROP` policy or previous platform hooks before switching Docker. The manager refuses that mixed state rather than changing the host's global firewall policy. Docker's native nftables backend remains an experimental Docker feature; qualify it against the installed Docker release before production use.

## Other configuration

- `DOCKER_BRIDGE`: host bridge for managed workload traffic.
- `DNS_RECURSER_TIMEOUT`, `TTL`: upstream DNS timeout and service-discovery cache time.
- `CPU_PERIOD`, `CPU_QUOTA`: Metadata Service CPU scheduling limits.
- `RELOAD_INTERVAL_LIMIT`, `ARP_SYNC_INTERVAL`: metadata reload and host ARP reconciliation intervals.

Network Plugin Manager still requires host networking, host PID visibility, the Docker socket, Docker state, kernel-module and runtime mounts, and the shared CNI volume. Metadata Service starts as root only to assign its link-local address, then drops to UID/GID 10001. Internal DNS shares its namespace. The `rancher-compose.yml` filename, `io.rancher.*` labels, `CATTLE_*` fallback variables, `/var/lib/rancher` CA path, and `rancher-cni-driver` volume are compatibility contracts, not a request to use legacy firewall rules.

These template files are MIT-licensed. The manager, metadata service, and internal DNS retain their Apache-2.0 licenses and bundled dependency notices. Verify image source and the recorded manifest digest in `catalog-images.json` before deployment.

Metadata and DNS are managed by the Server lifecycle. The manager no longer removes overlapping instances during upgrades and remains unready while waiting for Metadata recovery. Verify service health before completing an upgrade; image publication alone is not runtime acceptance.

Driver stop/start events and periodic reconciliation refresh the selected provider. Only eligible running local providers with a live process ID can be selected. Temporary metadata or Docker inspection failures remain visible and are retried; an unrelated unavailable driver does not block a healthy provider for another binary. No host firewall mode or administrator configuration is changed by provider selection.
