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
`ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.40`. The image source is
[`PastureStack/ipsec-vxlan-overlay-network@4711833178a05e5d225e364cce856bd108bdc707`](https://github.com/PastureStack/ipsec-vxlan-overlay-network/tree/4711833178a05e5d225e364cce856bd108bdc707);
the bundled controller is from
[`PastureStack/per-host-subnet@v0.2.5`](https://github.com/PastureStack/per-host-subnet/releases/tag/v0.2.5),
and the bundled IPAM executable is from
[`PastureStack/host-local-cni-ipam@v0.1.6`](https://github.com/PastureStack/host-local-cni-ipam/releases/tag/v0.1.6).

The template files and icon are MIT licensed. The runtime projects are
Apache-2.0; operating-system packages and bundled components retain their own
upstream licenses and notices.

Version 4 preserves `PASTURESTACK_DEBUG` as a string in the generated CNI JSON,
matching the CNI schema when the Catalog answer is a boolean. Version 3 resolves
host-specific bridge and IPAM labels through the control
plane's plain-text `/self/host/labels/<key>` endpoint. The previous version's
JSON assumption prevented managed workload creation on a real host. A subnet
label must be valid and non-overlapping; Network Plugin Manager validates it
before applying host firewall rules. This driver is optional, not a second
Catalog vendor or an automatic replacement for the encrypted IPsec overlay.
