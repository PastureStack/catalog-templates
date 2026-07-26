<!-- SPDX-License-Identifier: MIT -->

# PastureStack Windows Container Networking

This infrastructure entry defines the `nat` and `transparent` Docker network
drivers consumed by compatible Windows container workloads. Install it before
PastureStack Windows Network Services.

PastureStack is an independent community effort to preserve, audit, and modernize the Rancher 1.6 ecosystem. It is not affiliated with or endorsed by Rancher Labs or SUSE.

## Compatibility boundary

The Compose services are selector-only resources; the referenced pause image
is required by the legacy service schema but is not launched as a Windows
workload. The `io.rancher.service.selector.container` key and its historical
selector value are retained solely as control-protocol identifiers for
existing Windows agents. They are not user-facing branding and must be removed
only together with a replacement Windows agent contract.

## Validation status

The template parses through the reviewed Catalog Service and is restricted to
the Windows orchestration mode. No Windows host was available for an
end-to-end network-driver gate, so this entry remains a release candidate.

## License and provenance

The template files are MIT-licensed PastureStack contributions. The
selector-only placeholder image and bundled dependencies retain their
respective licenses and notices. The preserved Git history retains the
upstream Windows template provenance and authorship.
