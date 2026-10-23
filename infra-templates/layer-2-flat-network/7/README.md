# PastureStack Layer 2 Flat Network

This infrastructure template connects managed workloads directly to a shared
physical Layer 2 subnet. Every participating host must reach the same subnet
and gateway, and the selected workload range must not overlap DHCP, host, or
infrastructure addresses.

Automatic bridge setup is disabled by default because moving a host's physical
interface into a bridge can interrupt remote access when the interface, subnet,
or gateway is wrong. Prepare the bridge through the operating system first, or
verify out-of-band console access before enabling automatic setup.

The template uses
`ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.37`, which contains the
reviewed `pasture-bridge` and `flat-cni-ipam` executables. The image source is
[`PastureStack/ipsec-vxlan-overlay-network@20eb898da1b24ed3b8ab2c0ad212d6523adeddeb`](https://github.com/PastureStack/ipsec-vxlan-overlay-network/tree/20eb898da1b24ed3b8ab2c0ad212d6523adeddeb);
the Flat CNI IPAM source is
[`PastureStack/flat-cni-ipam@4676b320a03fec53ae68899fdf18c7e7f7340356`](https://github.com/PastureStack/flat-cni-ipam/tree/4676b320a03fec53ae68899fdf18c7e7f7340356).

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
