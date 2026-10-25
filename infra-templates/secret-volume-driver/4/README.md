<!-- SPDX-License-Identifier: MIT -->

# PastureStack Secret Volume v0.1.4 candidate

## Source candidate

This source prepares numeric revision 4 only. It is not published or
deployed. Catalog v0.3.16 and numeric revision 3 remain the published
installation coordinates. New component digests, producer identities, SBOMs
and scan receipts are pending. The candidate cannot pass the publication-
evidence gate yet; no new component acceptance is claimed.

Planned image replacements (published input -> unpublished candidate):

- `ghcr.io/pasturestack/secrets-flexvolume-plugin:v0.2.1` -> `ghcr.io/pasturestack/secrets-flexvolume-plugin:v0.2.2`

The runtime definitions preserve the prior revision byte-for-byte except for
these image tags and the visible Catalog version. Commands, defaults, resource
parameters, permissions, sidekicks, volumes, firewall choices and plugin
responsibilities retain their existing contracts. Obtain real publication
evidence before promoting this source candidate.

## Published revision 3 reference

The following guidance and validation statements describe the previous
published inputs only. Their evidence does not validate the candidate images.

This infrastructure entry installs one host-local Docker volume driver on
every eligible managed host. The compatible control plane supplies an opaque
authorization token for each approved secret volume. The driver fetches only
the corresponding encrypted records, verifies their signatures, decrypts them
with the host identity key, and exposes read-only files to the target workload
through an isolated in-memory filesystem.

### Security boundary

The service uses
`ghcr.io/pasturestack/secrets-flexvolume-plugin:v0.2.1`. The Catalog and user
interface intentionally use the semantic version tag without a manifest
digest.

The container:

- drops all Linux capabilities before adding `SYS_ADMIN`, which is needed to
  create and remove the isolated `tmpfs`, and `CHOWN`, which is needed to
  apply the workload's requested numeric ownership to secret files, plus
  `FOWNER`, which is needed to lock the final mode after that ownership
  change;
- disables Docker's default AppArmor profile because that generic profile
  blocks the required `tmpfs` mount syscall; the container remains
  non-privileged, drops every capability except `SYS_ADMIN`, `CHOWN`, and
  `FOWNER`, uses `no-new-privileges`, and is constrained by the remaining
  controls below;
- uses a read-only root filesystem and a bounded, non-executable temporary
  directory;
- does not use privileged mode, host networking, the host PID namespace, or a
  container-engine socket;
- reads the host identity key through one read-only bind mount; and
- writes only its Docker plugin socket and the dedicated shared volume root.

Secret files accept only safe relative paths, bounded UID and GID values, and
read-only modes. Values, tokens, credentials, identity keys, file names, and
encrypted envelopes are excluded from health responses and logs. A volume is
unmounted and erased after its final workload consumer releases it.

### Workload use

Create a secret through the compatible control plane, then select it from a
workload's **Secrets** section. The control plane creates the required volume
and supplies the authorization token; operators do not place secret material
in Compose, Catalog answers, or command-line arguments.

The driver registers as `pasturestack-secret-volume`. Health faults are
reported without automatically recreating the driver container so that active
mounts are not disturbed by a restart loop.

Source, operating instructions, security details, licensing, and release
evidence are available from the
[PastureStack Secret Volume Driver repository](https://github.com/PastureStack/secrets-flexvolume-plugin).

PastureStack is an independent community effort to preserve, audit, and
modernize the Rancher 1.6 ecosystem. It is not affiliated with or endorsed by
Rancher Labs or SUSE.
