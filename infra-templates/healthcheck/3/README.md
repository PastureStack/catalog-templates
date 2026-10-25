<!-- SPDX-License-Identifier: MIT -->

# Metadata Healthcheck v0.3.18 candidate

## Source candidate

This source prepares numeric revision 3 only. It is not published or
deployed. Catalog v0.3.16 and numeric revision 2 remain the published
installation coordinates. New component digests, producer identities, SBOMs
and scan receipts are pending. The candidate cannot pass the publication-
evidence gate yet; no new component acceptance is claimed.

Planned image replacements (published input -> unpublished candidate):

- `ghcr.io/pasturestack/metadata-healthcheck:v0.3.17` -> `ghcr.io/pasturestack/metadata-healthcheck:v0.3.18`

The runtime definitions preserve the prior revision byte-for-byte except for
these image tags and the visible Catalog version. Commands, defaults, resource
parameters, permissions, sidekicks, volumes, firewall choices and plugin
responsibilities retain their existing contracts. Obtain real publication
evidence before promoting this source candidate.

## Published revision 2 reference

The following guidance and validation statements describe the previous
published inputs only. Their evidence does not validate the candidate images.

This infrastructure stack runs one healthcheck agent on every eligible host. The agent reads health declarations from the established link-local Metadata endpoint, manages its private HAProxy process, and reports stable state changes to the compatible control API.

### Reviewed image

- Image: `ghcr.io/pasturestack/metadata-healthcheck:v0.3.17`
- Source: [`PastureStack/metadata-healthcheck@410993d3b3b2493bbd84a36f7d67cfefb8dd6705`](https://github.com/PastureStack/metadata-healthcheck/tree/410993d3b3b2493bbd84a36f7d67cfefb8dd6705)
- Source license: Apache-2.0; bundled operating-system packages retain their upstream licenses
- Security gate: Trivy HIGH 0, CRITICAL 0, image secrets 0, and source secrets 0
- Distribution gate: public GHCR and unauthenticated version-tag pull passed

### Compatibility boundary

The compatible control plane requires the literal `rancher-compose.yml` filename and the `io.rancher.*` labels in this template. They are protocol identifiers, not PastureStack branding. The `create_agent` flow supplies scoped per-instance credentials; the image translates those injected compatibility names to its public `PLATFORM_*` configuration only when explicit neutral values are absent.

`PLATFORM_CA_ROOT` points to the established read-only agent certificate mount. TCP 42 is a container-network readiness endpoint and is not published on a host port. The template does not mount the Docker socket, request privileged mode, or add Linux capabilities.

### Release boundary

The image-level integration gate passed with the default link-local address, without a neutral Metadata DNS alias, and with routine lifecycle messages on standard output while actual failures remain on standard error. Earlier Catalog-created deployments verified credential injection, compatibility mapping, global scheduling, readiness, restart, two-daemon reporting, and removal. Managed multi-host upgrade, rollback, and complete infrastructure-stack removal remain separate deployment acceptance checks. Do not use this template to modify an existing production control plane.
