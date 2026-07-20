<!-- SPDX-License-Identifier: MIT -->

# Supported Catalog Entries

The current catalog tree intentionally exposes only the entries below. Removal from the current tree does not delete upstream history; it prevents unreviewed templates from being presented as deployable software.

| Entry | Type | Version | Image policy | Release state |
|---|---|---|---|---|
| Web Service | Application stack | 1.30.4 | Public PastureStack GHCR mirror, multi-platform digest pinned | Single-host lifecycle passed |
| Metadata Healthcheck | Infrastructure stack | v0.3.14 | Public PastureStack GHCR image, linux/amd64 digest pinned | Integrated single-host health reporting passed |
| PastureStack Network Services | Infrastructure system stack | 0.3.0-rc2 | Three public PastureStack GHCR images, linux/amd64 digests pinned | Integrated single-host managed-network gate passed |
| PastureStack IPsec Overlay | Infrastructure network driver | 0.3.0-rc2 | Public PastureStack GHCR image, linux/amd64 digest pinned | Catalog-created two-host encrypted lifecycle, restart, upgrade, and rollback passed |

## Web Service evidence

- Image: `ghcr.io/pasturestack/web-service:1.30.4@sha256:97d490c12ba55b4946b01546d1c3ed324e8d41ab1c9fcb2a616aa470620e5b46`
- Image source: [`nginx/docker-nginx`](https://github.com/nginx/docker-nginx/tree/ccdab6c99ae2e2fc53a144dc68d6b8f44163adf2/stable/alpine)
- Distribution: [public PastureStack GHCR mirror](https://github.com/orgs/PastureStack/packages/container/package/web-service); the mirrored OCI index retains the reviewed upstream digest
- Reviewed: 2026-07-22
- Vulnerability gate: 0 HIGH and 0 CRITICAL findings with Trivy 0.70.0 and the database updated 2026-07-21
- Architectures in the pinned image index include `linux/amd64` and `linux/arm64/v8`

Catalog parsing, creation, HTTP reachability, metadata-driven health reporting, restart, upgrade, rollback, and removal passed against an isolated single-host Server candidate. The same digest-pinned configuration then scheduled one instance on each of two isolated Docker daemons, published the same host port on both, survived one daemon becoming unavailable and recovering, completed a rolling upgrade and native rollback without losing both endpoints, and removed both instances with CNI DEL and host-port release.

## Metadata Healthcheck evidence

- Image: `ghcr.io/pasturestack/metadata-healthcheck:v0.3.14@sha256:00d2e0a6c547d7f0e2e7344c19483e7459a2e75fd2062a19b5abfa92df0c9bce`
- Source: [`PastureStack/metadata-healthcheck@731e6c5d35a55ba79e2bfd50b456c35ef957a99a`](https://github.com/PastureStack/metadata-healthcheck/tree/731e6c5d35a55ba79e2bfd50b456c35ef957a99a)
- License: Apache-2.0 for the project; operating-system and bundled packages retain their upstream licenses
- Reviewed: 2026-07-22
- Vulnerability gate: 0 HIGH and 0 CRITICAL findings with Trivy 0.70.0 and the database updated 2026-07-22
- Component integration: metadata long polling, HAProxy configuration and socket, native neutral credentials, managed compatibility credentials, `INIT` then `UP` event reporting, and container-network TCP 42 readiness passed
- Distribution: the package is public and an unauthenticated pull returned the exact reviewed digest

This entry is not yet approved for a production control plane. A Catalog-created `system=true` stack passed credential injection, compatibility mapping, global scheduling, metadata resolution, HAProxy readiness, TCP port 42, `INIT` to `UP` reporting, restart, and removal on one isolated host. The same stack then scheduled healthy instances on two isolated Docker daemons, continued reporting while one daemon was unavailable, and converged after restart. Multi-host upgrade, rollback, and complete infrastructure-stack removal remain release blockers.

## PastureStack Network Services evidence

- Network Plugin Manager: `ghcr.io/pasturestack/network-plugin-manager:v0.6.34@sha256:6a1b0f04c5ea2f8e9aac5b26b3ff950847c6fc9ca3786450072a9ca179e9e67f`
- Network Plugin Manager source: [`PastureStack/network-plugin-manager@b4b61856d38a9410319688144ff635868571e35f`](https://github.com/PastureStack/network-plugin-manager/tree/b4b61856d38a9410319688144ff635868571e35f)
- Metadata Service: `ghcr.io/pasturestack/metadata-service:v0.9.11@sha256:00f35785580edc498f202e1d9670fecf913b5cc15f6d268912c57662a8b10723`
- Metadata Service source: [`PastureStack/metadata-service@2096eb100a6c900ab70a952483306965c2278fe9`](https://github.com/PastureStack/metadata-service/tree/2096eb100a6c900ab70a952483306965c2278fe9)
- Internal DNS: `ghcr.io/pasturestack/internal-dns:v0.17.11@sha256:a67a68e5d370ea01d6f1b81ab7340c0ecc6acfad4ed3efdf298d038c04a00f36`
- Internal DNS source: [`PastureStack/internal-dns@5459f857cb7ead00888e900d77e4dc713107fef1`](https://github.com/PastureStack/internal-dns/tree/5459f857cb7ead00888e900d77e4dc713107fef1)
- License: Apache-2.0 for each project; Ubuntu, Docker CLI, and bundled packages retain their upstream licenses and notices
- Reviewed: 2026-07-23
- Vulnerability gate: all three reviewed digests report 0 HIGH and 0 CRITICAL findings with Trivy 0.70.0 and the database updated 2026-07-22
- Distribution: each package is public and its Catalog reference is pinned to the reviewed manifest digest

This is a privileged release candidate. Static source, provenance, image, and template-rendering gates passed for its components. On an isolated single-host Server candidate, credential delivery, per-host global scheduling, CNI installation, Metadata and DNS access, control-plane return traffic, nft and legacy NAT reconciliation, native-label IKE SNAT, restart, and health reporting passed together with Metadata Healthcheck and IPsec Overlay. The same services scheduled globally on two isolated Docker daemons, provided Metadata and DNS to workloads on both, preserved the surviving endpoint during a daemon outage, and converged after restart. Multi-host Network Services upgrade, rollback, and complete infrastructure-stack removal remain required before production approval.

## PastureStack IPsec Overlay evidence

- Image: `ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.26@sha256:04ee8f438b8c19e49984a5319489b8c97fff7ca90459168699b6f4175f649a9b`
- Source: [`PastureStack/ipsec-vxlan-overlay-network@e80db2268c9c0182b3b627e0c185998d9db91524`](https://github.com/PastureStack/ipsec-vxlan-overlay-network/tree/e80db2268c9c0182b3b627e0c185998d9db91524)
- License: Apache-2.0 for the project; Ubuntu, strongSwan, CNI, Weave, and bundled dependencies retain their upstream licenses and notices
- Reviewed: 2026-07-23
- Vulnerability gate: 0 HIGH, 0 CRITICAL, and 0 detected image secrets with Trivy 0.70.0
- Runtime gates: encrypted two-host IPsec traffic, managed CNI, Metadata, DNS, published host ports, daemon restart recovery, rolling replacement, native upgrade and rollback, source race tests, and reproducible binary builds passed
- Distribution: anonymous manifest, layer range, digest pull, and digest execution returned the reviewed digest and source revision

This entry remains a privileged release candidate. The Catalog-created stack scheduled globally across two isolated Docker daemons. Managed workloads exchanged bidirectional HTTP and ICMP traffic through AES-GCM XFRM state, resolved service DNS, reached Metadata, and published the same host port on both hosts. A daemon stop and restart preserved the surviving endpoint and converged automatically. The fixed image passed a real rolling upgrade, a second rolling configuration replacement, native rollback, and steady-state checks across multiple reconciliation intervals. Complete infrastructure-stack removal and a clean multi-VM acceptance run remain required before production approval.
