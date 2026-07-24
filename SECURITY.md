# Security Policy

## Supported state

This repository is under migration review. Only entries listed in `SUPPORTED.md` are present in the current catalog tree; that list is still a release candidate until the Server release and isolated workload gates pass.

## Security boundaries

- Templates execute third-party images and may request privileged mode, host mounts, network access, cloud credentials, or the Docker socket.
- Every image must have a reviewed source, license, semantic version tag,
  architecture, and vulnerability assessment before release. Published version
  tags must never be overwritten; manifest digests belong only in release
  verification evidence.
- Dynamic image variables, mutable tags, unlisted registries, and image references absent from `catalog-images.json` fail the catalog audit.
- Questions and defaults must not embed secrets, private endpoints, or production data.
- Template icons and readmes are untrusted rendered content.
- The IPsec overlay candidate is intentionally privileged, joins host PID and
  network namespaces, installs CNI executables, reads scoped agent credentials,
  and changes XFRM, route, firewall, and bridge state. Its versioned release and
  compatibility contract must be validated together with the network-services
  stack on isolated hosts.
- The network-services candidate runs one privileged host-network manager per host with Docker socket, Docker state, kernel-module, runtime-mount, and shared-CNI access. Metadata credentials are scoped per instance and must never appear in template defaults, logs, or committed test output.
- The system-image-preloader candidate runs once per host with the Docker
  socket and scoped compatibility API credentials. Its optional host Docker
  configuration mount is read-only, privileged mode is disabled by default,
  and bounded failures must terminate instead of retrying forever.
- The secret-volume candidate reads the host identity key and writes only its
  dedicated plugin socket and shared volume root. It drops all capabilities
  before adding `SYS_ADMIN` solely for isolated `tmpfs` mounts. It does not use
  privileged mode, host networking, a host PID namespace, or the Docker socket.
  Secret values, authorization tokens, credentials, key material, file names,
  and encrypted envelopes must never appear in logs or committed evidence.

## Reporting

Report suspected vulnerabilities through this repository's private security advisory channel. Do not include live credentials or production template data in a public issue.
