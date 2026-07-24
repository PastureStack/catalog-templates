<!-- SPDX-License-Identifier: MIT -->

# Supported Catalog Entries

The current catalog tree intentionally exposes only the entries below. Removal
from the current tree does not delete upstream history; it prevents unreviewed
or out-of-scope templates from being presented as deployable software.

| Entry | Type | Version | Image policy | Release state |
|---|---|---|---|---|
| PastureStack Native | Project template | 0.3.0-rc6 | Composes only reviewed, semantic-versioned infrastructure entries | Clean single-host provisioning and restart passed; restored-data validation pending |
| Metadata Healthcheck | Infrastructure stack | v0.3.15 | Public PastureStack GHCR image with a non-overwritten version tag | Link-local Metadata integration passed; production rolling upgrade pending |
| PastureStack Network Services | Infrastructure system stack | 0.3.0-rc2 | Three public PastureStack GHCR images with explicit version tags | Integrated single-host managed-network gate passed |
| PastureStack IPsec Overlay | Infrastructure network driver | 0.3.0-rc2 | Public PastureStack GHCR image with an explicit version tag | Catalog-created two-host encrypted lifecycle, restart, upgrade, and rollback passed |
| PastureStack Layer 2 Flat Network | Optional infrastructure network driver | 0.3.0-rc8 | Reviewed network image with a semantic version tag; bridge setup is opt-in | Packaged Flat CNI ADD/DEL and isolated physical-bridge setup passed |
| Resource Scheduler | Infrastructure scheduling agent | v0.8.15 | Public PastureStack GHCR image with an explicit version tag | Production timeout fix, managed allocation, idempotent retry, and restart stability passed |
| PastureStack NFS Storage | Infrastructure storage driver | v0.9.13 | Public PastureStack GHCR image with an explicit version tag | NFS v3 create, mount, read/write, unmount, retain, safe purge, and anonymous-distribution gates passed |
| PastureStack Per-Host Subnet Network | Optional infrastructure network driver | 0.3.0-rc8 | Reviewed network image with a semantic version tag | Packaged Host-Local CNI ADD/DEL plus isolated route and IP-set reconciliation passed |

Deployable image references contain semantic version tags only. A published
version tag must never be replaced. Manifest digests are retained only in the
corresponding GitHub Release verification evidence; they are not placed in
Catalog, Compose, API, or user-interface values.

## PastureStack Native evidence

The project template references only the four enabled PastureStack
infrastructure entries. It retains the established system-stack instance names
needed by the compatible control plane while every template identifier resolves
through the `pasturestack` Catalog ID. On an isolated clean Server candidate,
the node agent became active, all four system stacks became healthy, all six
expected system images were verified, a workload served HTTP, the workload
recovered after a container restart, and cleanup completed. A restored-data
startup, complete multi-host provisioning, project-template upgrade, and
rollback gate remain required before production approval.

## Resource Scheduler evidence

