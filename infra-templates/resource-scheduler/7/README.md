<!-- SPDX-License-Identifier: MIT -->

# Resource Scheduler v0.8.21 candidate

## Source candidate

This source prepares numeric revision 7 only. It is not published or
deployed. Catalog v0.3.16 and numeric revision 6 remain the published
installation coordinates. New component digests, producer identities, SBOMs
and scan receipts are pending. The candidate cannot pass the publication-
evidence gate yet; no new component acceptance is claimed.

Planned image replacements (published input -> unpublished candidate):

- `ghcr.io/pasturestack/resource-scheduler:v0.8.20` -> `ghcr.io/pasturestack/resource-scheduler:v0.8.21`

The runtime definitions preserve the prior revision byte-for-byte except for
these image tags and the visible Catalog version. Commands, defaults, resource
parameters, permissions, sidekicks, volumes, firewall choices and plugin
responsibilities retain their existing contracts. Obtain real publication
evidence before promoting this source candidate.

## Published revision 6 reference

The following guidance and validation statements describe the previous
published inputs only. Their evidence does not validate the candidate images.

This template deploys the functional PastureStack resource scheduler as the
control plane's scheduling agent. It consumes the established control-plane
event and Metadata contracts while using the native PastureStack executable,
debug option, public image, and semantic version tag.

The runtime executes as UID and GID `10001:10001`. Only the scheduler binary
has permission to bind the compatibility health-check port.

This version reconnects the control-plane event subscriber after a clean
disconnect or an error and restarts the Metadata watcher after an error or a
recovered panic.

`/healthcheck` reports process liveness. `/readiness` reports whether the
control-plane and Metadata dependencies are currently available. A planned
control-plane restart can therefore make the service temporarily unready
without replacing the scheduler container.

This dependency-only security update uses the official Go and Ubuntu fixes.
Scheduling, questions, credentials, and health-check contracts are unchanged.
Packaged CI health evidence does not qualify a managed-system upgrade or rollback.
