# SPDX-License-Identifier: MIT
version: '2'

services:
  vxlan-network:
    image: ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.26
    command:
    - /bin/bash
    - -c
    - 'mkfifo /tmp/overlay-log; exec cat /tmp/overlay-log'
    network_mode: vxlan
    ports:
    - 4789:4789/udp
    labels:
      io.pasturestack.component: vxlan-overlay
      io.rancher.sidekicks: vxlan-router
      io.rancher.scheduler.global: 'true'
      io.rancher.cni.link_mtu_overhead: '0'
      io.rancher.internal.service.vxlan: 'true'
      io.rancher.service.selector.link: io.rancher.internal.service.vxlan=true
      io.rancher.network.macsync: 'true'
      io.rancher.network.arpsync: 'true'
    logging:
      driver: json-file
      options:
        max-size: 25m
        max-file: '2'

  vxlan-router:
    image: ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.26
    command: start-vxlan.sh
    cap_add:
    - NET_ADMIN
    network_mode: container:vxlan-network
    environment:
      PASTURESTACK_DEBUG: '${PASTURESTACK_DEBUG}'
    logging:
      driver: json-file
      options:
        max-size: 25m
        max-file: '2'
    sysctls:
      net.ipv4.conf.all.send_redirects: '0'
      net.ipv4.conf.default.send_redirects: '0'

  cni-driver:
    image: ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.26
    command: start-cni-driver.sh
    privileged: true
    network_mode: host
    pid: host
    environment:
      PASTURESTACK_DEBUG: '${PASTURESTACK_DEBUG}'
    labels:
      io.pasturestack.component: vxlan-overlay-cni
      io.rancher.scheduler.global: 'true'
      io.rancher.network.cni.binary: pasture-bridge
      io.rancher.container.dns: 'true'
    logging:
      driver: json-file
      options:
        max-size: 25m
        max-file: '2'
    volumes:
    - /var/run/docker.sock:/var/run/docker.sock
    - rancher-cni-driver:/opt/cni-driver
    network_driver:
      name: PastureStack VXLAN Overlay Network
      default_network:
        name: vxlan
        host_ports: {{ .Values.HOST_PORTS }}
        subnets:
        - network_address: 10.42.0.0/16
        dns:
        - 169.254.169.250
        dns_search:
        - pasture.internal
      cni_config:
        '10-pasturestack-vxlan.conf':
          name: pasturestack-cni-network
          type: pasture-bridge
          bridge: $DOCKER_BRIDGE
          bridgeSubnet: 10.42.0.0/16
          logToFile: /var/log/pasturestack-cni.log
          isDebugLevel: ${PASTURESTACK_DEBUG}
          isDefaultGateway: true
          hostNat: true
          hairpinMode: {{ .Values.PASTURESTACK_HAIRPIN_MODE }}
          promiscMode: {{ .Values.PASTURESTACK_PROMISCUOUS_MODE }}
          mtu: ${MTU}
          linkMTUOverhead: 50
          ipam:
            type: metadata-cni-ipam
            subnetPrefixSize: /16
            logToFile: /var/log/pasturestack-cni.log
            isDebugLevel: ${PASTURESTACK_DEBUG}
