<!-- SPDX-License-Identifier: MIT -->

# PastureStack Network Diagnostics

This infrastructure entry installs one authenticated aggregation service and
one non-root collector on every eligible managed host. The collectors send
only bounded aggregate counters and a pseudonymous host identifier. They do
not send interface names, IP or MAC addresses, routes, resolver values, host
names, container or process names, commands, environment variables, workload
content, files, credentials, or logs.

## Installation

Provide a random token containing 32 to 256 characters. The same token
authorizes collector uploads and operator API requests. It is masked by the
Catalog form, supplied only through container environment variables, and never
accepted as a command-line argument or written to application logs.

The service publishes port `8091` by default so it does not conflict with the
control plane on port `8080`. After installation, open
`http://MANAGED_HOST:8091/` for the English operator page, or send
`Accept-Language: zh-TW` for Traditional Chinese. The health endpoint is
public; summary and bundle endpoints require
`Authorization: Bearer <collection-token>`.

Snapshots are retained in the stack-owned `network-diagnostics-data` local
volume. Back up or migrate that volume before moving the service to another
host. Removing the stack may remove the volume depending on the control-plane
cleanup option selected by the operator.

## Runtime boundary

The agent is globally scheduled and reads only `/proc`, `/etc/resolv.conf`,
and `/etc/machine-id` through read-only mounts. The machine identifier is used
only as local input to an HMAC-SHA-256 pseudonym and is never transmitted.
Neither container requests privileged mode, host networking, host PID
visibility, Linux capabilities, a container-engine socket, or writable host
storage. The service runs as numeric user `65532` from a shell-free image.

## License and provenance

The template files are MIT-licensed PastureStack contributions. The agent
retains its inherited Apache License 2.0 and upstream history. The service is a
new Apache-2.0 PastureStack implementation whose historical upstream reference
has no repository-level license; historical source and history are excluded
from the current release. See each source repository and
`catalog-images.json` for the exact reviewed boundaries.
