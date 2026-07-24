<!-- SPDX-License-Identifier: MIT -->

# PastureStack Amazon ECR Credential Sync v3.1.0

This infrastructure service refreshes the short-lived Docker registry
credentials returned by Amazon Elastic Container Registry. It synchronizes
immediately after startup and every six hours thereafter.

## Reviewed image

- Image: `ghcr.io/pasturestack/ecr-credential-sync:v3.1.0`
- Source: [`PastureStack/ecr-credential-sync@v3.1.0`](https://github.com/PastureStack/ecr-credential-sync/tree/v3.1.0)
- Upstream: [`rancher/rancher-ecr-credentials`](https://github.com/rancher/rancher-ecr-credentials)
- Source license: Apache-2.0; Ubuntu and vendored Go dependencies retain their
  upstream licenses and notices
- Runtime user: `10001:10001`
- Security gate: Trivy HIGH 0 and CRITICAL 0
- Distribution gate: public GHCR and anonymous version-tag manifest access
  passed

PastureStack is an independent community effort to preserve, audit, and
modernize the Rancher 1.6 ecosystem. It is not affiliated with or endorsed by
Rancher Labs or SUSE.

## Security boundary

Use an environment-scoped API key and the least-privilege AWS permissions
required to call the ECR authorization-token API. Password questions are
masked in the launch form, but the deployed service still receives those
values as container environment variables. Restrict access to the stack,
service configuration, and host runtime.

For the current environment, the compatible control plane injects its
environment API credentials through the literal `io.rancher.*` agent labels
and historical `CATTLE_*` variables. The startup command maps those protocol
identifiers to the neutral `PLATFORM_*` runtime contract. They are compatibility
identifiers, not PastureStack branding.

The shared AWS profile mount is disabled by default. When enabled, the selected
host directory is mounted read-only at `/home/pasturestack/.aws`. The service
does not require privileged mode, host networking, a Docker socket, or host
filesystem access beyond that optional credential directory.

## Validation and lifecycle

The release passed race-enabled unit tests, static analysis, mock Amazon ECR
request signing, registry and credential create/update integration tests,
health endpoint checks, non-root and OCI metadata checks, license-file
verification, current HIGH/CRITICAL vulnerability and secret scans, and an
isolated container lifecycle test. Logs were checked to ensure that AWS,
environment API, authorization-token, and role credentials were not exposed.

To roll back, upgrade this stack to the previously reviewed Catalog revision
and semantic image tag. Remove only the exact stack, service, and optional
profile mount created for this component; no broad host cleanup is required.
