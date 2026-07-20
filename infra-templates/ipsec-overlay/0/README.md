<!-- SPDX-License-Identifier: MIT -->

# PastureStack IPsec Overlay 0.3.0-rc1

This infrastructure template installs the reviewed IPsec overlay data plane on every eligible host. A network-holder service owns the managed namespace, the router applies host XFRM and route state, the connectivity sidecar exposes the control-plane health contract, and the CNI sidecar supplies the reviewed bridge and address-management executables.

## Reviewed image

- Image: `ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.25@sha256:f0a7e61a3c35f5f5ba347a0c74d87b736229dcb73a17de90aaa38df4d94e2e5f`
- Source: [`PastureStack/ipsec-vxlan-overlay-network@0561fa07b74c750e3e9d7ae04c1ee2ec12590de0`](https://github.com/PastureStack/ipsec-vxlan-overlay-network/tree/0561fa07b74c750e3e9d7ae04c1ee2ec12590de0)
- Source license: Apache-2.0; Ubuntu, strongSwan, CNI, Weave, and bundled dependencies retain their upstream licenses and notices
- Security gate: Trivy HIGH 0, CRITICAL 0, image secrets 0, and personal-marker scan passed
- Runtime gate: encrypted two-node IPsec traffic, two-node VXLAN traffic, CNI installation, and strongSwan VICI passed
- Distribution gate: public anonymous manifest, layer, digest pull, and digest execution passed

## Privilege and secret boundary

The router is privileged, joins the host PID and network namespaces, and changes XFRM, route, firewall, bridge, ARP, and forwarding state. The CNI sidecar is privileged and accesses the Docker socket. These permissions are required by this compatibility architecture and must not be copied to ordinary workloads.

The router receives a scoped create-agent credential from the compatible control plane and downloads the generated IPsec pre-shared key through the authenticated `configcontent/psk` contract. This template does not accept a user-supplied key and never places a key in the public Catalog repository, Compose variables, image, or logs.

## Compatibility boundary

The literal `rancher-compose.yml` filename, `minimum_rancher_version` key, required `io.rancher.*` orchestration labels, `rancher-cni-driver` shared volume, and `ipsec` agent-service marker are consumed by the compatible control plane and network plugin manager. They are protocol identifiers, not PastureStack branding. User-facing names, image coordinates, commands, environment variables, CNI names, log paths, and the `pasture.internal` search suffix use current PastureStack identifiers.

The data plane currently supports the compatibility network `10.42.0.0/16`; the template intentionally does not expose a subnet selector that the runtime cannot safely honor.

## Release boundary

The image and isolated two-node data-plane gates have passed. A clean single-host Server candidate also created the real network-driver stack after Metadata Healthcheck and Network Services, assigned its managed CNI address in 13.2 seconds, reached Metadata, DNS, and the control plane, reported healthy in 18.3 seconds, and passed a deactivate/activate cycle. This Catalog entry remains a release candidate until workloads run on at least two isolated hosts, verify encrypted traffic and published host ports, survive host restarts, and pass upgrade, rollback, and removal without changing an existing production control plane.
