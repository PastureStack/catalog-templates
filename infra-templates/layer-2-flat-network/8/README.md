<!-- SPDX-License-Identifier: MIT -->

# PastureStack Layer 2 Flat Network v0.3.6 candidate

## Source candidate

This source prepares numeric revision 8 only. It is not published or
deployed. Catalog v0.3.16 and numeric revision 7 remain the published
installation coordinates. New component digests, producer identities, SBOMs
and scan receipts are pending. The candidate cannot pass the publication-
evidence gate yet; no new component acceptance is claimed.

Planned image replacements (published input -> unpublished candidate):

- `ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.40` -> `ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.41`

The runtime definitions preserve the prior revision byte-for-byte except for
these image tags and the visible Catalog version. Commands, defaults, resource
parameters, permissions, sidekicks, volumes, firewall choices and plugin
responsibilities retain their existing contracts. Obtain real publication
evidence before promoting this source candidate.

## Published revision 7 reference

The following guidance and validation statements describe the previous
published inputs only. Their evidence does not validate the candidate images.

This infrastructure template connects managed workloads directly to a shared
physical Layer 2 subnet. Every participating host must reach the same subnet
and gateway, and the selected workload range must not overlap DHCP, host, or
infrastructure addresses.

Automatic bridge setup is disabled by default because moving a host's physical
interface into a bridge can interrupt remote access when the interface, subnet,
or gateway is wrong. Prepare the bridge through the operating system first, or
verify out-of-band console access before enabling automatic setup.

The template uses
`ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.40`, which contains the
reviewed `pasture-bridge` and `flat-cni-ipam` executables. The image source is
[`PastureStack/ipsec-vxlan-overlay-network@4711833178a05e5d225e364cce856bd108bdc707`](https://github.com/PastureStack/ipsec-vxlan-overlay-network/tree/4711833178a05e5d225e364cce856bd108bdc707);
the Flat CNI IPAM source is
[`PastureStack/flat-cni-ipam@v0.1.6`](https://github.com/PastureStack/flat-cni-ipam/releases/tag/v0.1.6).

The template files and icon are MIT licensed. The runtime projects are
Apache-2.0; operating-system packages and bundled components retain their own
upstream licenses and notices.

Version 6 retains version 5's correctly typed `PASTURESTACK_DEBUG` value and
bridge ownership boundary. Flat IPAM now distinguishes an explicit host
address from a network prefix: it keeps the explicit address, or selects the
first usable address only when that address is present on the bridge. If a
multi-address bridge remains ambiguous, allocation fails instead of guessing.
The change does not alter firewall, IPsec, VXLAN, or physical-interface setup.
Verify the real Layer 2 path and rollback before enabling this optional driver
on a host.
