<!-- SPDX-License-Identifier: MIT -->

# PastureStack Network Services

This infrastructure stack installs one Network Plugin Manager, Metadata Service, and Internal DNS instance on every eligible host. Together they provide the host CNI configuration, network-driver executable wrappers, workload metadata, service discovery, host routes, host-port rules, and network reconciliation required by managed workloads.

All three images are public PastureStack GHCR packages pinned by immutable digest. Its integrated single-host gate passed with Metadata Healthcheck and IPsec Overlay. Install and activate Metadata Healthcheck before treating infrastructure health as authoritative, then install this stack before IPsec Overlay. The stack remains a release candidate until its complete multi-host managed-network lifecycle has passed on isolated hosts.

## Configuration

- `DOCKER_BRIDGE` selects the host bridge used by managed workload traffic.
- `DNS_RECURSER_TIMEOUT` limits upstream DNS query time.
- `TTL` controls internal service-discovery caching.
- `CPU_PERIOD` and `CPU_QUOTA` bound Metadata Service CPU use.
- `RELOAD_INTERVAL_LIMIT` rate-limits metadata configuration reloads.
- `ARP_SYNC_INTERVAL` controls host ARP reconciliation.

## Privilege boundary

Network Plugin Manager uses host networking, host PID visibility, the Docker socket, Docker state, kernel modules, runtime mounts, and the shared CNI volume. Metadata Service receives scoped per-instance credentials from the compatible control plane and owns the link-local metadata address. It starts as root only long enough to assign that address, then its image entrypoint drops to UID and GID 10001 before starting the service. Internal DNS shares the Metadata Service network namespace.

The literal `rancher-compose.yml` filename, `io.rancher.*` labels, `CATTLE_*` fallback variables, `/var/lib/rancher` CA path, and `rancher-cni-driver` volume are temporary compatibility contracts consumed by the existing control protocol. They are not PastureStack branding. Do not remove them independently of their producers and consumers.

## License and provenance

The template files are MIT-licensed PastureStack contributions. Network Plugin Manager, Metadata Service, and Internal DNS are Apache-2.0 projects; Ubuntu and bundled dependencies retain their own licenses and notices. See the source repositories and `catalog-images.json` for the reviewed commits and image boundaries.
