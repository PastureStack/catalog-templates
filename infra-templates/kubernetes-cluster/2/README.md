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
