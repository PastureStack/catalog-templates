# SPDX-License-Identifier: MIT
version: '2'

services:
  network-diagnostics-service:
    image: ghcr.io/pasturestack/network-diagnostics-service:v0.2.0
    restart: always
    environment:
      PASTURESTACK_DIAGNOSTICS_TOKEN: '${COLLECTION_TOKEN}'
      PASTURESTACK_DIAGNOSTICS_HISTORY_LENGTH: '${HISTORY_LENGTH}'
      PASTURESTACK_DIAGNOSTICS_MAX_AGENTS: '${MAX_AGENTS}'
      PASTURESTACK_DIAGNOSTICS_RETENTION_HOURS: '${RETENTION_HOURS}'
    ports:
      - '${PUBLISHED_PORT}:8080'
    volumes:
      - network-diagnostics-data:/var/lib/pasturestack-network-diagnostics
    labels:
      io.pasturestack.component: network-diagnostics-service
    cpu_shares: 256
    mem_limit: 256m
    logging:
      driver: json-file
      options:
        max-size: 25m
        max-file: '2'

  network-diagnostics-agent:
    image: ghcr.io/pasturestack/network-diagnostics-agent:v0.2.0
    restart: always
    environment:
      PASTURESTACK_DIAGNOSTICS_TOKEN: '${COLLECTION_TOKEN}'
      PASTURESTACK_DIAGNOSTICS_URL: 'http://network-diagnostics-service:8080'
      PASTURESTACK_DIAGNOSTICS_INTERVAL_SECONDS: '${COLLECTION_INTERVAL_SECONDS}'
      PASTURESTACK_DIAGNOSTICS_REQUEST_TIMEOUT_SECONDS: '${REQUEST_TIMEOUT_SECONDS}'
    expose:
      - '8090'
    volumes:
      - /proc:/host/proc:ro
      - /etc/resolv.conf:/host/etc/resolv.conf:ro
      - /etc/machine-id:/host/etc/machine-id:ro
    labels:
      io.pasturestack.component: network-diagnostics-agent
      io.rancher.scheduler.global: 'true'
    cpu_shares: 128
    mem_limit: 64m
    logging:
      driver: json-file
      options:
        max-size: 10m
        max-file: '2'

volumes:
  network-diagnostics-data:
    driver: local
