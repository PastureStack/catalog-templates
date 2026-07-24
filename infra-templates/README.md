<!-- SPDX-License-Identifier: MIT -->

# Infrastructure Templates

`PastureStack Container Schedule` is enabled with a public, immutable
version-tagged image. Race-enabled tests, static analysis, anonymous
distribution, a HIGH/CRITICAL vulnerability scan, and a real Docker start/stop
lifecycle passed. The service mounts the Docker socket read-write and therefore
must be treated as host-administrative infrastructure. It does not request
privileged mode or publish a host port.

`Metadata Healthcheck` is enabled as an infrastructure release candidate. Its image is public, referenced by an explicit semantic version tag, reviewed, and tested against the established link-local Metadata endpoint without depending on a DNS alias. Earlier Catalog-created lifecycle tests passed credential injection, compatibility mapping, global scheduling, readiness, restart, two-daemon reporting, and removal. A fresh v0.3.15 multi-host upgrade, rollback, and complete infrastructure-stack removal remain required.

`PastureStack IPsec Overlay` is also enabled as a release candidate. Its public versioned release has passed encrypted two-host traffic, CNI installation, strongSwan VICI, vulnerability, secret, provenance, and anonymous-distribution gates. The Catalog-created stack scheduled globally across two isolated Docker daemons together with Network Services and Metadata Healthcheck. Managed workloads passed Metadata, DNS, bidirectional HTTP and ICMP, AES-GCM XFRM, published host ports, daemon restart recovery, rolling replacement, upgrade, and native rollback. The template deliberately retains only the control-plane labels, filename, version gate, volume name, and service marker required by the compatible protocol. Complete infrastructure-stack removal and a clean multi-VM acceptance run remain required before production approval.

`PastureStack Network Services` is enabled as a release candidate with public, version-tagged Network Plugin Manager, Metadata Service, and Internal DNS images. It retains the existing control-plane labels, credential fallbacks, CA path, and shared CNI volume only where the compatible protocol still consumes them. Its combined single-host managed-network gate passed together with the overlay and healthcheck candidates. The same services then scheduled globally on two isolated Docker daemons, served managed workloads on both, and converged after a daemon restart. Multi-host upgrade, rollback, and complete infrastructure-stack removal remain under validation.

`PastureStack Network Diagnostics` is enabled with two public, version-tagged
images. Its real agent and service images passed reproducible-build, source,
license, vulnerability, secret, anonymous-distribution, non-root, bounded-data,
authenticated upload, bundle, persistence, localization, restart, and cleanup
checks. The agent reads only three host paths through read-only mounts and does
not request privileged mode, host namespaces, capabilities, a container-engine
socket, or writable host storage.

`PastureStack Network Policy Manager` is enabled with a public,
version-tagged image. Unit, race, repeated shuffled, static-analysis,
anonymous-distribution, HIGH/CRITICAL vulnerability, graceful cleanup, and
five consecutive two-host policy lifecycle gates passed. It uses host
networking with only `NET_ADMIN`, drops all other capabilities, and does not
request privileged mode, host PID, a container-engine socket, host filesystem
mounts, API credentials, or secret input. The health strategy reports faults
without automatically recreating the container.

`PastureStack NFS Storage` is enabled as a release candidate with a public,
version-tagged storage-driver image. Source, license, anonymous distribution,
image vulnerabilities, image secrets, NFS v3 mounting, read/write behavior,
safe owned-subdirectory purging, and direct-export retention have passed. Its
default removal policy retains data. Multi-host upgrade and rollback remain
under validation.

`PastureStack Secret Volume` is enabled with a public, version-tagged
host-local storage-driver image. Repeated and race-enabled tests, static
analysis, deterministic builds, anonymous distribution, HIGH/CRITICAL
vulnerability scanning, image-secret scanning, authenticated envelope
verification, encrypted-record decryption, read-only file modes,
multiple-consumer handling, and isolated `tmpfs` cleanup have passed. It drops
all Linux capabilities before adding only `SYS_ADMIN` for the memory-backed
mount and does not use privileged mode, host networking, a container-engine
socket, or unrestricted host storage. A complete Catalog-created two-host
workload lifecycle remains under validation.

`PastureStack Vault Volume` is enabled with public, version-tagged bridge and
driver images. Repeated and race-enabled tests, static analysis, deterministic
builds, anonymous distribution, HIGH/CRITICAL and image-secret scans, real
Vault response wrapping and unwrap, read-only `0400` issuing-token Secret
input, host authentication, policy allowlisting, restart recovery, accessor
revocation, and exact cleanup passed. The bridge remains unprivileged and
non-root. The global driver adds only the capabilities required for its
isolated memory-backed volume lifecycle and does not use host networking, a
host PID namespace, or a container-engine socket.

`PastureStack Amazon EBS Storage` is enabled with a real external-volume
driver and a public, version-tagged image. Existing volumes are the safe
default. Creating, formatting, detaching, or deleting a cloud volume requires
an explicit provisioning opt-in, and new volumes request encryption. Source,
license, anonymous distribution, image vulnerabilities, image secrets, safe
initialization, identifier validation, and provisioning-denial gates have
passed. A live AWS lifecycle remains under validation.

`PastureStack Amazon EFS Storage` is enabled with a real external-volume
driver and a public, version-tagged image. Existing filesystems are the safe
default. Creating a filesystem or mount target requires an explicit
provisioning opt-in plus operator-supplied subnet and security-group
identifiers. The driver never creates unrestricted NFS ingress. Source,
license, anonymous distribution, image vulnerabilities, image secrets, safe
initialization, identifier validation, and provisioning-denial gates have
passed. A live AWS lifecycle remains under validation.

`PastureStack Route 53 DNS Sync` is enabled with a public, version-tagged
External DNS Sync image. Race-enabled tests, static analysis, current
HIGH/CRITICAL and image-secret scans, non-root execution, and a complete
loopback Route 53-compatible create, update, restart, and removal lifecycle
passed. The template does not request privileged mode, host networking, a
Docker socket, or writable host storage. AWS permissions must be scoped to the
selected hosted zone.

`PastureStack VXLAN Overlay Network` is an optional release candidate backed
by the same reviewed, semantic-versioned network image as the encrypted
overlay. Its isolated two-node forwarding and overlay traffic gate passed.
VXLAN traffic is not encrypted and requires UDP port `4789` between all
participating hosts. It is not installed by the default project template.

Install and activate `Metadata Healthcheck` before using infrastructure health as a release signal. Then install `PastureStack Network Services`, followed by `PastureStack IPsec Overlay`. Network Services supplies the CNI, Metadata, and DNS contracts; Metadata Healthcheck converts the declared `/connectivity` probe into control-plane health events.

Additional infrastructure templates are added only after every Runtime image
they reference is public, assigned a non-overwritten semantic version tag,
reviewed, and validated at the required privilege boundary.
