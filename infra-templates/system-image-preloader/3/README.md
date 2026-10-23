<!-- SPDX-License-Identifier: MIT -->

# PastureStack System Image Preloader v0.3.0

This global, start-once infrastructure service discovers the images used by
compatible system stacks and asks each host Docker daemon to cache images that
are not already present.

## Reviewed image

- Image: `ghcr.io/pasturestack/system-image-preloader:v0.3.0`
- Source: [`PastureStack/system-image-preloader@150c78dbdb3f487a7003c83339cca5b76dde97f4`](https://github.com/PastureStack/system-image-preloader/tree/150c78dbdb3f487a7003c83339cca5b76dde97f4)
- Source license: Apache-2.0; Ubuntu, Docker CLI, `yq`, `gomplate`, and their
  dependencies retain their upstream licenses and notices
- Security gate: Trivy HIGH 0 and CRITICAL 0
- Distribution gate: public GHCR and anonymous version-tag manifest access
  passed

## Security boundary

The service mounts `/var/run/docker.sock` read-write. Docker socket access is
equivalent to host administrator access, so deploy only the reviewed image and
restrict who can edit this stack. The service receives scoped compatibility API
credentials automatically and never enables credential-bearing shell tracing.

Private-registry credentials are optional. When enabled, the selected host
Docker `config.json` is mounted read-only. Privileged mode remains off by
default and should be enabled only when required by the host security policy.
Image-pull retries and CPU-pressure waits are bounded.

The compatible control plane requires the literal `rancher-compose.yml`
filename and `io.rancher.*` agent and scheduling labels in this template. They
are protocol identifiers, not PastureStack branding.

## Validation

The release passed offline retry and URL-contract tests, container help and
version smoke tests, OCI metadata and license checks, a current HIGH/CRITICAL
vulnerability scan, and an isolated end-to-end lifecycle test. The lifecycle
test used mock metadata, environment, and Catalog APIs and verified that the
runtime discovered a Compose image and cached its semantic tag through a real
Docker socket. It removed only its exact test resources and performed no broad
prune.
