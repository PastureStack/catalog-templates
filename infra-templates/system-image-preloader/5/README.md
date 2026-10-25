<!-- SPDX-License-Identifier: MIT -->

# System Image Preloader

This global start-once service discovers system-stack image references and asks each host Docker daemon to cache absent images.

Numeric revision 5 (display version `v0.3.4`) uses the published image `ghcr.io/pasturestack/system-image-preloader:v0.3.4`.
Previous revision 4 and `ghcr.io/pasturestack/system-image-preloader:v0.3.3` remain available.
Questions, environment, resource parameters, volumes, permissions and plugin ownership are unchanged.
Exact publication records are in `catalog-images.json`; environment acceptance remains separate.

### Reviewed image

- Image: `ghcr.io/pasturestack/system-image-preloader:v0.3.4`
- Source: [`PastureStack/system-image-preloader@624a45cd001a92cdf5132f487ba14e161dff40d2`](https://github.com/PastureStack/system-image-preloader/tree/624a45cd001a92cdf5132f487ba14e161dff40d2)
- Source license: Apache-2.0; Ubuntu, Docker CLI, `yq`, `gomplate`, and their
  dependencies retain their upstream licenses and notices
- Security gate: full-severity scan, no available fix, no unreviewed finding or secret
- Distribution gate: public GHCR and anonymous version-tag manifest access
  passed

### Security boundary

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

### Validation

Published image identity, runtime SBOM, raw and effective findings, and package
installation verification are recorded in `catalog-images.json`. Catalog source
and API contracts verify the new default and retained revisions. Managed-host
image caching, upgrade and rollback acceptance remain environment-specific.
