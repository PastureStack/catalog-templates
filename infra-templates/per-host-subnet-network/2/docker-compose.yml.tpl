# SPDX-License-Identifier: MIT
version: '2'

services:
  per-host-subnet-controller:
    image: ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.26
    command: per-host-subnet
    privileged: true
    network_mode: host
    pid: host
    environment:
      PLATFORM_DEBUG: '${PASTURESTACK_DEBUG}'
      PLATFORM_METADATA_URL: http://169.254.169.250/2016-07-29
      PLATFORM_METADATA_STARTUP_TIMEOUT: '${METADATA_STARTUP_TIMEOUT}'
      PLATFORM_WATCH_INTERVAL: '${WATCH_INTERVAL}'
      PLATFORM_ENABLE_ROUTE_UPDATE: '${ENABLE_ROUTE_UPDATE}'
      PLATFORM_ROUTE_UPDATE_PROVIDER: host-gateway
    labels:
      io.pasturestack.component: per-host-subnet-controller
      io.rancher.scheduler.global: 'true'
    logging:
      driver: json-file
      options:
        max-size: 25m
        max-file: '2'

  per-host-subnet-cni:
    image: ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.26
    command: start-cni-driver.sh
    privileged: true
    network_mode: host
    pid: host
    environment:
      PASTURESTACK_DEBUG: '${PASTURESTACK_DEBUG}'
    labels:
      io.pasturestack.component: per-host-subnet-cni
      io.rancher.network.cni.binary: pasture-bridge
      io.rancher.container.dns: 'true'
      io.rancher.scheduler.global: 'true'
    volumes:
    - /var/run/docker.sock:/var/run/docker.sock
    - rancher-cni-driver:/opt/cni-driver
    logging:
      driver: json-file
      options:
        max-size: 25m
        max-file: '2'
    network_driver:
      name: PastureStack Per-Host Subnet Network
      default_network:
        name: per-host-subnet
        host_ports: {{ .Values.HOST_PORTS }}
        dns:
        - 169.254.169.250
        dns_search:
        - pasture.internal
      cni_config:
        '10-pasturestack-per-host-subnet.conf':
          name: pasturestack-per-host-subnet-network
          type: pasture-bridge
          bridge: ${BRIDGE}
          bridgeSubnet: '__host_label__: io.pasturestack.network.per-host-subnet.subnet'
          logToFile: /var/log/pasturestack-cni.log
          isDebugLevel: ${PASTURESTACK_DEBUG}
          isDefaultGateway: true
          hostNat: {{ .Values.HOST_NAT }}
          hairpinMode: {{ .Values.HAIRPIN_MODE }}
          promiscMode: {{ .Values.PROMISCUOUS_MODE }}
          mtu: ${MTU}
          ipam:
            type: host-local-cni-ipam
            subnet: '__host_label__: io.pasturestack.network.per-host-subnet.subnet'
            rangeStart: '__host_label__: io.pasturestack.network.per-host-subnet.range-start'
            rangeEnd: '__host_label__: io.pasturestack.network.per-host-subnet.range-end'
            dataDir: /opt/cni/state
            metadataURL: http://169.254.169.250/2016-07-29
            logToFile: /var/log/pasturestack-cni.log
            isDebugLevel: ${PASTURESTACK_DEBUG}
