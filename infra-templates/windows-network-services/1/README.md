<!-- SPDX-License-Identifier: MIT -->

# PastureStack Windows Network Services

This infrastructure stack installs one Metadata Service and Internal DNS
instance on every eligible Windows host. Install PastureStack Windows Container
Networking first so the required `nat` and `transparent` network drivers exist.

PastureStack is an independent community effort to preserve, audit, and modernize the Rancher 1.6 ecosystem. It is not affiliated with or endorsed by Rancher Labs or SUSE.

## Requirements and behavior

- A Windows Server 2022-compatible container host carrying the
  `io.rancher.host.os=windows` compatibility label.
- The Windows container networking entry installed and active.
- Link-local addresses `169.254.169.250` and `169.254.169.251` available inside
  the transparent container network.

Metadata Service receives an environment-scoped credential from the existing
control protocol. Internal DNS reads the dated Metadata API, answers service
discovery queries on the second link-local address, and never recursively
forwards queries back to either infrastructure address.

## Validation status

Both Windows executables passed cross-compilation and source tests. Their PE
format, image contents, bundled license files, anonymous GHCR access, and
vulnerability reports were reviewed. No Windows host was available for an
end-to-end runtime gate, so this entry remains a release candidate.

## License and provenance

The template files are MIT-licensed PastureStack contributions. Both service
sources and images are Apache-2.0; the Microsoft Nano Server bases and bundled
dependencies retain their own license terms and notices. The source
repositories preserve upstream history, authorship, dates, and notices.
