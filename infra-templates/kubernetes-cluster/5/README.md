# PastureStack Kubernetes Cluster

PastureStack is an independent community effort to preserve, audit, and modernize the Rancher 1.6 ecosystem. It is not affiliated with or endorsed by Rancher Labs or SUSE.

This catalog template deploys a Kubernetes 1.12.10 compatibility cluster with maintained PastureStack runtime images. It is derived from the upstream `rancher/catalog` Kubernetes template version 63. The repository preserves the upstream Git history, authorship, dates, license, and attribution.

## Included runtime

- Kubernetes 1.12.10 compatibility package
- etcd 2.3.7 compatibility service with TLS and backups
- kubectl service and interactive shell
- host-file updater
- control-plane integration agent
- authentication webhook bridge
- ingress load-balancer service
- dedicated pod-pause and data-volume helper images

All user-facing image references use semantic version tags. Immutable digests, SBOMs, vulnerability scans, and integration evidence are retained outside the catalog interface.

## Compatibility update 5

This revision changes only the etcd service image to
`etcd-compat:v2.3.7-pasturestack.2`. The compatibility release replaces
permissive health-probe TLS with mutual TLS that verifies the managed service
identity, restores Unix-socket v3 client endpoints on Go 1.26, and uses fixed
gRPC error format strings. Its image has 0 Critical and 0 High Trivy findings,
0 detected image secrets, and a 130-component CycloneDX SBOM. Catalog revision
4 remains byte-for-byte immutable for definition comparison and rollback.

This security update does not change the persisted etcd data format or claim
that etcd 2.3 is supported upstream. Back up and restore-test the data before
upgrading an existing control-plane stack.

## Compatibility update 4

This revision keeps every control-plane service on the reviewed
`kubernetes-package:v1.12.10-pasturestack.3` release and updates both
catalog-operation services to `kubectl-service:v0.9.11-pasturestack.5`.
The new kubectl-service release restricts Kubernetes API discovery to approved
internal endpoints, rejects redirects and unsafe namespace values, and keeps
untrusted request data out of operational logs. Its CodeQL request-forgery and
log-injection alerts were fixed in code, not dismissed; its published image has
0 Critical and 0 High Trivy findings and 0 detected image secrets. The matching
package release continues to use the reviewed
`tiller:v2.17.0-pasturestack.2` compatibility image and verifies all Helm 2
release records before and after its rolling update. The previous template
remains immutable as version 3 so an operator can compare or roll back the
Catalog definition.

These revisions close the stale-image and release-mapping gap; they do not make
Kubernetes 1.12, etcd 2.3, or Helm 2 supported again. Treat this template as an
isolated import and migration boundary, preserve the etcd and Helm release
backups, and follow the staged retirement plan in the component repositories.

## Deliberately excluded legacy add-ons

The historical template could install Dashboard, KubeDNS, Heapster, Grafana, InfluxDB, and Tiller images. Those optional third-party images are not copied into PastureStack: several contain Critical vulnerabilities, and the retired projects are outside this official-platform migration scope. The template therefore does not expose an add-on switch that could create an insecure or broken deployment.

The core cluster remains suitable for API, scheduling, service-networking, authentication, ingress, backup, and pod-sandbox compatibility tests. Cluster DNS and monitoring require separately reviewed components before production use.

## Required host ports

Open TCP ports `10250` and `10255` for kubectl access. Exposed NodePort services use TCP ports `30000` through `32767` by default.

## Plane isolation

The default `none` mode allows a compact proof-of-concept deployment. For production-style separation, select `required` and label hosts with `compute=true`, `orchestration=true`, and `etcd=true`.

## Upgrade safety

Do not upgrade an existing cluster from a historical template older than `v1.2.4-rancher9` directly. Upgrade through the historical `v1.5.4-rancher1` boundary first and take an etcd backup. Test restores before changing the live stack.

## Compatibility identifiers

The template retains a limited set of `io.rancher.*` labels, `minimum_rancher_version`, internal `.rancher.internal` DNS names, provider values, and controller environment variables. They are protocol identifiers required by the Cattle 1.6 API and are not current product branding. Service names and user-facing descriptions use PastureStack terminology.

The template is licensed under Apache License 2.0. Each referenced image and included package retains its own license and attribution.
