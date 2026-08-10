<!-- SPDX-License-Identifier: MIT -->

# Resource Scheduler v0.8.16

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
