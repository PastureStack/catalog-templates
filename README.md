# PastureStack Catalog Templates

Catalog Templates preserves and audits application and infrastructure templates consumed by the compatible catalog service.

PastureStack is an independent community effort to preserve, audit, and modernize the Rancher 1.6 ecosystem. It is not affiliated with or endorsed by Rancher Labs or SUSE.

**Upstream:** [`rancher/rancher-catalog`](https://github.com/rancher/rancher-catalog). This GitHub fork preserves upstream history, authorship, dates, tags, notices, and template provenance. PastureStack maintenance is consolidated into one commit after the preserved upstream boundary.

## Project status

This source tree provides Catalog `v0.3.15`; its GitHub tag and Release determine
when it is published. It exposes one Native project template and twenty-one
reviewed infrastructure entries. See [SUPPORTED.md](SUPPORTED.md) for the
current versions and [catalog-provenance.json](catalog-provenance.json) for
preserved upstream origins. General third-party application examples and the
obsolete Rancher-era Kubernetes stack are not deployable entries.

New template revisions consume published PastureStack runtime artifacts built
from verified upstream inputs. Image tags, producer commits, manifest digests,
licenses and runtime evidence are recorded in [catalog-images.json](catalog-images.json).
Deployable Compose definitions use numeric release tags, not digest suffixes.
New default runtime versions are accepted after their component security gates.
Available fixes and unreviewed findings block those component gates.
Officially unfixed Low/Medium findings remain tracked, not resolved; narrowly
scoped VEX decisions require product-specific evidence and retain the raw scan.
A clean gate is not a claim that every dependency has zero reported CVEs.

Catalog validation covers template structure, retained versions, Traditional
Chinese labels, exact image references and Catalog Service API lookups. CI uses
Python `3.14.9`, hash-locked dependencies, the explicitly downstream
`pip 26.2.2+pasturestack.1` wheel and official certifi `2026.10.19`. The shared
pip rebuild changes only released urllib3 to `2.8.0`, preserving other vendored
files, licenses and RECORD integrity. Streaming and trusted/untrusted TLS tests
run in an isolated environment, not the runner's global Python installation.

Published artifacts and successful Catalog checks do not replace environment
acceptance. Verify managed upgrades, rollback and the selected host firewall
backend on isolated hosts before changing an existing installation. Network
Plugin Manager owns host NAT and host-port rules; IPsec owns XFRM and routes;
Network Policy Manager owns only its policy table. Templates do not silently
switch the host's Docker firewall backend. Windows definitions retain their
existing platform restrictions; a Windows-host runtime matrix is not claimed.
No automatic deployment is performed by this repository.

## Version retention contract

Published numeric template directories are immutable: do not delete, renumber
or silently replace a revision that a Server release or installed stack can
reference. This release adds new directories and updates defaults while keeping
the previously published definitions unchanged. The integration gate resolves
both retained and current version IDs through Catalog Service so existing
stacks do not regress to a version-detail 404.

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
value when a translation is absent. The current twenty-two entries include Taiwan
Traditional Chinese (`zh-tw`) labels. Runtime configuration keys, Compose
fields, image names, and third-party content are not translated because doing
so would break interoperability or alter upstream material.
