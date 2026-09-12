<!-- SPDX-License-Identifier: MIT -->

# PastureStack IPsec Overlay 0.3.2 (template publication pending)

This infrastructure template is a candidate for the IPsec overlay data plane on every eligible host. A network-holder service owns the managed namespace, the router applies host XFRM and route state, the connectivity sidecar exposes the control-plane health contract, and the CNI sidecar supplies the bridge and address-management executables.

## Candidate template — published image

- Image: `ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.27` is published. Its immutable manifest digest, source revision, and runtime-image security scan are recorded in `catalog-images.json`. The catalog template and backend-specific host lifecycle gates remain pending; do not deploy this candidate yet.
- The `v0.14.26` evidence in version `3` is historical and does not validate this candidate image.
- Source license: Apache-2.0; Ubuntu, strongSwan, CNI, Weave, and bundled dependencies retain their upstream licenses and notices.

## Privilege and secret boundary

The router is privileged and uses host PID and network namespaces. In native `nftables` mode it synchronizes XFRM and routes only; Network Plugin Manager owns the overlay bridge-subnet forward mark and NAT exclusion in its own host firewall rules. The router does not create another nftables mark table or change Docker's tables. The explicit `iptables-nft` and `iptables-legacy` modes keep their respective xtables-specific paths, separate from native nftables. The CNI sidecar is privileged and accesses the Docker socket. These permissions are required by this compatibility architecture and must not be copied to ordinary workloads.

The router receives a scoped create-agent credential from the compatible control plane and downloads the generated IPsec pre-shared key through the authenticated `configcontent/psk` contract. This template does not accept a user-supplied key and never places a key in the public Catalog repository, Compose variables, image, or logs.

## Compatibility boundary

The literal `rancher-compose.yml` filename, `minimum_rancher_version` key, required `io.rancher.*` orchestration labels, `rancher-cni-driver` shared volume, and `ipsec` agent-service marker are consumed by the compatible control plane and network plugin manager. They are protocol identifiers, not PastureStack branding. User-facing names, image coordinates, commands, environment variables, CNI names, log paths, and the `pasture.internal` search suffix use current PastureStack identifiers.

The data plane currently supports the compatibility network `10.42.0.0/16`; the template intentionally does not expose a subnet selector that the runtime cannot safely honor.

The host firewall backend is selected explicitly or left at `auto`. The four supported choices are `auto`, native `nftables`, `iptables-nft`, and `iptables-legacy`. The selection is passed only to `overlay-router` through `PASTURESTACK_FIREWALL_BACKEND`. An explicit mismatch fails safely; selecting a modern backend must not activate legacy rules. Use legacy only on an intentionally configured legacy host, and align this choice with the Network Services template on the same environment.

The Native project definition lists Network Services before IPsec, but list order alone does not establish a health dependency. Before creating or upgrading this overlay, apply the matching Network Services version and wait until Network Plugin Manager is healthy on every target host. In native `nftables` mode, first satisfy that template's Docker firewall-backend, bridge-accept-fwmark, and persistent IPv4-forwarding prerequisites; an IPsec router alone cannot provide the manager-owned forwarding and NAT rules.

## Release boundary

The `v0.14.27` image is published and locked by its real manifest digest. Before promoting this catalog candidate, run the catalog audit and validate the selected backend on modern nft-only and explicit legacy hosts as appropriate. The earlier `v0.14.26` two-host and rolling-upgrade results apply only to version `3`; they are not evidence for this candidate.
