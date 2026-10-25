<!-- SPDX-License-Identifier: MIT -->

# PastureStack Windows Container Networking v0.1.2 candidate

## Source candidate

This source prepares numeric revision 4 only. It is not published or
deployed. Catalog v0.3.16 and numeric revision 3 remain the published
installation coordinates. New component digests, producer identities, SBOMs
and scan receipts are pending. The candidate cannot pass the publication-
evidence gate yet; no new component acceptance is claimed.

Planned image replacements (published input -> unpublished candidate):

- `ghcr.io/pasturestack/pod-pause-image:v3.0.5` -> `ghcr.io/pasturestack/pod-pause-image:v3.0.6`

The runtime definitions preserve the prior revision byte-for-byte except for
these image tags and the visible Catalog version. Commands, defaults, resource
parameters, permissions, sidekicks, volumes, firewall choices and plugin
responsibilities retain their existing contracts. Obtain real publication
evidence before promoting this source candidate.

## Published revision 3 reference

The following guidance and validation statements describe the previous
published inputs only. Their evidence does not validate the candidate images.

This infrastructure entry defines the `nat` and `transparent` Docker network
drivers consumed by compatible Windows container workloads. Install it before
PastureStack Windows Network Services.

PastureStack is an independent community effort to preserve, audit, and modernize the Rancher 1.6 ecosystem. It is not affiliated with or endorsed by Rancher Labs or SUSE.

### Compatibility boundary

The Compose services are selector-only resources; the referenced pause image
is required by the legacy service schema but is not launched as a Windows
workload. The `io.rancher.service.selector.container` key and its historical
selector value are retained solely as control-protocol identifiers for
existing Windows agents. They are not user-facing branding and must be removed
only together with a replacement Windows agent contract.

### Validation status

The template parses through the reviewed Catalog Service and is restricted to
the Windows orchestration mode. No Windows host was available for an
end-to-end network-driver gate, so this entry remains a release candidate.

### License and provenance

The template files are MIT-licensed PastureStack contributions. The
selector-only placeholder image and bundled dependencies retain their
respective licenses and notices. The preserved Git history retains the
upstream Windows template provenance and authorship.
