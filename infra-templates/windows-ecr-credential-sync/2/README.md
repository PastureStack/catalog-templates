<!-- SPDX-License-Identifier: MIT -->

# PastureStack Windows ECR Credential Sync

This infrastructure stack refreshes short-lived Amazon Elastic Container
Registry credentials from a compatible Windows environment. It schedules only
on hosts carrying the compatibility label `io.rancher.host.os=windows`.

PastureStack is an independent community effort to preserve, audit, and modernize the Rancher 1.6 ecosystem. It is not affiliated with or endorsed by Rancher Labs or SUSE.

## Requirements

- A Windows Server 2022-compatible container host.
- Least-privilege AWS credentials that can request ECR authorization tokens.
- An environment-scoped API credential when another environment is selected.

The image is public on GHCR and is referenced by the semantic tag
`v3.1.2-windows-ltsc2022`; Catalog never places an image digest in the
user-facing Compose definition. The executable accepts neutral `PLATFORM_*`
variables and a bounded compatibility fallback for credentials injected by the
existing control protocol.

## Validation status

The Windows executable was cross-compiled and tested from the preserved source
history. Its PE format, image contents, bundled license files, anonymous GHCR
access, and vulnerability report were reviewed. No Windows host was available
for an end-to-end runtime gate, so this entry remains a release candidate and
must not be represented as Windows-runtime accepted.

## License and provenance

The template files are MIT-licensed PastureStack contributions. The service
source and image are Apache-2.0; the Microsoft Nano Server base and bundled
dependencies retain their own license terms and notices. The source repository
preserves upstream history, authorship, dates, and notices.
