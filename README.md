# PastureStack Catalog Templates

Catalog Templates preserves and audits application and infrastructure templates consumed by the compatible catalog service.

PastureStack is an independent community effort to preserve, audit, and modernize the Rancher 1.6 ecosystem. It is not affiliated with or endorsed by Rancher Labs or SUSE.

**Upstream:** [`rancher/rancher-catalog`](https://github.com/rancher/rancher-catalog). This GitHub fork preserves upstream history, authorship, dates, tags, notices, and template provenance. PastureStack maintenance is consolidated into one commit after the preserved upstream boundary.

## Project status

The current tree is a deliberately small release candidate. It contains only
templates whose image source, semantic version tag, license boundary, and
vulnerability result are recorded in
[catalog-images.json](catalog-images.json). Historical upstream templates and
earlier migration work remain available through the preserved Git history, but
they are not exposed as deployable catalog entries.

The supported set contains the `PastureStack Native` project template and nine
infrastructure entries: `PastureStack Container Schedule`, `Metadata
Healthcheck`, `PastureStack Network Services`, `PastureStack IPsec Overlay`,
`Resource Scheduler`, and `PastureStack NFS Storage`, together with the alternative
`PastureStack Layer 2 Flat Network` and `PastureStack Per-Host Subnet Network`
drivers, plus the optional `PastureStack VXLAN Overlay Network`. General
third-party application examples are intentionally excluded.
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
image references. No automatic CI/CD trigger or production-readiness claim is
enabled. The manually dispatched validation workflow checks the exact selected
commit with the immutable Catalog Service release before a Server release pins
it.

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
value when a translation is absent. The current ten entries include Taiwan
Traditional Chinese (`zh-tw`) labels. Runtime configuration keys, Compose
fields, image names, and third-party content are not translated because doing
so would break interoperability or alter upstream material.