- Image: `ghcr.io/pasturestack/resource-scheduler:v0.8.15`
- Source: [`PastureStack/resource-scheduler@0423c1d2af3859cc1145fe2c5ed2407b312a5bb9`](https://github.com/PastureStack/resource-scheduler/tree/0423c1d2af3859cc1145fe2c5ed2407b312a5bb9)
- Release: [`v0.8.15`](https://github.com/PastureStack/resource-scheduler/releases/tag/v0.8.15)
- License: Apache-2.0 for the project; Ubuntu and bundled dependencies retain their upstream licenses and notices
- Reviewed: 2026-07-24
- Vulnerability gate: 0 HIGH and 0 CRITICAL findings with Trivy 0.72.0
- Runtime gate: the production service remained healthy for more than four minutes with `start_count=1`; the replaced build had reached `start_count=110`

The functional runtime passed race-enabled tests, source and license gates,
reproducible binary and image builds, non-root execution, public version-tag
pull, and a live Metadata contract. Tests cover idempotent retries of a
workload's own host-port reservation and reject reservations owned by another
workload. Version `v0.8.15` restores the established behavior of retrying a
transient Metadata long-poll timeout instead of terminating the scheduler.
Complete multi-host scheduler upgrade, rollback, and restored-data behavior
remain integrated release-candidate gates.

## PastureStack NFS Storage evidence

- Image: `ghcr.io/pasturestack/nfs-storage-driver:v0.9.13`
- Source: [`PastureStack/storage-plugins@a36faadc616afe4c427a6bda7f33d88f9c496ba8`](https://github.com/PastureStack/storage-plugins/tree/a36faadc616afe4c427a6bda7f33d88f9c496ba8)
- Release tag: [`v0.9.13`](https://github.com/PastureStack/storage-plugins/releases/tag/v0.9.13)
- License: Apache-2.0 for the project; Ubuntu, the NFS client, and bundled dependencies retain their upstream licenses and notices
- Reviewed: 2026-07-24
- Vulnerability gate: 0 HIGH, 0 CRITICAL, and 0 detected image secrets with Trivy 0.70.0
- Runtime gates: anonymous public pull; Catalog deployment on two active hosts;
  control-plane Volume creation; NFS v3 mount, write/read, unmount, and removal
  against a real server export; 60-second zero-restart stability

The default removal policy is `retain`. An explicit `purge` deletes only a
validated subdirectory owned by the driver. Direct export references remain
externally managed and are retained even when a caller requests a purge.
The production acceptance workload and its Volume were removed without
residual data, while the healthy global driver stack remained deployed.
Complete multi-host upgrade and rollback remain release-candidate gates.

## Alternative network driver evidence

Both optional network entries use
`ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.26`, whose source,
license, vulnerability, and public-distribution evidence is recorded below.
The same immutable image bundles:

- [`PastureStack/flat-cni-ipam@047eb2ffc5a985810fbc8a9a25150698facc6ae6`](https://github.com/PastureStack/flat-cni-ipam/tree/047eb2ffc5a985810fbc8a9a25150698facc6ae6)
  as release `v0.1.3`;
- [`PastureStack/per-host-subnet@babe7d7f2b7f67a18883b9ed99d17483c8854315`](https://github.com/PastureStack/per-host-subnet/tree/babe7d7f2b7f67a18883b9ed99d17483c8854315)
  as release `v0.2.7`;
- [`PastureStack/host-local-cni-ipam@e79e1721f78a9579145cd89d8ad5083ae24633f5`](https://github.com/PastureStack/host-local-cni-ipam/tree/e79e1721f78a9579145cd89d8ad5083ae24633f5)
  as release `v0.1.3`.

On an isolated Linux network namespace, the packaged Layer 2 path created a
bridge, preserved the interface address and default route, assigned a workload
address, installed the link-local Metadata route, and removed the workload
interface. The packaged Per-Host path allocated and released a host-local
address, reconciled a remote subnet through a host gateway with protocol 99 and
priority 45160, and maintained only its dedicated
`pasturestack-no-host-nat` IP set.

The Layer 2 template leaves automatic physical-interface bridge setup disabled
by default. The Per-Host template requires a unique
`io.pasturestack.network.per-host-subnet.subnet` label on every participating
host. Neither optional driver is installed by the default project template.
Clean multi-VM deployment, upgrade, rollback, and coexistence testing remain
release-candidate gates.

## Metadata Healthcheck evidence

- Image: `ghcr.io/pasturestack/metadata-healthcheck:v0.3.15`
- Source: [`PastureStack/metadata-healthcheck@b7ca40062ae22988c0c40af05eafe5b1ee8846bc`](https://github.com/PastureStack/metadata-healthcheck/tree/b7ca40062ae22988c0c40af05eafe5b1ee8846bc)
- License: Apache-2.0 for the project; operating-system and bundled packages retain their upstream licenses
- Reviewed: 2026-07-24
- Vulnerability gate: 0 HIGH and 0 CRITICAL findings with Trivy 0.70.0
- Component integration: link-local Metadata, long polling, HAProxy configuration and socket, credential compatibility, event reporting, and TCP readiness passed

This entry remains a release candidate. Version `v0.3.15` corrects the default
endpoint to the established link-local address after production validation
showed that a neutral DNS alias is not present on every managed host. A fresh
multi-host upgrade, rollback, and complete infrastructure-stack removal remain
release blockers.

## PastureStack Network Services evidence

- Network Plugin Manager: `ghcr.io/pasturestack/network-plugin-manager:v0.6.34`
- Network Plugin Manager source: [`PastureStack/network-plugin-manager@b4b61856d38a9410319688144ff635868571e35f`](https://github.com/PastureStack/network-plugin-manager/tree/b4b61856d38a9410319688144ff635868571e35f)
- Metadata Service: `ghcr.io/pasturestack/metadata-service:v0.9.11`
- Metadata Service source: [`PastureStack/metadata-service@2096eb100a6c900ab70a952483306965c2278fe9`](https://github.com/PastureStack/metadata-service/tree/2096eb100a6c900ab70a952483306965c2278fe9)
- Internal DNS: `ghcr.io/pasturestack/internal-dns:v0.17.11`
- Internal DNS source: [`PastureStack/internal-dns@5459f857cb7ead00888e900d77e4dc713107fef1`](https://github.com/PastureStack/internal-dns/tree/5459f857cb7ead00888e900d77e4dc713107fef1)
- License: Apache-2.0 for each project; Ubuntu, Docker CLI, and bundled packages retain their upstream licenses and notices
- Reviewed: 2026-07-23
- Vulnerability gate: all three releases report 0 HIGH and 0 CRITICAL findings with Trivy 0.70.0

This is a privileged release candidate. On isolated hosts, credential delivery,
per-host scheduling, CNI installation, Metadata and DNS access, control-plane
return traffic, NAT reconciliation, restart, and health reporting passed
together with Metadata Healthcheck and IPsec Overlay. Multi-host upgrade,
rollback, and complete infrastructure-stack removal remain required before
production approval.

## PastureStack IPsec Overlay evidence

- Image: `ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.26`
- Source: [`PastureStack/ipsec-vxlan-overlay-network@e80db2268c9c0182b3b627e0c185998d9db91524`](https://github.com/PastureStack/ipsec-vxlan-overlay-network/tree/e80db2268c9c0182b3b627e0c185998d9db91524)
- License: Apache-2.0 for the project; Ubuntu, strongSwan, CNI, Weave, and bundled dependencies retain their upstream licenses and notices
- Reviewed: 2026-07-23
- Vulnerability gate: 0 HIGH, 0 CRITICAL, and 0 detected image secrets with Trivy 0.70.0
- Runtime gates: encrypted two-host IPsec traffic, managed CNI, Metadata, DNS, published host ports, daemon restart recovery, rolling replacement, native upgrade, and rollback passed

This entry remains a privileged release candidate. Managed workloads exchanged
bidirectional HTTP and ICMP traffic through AES-GCM XFRM state, resolved service
DNS, reached Metadata, and published the same host port on both isolated hosts.
Complete infrastructure-stack removal and a clean multi-VM acceptance run
remain required before production approval.
