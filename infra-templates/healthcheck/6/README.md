<!-- SPDX-License-Identifier: MIT -->

# Metadata Healthcheck

Revision 6 uses `metadata-healthcheck:v0.3.21` with the Ubuntu 26.04 glibc
update from [USN-9065-1](https://ubuntu.com/security/notices/USN-9065-1).
Health reporting and the TCP 42 readiness probe use the same settings as
revision 5. The previous revision remains available for rollback.

See [the image release](https://github.com/PastureStack/metadata-healthcheck/releases/tag/v0.3.21)
and the exact manifest, SBOM and scan records in `catalog-images.json`.
