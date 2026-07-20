# SPDX-License-Identifier: MIT
version: '2'

services:
  overlay-network:
    image: ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.25@sha256:f0a7e61a3c35f5f5ba347a0c74d87b736229dcb73a17de90aaa38df4d94e2e5f
    command:
    - /bin/bash
    - -c
    - 'mkfifo /tmp/overlay-log; exec cat /tmp/overlay-log'
    network_mode: ipsec
    labels:
      io.pasturestack.component: ipsec-overlay
      io.rancher.sidekicks: overlay-router,connectivity-check
      io.rancher.scheduler.global: 'true'
      io.rancher.cni.link_mtu_overhead: '0'
      io.rancher.network.macsync: 'true'
      io.rancher.network.arpsync: 'true'

  overlay-router:
    image: ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.25@sha256:f0a7e61a3c35f5f5ba347a0c74d87b736229dcb73a17de90aaa38df4d94e2e5f
    command: start-ipsec.sh
    privileged: true
    network_mode: container:overlay-network
    pid: host
    environment:
      PASTURESTACK_DEBUG: '${PASTURESTACK_DEBUG}'
      PASTURESTACK_NETWORK_XFRM_NETNS_PATH: /proc/1/ns/net
      PASTURESTACK_NETWORK_XFRM_TUNNEL_SOURCE: host
      PASTURESTACK_NETWORK_RUN_IN_HOST_NETNS: 'true'
      PASTURESTACK_NETWORK_ARP_INTERFACE: '${DOCKER_BRIDGE}'
      PASTURESTACK_NETWORK_SYNC_HOST_ROUTES: 'true'
    labels:
      io.pasturestack.component: ipsec-overlay-router
      io.rancher.container.create_agent: 'true'
      io.rancher.container.agent_service.ipsec: 'true'
    logging:
      driver: json-file
      options:
        max-size: 25m
        max-file: '2'
    sysctls:
      net.ipv4.conf.all.send_redirects: '0'
      net.ipv4.conf.default.send_redirects: '0'

  connectivity-check:
    image: ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.25@sha256:f0a7e61a3c35f5f5ba347a0c74d87b736229dcb73a17de90aaa38df4d94e2e5f
    command:
    - ipsec-vxlan-connectivity-check
    - --connectivity-check-interval
    - '${CONNECTIVITY_CHECK_INTERVAL}'
    - --peer-connection-timeout
    - '${PEER_CONNECTION_TIMEOUT}'
    network_mode: container:overlay-network
    environment:
      PASTURESTACK_DEBUG: '${PASTURESTACK_DEBUG}'
      PASTURESTACK_METADATA_ADDRESS: 169.254.169.250
    labels:
      io.pasturestack.component: ipsec-overlay-connectivity

  cni-driver:
    image: ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.25@sha256:f0a7e61a3c35f5f5ba347a0c74d87b736229dcb73a17de90aaa38df4d94e2e5f
    command: start-cni-driver.sh
    privileged: true
    network_mode: host
    pid: host
    environment:
      PASTURESTACK_DEBUG: '${PASTURESTACK_DEBUG}'
    labels:
      io.pasturestack.component: ipsec-overlay-cni
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
      name: PastureStack IPsec Overlay
      default_network:
        name: ipsec
        host_ports: {{ .Values.HOST_PORTS }}
        subnets:
        - network_address: 10.42.0.0/16
        dns:
        - 169.254.169.250
        dns_search:
        - pasture.internal
      cni_config:
        '10-pasturestack.conf':
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
          linkMTUOverhead: 98
          ipam:
            type: metadata-cni-ipam
            subnetPrefixSize: /16
            logToFile: /var/log/pasturestack-cni.log
            isDebugLevel: ${PASTURESTACK_DEBUG}
