# Compatibility Contract

The catalog format requires established `rancher-compose.yml` filenames and version-gating keys containing the historical product identifier. Existing servers and catalog-service schemas consume these values literally, so they remain compatibility contracts rather than PastureStack branding.

Historical template revisions are preserved in Git history, not exposed from the current catalog tree. A template returns to the current tree only after each executable image has a reviewed source, license boundary, immutable digest, architecture, vulnerability result, and deployment test. Never substitute an unrelated image merely to make a template pull successfully.

Treat every published numeric template-version directory as immutable. A
changed image, manifest, question, or version must use a new numeric directory
and update the template metadata; overwriting an existing directory reuses the
same catalog version ID and an installed catalog service can continue serving
its cached content. Integration tests must assert both the human-readable
version and the numeric suffix of the default-version link.

Literal compatibility filenames, schema keys, labels, environment variables, provider values, binary names, and persisted paths retain their established identifiers when changing them would break the catalog protocol or the software inside an unpublished image. They are compatibility debt, not current branding, and must be retired together with the dependent implementation rather than changed in isolation.

The `PastureStack IPsec Overlay` release candidate keeps the literal `rancher-compose.yml` filename, `minimum_rancher_version` key, required `io.rancher.*` orchestration labels, `rancher-cni-driver` shared volume, and `ipsec` agent-service marker. The compatible control plane and network plugin manager consume those values literally. All user-facing names, image coordinates, executable names, environment variables, CNI names, log paths, and DNS search suffixes in the new template use PastureStack-neutral identifiers.

The `PastureStack Network Services` release candidate keeps the same catalog filename and version gate, required `io.rancher.*` orchestration labels, `CATTLE_*` credential fallbacks, `/var/lib/rancher` CA path, and `rancher-cni-driver` shared volume. These values are produced or consumed by the compatible control plane and existing host-network contract. Public service names, image coordinates, executables, primary environment variables, and user-facing metadata use PastureStack-neutral identifiers.

Before release, validate YAML, questions, defaults, upgrade paths, sidekicks, labels, health checks, storage, networking, every referenced image digest, source repository, license, architecture, and rollback in isolated VMs. The literal `rancher-compose.yml` filename and version-gating keys remain only because the compatible Catalog protocol requires them.
