# PastureStack Catalog Templates

Catalog Templates preserves and audits application and infrastructure templates consumed by the compatible catalog service.

PastureStack is an independent community effort to preserve, audit, and modernize the Rancher 1.6 ecosystem. It is not affiliated with or endorsed by Rancher Labs or SUSE.

**Upstream:** [`rancher/rancher-catalog`](https://github.com/rancher/rancher-catalog). This GitHub fork preserves upstream history, authorship, dates, tags, notices, and template provenance. PastureStack maintenance is consolidated into one commit after the preserved upstream boundary.

## Project status

Earlier prerelease coordinates are retired from current release references;
their reviewed source commits remain in Git history. This source tree targets
the pure numeric coordinate `v0.3.12`; the GitHub tag and Release, rather than
this README, determine when it is published. Product identity is carried by
the repository, catalog metadata, and provenance rather than the version tag.

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
second container start. Network Services version `8` moves to `v0.8.20`,
rejects malformed per-host subnet labels before applying host firewall rules,
and preserves routed container source IPs between validated active peers. It
also restores bounded inbound forwarding for fixed shared overlay subnets,
binds every forwarding rule to the exact configured subnet and managed bridge,
and protects bridge traffic from `route_localnet` loopback routing while
preserving and restoring the operator's original per-bridge setting. Layer 2 Flat Network
version `4` moves to `v0.14.36` so the CNI
preserves an operator-configured bridge address.
Restored-data provisioning, complete multi-host
scheduler lifecycle, and complete project-template upgrade and rollback remain
release-candidate gates. The two alternative network drivers passed packaged
CNI address allocation and cleanup in isolated Linux network namespaces.
Layer 2 bridge setup and the Per-Host controller's marked routes and dedicated
IP set also passed without changing a production host interface. Per-Host
version `3` uses the control plane's plain-text host-label endpoint. On two
isolated Ubuntu 26.04.1 / Docker 29.8 hosts, the source-equivalent candidate
passed bidirectional workload ping and TCP, service DNS, egress, a published
host port, Docker restart, and both host reboots. The peer was explicitly
tested with native nftables, iptables-nft, and iptables-legacy, then restored
to its original iptables-legacy configuration. This does not qualify every
existing deployment's upgrade or rollback path. The
alternative drivers are not installed automatically by the project template.

Firewall acceptance keeps module ownership intact: Network Plugin Manager
alone manages host NAT, forwarding marks, and host-port `CATTLE_*` chains;
IPsec Overlay manages XFRM and routes without patching those host chains;
Network Policy Manager manages only its own nftables policy table. The bridge
CNI templates pass `hostNat` to Network Plugin Manager and never enable the
CNI binary's separate `ipMasq` host-NAT path. VXLAN's local MASQUERADE rule is
confined to the overlay container's network namespace. Host-chain writers
must follow the host's active Docker backend, including iptables-nft or
iptables-legacy on a new Ubuntu release, and must fail on a mismatch without
silently switching backends; the policy manager's independent nftables table
coexists with all three modes. The three-backend isolated rule tests do not
replace the coupled two-host service, workload egress/DNS, restart, and
rollback gates before the new Catalog versions become deployable.

IPsec Overlay template version `6` targets `v0.14.31`, retaining version `5`'s
bounded port handoff. It retries a temporarily offline peer through the
existing health reconciliation without restarting the shared charon daemon or
changing Network Plugin Manager's host-firewall ownership. The exact image
digest, security result, and two-host peer-restart evidence are separate
publication gates; earlier template versions remain unchanged.

IPsec Overlay template version `7` targets `v0.14.32` for the same managed
network contract. A live two-host upgrade exposed two long-lived established
IKE SAs for one peer, so version `7` is retained only for existing stacks and
is not the recommended update. Version `8` targets `v0.14.33`: the IPsec
module alone handles peer-SA recovery and conservative cleanup of an idle
duplicate, while Network Plugin Manager retains sole ownership of host NAT,
forwarding marks, and host ports. The three-backend firewall selection is
unchanged. Version `9` uses `v0.14.34` and corrects the bundled CNI host-label
adapter for the per-host driver. Image digests and live upgrade evidence are
separate gates; neither package source tests nor one-host allocation prove the
encrypted two-host lifecycle.

Version `10` uses the published `v0.14.35` image and bounds the connectivity
sidecar's TCP 80 bind retry during a managed upgrade. It does not alter
firewall ownership or backend selection. The image digest is recorded in
`catalog-images.json`; live Catalog activation and two-host lifecycle remain
separate acceptance gates.

IPsec Overlay version `11` and VXLAN Overlay Network version `5` explicitly
declare the fixed shared-subnet ingress contract consumed by Network Plugin
Manager `v0.8.20`. The rule is limited to traffic whose source and destination
are both inside the configured `10.42.0.0/16` subnet and whose output interface
is the exact managed bridge. Overlay routers retain their existing data-plane
responsibilities and do not take ownership of host firewall chains.

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
from reviewed immutable source snapshots; their original commits and contents
remain available in Git history without making prerelease tag names part of the
current operator workflow. Taiwan Traditional Chinese readmes are added without
changing those workload definitions. The integration gate is configured to resolve all 26
retained and current version IDs through Catalog Service
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
