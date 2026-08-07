# Compatibility Contract

The catalog format requires established `rancher-compose.yml` filenames and version-gating keys containing the historical product identifier. Existing servers and catalog-service schemas consume these values literally, so they remain compatibility contracts rather than PastureStack branding.

Historical template revisions are preserved in Git history, not exposed from
the current catalog tree. A template returns to the current tree only after
each executable image has a reviewed source, license boundary, semantic version
tag, architecture, vulnerability result, and deployment test. Published
version tags are never overwritten, and release digests remain verification
evidence outside deployable references. Never substitute an unrelated image
merely to make a template pull successfully.

Treat every published numeric template-version directory as immutable. A
changed image, manifest, question, or version must use a new numeric directory
and update the template metadata; overwriting an existing directory reuses the
same catalog version ID and an installed catalog service can continue serving
its cached content. Integration tests must assert both the human-readable
version and the numeric suffix of the default-version link.

Kubernetes catalog revision 5 changes only the etcd compatibility image from
`v2.3.7-pasturestack.1` to `v2.3.7-pasturestack.2`. Revisions 2, 3, and 4 are
retained byte-for-byte, and their older image lock remains part of the catalog
evidence. This avoids silently changing the definition already associated with
an installed catalog version ID.

Literal compatibility filenames, schema keys, labels, environment variables, provider values, binary names, and persisted paths retain their established identifiers when changing them would break the catalog protocol or the software inside an unpublished image. They are compatibility debt, not current branding, and must be retired together with the dependent implementation rather than changed in isolation.

The `PastureStack IPsec Overlay` release candidate keeps the literal `rancher-compose.yml` filename, `minimum_rancher_version` key, required `io.rancher.*` orchestration labels, `rancher-cni-driver` shared volume, and `ipsec` agent-service marker. The compatible control plane and network plugin manager consume those values literally. All user-facing names, image coordinates, executable names, environment variables, CNI names, log paths, and DNS search suffixes in the new template use PastureStack-neutral identifiers.

The `PastureStack Network Services` release candidate keeps the same catalog filename and version gate, required `io.rancher.*` orchestration labels, `CATTLE_*` credential fallbacks, `/var/lib/rancher` CA path, and `rancher-cni-driver` shared volume. These values are produced or consumed by the compatible control plane and existing host-network contract. Public service names, image coordinates, executables, primary environment variables, and user-facing metadata use PastureStack-neutral identifiers.

The `PastureStack Network Diagnostics` release candidate keeps only the
catalog filename, version gate, and global scheduling label required by the
compatible control plane. Its images, services, variables, persisted volume,
paths, API, localization labels, and user-facing metadata use PastureStack
identifiers. Direct host and network identifiers are excluded from the
collection schema rather than renamed after collection.

The PastureStack NFS, Amazon EBS, and Amazon EFS storage release candidates
keep the catalog filename, version gate, required `io.rancher.*` scheduling
and agent labels, injected `CATTLE_*` credentials, compatibility host path
`/var/lib/rancher/volumes`, and storage-driver schema because the compatible
control plane and Docker plugin bridge consume them literally. The path is
mounted into the neutral runtime path `/var/lib/pasturestack/volumes`.
User-facing names, image coordinates, service names, executables, primary
debug variables, socket names, and volume-driver names use PastureStack
identifiers.

The `PastureStack Secret Volume` release candidate keeps the catalog filename,
version gate, required `io.rancher.*` global-scheduling and credential
injection labels, compatibility host-key source path, storage-driver schema,
secret-volume capability, and an opaque legacy option name accepted only at
runtime. The compatible control plane and Docker Volume Plugin API consume
these values literally. User-facing names, image coordinates, service and
driver names, plugin socket, volume root, current option name, health API, and
documentation use PastureStack-neutral identifiers.

The `PastureStack Layer 2 Flat Network` release candidate keeps the catalog
filename, version gate, required `io.rancher.*` scheduling and CNI-discovery
labels, and the `rancher-cni-driver` shared volume because the compatible
control plane and network plugin manager consume them literally. Its service,
network driver, CNI type, IPAM type, log file, DNS suffix, environment
variables, and user-facing metadata use PastureStack-neutral identifiers.

The `PastureStack Per-Host Subnet Network` release candidate keeps the same
catalog filename, version gate, scheduling and CNI-discovery labels, and shared
CNI volume. New host labels, service names, route-provider value, CNI and IPAM
types, persisted state path, internal DNS suffix, and user-facing metadata use
PastureStack identifiers. Existing host labels are not silently adopted;
operators must set a unique PastureStack subnet label before deployment.

Before release, validate YAML, questions, defaults, upgrade paths, sidekicks,
labels, health checks, storage, networking, every referenced image version,
source repository, license, architecture, and rollback in isolated VMs. The
literal `rancher-compose.yml` filename and version-gating keys remain only
because the compatible Catalog protocol requires them.

Localized display metadata uses optional
`io.pasturestack.catalog.name.<locale>` and
`io.pasturestack.catalog.description.<locale>` labels. These labels never
replace the canonical English `name` and `description` fields, so older clients
and unsupported locales retain deterministic fallback text.
