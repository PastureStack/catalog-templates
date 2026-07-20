<!-- SPDX-License-Identifier: MIT -->

# PastureStack IPsec Overlay 0.3.0-rc2

This infrastructure template installs the reviewed IPsec overlay data plane on every eligible host. A network-holder service owns the managed namespace, the router applies host XFRM and route state, the connectivity sidecar exposes the control-plane health contract, and the CNI sidecar supplies the reviewed bridge and address-management executables.

## Reviewed image

- Image: `ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.26@sha256:04ee8f438b8c19e49984a5319489b8c97fff7ca90459168699b6f4175f649a9b`
- Source: [`PastureStack/ipsec-vxlan-overlay-network@e80db2268c9c0182b3b627e0c185998d9db91524`](https://github.com/PastureStack/ipsec-vxlan-overlay-network/tree/e80db2268c9c0182b3b627e0c185998d9db91524)
- Source license: Apache-2.0; Ubuntu, strongSwan, CNI, Weave, and bundled dependencies retain their upstream licenses and notices
- Security gate: Trivy HIGH 0, CRITICAL 0, image secrets 0, and personal-marker scan passed
- Runtime gate: encrypted two-host IPsec traffic, managed CNI, Metadata, DNS, published host ports, daemon restart recovery, rolling replacement, upgrade, and rollback passed
- Distribution gate: public anonymous manifest, layer, digest pull, and digest execution passed

## Privilege and secret boundary

The router is privileged, joins the host PID and network namespaces, and changes XFRM, route, firewall, bridge, ARP, and forwarding state. The CNI sidecar is privileged and accesses the Docker socket. These permissions are required by this compatibility architecture and must not be copied to ordinary workloads.

The router receives a scoped create-agent credential from the compatible control plane and downloads the generated IPsec pre-shared key through the authenticated `configcontent/psk` contract. This template does not accept a user-supplied key and never places a key in the public Catalog repository, Compose variables, image, or logs.

## Compatibility boundary

The literal `rancher-compose.yml` filename, `minimum_rancher_version` key, required `io.rancher.*` orchestration labels, `rancher-cni-driver` shared volume, and `ipsec` agent-service marker are consumed by the compatible control plane and network plugin manager. They are protocol identifiers, not PastureStack branding. User-facing names, image coordinates, commands, environment variables, CNI names, log paths, and the `pasture.internal` search suffix use current PastureStack identifiers.

The data plane currently supports the compatibility network `10.42.0.0/16`; the template intentionally does not expose a subnet selector that the runtime cannot safely honor.

## Release boundary

The image, isolated data-plane, and Catalog-created two-host gates have passed. Managed workloads ran on both isolated Docker daemons, exchanged bidirectional HTTP and ICMP traffic through AES-GCM XFRM state, resolved service DNS, reached Metadata, and published the same host port on both hosts. A daemon stop and restart preserved service availability and converged automatically. The fixed image also passed a real rolling upgrade, a second rolling configuration replacement, native rollback, and steady-state checks that span multiple health-reconciliation intervals. Removal of the complete infrastructure stack and a clean multi-VM acceptance run remain required before production approval.
