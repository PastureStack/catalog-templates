# SPDX-License-Identifier: MIT
version: '2'

services:
  windows-ecr-credential-sync:
    image: ghcr.io/pasturestack/ecr-credential-sync-windows:v3.1.2-windows-ltsc2022
    environment:
      AUTO_CREATE: '${AUTO_CREATE}'
      AWS_ACCESS_KEY_ID: '${AWS_ACCESS_KEY_ID}'
      AWS_ECR_ENDPOINT_URL: '${AWS_ECR_ENDPOINT_URL}'
      AWS_ECR_REGISTRY_IDS: '${AWS_ECR_REGISTRY_IDS}'
      AWS_REGION: '${AWS_REGION}'
      AWS_ROLE_ARN: '${AWS_ROLE_ARN}'
      AWS_SECRET_ACCESS_KEY: '${AWS_SECRET_ACCESS_KEY}'
      AWS_SESSION_TOKEN: '${AWS_SESSION_TOKEN}'
      LISTEN_PORT: '8080'
      LOG_LEVEL: '${LOG_LEVEL}'
    {{ if eq .Values.REGISTRY_ENVIRONMENT "other"}}
      PLATFORM_URL: '${PLATFORM_URL}'
      PLATFORM_ACCESS_KEY: '${PLATFORM_ACCESS_KEY}'
      PLATFORM_SECRET_KEY: '${PLATFORM_SECRET_KEY}'
    {{ end}}
    labels:
      io.rancher.scheduler.affinity:host_label: io.rancher.host.os=windows
    {{ if eq .Values.REGISTRY_ENVIRONMENT "current"}}
      io.rancher.container.create_agent: 'true'
      io.rancher.container.agent.role: environment
      io.rancher.container.agent.volumes_strategy: skip
      io.rancher.container.create_agent_label: 'no'
    {{ end}}
    cpu_shares: 128
    mem_limit: 128m
    logging:
      driver: json-file
      options:
        max-size: 10m
        max-file: '2'
