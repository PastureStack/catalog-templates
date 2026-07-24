# SPDX-License-Identifier: MIT
version: '2'
services:
  route53-dns-sync:
    image: ghcr.io/pasturestack/external-dns-sync:v0.8.0
    command:
      - -provider=route53
    expose:
      - '10000'
    environment:
      AWS_ACCESS_KEY_ID: '${AWS_ACCESS_KEY_ID}'
      AWS_REGION: '${AWS_REGION}'
      AWS_SECRET_ACCESS_KEY: '${AWS_SECRET_ACCESS_KEY}'
      AWS_SESSION_TOKEN: '${AWS_SESSION_TOKEN}'
      NAME_TEMPLATE: '${NAME_TEMPLATE}'
      ROOT_DOMAIN: '${ROOT_DOMAIN}'
      ROUTE53_MAX_RETRIES: '${ROUTE53_MAX_RETRIES}'
      ROUTE53_ZONE_ID: '${ROUTE53_ZONE_ID}'
      TTL: '${TTL}'
    labels:
      io.pasturestack.component: route53-dns-sync
      io.rancher.container.create_agent: 'true'
      io.rancher.container.agent.role: external-dns
    {{ if eq .Values.MOUNT_PLATFORM_CA "true"}}
    volumes:
      - ${PLATFORM_CA_FILE}:/var/lib/pasturestack/etc/ssl/ca.crt:ro
    {{ end}}
    cpu_shares: 128
    mem_limit: 128m
    logging:
      driver: json-file
      options:
        max-size: 10m
        max-file: '2'
