<!-- SPDX-License-Identifier: MIT -->

# Legacy Container Crontab upgrade to Container Cron v0.6.2

This compatibility entry is hidden from the Catalog launch list. New installations
continue to use `pasturestack:infra*container-schedule:4`. The compatibility entry
exists only to resolve and upgrade an installed
`catalog://library:infra*container-crontab:3` through the ordinary Stack
`upgrade`, `finishupgrade`, and `rollback` actions.

Revision 3 preserves the original upstream Compose files, questions, and README
from [rancher/rancher-catalog@52a5850bc49247eadd84045da890deaeaeddb9a4](https://github.com/rancher/rancher-catalog/tree/52a5850bc49247eadd84045da890deaeaeddb9a4/infra-templates/container-crontab/3).
Its `rancher/container-crontab:v0.5.0` image is legacy rollback material with an
unassessed current security status; it is never a new-install default or claimed
to satisfy the current runtime security gate.

Revision 4 uses the already published
`ghcr.io/pasturestack/container-cron:v0.6.2`; its source, manifest digest, SBOM,
and runtime scan receipts are recorded in `catalog-images.json`. It keeps the
`container-crontab` service key and the `metrics` and `debug` answer names. The
upgrade replaces the existing service rather than adding `container-schedule`.
The stored identifier advances normally from `:3` to `:4` in its original
namespace. Resolving the alias alone does not edit an installed Stack.

The service runs globally and retains Docker socket access, an always-restart
policy, and container-name hostname assignment. The historical `--rancher-mode`
switch maps to the maintained runtime's `--metadata-mode` flag. This preserves
the Metadata service-state checks: managed workload jobs run only while their
service is `active` and are deactivated while the service is inactive or waiting
for upgrade confirmation. The obsolete Docker API version override is removed.
Managed workload labels, including
`cron.schedule`, `cron.action`, `cron.restart_timeout`, and any existing timezone
labels or `TZ` environment values, belong to the workload and must remain
unchanged. This revision does not introduce a `cron.timezone` interpretation.

The upgrade strategy explicitly uses `start_first: false`. The old scheduler
must stop before its replacement starts on each host; rollback uses the same
service upgrade strategy. The runtime has no cross-process leader election.
Do not run the canonical Container Schedule service beside this compatibility
service on the same Docker daemon.

Before finishing an upgrade, verify the same Stack and service identities, the
original `metrics`/`debug` answers, unchanged workload labels/options, and Docker
events showing no old/new scheduler overlap. Exercise rollback before
`finishupgrade`; finishing discards the ordinary rollback window. A failed new
image start must remain recoverable by the ordinary Stack rollback action.
