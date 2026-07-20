<!-- SPDX-License-Identifier: MIT -->

# Metadata Healthcheck v0.3.14

This infrastructure stack runs one healthcheck agent on every eligible host. The agent reads health declarations from the neutral `metadata` service, manages its private HAProxy process, and reports stable state changes to the compatible control API.

## Reviewed image

- Image: `ghcr.io/pasturestack/metadata-healthcheck:v0.3.14@sha256:00d2e0a6c547d7f0e2e7344c19483e7459a2e75fd2062a19b5abfa92df0c9bce`
- Source: [`PastureStack/metadata-healthcheck@731e6c5d35a55ba79e2bfd50b456c35ef957a99a`](https://github.com/PastureStack/metadata-healthcheck/tree/731e6c5d35a55ba79e2bfd50b456c35ef957a99a)
- Source license: Apache-2.0; bundled operating-system packages retain their upstream licenses
- Security gate: Trivy HIGH 0, CRITICAL 0, image secrets 0, and source secrets 0
- Distribution gate: public GHCR and unauthenticated digest verification passed

## Compatibility boundary

The compatible control plane requires the literal `rancher-compose.yml` filename and the `io.rancher.*` labels in this template. They are protocol identifiers, not PastureStack branding. The `create_agent` flow supplies scoped per-instance credentials; the image translates those injected compatibility names to its public `PLATFORM_*` configuration only when explicit neutral values are absent.

`PLATFORM_CA_ROOT` points to the established read-only agent certificate mount. TCP 42 is a container-network readiness endpoint and is not published on a host port. The template does not mount the Docker socket, request privileged mode, or add Linux capabilities.

## Release boundary

The image-level integration gates have passed. A Catalog-created `system=true` deployment has also verified credential injection, compatibility mapping, global scheduling, readiness, restart, and removal on one isolated host. That proof used a non-CNI test scaffold. The stack remains a release candidate until production network services, two-host health reporting, upgrade, and rollback pass on isolated VM snapshots. Do not use this template to modify an existing production control plane.
