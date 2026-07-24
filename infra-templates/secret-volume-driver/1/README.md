# PastureStack Secret Volume

This infrastructure entry installs one host-local Docker volume driver on
every eligible managed host. The compatible control plane supplies an opaque
authorization token for each approved secret volume. The driver fetches only
the corresponding encrypted records, verifies their signatures, decrypts them
with the host identity key, and exposes read-only files to the target workload
through an isolated in-memory filesystem.

## Security boundary

The service uses
`ghcr.io/pasturestack/secrets-flexvolume-plugin:v0.1.0`. The Catalog and user
interface intentionally use the semantic version tag without a manifest
digest.

The container:

- drops all Linux capabilities before adding only `SYS_ADMIN`, which is needed
  to create and remove the isolated `tmpfs`;
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

## Workload use

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
