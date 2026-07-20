<!-- SPDX-License-Identifier: MIT -->

# PastureStack Native

This project template installs the reviewed infrastructure services required by
the native orchestration runtime:

- network management, Metadata, and internal DNS;
- encrypted IPsec and VXLAN workload networking;
- resource scheduling; and
- container health reporting.

Every referenced infrastructure template uses a public PastureStack image
pinned by an immutable digest. The compatibility runtime interprets the
template and provisions the system stacks; no separate catalog website or
operator-hosted image registry is required.
