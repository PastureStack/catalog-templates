<!-- SPDX-License-Identifier: MIT -->

# Infrastructure Templates

`Metadata Healthcheck` is enabled as an infrastructure release candidate. Its image is public, pinned by digest, reviewed, and component-tested on an isolated Linux VM. A Catalog-created `system=true` stack has passed credential injection, compatibility mapping, global scheduling, readiness, restart, and removal on one isolated host. It has also reported the real overlay connectivity check through the managed CNI network. It is not production-approved until multi-host reporting, upgrade, and rollback tests pass.

`PastureStack IPsec Overlay` is also enabled as a release candidate. Its public digest has passed two-node encrypted traffic, VXLAN fallback, CNI installation, strongSwan VICI, vulnerability, secret, provenance, and anonymous-distribution gates. Catalog creation, managed CNI addressing, Metadata, DNS, control-plane return traffic, connectivity health, and a deactivate/activate cycle passed together with Network Services and Metadata Healthcheck on one isolated host. The template deliberately retains only the control-plane labels, filename, version gate, volume name, and service marker required by the compatible protocol. The complete multi-host Catalog lifecycle, published host ports, host restart, upgrade, and rollback remain required before production approval.

`PastureStack Network Services` is enabled as a release candidate with public, digest-pinned Network Plugin Manager, Metadata Service, and Internal DNS images. It retains the existing control-plane labels, credential fallbacks, CA path, and shared CNI volume only where the compatible protocol still consumes them. Its combined single-host managed-network gate passed together with the overlay and healthcheck candidates; the multi-host Catalog lifecycle remains under validation.

Install and activate `Metadata Healthcheck` before using infrastructure health as a release signal. Then install `PastureStack Network Services`, followed by `PastureStack IPsec Overlay`. Network Services supplies the CNI, Metadata, and DNS contracts; Metadata Healthcheck converts the declared `/connectivity` probe into control-plane health events.

Additional infrastructure templates are added only after every Runtime image they reference is public, pinned by digest, reviewed, and validated at the required privilege boundary.
