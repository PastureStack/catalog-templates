<!-- SPDX-License-Identifier: MIT -->

# PastureStack Vault Volume v0.2.3 candidate

## Source candidate

This source prepares numeric revision 5 only. It is not published or
deployed. Catalog v0.3.16 and numeric revision 4 remain the published
installation coordinates. New component digests, producer identities, SBOMs
and scan receipts are pending. The candidate cannot pass the publication-
evidence gate yet; no new component acceptance is claimed.

Planned image replacements (published input -> unpublished candidate):

- `ghcr.io/pasturestack/vault-secrets-bridge:v0.1.2` -> `ghcr.io/pasturestack/vault-secrets-bridge:v0.1.3`
- `ghcr.io/pasturestack/secrets-flexvolume-plugin:v0.2.1` -> `ghcr.io/pasturestack/secrets-flexvolume-plugin:v0.2.2`

The runtime definitions preserve the prior revision byte-for-byte except for
these image tags and the visible Catalog version. Commands, defaults, resource
parameters, permissions, sidekicks, volumes, firewall choices and plugin
responsibilities retain their existing contracts. Obtain real publication
evidence before promoting this source candidate.

## Published revision 4 reference

The following guidance and validation statements describe the previous
published inputs only. Their evidence does not validate the candidate images.

This infrastructure entry installs one unprivileged environment bridge and one
host-local Docker volume driver on every eligible managed host. A workload
requests an allowed policy set; the driver signs the request with the host
identity key, and the bridge verifies the active host before asking Vault for a
short-lived, response-wrapped child token.

The bridge is configured with an existing platform Secret containing one
renewable, narrowly scoped issuing token. The Secret is mounted read-only and
read from a file. It is not placed in Compose environment values, command-line
arguments, health responses, or logs.

### Vault preparation

Create a token role whose allowed policies are limited to the applications in
this environment. Create a renewable issuing token that can create child tokens
through that role and revoke their accessors, store the token as a platform
Secret, and select that Secret while installing this card. Keep the child-token
and response-wrapping lifetimes short.

The Catalog allowlist is an additional boundary: a workload request must be a
subset of the comma-separated policies entered during installation.

### Workload use

```yaml
version: '2'
services:
  application:
    image: example/application:v1.0.0
    volumes:
    - vault-token:/run/vault:ro

volumes:
  vault-token:
    driver: pasturestack-vault-volume
    driver_opts:
      io.pasturestack.vault.policies: default,application
      io.pasturestack.vault.file: token
      io.pasturestack.vault.uid: '1000'
      io.pasturestack.vault.gid: '1000'
      io.pasturestack.vault.mode: '0400'
    per_container: true
```

The file contains a response-wrapping token, not the issuing token or an
unwrapped child token. The application unwraps it once through the Vault API.
After the final workload consumer releases the volume, the driver asks the
bridge to revoke the child-token accessor and erases the memory-backed volume.

### Security boundary

The bridge uses
`ghcr.io/pasturestack/vault-secrets-bridge:v0.1.2`. It runs as UID 65532,
drops all Linux capabilities, uses a read-only root filesystem, and persists
only an encrypted accessor record in its dedicated state volume.

The driver uses
`ghcr.io/pasturestack/secrets-flexvolume-plugin:v0.2.1`. It drops all
capabilities before adding only `SYS_ADMIN`, `CHOWN`, and `FOWNER` for the
isolated `tmpfs` lifecycle and requested read-only ownership. It does not use
privileged mode, host networking, the host PID namespace, or a
container-engine socket.

Both images are public and use semantic version tags in Catalog and user
interfaces. Manifest digests remain release-verification evidence and are not
shown as deployment coordinates.

Source, security details, licensing, and release evidence are available from
the [Vault Secrets Bridge](https://github.com/PastureStack/vault-secrets-bridge)
and [Secret Volume Driver](https://github.com/PastureStack/secrets-flexvolume-plugin)
repositories.

PastureStack is an independent community effort to preserve, audit, and
modernize the Rancher 1.6 ecosystem. It is not affiliated with or endorsed by
Rancher Labs or SUSE.
