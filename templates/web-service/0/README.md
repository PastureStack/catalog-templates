<!-- SPDX-License-Identifier: MIT -->

# Web Service 1.30.4

This application stack runs the reviewed upstream NGINX image on a configurable public port. PastureStack mirrors the exact multi-platform OCI digest to public GHCR, so deployment does not depend on a mutable tag, a private registry, or an operator-hosted artifact server.

The template configures one service instance and a TCP health check on container port 80. The default public port is 8088. Change it if that port is already in use on the selected host.

## Supply-chain boundary

- Image source: [`nginx/docker-nginx`](https://github.com/nginx/docker-nginx/tree/ccdab6c99ae2e2fc53a144dc68d6b8f44163adf2/stable/alpine)
- PastureStack mirror: [`ghcr.io/pasturestack/web-service`](https://github.com/orgs/PastureStack/packages/container/package/web-service)
- Immutable image digest: `sha256:97d490c12ba55b4946b01546d1c3ed324e8d41ab1c9fcb2a616aa470620e5b46`

The mirror preserves the reviewed upstream image digest and does not relicense its contents. The MIT license in this template directory covers only the PastureStack-authored template files. NGINX, Alpine Linux, and bundled packages retain their upstream licenses.
