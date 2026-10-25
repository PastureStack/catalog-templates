<!-- SPDX-License-Identifier: MIT -->

# PastureStack Network Policy Manager v0.3.5 candidate

## Source candidate

This source prepares numeric revision 5 only. It is not published or
deployed. Catalog v0.3.16 and numeric revision 4 remain the published
installation coordinates. New component digests, producer identities, SBOMs
and scan receipts are pending. The candidate cannot pass the publication-
evidence gate yet; no new component acceptance is claimed.

Planned image replacements (published input -> unpublished candidate):

- `ghcr.io/pasturestack/network-policy-manager:v0.3.2` -> `ghcr.io/pasturestack/network-policy-manager:v0.3.3`

The runtime definitions preserve the prior revision byte-for-byte except for
these image tags and the visible Catalog version. Commands, defaults, resource
parameters, permissions, sidekicks, volumes, firewall choices and plugin
responsibilities retain their existing contracts. Obtain real publication
evidence before promoting this source candidate.

## Published revision 4 reference

The following guidance and validation statements describe the previous
published inputs only. Their evidence does not validate the candidate images.

This infrastructure entry installs one policy agent on every eligible managed
host. Each agent reads the established link-local Metadata endpoint, compiles
the active network policy, and atomically replaces only
`table inet pasturestack_policy`.

### Runtime behavior

The agent checks Metadata every 20 seconds. Valid policy changes preserve
established and related connections, allow required system traffic, and apply
the configured default action to local application workloads. A transient
Metadata or policy error keeps the last-known-good table. If valid Metadata
remains unavailable for ten minutes, the agent enters a visible availability-
safe fail-open state and restores enforcement after reconciliation succeeds.

The diagnostic readiness endpoint listens on host port `8092`. Rancher 1.6
cannot address a health target for a host-network container without a container
IP, so this revision deliberately does not declare a Rancher health check that
would remain indefinitely in `initializing`. Operators can query `/readyz`
directly on each managed host; failures omit identifiers, addresses, labels,
selectors, and policy documents.

### Security boundary

The container uses host networking and only `NET_ADMIN`. It drops every other
capability, runs with a read-only root filesystem and
`no-new-privileges`, and does not use privileged mode, host PID, a
container-engine socket, host filesystem mounts, API credentials, or secret
input.

Graceful stack removal stops reconciliation and deletes only the independently
owned nftables table. An unexpected container or host failure leaves the
last-known-good table in place. Review the source repository before changing
the polling, stale-data, or shutdown behavior.

### License and provenance

The template files and original icon are MIT-licensed PastureStack
contributions. The image source retains its Apache License 2.0, preserved
upstream history, authorship, and notices. Ubuntu, nftables, and bundled
dependencies retain their respective upstream licenses.

PastureStack is an independent community effort to preserve, audit, and
modernize the Rancher 1.6 ecosystem. It is not affiliated with or endorsed by
Rancher Labs or SUSE.
