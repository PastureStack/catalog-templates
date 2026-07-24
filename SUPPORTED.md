<!-- SPDX-License-Identifier: MIT -->

# Supported Catalog Entries

The current catalog tree intentionally exposes only the entries below. Removal
from the current tree does not delete upstream history; it prevents unreviewed
or out-of-scope templates from being presented as deployable software.

| Entry | Type | Version | Image policy | Release state |
|---|---|---|---|---|
| PastureStack Native | Project template | 0.3.0-rc6 | Composes only reviewed, semantic-versioned infrastructure entries | Clean single-host provisioning and restart passed; restored-data validation pending |
| PastureStack Container Schedule | Infrastructure scheduling service | v0.6.0 | Public PastureStack GHCR image with an explicit version tag | Race tests, anonymous distribution, HIGH/CRITICAL scan, and Docker start/stop lifecycle passed |
| PastureStack System Image Preloader | Infrastructure image-cache service | v0.3.0 | Public PastureStack GHCR image with an explicit version tag | Mock compatibility API discovery, real Docker pull/cache lifecycle, anonymous distribution, and HIGH/CRITICAL scan passed |
| Metadata Healthcheck | Infrastructure stack | v0.3.15 | Public PastureStack GHCR image with a non-overwritten version tag | Link-local Metadata integration passed; production rolling upgrade pending |
| PastureStack Network Services | Infrastructure system stack | 0.3.0-rc2 | Three public PastureStack GHCR images with explicit version tags | Integrated single-host managed-network gate passed |
| PastureStack Network Diagnostics | Infrastructure diagnostics service | v0.2.0 | Two public PastureStack GHCR images with explicit version tags | Reproducible builds, anonymous distribution, full snapshot and bundle lifecycle, persistence, localization, and HIGH/CRITICAL scan passed |
| PastureStack IPsec Overlay | Infrastructure network driver | 0.3.0-rc2 | Public PastureStack GHCR image with an explicit version tag | Catalog-created two-host encrypted lifecycle, restart, upgrade, and rollback passed |
| PastureStack Layer 2 Flat Network | Optional infrastructure network driver | 0.3.0-rc8 | Reviewed network image with a semantic version tag; bridge setup is opt-in | Packaged Flat CNI ADD/DEL and isolated physical-bridge setup passed |
| Resource Scheduler | Infrastructure scheduling agent | v0.8.15 | Public PastureStack GHCR image with an explicit version tag | Production timeout fix, managed allocation, idempotent retry, and restart stability passed |
| PastureStack Route 53 DNS Sync | Infrastructure external-DNS agent | v0.8.0 | Public PastureStack GHCR image with an explicit version tag | Route 53 create, update, restart, removal, health, secret, and vulnerability gates passed |
| PastureStack Amazon EBS Storage | Infrastructure block-storage driver | v0.10.0 | Public PastureStack GHCR image with an explicit version tag | Existing-volume contract, safe opt-in provisioning boundary, anonymous distribution, and HIGH/CRITICAL scan passed; live AWS lifecycle pending |
| PastureStack Amazon EFS Storage | Infrastructure shared-storage driver | v0.10.0 | Public PastureStack GHCR image with an explicit version tag | Existing-filesystem contract, controlled mount-target provisioning boundary, anonymous distribution, and HIGH/CRITICAL scan passed; live AWS lifecycle pending |
| PastureStack NFS Storage | Infrastructure storage driver | v0.10.0 | Public PastureStack GHCR image with an explicit version tag | NFS v3 create, mount, read/write, unmount, retain, safe purge, anonymous distribution, and HIGH/CRITICAL scan passed |
| PastureStack Per-Host Subnet Network | Optional infrastructure network driver | 0.3.0-rc8 | Reviewed network image with a semantic version tag | Packaged Host-Local CNI ADD/DEL plus isolated route and IP-set reconciliation passed |
| PastureStack VXLAN Overlay Network | Optional infrastructure network driver | 0.3.0-rc9 | Reviewed network image with a semantic version tag | Isolated two-node VXLAN forwarding and overlay traffic passed; Catalog lifecycle pending |

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

## PastureStack Container Schedule evidence

