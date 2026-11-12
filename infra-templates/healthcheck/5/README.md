<!-- SPDX-License-Identifier: MIT -->

# Metadata Healthcheck

Revision 5 uses the published `ghcr.io/pasturestack/metadata-healthcheck:v0.3.20`
image with Ubuntu HAProxy 3.2.25-0ubuntu0.26.04.2 and the official Perl,
CA and APT updates. Revision 4 remains available for rollback.

The agent reads workload health declarations from the link-local Metadata
endpoint and sends health reports using the scoped agent credentials.
TCP 42 remains the container readiness endpoint.

See [the image release](https://github.com/PastureStack/metadata-healthcheck/releases/tag/v0.3.20)
and the exact manifest, SBOM and scan records in `catalog-images.json`.
