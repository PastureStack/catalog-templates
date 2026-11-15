<!-- SPDX-License-Identifier: MIT -->

# Per-Host Subnet Network

The image uses the official Ubuntu 26.04 Brotli package from [USN-8956-1](https://ubuntu.com/security/notices/USN-8956-1).

This driver routes managed host subnets without encryption. Network Plugin Manager retains host NAT and host-port ownership.

Numeric revision 9 (display version `v0.3.7`) uses the published image `ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.44`.
Previous revision 8 and `ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.43` remain available.
Questions, environment, resource parameters, volumes, permissions and plugin ownership are unchanged.
Exact publication records are in `catalog-images.json`; environment acceptance remains separate.