- Image: `ghcr.io/pasturestack/container-cron:v0.6.0`
- Source: [`PastureStack/container-cron@8645472791ebbc9f78628af716e061139554fb38`](https://github.com/PastureStack/container-cron/tree/8645472791ebbc9f78628af716e061139554fb38)
- Release: [`v0.6.0`](https://github.com/PastureStack/container-cron/releases/tag/v0.6.0)
- License: Apache-2.0 for the project; Ubuntu and bundled Go dependencies
  retain their upstream licenses and notices
- Reviewed: 2026-07-25
- Vulnerability gate: 0 HIGH and 0 CRITICAL findings with Trivy 0.70.0
- Runtime gate: scheduled start and stop actions passed against Docker 29.4
  with no residual test containers

The service is global and requires read-write access to the host Docker socket.
It does not request privileged mode or publish a host port. The Catalog card
uses only the immutable semantic version tag; the release digest is retained
as internal verification evidence and is not exposed in Compose or the UI.

## PastureStack System Image Preloader evidence

- Image: `ghcr.io/pasturestack/system-image-preloader:v0.3.0`
- Source: [`PastureStack/system-image-preloader@150c78dbdb3f487a7003c83339cca5b76dde97f4`](https://github.com/PastureStack/system-image-preloader/tree/150c78dbdb3f487a7003c83339cca5b76dde97f4)
- Release: [`v0.3.0`](https://github.com/PastureStack/system-image-preloader/releases/tag/v0.3.0)
- License: Apache-2.0 for the project; Ubuntu, Docker CLI, `yq`, `gomplate`,
  and bundled dependencies retain their upstream licenses and notices
- Reviewed: 2026-07-25
- Vulnerability gate: 0 HIGH and 0 CRITICAL findings with Trivy 0.70.0
- Runtime gate: mock metadata, environment, and Catalog APIs resolved a
  Compose image, and the service cached that semantic tag through a real Docker
  socket without residual test resources

The service is global and start-once. It requires read-write access to the host
Docker socket, receives scoped compatibility API credentials, and optionally
reads a host Docker client configuration for private registries. Privileged
mode is disabled by default. Image pulls and CPU waits are bounded, and the
Catalog card never exposes a manifest digest.

## PastureStack Network Diagnostics evidence

- Agent image: `ghcr.io/pasturestack/network-diagnostics-agent:v0.2.0`
- Agent source: [`PastureStack/network-diagnostics-agent@01f8eefa4db9735a084e6470d814aaef4722e924`](https://github.com/PastureStack/network-diagnostics-agent/tree/01f8eefa4db9735a084e6470d814aaef4722e924)
- Agent release: [`v0.2.0`](https://github.com/PastureStack/network-diagnostics-agent/releases/tag/v0.2.0)
- Service image: `ghcr.io/pasturestack/network-diagnostics-service:v0.2.0`
- Service source: [`PastureStack/network-diagnostics-service@b3e1af66e91c4d04df20d59241262a5ba1655ece`](https://github.com/PastureStack/network-diagnostics-service/tree/b3e1af66e91c4d04df20d59241262a5ba1655ece)
- Service release: [`v0.2.0`](https://github.com/PastureStack/network-diagnostics-service/releases/tag/v0.2.0)
- License: the agent retains inherited Apache-2.0 source and history. Apache-2.0 applies to the new service root commit only; historical upstream service source and history are excluded because that repository has no repository-level license.
- Reviewed: 2026-07-25
- Vulnerability gate: both images have 0 HIGH, 0 CRITICAL, and 0 detected image secrets with Trivy 0.70.0.
- Runtime gate: a real agent uploaded a bounded host summary to an authenticated service; summary, ZIP creation, download, deletion, persistence across restart, Traditional Chinese response selection, health, and cleanup passed with zero restarts.
- Distribution gate: both immutable version tags are public and anonymous manifest access passed.

The agent sends only aggregate counters and a token-derived pseudonymous host
identifier. It runs globally without root, privileged mode, host PID or network
namespaces, Linux capabilities, or a container-engine socket. The service runs
as UID/GID `65532:65532` from a shell-free image, uses a stack-owned volume,
and requires the shared deployment token for all snapshot and bundle APIs. The
Catalog publishes port `8091` by default to avoid the control-plane port.

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

## PastureStack Route 53 DNS Sync evidence

- Image: `ghcr.io/pasturestack/external-dns-sync:v0.8.0`
- Source: [`PastureStack/external-dns-sync@dacc0bfceb633ed69a7df9b7612c11d4f72179eb`](https://github.com/PastureStack/external-dns-sync/tree/dacc0bfceb633ed69a7df9b7612c11d4f72179eb)
- Release: [`v0.8.0`](https://github.com/PastureStack/external-dns-sync/releases/tag/v0.8.0)
- Upstream: [`rancher-archives/external-dns`](https://github.com/rancher-archives/external-dns)
- License: Apache-2.0 for the project; Ubuntu and vendored Go dependencies
  retain their upstream licenses and notices
- Reviewed: 2026-07-25
- Vulnerability gate: 0 HIGH, 0 CRITICAL, and 0 detected image secrets with Trivy 0.70.0
- Runtime gate: a loopback Route 53-compatible fixture passed A-record and
  ownership-TXT creation, address update, manual restart, complete owned-record
  removal, dependency health, API authentication, and secret-redaction checks

The runtime executes as UID/GID `10001:10001` without privileged mode, host
networking, a Docker socket, or writable host storage. It registers only the
Route 53 provider. Existing DNS policy labels remain readable as bounded
compatibility identifiers, while neutral PastureStack labels take precedence.
The Catalog card does not expose the isolated-test endpoint override and uses
only the semantic release tag.

## PastureStack Amazon EBS Storage evidence

- Image: `ghcr.io/pasturestack/ebs-storage-driver:v0.10.0`
- Source: [`PastureStack/storage-plugins@38fa6f717c02b630777f3005fd813cb2179bf7ea`](https://github.com/PastureStack/storage-plugins/tree/38fa6f717c02b630777f3005fd813cb2179bf7ea)
- Release tag: [`v0.10.0`](https://github.com/PastureStack/storage-plugins/releases/tag/v0.10.0)
- License: Apache-2.0 for the project; Ubuntu, AWS CLI, filesystem tools,
  and bundled dependencies retain their upstream licenses and notices
- Reviewed: 2026-07-25
- Vulnerability gate: 0 HIGH, 0 CRITICAL, and 0 detected image secrets with
  Trivy 0.70.0
- Runtime gates: anonymous public pull; version and initialization smoke;
  existing-volume create contract; invalid identifier rejection; and
  provisioning rejection while the explicit opt-in is disabled

Existing EBS volumes are the safe default. Cloud creation, formatting,
detachment, and deletion are unavailable unless an operator explicitly enables
cloud provisioning. Newly provisioned volumes request encryption by default.
The driver validates identifiers and mount paths and uses IMDSv2 when it must
discover a region. A live AWS attach, mount, restart, detach, and deletion
lifecycle remains required before declaring cloud provisioning production
ready.

## PastureStack Amazon EFS Storage evidence

- Image: `ghcr.io/pasturestack/efs-storage-driver:v0.10.0`
- Source: [`PastureStack/storage-plugins@38fa6f717c02b630777f3005fd813cb2179bf7ea`](https://github.com/PastureStack/storage-plugins/tree/38fa6f717c02b630777f3005fd813cb2179bf7ea)
- Release tag: [`v0.10.0`](https://github.com/PastureStack/storage-plugins/releases/tag/v0.10.0)
- License: Apache-2.0 for the project; Ubuntu, AWS CLI, the NFS client, and
  bundled dependencies retain their upstream licenses and notices
- Reviewed: 2026-07-25
- Vulnerability gate: 0 HIGH, 0 CRITICAL, and 0 detected image secrets with
  Trivy 0.70.0
- Runtime gates: anonymous public pull; version and initialization smoke;
  existing-filesystem create contract; invalid identifier rejection; and
  provisioning rejection while the explicit opt-in is disabled

Existing EFS filesystems are the safe default. Cloud provisioning requires an
explicit subnet and security-group identifier in addition to the opt-in flag.
The driver does not create a security group and never adds unrestricted NFS
ingress. Initialization does not contact a cloud API, so the global service can
remain stable on non-AWS hosts. A live AWS mount, restart, mount-target, and
deletion lifecycle remains required before declaring cloud provisioning
production ready.

## PastureStack NFS Storage evidence

- Image: `ghcr.io/pasturestack/nfs-storage-driver:v0.10.0`
- Source: [`PastureStack/storage-plugins@38fa6f717c02b630777f3005fd813cb2179bf7ea`](https://github.com/PastureStack/storage-plugins/tree/38fa6f717c02b630777f3005fd813cb2179bf7ea)
- Release tag: [`v0.10.0`](https://github.com/PastureStack/storage-plugins/releases/tag/v0.10.0)
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

All three optional network entries use
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

The VXLAN entry reuses the reviewed network image's dedicated VXLAN startup
path. Two isolated privileged nodes established UDP VXLAN forwarding entries
and exchanged overlay traffic. VXLAN does not encrypt traffic, requires UDP
port `4789` across participating hosts, and is not installed by the default
project template.

The Layer 2 template leaves automatic physical-interface bridge setup disabled
by default. The Per-Host template requires a unique
`io.pasturestack.network.per-host-subnet.subnet` label on every participating
host. None of the optional drivers is installed by the default project
template.
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
