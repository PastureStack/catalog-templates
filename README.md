# PastureStack Catalog Templates

Catalog Templates preserves and audits application and infrastructure templates consumed by the compatible catalog service.

PastureStack is an independent community effort to preserve, audit, and modernize the Rancher 1.6 ecosystem. It is not affiliated with or endorsed by Rancher Labs or SUSE.

**Upstream:** [`rancher/rancher-catalog`](https://github.com/rancher/rancher-catalog). This GitHub fork preserves upstream history, authorship, dates, tags, notices, and template provenance. PastureStack maintenance is consolidated into one commit after the preserved upstream boundary.

## Project status

The current tree is a deliberately small release candidate. It contains only templates whose image source, immutable digest, license boundary, and vulnerability result are recorded in [catalog-images.json](catalog-images.json). Historical upstream templates and earlier migration work remain available through the preserved Git history, but they are not exposed as deployable catalog entries.

The supported set currently contains the `Web Service` application template plus `Metadata Healthcheck`, `PastureStack Network Services`, and `PastureStack IPsec Overlay` infrastructure release candidates. The Web Service create, health, restart, upgrade, rollback, and removal lifecycle has passed on an isolated single-host Server candidate. The three infrastructure entries have now passed together on an isolated single host: global scheduling, CNI addressing, Metadata, DNS, control-plane return traffic, firewall reconciliation, connectivity health reporting, and an overlay deactivate/activate cycle. Their images are public and pinned by immutable digest. Isolated two-node IPsec and VXLAN data-plane gates also passed, but the complete Catalog-created multi-host lifecycle, published host ports, host restart, upgrade, rollback, and removal are still required. Other system templates return only after all of their Runtime images meet the same gates. No CI/CD or production-readiness claim is enabled.

## Distribution

The public Git repository is the catalog source. A reviewed Server release consumes its HTTPS clone URL together with the `main` branch and a full pinned commit SHA; operators do not need to deploy a separate catalog website or Git mirror. Template definitions, version metadata, descriptions, and icons live in this repository. Versioned binary payloads use immutable GitHub Release assets. Catalog images are distributed through public PastureStack GHCR coordinates pinned by digest; mirrored third-party images retain their upstream licenses and provenance.

See [SUPPORTED.md](SUPPORTED.md) for the exact enabled set and review evidence.

## Validate locally

```sh
bash scripts/audit-deployable-images
CATALOG_SERVICE_BIN=/path/to/reviewed/catalog-service bash scripts/test
```

The integration test never downloads its service dependency. Supply a locally reviewed binary through `CATALOG_SERVICE_BIN`. Its test configuration uses the repository branch together with the exact current commit as `pinnedCommit`.

Templates use established compatibility filenames and schema keys. See [COMPATIBILITY.md](COMPATIBILITY.md), [SECURITY.md](SECURITY.md), [ORIGIN.md](ORIGIN.md), and [LICENSING.md](LICENSING.md).

## Language support

Public repository documentation and catalog metadata are English. The compatible Web Console provides the localized application and system terminology. Runtime configuration keys, Compose fields, image names, and third-party content are not translated because doing so would break interoperability or alter upstream material.
