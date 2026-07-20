<!-- SPDX-License-Identifier: MIT -->

# Supported Catalog Entries

The current catalog tree intentionally exposes only the entries below. Removal from the current tree does not delete upstream history; it prevents unreviewed templates from being presented as deployable software.

| Entry | Type | Version | Image policy | Release state |
|---|---|---|---|---|
| Web Service | Application stack | 1.30.4 | Public PastureStack GHCR mirror, multi-platform digest pinned | Single-host lifecycle passed |
| PastureStack Native | Project template | 0.3.0-rc5 | Composes only reviewed, digest-pinned infrastructure entries | Clean single-host provisioning and restart passed; restored-data validation pending |
| Metadata Healthcheck | Infrastructure stack | v0.3.15 | Public PastureStack GHCR image, linux/amd64 digest pinned | Link-local Metadata integration passed; production rolling upgrade pending |
| PastureStack Network Services | Infrastructure system stack | 0.3.0-rc2 | Three public PastureStack GHCR images, linux/amd64 digests pinned | Integrated single-host managed-network gate passed |
| PastureStack IPsec Overlay | Infrastructure network driver | 0.3.0-rc2 | Public PastureStack GHCR image, linux/amd64 digest pinned | Catalog-created two-host encrypted lifecycle, restart, upgrade, and rollback passed |
| Resource Scheduler | Infrastructure scheduling agent | v0.8.14 | Public PastureStack GHCR image, linux/amd64 digest pinned | Managed allocation, idempotent retry, and restart passed; multi-host lifecycle pending |

## PastureStack Native evidence

The project template references only the four enabled PastureStack
infrastructure entries. It retains the established system-stack instance names
needed by the compatible control plane while every template identifier resolves
through the `pasturestack` Catalog ID. On an isolated clean Server candidate,
the node agent became active, all four system stacks became healthy, all six
expected system images were verified, a catalog workload served HTTP, the
workload recovered after a container restart, and cleanup completed. A
restored-data startup, multi-host provisioning, complete project-template
upgrade, and rollback gate is still required before production approval.

## Resource Scheduler evidence

- Image: `ghcr.io/pasturestack/resource-scheduler:v0.8.14@sha256:82742768223b8e9284f02e629e831efc1809266a8f2e8fc2049821d142b5e600`
- Source: [`PastureStack/resource-scheduler@09696440259c81b23f8bdec9b4cee98feebc8e26`](https://github.com/PastureStack/resource-scheduler/tree/09696440259c81b23f8bdec9b4cee98feebc8e26)
- License: Apache-2.0 for the project; Ubuntu and bundled dependencies retain their upstream licenses and notices
- Reviewed: 2026-07-23
- Vulnerability gate: 0 HIGH and 0 CRITICAL findings with Trivy 0.70.0 and the database updated 2026-07-22
- Distribution: the package is public and an unauthenticated pull returned the exact reviewed digest

The functional runtime passed race-enabled tests, source and license gates,
reproducible binary and image builds, non-root execution, anonymous digest
execution, and a live Metadata contract. Tests cover idempotent retries of a
workload's own host-port reservation and reject reservations owned by another
workload. Clean project-template provisioning then passed managed allocation,
exact image assignment, HTTP reachability, container restart recovery, and
cleanup on an isolated VM. Multi-host scheduler lifecycle, stack upgrade and
rollback, and restored-data behavior remain integrated release-candidate gates.

## Web Service evidence

- Image: `ghcr.io/pasturestack/web-service:1.30.4@sha256:97d490c12ba55b4946b01546d1c3ed324e8d41ab1c9fcb2a616aa470620e5b46`
- Image source: [`nginx/docker-nginx`](https://github.com/nginx/docker-nginx/tree/ccdab6c99ae2e2fc53a144dc68d6b8f44163adf2/stable/alpine)
- Distribution: [public PastureStack GHCR mirror](https://github.com/orgs/PastureStack/packages/container/package/web-service); the mirrored OCI index retains the reviewed upstream digest
- Reviewed: 2026-07-22
- Vulnerability gate: 0 HIGH and 0 CRITICAL findings with Trivy 0.70.0 and the database updated 2026-07-21
- Architectures in the pinned image index include `linux/amd64` and `linux/arm64/v8`

Catalog parsing, creation, HTTP reachability, metadata-driven health reporting, restart, upgrade, rollback, and removal passed against an isolated single-host Server candidate. The same digest-pinned configuration then scheduled one instance on each of two isolated Docker daemons, published the same host port on both, survived one daemon becoming unavailable and recovering, completed a rolling upgrade and native rollback without losing both endpoints, and removed both instances with CNI DEL and host-port release.

## Metadata Healthcheck evidence

- Image: `ghcr.io/pasturestack/metadata-healthcheck:v0.3.15@sha256:9dfd47f2ec6b55faa21cd607d7a88b7761eb697bfb4132a3d4ab53ce35b3dbb7`
- Source: [`PastureStack/metadata-healthcheck@b7ca40062ae22988c0c40af05eafe5b1ee8846bc`](https://github.com/PastureStack/metadata-healthcheck/tree/b7ca40062ae22988c0c40af05eafe5b1ee8846bc)
- License: Apache-2.0 for the project; operating-system and bundled packages retain their upstream licenses
- Reviewed: 2026-07-24
- Vulnerability gate: 0 HIGH and 0 CRITICAL findings with Trivy 0.70.0 and the database updated 2026-07-23
- Component integration: the default link-local Metadata endpoint, long polling, HAProxy configuration and socket, native neutral credentials, managed compatibility credentials, `INIT` then `UP` event reporting, and container-network TCP 42 readiness passed without a neutral DNS alias
- Distribution: the package is public and an unauthenticated pull returned the exact reviewed digest

This entry is not yet approved for a production control plane. Earlier Catalog-created lifecycle tests passed credential injection, compatibility mapping, global scheduling, HAProxy readiness, TCP port 42, `INIT` to `UP` reporting, restart, two-daemon convergence, and removal. Version v0.3.15 corrects the default endpoint to the established link-local address after a production upgrade exposed that the neutral DNS alias is not present on every managed host. A fresh multi-host upgrade, rollback, and complete infrastructure-stack removal remain release blockers.

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
