<!-- SPDX-License-Identifier: MIT -->

# Resource Scheduler v0.8.14

This template deploys the functional PastureStack resource scheduler as the
control plane's scheduling agent. It consumes the established control-plane
event and Metadata contracts while using the native PastureStack executable,
debug option, public image, and immutable image digest.

The runtime executes as UID and GID `10001:10001`. Only the scheduler binary
has permission to bind the compatibility health-check port.

This version treats a retry of the same workload's host-port reservation as
idempotent while continuing to reject a conflicting reservation owned by a
different workload.
