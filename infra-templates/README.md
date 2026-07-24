<!-- SPDX-License-Identifier: MIT -->

# Infrastructure Templates

`Metadata Healthcheck` is enabled as an infrastructure release candidate. Its image is public, referenced by an explicit semantic version tag, reviewed, and tested against the established link-local Metadata endpoint without depending on a DNS alias. Earlier Catalog-created lifecycle tests passed credential injection, compatibility mapping, global scheduling, readiness, restart, two-daemon reporting, and removal. A fresh v0.3.15 multi-host upgrade, rollback, and complete infrastructure-stack removal remain required.

`PastureStack IPsec Overlay` is also enabled as a release candidate. Its public versioned release has passed encrypted two-host traffic, CNI installation, strongSwan VICI, vulnerability, secret, provenance, and anonymous-distribution gates. The Catalog-created stack scheduled globally across two isolated Docker daemons together with Network Services and Metadata Healthcheck. Managed workloads passed Metadata, DNS, bidirectional HTTP and ICMP, AES-GCM XFRM, published host ports, daemon restart recovery, rolling replacement, upgrade, and native rollback. The template deliberately retains only the control-plane labels, filename, version gate, volume name, and service marker required by the compatible protocol. Complete infrastructure-stack removal and a clean multi-VM acceptance run remain required before production approval.

`PastureStack Network Services` is enabled as a release candidate with public, version-tagged Network Plugin Manager, Metadata Service, and Internal DNS images. It retains the existing control-plane labels, credential fallbacks, CA path, and shared CNI volume only where the compatible protocol still consumes them. Its combined single-host managed-network gate passed together with the overlay and healthcheck candidates. The same services then scheduled globally on two isolated Docker daemons, served managed workloads on both, and converged after a daemon restart. Multi-host upgrade, rollback, and complete infrastructure-stack removal remain under validation.

Install and activate `Metadata Healthcheck` before using infrastructure health as a release signal. Then install `PastureStack Network Services`, followed by `PastureStack IPsec Overlay`. Network Services supplies the CNI, Metadata, and DNS contracts; Metadata Healthcheck converts the declared `/connectivity` probe into control-plane health events.

Additional infrastructure templates are added only after every Runtime image
they reference is public, assigned a non-overwritten semantic version tag,
reviewed, and validated at the required privilege boundary.
