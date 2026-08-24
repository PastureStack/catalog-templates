# PastureStack Catalog Templates

Catalog Templates preserves and audits application and infrastructure templates consumed by the compatible catalog service.

PastureStack is an independent community effort to preserve, audit, and modernize the Rancher 1.6 ecosystem. It is not affiliated with or endorsed by Rancher Labs or SUSE.

**Upstream:** [`rancher/rancher-catalog`](https://github.com/rancher/rancher-catalog). This GitHub fork preserves upstream history, authorship, dates, tags, notices, and template provenance. PastureStack maintenance is consolidated into one commit after the preserved upstream boundary.

## Project status

The current tree is a deliberately small release candidate. It contains only
templates whose image source, semantic version tag, license boundary, and
vulnerability result are recorded in
[catalog-images.json](catalog-images.json). Historical upstream templates and
unreviewed migration work remain available through the preserved Git history,
but they are not exposed as deployable catalog entries. Previously published
PastureStack template versions remain in their original numeric version
directories when an installed system stack can still reference them; the
current reviewed version remains the default.

The supported set contains the `PastureStack Native` project template and
twenty-one infrastructure entries selected from the preserved upstream
first-party catalog: `PastureStack Container Schedule`,
`PastureStack Amazon ECR Credential Sync`, `PastureStack System Image
Preloader`, `Metadata Healthcheck`, `PastureStack Network Services`,
`PastureStack Network Diagnostics`, `PastureStack Network Policy Manager`,
`PastureStack IPsec Overlay`,
`PastureStack Windows ECR Credential Sync`,
`PastureStack Windows Network Services`,
`PastureStack Windows Container Networking`,
`Resource Scheduler`, `PastureStack Amazon EBS Storage`,
`PastureStack Amazon EFS Storage`, `PastureStack NFS Storage`,
`PastureStack Secret Volume`, `PastureStack Vault Volume`, and
`PastureStack Route 53 DNS Sync`, together
with the alternative
`PastureStack Layer 2 Flat Network`, `PastureStack Per-Host Subnet Network`,
and `PastureStack VXLAN Overlay Network` drivers. General third-party
application examples are intentionally excluded.
The source path and historical upstream status of every enabled
infrastructure entry are recorded in
[catalog-provenance.json](catalog-provenance.json). These provenance records
describe the source tree at the preserved boundary; they do not claim current
vendor certification, endorsement, or support for the PastureStack revisions.
The former Rancher-era Kubernetes entry is no longer deployable from this
catalog. Its Kubernetes 1.12, etcd 2.3, Docker-shim, and Helm 2 contracts cannot
be upgraded by replacing an image tag. The historical templates remain in Git;
new clusters must use a current Kubernetes provisioning path and the separately
maintained `kubernetes-package` component bundle where appropriate.
The three Windows entries restore the official upstream ECR, Metadata/DNS, and
NAT/transparent-networking intents with PastureStack-owned semantic image
tags. Their source tests, Windows cross-compilation, PE inspection, license
files, anonymous distribution, and vulnerability gates passed. No Windows
container host was available for an end-to-end runtime gate, so these entries
remain explicitly identified as release candidates and schedule only to
compatible Windows Server 2022 hosts.
These entries
passed clean project-template provisioning on an isolated VM: the node agent
became active, all four system stacks became healthy, and all six system images
were verified. The network, overlay, and health entries also passed multi-host
managed-network, Metadata, DNS, control-plane return-traffic, firewall,
health-reporting, and encrypted-workload gates. The scheduler passed source,
build, security, public distribution, live Metadata, idempotent reservation,
managed allocation, and restart gates. Version `v0.8.15` additionally remained
healthy through repeated Metadata long-poll windows in production without a
second container start. Restored-data provisioning, complete multi-host
scheduler lifecycle, and complete project-template upgrade and rollback remain
release-candidate gates. The two alternative network drivers passed packaged
CNI address allocation and cleanup in isolated Linux network namespaces.
Layer 2 bridge setup and the Per-Host controller's marked routes and dedicated
IP set also passed without changing a production host interface. They are not
installed automatically by the project template.

Deployable Compose files use semantic version tags only. A published version
tag must never be replaced. Manifest digests remain release-verification
evidence and are not inserted into Catalog, Compose, API, or user-interface
image references. No automatic deployment or publishing trigger is enabled.
The manually dispatched compatibility workflow uses Python `3.14.6`, verifies
every Python dependency against its PyPI SHA-256, and runs flake8, pytest, the
Catalog audit, and Catalog Service API gates against the exact selected commit.
GitHub CodeQL independently scans the Actions and Python sources. A Server
release pins the Catalog only after those gates pass; none of these checks is a
production-readiness claim.

## Version retention contract

A numeric template version becomes immutable after a Server release or a live
stack can reference it. It must not be deleted, renumbered, or silently replaced
when a later version is added. This repository therefore retains every version
still referenced by the reviewed deployment: Metadata Healthcheck `0`;
IPsec Overlay, Network Services, NFS Storage, Resource Scheduler, Network
Diagnostics, Network Policy Manager, and Secret Volume Driver `1`; and each
corresponding current definition. Historical definitions are restored exactly
from the reviewed `v0.3.0-rc21` tag, except NFS Storage `1`, whose deployed
`v0.9.13` definition comes from `v0.3.0-rc13`. Taiwan Traditional Chinese
readmes are added without changing those workload definitions. The integration
gate resolves all 16 retained and current version IDs through Catalog Service
so an existing stack cannot regress to a version-detail 404.

## Distribution

The public Git repository is the catalog source. A reviewed Server release
consumes its HTTPS clone URL together with the `main` branch and a full pinned
commit SHA; operators do not need to deploy a separate catalog website or Git
mirror. Template definitions, version metadata, descriptions, and icons live
in this repository. Versioned binary payloads use immutable GitHub Release
assets. Catalog images are distributed through public PastureStack GHCR
coordinates with explicit semantic version tags.

See [SUPPORTED.md](SUPPORTED.md) for the exact enabled set and review evidence.

## Validate locally

```sh
bash scripts/audit-deployable-images
CATALOG_SERVICE_BIN=/path/to/reviewed/catalog-service bash scripts/test
```

The integration test never downloads its service dependency. Supply a locally reviewed binary through `CATALOG_SERVICE_BIN`. Its test configuration uses the repository branch together with the exact current commit as `pinnedCommit`.

Templates use established compatibility filenames and schema keys. See [COMPATIBILITY.md](COMPATIBILITY.md), [SECURITY.md](SECURITY.md), [ORIGIN.md](ORIGIN.md), and [LICENSING.md](LICENSING.md).

## Language support

Canonical public repository documentation and catalog metadata remain English.
Enabled templates may additionally expose user-interface translations through
`io.pasturestack.catalog.name.<locale>` and
`io.pasturestack.catalog.description.<locale>` labels. The compatible Web
Console selects an exact locale label and falls back to the canonical English
value when a translation is absent. The current twenty-three entries include Taiwan
Traditional Chinese (`zh-tw`) labels. Runtime configuration keys, Compose
fields, image names, and third-party content are not translated because doing
so would break interoperability or alter upstream material.
