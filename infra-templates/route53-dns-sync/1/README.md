# PastureStack Route 53 DNS Sync

> PastureStack is an independent community effort to preserve, audit, and modernize the Rancher 1.6 ecosystem. It is not affiliated with or endorsed by Rancher Labs or SUSE.

This infrastructure template synchronizes service addresses from one compatible
environment to an existing Amazon Route 53 hosted zone.

- Image: `ghcr.io/pasturestack/external-dns-sync:v0.8.0`
- Source: [`PastureStack/external-dns-sync@v0.8.0`](https://github.com/PastureStack/external-dns-sync/tree/v0.8.0)
- Upstream: [`rancher-archives/external-dns`](https://github.com/rancher-archives/external-dns)

The image reference always uses the semantic release tag. Published Catalog
manifests do not expose an image digest because long digest text breaks the
legacy service interface. Release validation records immutable identity
separately.

## DNS behavior

The default A-record name is:

```text
<service>.<stack>.<environment>.<hosted-zone>
```

The service also maintains one ownership TXT record. It uses that record to
update or remove only the A records it owns. Existing unrelated records in the
hosted zone are not managed.

The current compatible control plane injects environment-scoped API
credentials through its agent-role protocol. The runtime maps those values to
the neutral PastureStack API contract. A reviewed host CA file can optionally
be mounted read-only when a private certificate authority is required.

## AWS permissions

Use an IAM role whenever practical. Otherwise, create a dedicated access key
with permissions limited to the hosted zone used by this stack. The minimum
API actions are:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "route53:GetHostedZone",
        "route53:GetHostedZoneCount",
        "route53:ListHostedZonesByName",
        "route53:ListResourceRecordSets"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "route53:ChangeResourceRecordSets",
      "Resource": "arn:aws:route53:::hostedzone/<HOSTED_ZONE_ID>"
    }
  ]
}
```

Replace `<HOSTED_ZONE_ID>` with the selected zone. Do not commit credentials or
include them in issue reports, screenshots, or diagnostic logs.

## Upgrade compatibility

Neutral PastureStack DNS policy labels take precedence. The runtime also reads
the four documented historical service and host label identifiers so existing
workloads retain their DNS policy during an in-place upgrade. See the runtime
repository's `COMPATIBILITY.md` for the exact bounded protocol surface.

Only one active DNS Sync instance should manage a given environment and hosted
zone combination. Before changing the TTL during an upgrade from a pre-0.6
runtime, complete the runtime upgrade first and change the TTL in a second
operation.

## Runtime boundary

The container runs as UID/GID `10001:10001`. It does not use privileged mode,
host networking, a Docker socket, or writable host storage. Its dependency-aware
health endpoint is available only on container port `10000`.

The template is MIT-licensed. External DNS Sync remains Apache-2.0, and its
bundled dependencies retain their own licenses and notices. Upstream Git
history and authorship are preserved in the source repository.
