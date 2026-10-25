<!-- SPDX-License-Identifier: MIT -->

# PastureStack Container Schedule v0.6.2 candidate

## Source candidate

This source prepares numeric revision 4 only. It is not published or
deployed. Catalog v0.3.16 and numeric revision 3 remain the published
installation coordinates. New component digests, producer identities, SBOMs
and scan receipts are pending. The candidate cannot pass the publication-
evidence gate yet; no new component acceptance is claimed.

Planned image replacements (published input -> unpublished candidate):

- `ghcr.io/pasturestack/container-cron:v0.6.1` -> `ghcr.io/pasturestack/container-cron:v0.6.2`

The runtime definitions preserve the prior revision byte-for-byte except for
these image tags and the visible Catalog version. Commands, defaults, resource
parameters, permissions, sidekicks, volumes, firewall choices and plugin
responsibilities retain their existing contracts. Obtain real publication
evidence before promoting this source candidate.

## Published revision 3 reference

The following guidance and validation statements describe the previous
published inputs only. Their evidence does not validate the candidate images.

This infrastructure service watches Docker container events and runs scheduled
`start`, `stop`, or `restart` actions. A managed workload opts in with these
labels:

- `cron.schedule`: required six-field Cron expression.
- `cron.action`: optional `start`, `stop`, or `restart`; the default is
  `start`.
- `cron.restart_timeout`: optional stop or restart timeout in seconds.

### Reviewed image

- Image: `ghcr.io/pasturestack/container-cron:v0.6.1`
- Source: [`PastureStack/container-cron@2cce2cc80f2590239d5ef758a21c54a3f1e0f2b9`](https://github.com/PastureStack/container-cron/tree/2cce2cc80f2590239d5ef758a21c54a3f1e0f2b9)
- Source license: Apache-2.0; Ubuntu and bundled Go dependencies retain their
  upstream licenses
- Security gate: Trivy HIGH 0 and CRITICAL 0 for the operating system and Go
  binary
- Distribution gate: public GHCR and anonymous version-tag manifest access
  passed

### Security boundary

The service mounts `/var/run/docker.sock` read-write so it can control
containers. Docker socket access is equivalent to host administrator access.
Deploy this card only as a trusted global infrastructure service. It does not
request privileged mode, publish a host port, or accept a remote Docker
endpoint by default.

The compatible control plane requires the literal `rancher-compose.yml`
filename and `io.rancher.*` scheduling labels in this template. They are
protocol identifiers, not PastureStack branding.

### Validation

The release passed race-enabled unit tests, static analysis, image metadata and
license checks, a current HIGH/CRITICAL vulnerability scan, and an isolated
Docker lifecycle test. The test created one stopped workload and one
running workload, then verified that the service started the first and stopped
the second on schedule. All test containers were removed afterward.

The deployment intentionally uses the neutral container-event mode. It does
not depend on a branded legacy command-line switch or on service-state
translation through Metadata.
