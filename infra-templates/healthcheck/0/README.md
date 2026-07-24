<!-- SPDX-License-Identifier: MIT -->

# Metadata Healthcheck v0.3.15

This infrastructure stack runs one healthcheck agent on every eligible host. The agent reads health declarations from the established link-local Metadata endpoint, manages its private HAProxy process, and reports stable state changes to the compatible control API.

## Reviewed image

- Image: `ghcr.io/pasturestack/metadata-healthcheck:v0.3.15`
- Source: [`PastureStack/metadata-healthcheck@b7ca40062ae22988c0c40af05eafe5b1ee8846bc`](https://github.com/PastureStack/metadata-healthcheck/tree/b7ca40062ae22988c0c40af05eafe5b1ee8846bc)
- Source license: Apache-2.0; bundled operating-system packages retain their upstream licenses
- Security gate: Trivy HIGH 0, CRITICAL 0, image secrets 0, and source secrets 0
- Distribution gate: public GHCR and unauthenticated version-tag pull passed

## Compatibility boundary

The compatible control plane requires the literal `rancher-compose.yml` filename and the `io.rancher.*` labels in this template. They are protocol identifiers, not PastureStack branding. The `create_agent` flow supplies scoped per-instance credentials; the image translates those injected compatibility names to its public `PLATFORM_*` configuration only when explicit neutral values are absent.

`PLATFORM_CA_ROOT` points to the established read-only agent certificate mount. TCP 42 is a container-network readiness endpoint and is not published on a host port. The template does not mount the Docker socket, request privileged mode, or add Linux capabilities.

## Release boundary

The image-level integration gate passed with the default link-local address and without a neutral Metadata DNS alias. Earlier Catalog-created deployments verified credential injection, compatibility mapping, global scheduling, readiness, restart, two-daemon reporting, and removal. The stack remains a release candidate until v0.3.15 passes a fresh multi-host upgrade, rollback, and complete infrastructure-stack removal on isolated VM snapshots. Do not use this template to modify an existing production control plane.
