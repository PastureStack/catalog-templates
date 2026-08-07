# SPDX-License-Identifier: MIT
version: '2'

services:
  network-plugin-manager:
    image: ghcr.io/pasturestack/network-plugin-manager:v0.6.34
    privileged: true
    network_mode: host
    pid: host
    command:
    - network-plugin-manager
    - --metadata-url
    - http://169.254.169.250/2016-07-29
    - --arpsync-interval
    - '${ARP_SYNC_INTERVAL}'
    environment:
      DOCKER_BRIDGE: '${DOCKER_BRIDGE}'
      METADATA_IP: 169.254.169.250
    volumes:
    - /var/run/docker.sock:/var/run/docker.sock
    - /var/lib/docker:/var/lib/docker
    - /lib/modules:/lib/modules:ro
    - /run:/run
    - /var/run:/var/run
    - rancher-cni-driver:/etc/cni
    - rancher-cni-driver:/opt/cni
    labels:
      io.pasturestack.component: network-plugin-manager
      io.rancher.scheduler.global: 'true'
    logging:
      driver: json-file
      options:
        max-size: 25m
        max-file: '2'

  metadata:
    image: ghcr.io/pasturestack/metadata-service:v0.9.11
    user: root
    cap_add:
    - NET_ADMIN
    network_mode: bridge
    command:
    - /bin/bash
    - -ec
    - |
      export PLATFORM_URL="$${PLATFORM_URL:-$${CATTLE_URL:-}}"
      export PLATFORM_ACCESS_KEY="$${PLATFORM_ACCESS_KEY:-$${CATTLE_ACCESS_KEY:-}}"
      export PLATFORM_SECRET_KEY="$${PLATFORM_SECRET_KEY:-$${CATTLE_SECRET_KEY:-}}"
      exec metadata-service --reload-interval-limit="${RELOAD_INTERVAL_LIMIT}" --subscribe
    environment:
      PLATFORM_CA_ROOT: /var/lib/rancher/etc/ssl/ca.crt
    labels:
      io.pasturestack.component: metadata-service
      io.rancher.sidekicks: dns
      io.rancher.container.create_agent: 'true'
      io.rancher.scheduler.global: 'true'
      io.rancher.container.agent_service.metadata: 'true'
    logging:
      driver: json-file
      options:
        max-size: 25m
        max-file: '2'
    sysctls:
      net.ipv4.conf.all.send_redirects: '0'
      net.ipv4.conf.default.send_redirects: '0'
    cpu_period: ${CPU_PERIOD}
    cpu_quota: ${CPU_QUOTA}

  dns:
    image: ghcr.io/pasturestack/internal-dns:v0.17.11
    network_mode: container:metadata
    command:
    - internal-dns
    - --listen
    - 169.254.169.250:53
    - --recurser-timeout
    - '${DNS_RECURSER_TIMEOUT}'
    - --ttl
    - '${TTL}'
    environment:
      PLATFORM_METADATA_ENABLED: 'true'
      PLATFORM_METADATA_URL: http://localhost/2016-07-29
      PLATFORM_METADATA_ANSWER: 169.254.169.250
      NEVER_RECURSE_TO: 169.254.169.250
      PLATFORM_DNS_ANSWERS_FILE: /etc/internal-dns/answers.json
    labels:
      io.pasturestack.component: internal-dns
      io.rancher.scheduler.global: 'true'
    logging:
      driver: json-file
      options:
        max-size: 25m
        max-file: '2'
