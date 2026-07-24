# SPDX-License-Identifier: MIT
version: '2'

services:
  layer-2-flat-cni:
    image: ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.26
    privileged: true
    network_mode: host
    pid: host
{{- if eq .Values.AUTO_SETUP_LAYER_2_BRIDGE "true" }}
    command:
    - /bin/bash
    - -ceu
    - start-flat.sh && exec start-cni-driver.sh
{{- else }}
    command: start-cni-driver.sh
{{- end }}
    environment:
      PASTURESTACK_DEBUG: '${PASTURESTACK_DEBUG}'
      PASTURESTACK_METADATA_ADDRESS: '${PASTURESTACK_METADATA_ADDRESS}'
      FLAT_IF: '${FLAT_INTERFACE}'
      FLAT_BRIDGE: '${LAYER_2_BRIDGE}'
      MTU: '${MTU}'
    labels:
      io.pasturestack.component: layer-2-flat-cni
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
      name: PastureStack Layer 2 Flat Network
      default_network:
        name: layer-2-flat
        host_ports: {{ .Values.HOST_PORTS }}
        subnets:
        - network_address: ${SUBNET}
          start_address: ${START_ADDRESS}
          end_address: ${END_ADDRESS}
        dns:
        - 169.254.169.250
        dns_search:
        - pasture.internal
      cni_config:
        '10-pasturestack-layer-2-flat.conf':
          name: pasturestack-layer-2-flat-network
          type: pasture-bridge
          bridge: ${LAYER_2_BRIDGE}
          bridgeSubnet: ${SUBNET}
          logToFile: /var/log/pasturestack-cni.log
          isDebugLevel: ${PASTURESTACK_DEBUG}
          hostNat: false
          mtu: ${MTU}
          skipBridgeConfigureIP: true
          skipFastPath: true
          ipam:
            type: flat-cni-ipam
            metadataURL: http://169.254.169.250/2015-12-19
            metadataAddress: 169.254.169.250
            logToFile: /var/log/pasturestack-cni.log
            isDebugLevel: ${PASTURESTACK_DEBUG}
            routes:
            - dst: 0.0.0.0/0
              gw: ${GATEWAY}
