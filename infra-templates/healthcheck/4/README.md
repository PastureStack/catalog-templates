<!-- SPDX-License-Identifier: MIT -->

# Metadata Healthcheck

Numeric revision 4 uses the published image `ghcr.io/pasturestack/metadata-healthcheck:v0.3.19`.
Previous revision 3 remains available with `ghcr.io/pasturestack/metadata-healthcheck:v0.3.18`.
Questions, service configuration, scheduling and permissions retain their established contracts.

This infrastructure stack runs a healthcheck agent on each eligible host. It reads
health declarations from the established link-local Metadata endpoint, manages
its private HAProxy process, and reports stable state changes to the compatible control API.

## Image and compatibility

- Image: `ghcr.io/pasturestack/metadata-healthcheck:v0.3.19`
- Source: [PastureStack/metadata-healthcheck@6fd1fa81623dc9061d6b72a7a4d4b1c5d3b5fc37](https://github.com/PastureStack/metadata-healthcheck/tree/6fd1fa81623dc9061d6b72a7a4d4b1c5d3b5fc37)
- Source license: Apache-2.0; bundled packages retain their upstream licenses and notices.
- Exact manifest digest, runtime SBOM, raw/effective findings and publication evidence are recorded in `catalog-images.json`.

The compatible control plane requires the literal `rancher-compose.yml` filename
and `io.rancher.*` protocol labels. The `create_agent` flow supplies scoped
per-instance credentials; compatibility names map to public `PLATFORM_*`
configuration only when explicit neutral values are absent.

`PLATFORM_CA_ROOT` uses the established read-only agent certificate mount.
Container-network TCP 42 is a readiness endpoint and is not a published host port.
The template does not mount the Docker socket, request privileged mode, or add Linux capabilities.

## Upgrade boundary

Published image verification and tracked unfixed Low/Medium findings are separate
from deployment acceptance. Preserve existing lifecycle evidence; verify the
affected readiness path and managed-host upgrade/rollback before changing an
existing installation. Do not treat publication as a new full role or host matrix PASS.
