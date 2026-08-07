# PastureStack Per-Host Subnet Network

This infrastructure template assigns a different workload subnet to each host
and maintains marked host-gateway routes between those subnets. Before
deployment, add a unique label to every participating host:

```text
io.pasturestack.network.per-host-subnet.subnet=10.50.1.0/24
```

Use a different, non-overlapping subnet on each host. Optional allocation
bounds use
`io.pasturestack.network.per-host-subnet.range-start` and
`io.pasturestack.network.per-host-subnet.range-end`. The controller accepts
`io.pasturestack.network.per-host-subnet.override-agent-ip` only when metadata
does not advertise the address that other hosts can route through.

The template uses
`ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.26`. The image source is
[`PastureStack/ipsec-vxlan-overlay-network@e80db2268c9c0182b3b627e0c185998d9db91524`](https://github.com/PastureStack/ipsec-vxlan-overlay-network/tree/e80db2268c9c0182b3b627e0c185998d9db91524);
the bundled controller is from
[`PastureStack/per-host-subnet@babe7d7f2b7f67a18883b9ed99d17483c8854315`](https://github.com/PastureStack/per-host-subnet/tree/babe7d7f2b7f67a18883b9ed99d17483c8854315),
and the bundled IPAM executable is from
[`PastureStack/host-local-cni-ipam@e79e1721f78a9579145cd89d8ad5083ae24633f5`](https://github.com/PastureStack/host-local-cni-ipam/tree/e79e1721f78a9579145cd89d8ad5083ae24633f5).

The template files and icon are MIT licensed. The runtime projects are
Apache-2.0; operating-system packages and bundled components retain their own
upstream licenses and notices.
