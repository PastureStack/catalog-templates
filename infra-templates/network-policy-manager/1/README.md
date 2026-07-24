<!-- SPDX-License-Identifier: MIT -->

# PastureStack Network Policy Manager

This infrastructure entry installs one policy agent on every eligible managed
host. Each agent reads the established link-local Metadata endpoint, compiles
the active network policy, and atomically replaces only
`table inet pasturestack_policy`.

## Runtime behavior

The agent checks Metadata every 20 seconds. Valid policy changes preserve
established and related connections, allow required system traffic, and apply
the configured default action to local application workloads. A transient
Metadata or policy error keeps the last-known-good table. If valid Metadata
remains unavailable for ten minutes, the agent enters a visible availability-
safe fail-open state and restores enforcement after reconciliation succeeds.

The readiness endpoint listens on host port `8092`. Health-check failures are
reported without identifiers, addresses, labels, selectors, or policy
documents. The Catalog health strategy does not recreate containers
automatically, so a policy or Metadata fault cannot cause a restart loop.

## Security boundary

The container uses host networking and only `NET_ADMIN`. It drops every other
capability, runs with a read-only root filesystem and
`no-new-privileges`, and does not use privileged mode, host PID, a
container-engine socket, host filesystem mounts, API credentials, or secret
input.

Graceful stack removal stops reconciliation and deletes only the independently
owned nftables table. An unexpected container or host failure leaves the
last-known-good table in place. Review the source repository before changing
the polling, stale-data, or shutdown behavior.

## License and provenance

The template files and original icon are MIT-licensed PastureStack
contributions. The image source retains its Apache License 2.0, preserved
upstream history, authorship, and notices. Ubuntu, nftables, and bundled
dependencies retain their respective upstream licenses.

PastureStack is an independent community effort to preserve, audit, and
modernize the Rancher 1.6 ecosystem. It is not affiliated with or endorsed by
Rancher Labs or SUSE.
