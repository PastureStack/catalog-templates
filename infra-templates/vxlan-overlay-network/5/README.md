<!-- SPDX-License-Identifier: MIT -->

# PastureStack VXLAN Overlay Network 0.3.3

This optional infrastructure template installs an unencrypted VXLAN data
plane across managed hosts. It publishes UDP port `4789`, runs one router
sidecar per network holder, and installs the reviewed CNI executables on each
eligible host.

## Reviewed image

- Image: `ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.34`
- Template version `5` explicitly declares `allowSharedSubnetIngress: true` for the fixed `10.42.0.0/16` CNI network. Network Plugin Manager `v0.8.20` uses this bounded contract for cross-host workload forwarding; version `4` remains available for existing stacks.
- Source: [`PastureStack/ipsec-vxlan-overlay-network@db5a506346f521c6947b21a1a60cef6dd546f983`](https://github.com/PastureStack/ipsec-vxlan-overlay-network/tree/db5a506346f521c6947b21a1a60cef6dd546f983)
- Source license: Apache-2.0; Ubuntu, CNI, Weave, and bundled dependencies retain their upstream licenses and notices
- Security gate: Trivy HIGH 0, CRITICAL 0, image secrets 0, and personal-marker scan passed
- Runtime gate: the earlier version passed isolated two-node VXLAN forwarding; repeat the managed lifecycle gate for this new image before treating it as production-ready

## Security and network boundary

VXLAN encapsulates traffic but does not encrypt or authenticate it. Use this
driver only on a trusted host network. Every participating host must allow
inbound and outbound UDP port `4789`. Select the IPsec template when encrypted
host-to-host traffic is required.

The router receives `NET_ADMIN` in the network-holder namespace. The CNI
sidecar is privileged, joins the host network and PID namespaces, and accesses
the Docker socket so it can install and operate the compatibility CNI path.
These permissions must not be copied to ordinary workloads.

The managed network is `10.42.0.0/16`. This release intentionally does not
expose a subnet selector because the reviewed startup path does not safely
honor arbitrary subnets. Network Plugin Manager alone consumes the explicit
shared-subnet ingress contract and owns the corresponding host forwarding
rule; the VXLAN router remains confined to its data-plane namespace.

## Compatibility boundary

The literal `rancher-compose.yml` filename, `minimum_rancher_version` key,
required `io.rancher.*` orchestration labels, and `rancher-cni-driver` shared
volume are consumed by the compatible control plane. They are protocol
identifiers, not PastureStack branding. User-facing names, image coordinates,
environment variables, CNI names, log paths, and the `pasture.internal` search
suffix use current PastureStack identifiers.
