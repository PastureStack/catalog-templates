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
`ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.26`, which contains the
reviewed `pasture-bridge` and `flat-cni-ipam` executables. The image source is
[`PastureStack/ipsec-vxlan-overlay-network@e80db2268c9c0182b3b627e0c185998d9db91524`](https://github.com/PastureStack/ipsec-vxlan-overlay-network/tree/e80db2268c9c0182b3b627e0c185998d9db91524);
the Flat CNI IPAM source is
[`PastureStack/flat-cni-ipam@047eb2ffc5a985810fbc8a9a25150698facc6ae6`](https://github.com/PastureStack/flat-cni-ipam/tree/047eb2ffc5a985810fbc8a9a25150698facc6ae6).

The template files and icon are MIT licensed. The runtime projects are
Apache-2.0; operating-system packages and bundled components retain their own
upstream licenses and notices.
