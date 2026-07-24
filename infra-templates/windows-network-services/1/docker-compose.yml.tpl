# SPDX-License-Identifier: MIT
version: '2'

services:
  windows-metadata:
    image: ghcr.io/pasturestack/metadata-service-windows:v0.9.12-windows-ltsc2022
    network_mode: transparent
    command:
    - --reload-interval-limit=${RELOAD_INTERVAL_LIMIT}
    - --subscribe
    labels:
      io.pasturestack.component: windows-metadata-service
      io.rancher.sidekicks: windows-internal-dns
      io.rancher.container.create_agent: 'true'
      io.rancher.container.agent.volumes_strategy: skip
      io.rancher.container.create_agent_label: 'no'
      io.rancher.container.agent_service.metadata: 'true'
      io.rancher.scheduler.affinity:host_label: io.rancher.host.os=windows
      io.rancher.scheduler.global: 'true'
    logging:
      driver: json-file
      options:
        max-size: 25m
        max-file: '2'

  windows-internal-dns:
    image: ghcr.io/pasturestack/internal-dns-windows:v0.17.12-windows-ltsc2022
    network_mode: transparent
    command:
    - --listen=169.254.169.251:53
    - --metadata-url=http://169.254.169.250/2016-07-29
    - --metadata-answer=169.254.169.250
    - --answers=C:\pasturestack\answers.json
    - --recurser-timeout=${DNS_RECURSER_TIMEOUT}
    - --ttl=${TTL}
    - --never-recurse-to=169.254.169.250,169.254.169.251
    labels:
      io.pasturestack.component: windows-internal-dns
      io.rancher.scheduler.affinity:host_label: io.rancher.host.os=windows
      io.rancher.scheduler.global: 'true'
    links:
    - windows-metadata
    logging:
      driver: json-file
      options:
        max-size: 25m
        max-file: '2'
