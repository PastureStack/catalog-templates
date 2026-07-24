# SPDX-License-Identifier: MIT
version: '2'
services:
  ecr-credential-sync:
    image: ghcr.io/pasturestack/ecr-credential-sync:v3.1.0
    entrypoint:
      - /bin/sh
      - -ec
    command:
      - |
        export PLATFORM_URL="$${PLATFORM_URL:-$${CATTLE_URL:-}}"
        export PLATFORM_ACCESS_KEY="$${PLATFORM_ACCESS_KEY:-$${CATTLE_ACCESS_KEY:-}}"
        export PLATFORM_SECRET_KEY="$${PLATFORM_SECRET_KEY:-$${CATTLE_SECRET_KEY:-}}"
        exec /usr/local/bin/ecr-credential-sync
    environment:
      AUTO_CREATE: '${AUTO_CREATE}'
      AWS_ACCESS_KEY_ID: '${AWS_ACCESS_KEY_ID}'
      AWS_ECR_ENDPOINT_URL: '${AWS_ECR_ENDPOINT_URL}'
      AWS_ECR_REGISTRY_IDS: '${AWS_ECR_REGISTRY_IDS}'
      AWS_PROFILE: '${AWS_PROFILE}'
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
    {{ if eq .Values.USE_SHARED_AWS_PROFILE "true"}}
    volumes:
      - ${AWS_PROFILE_DIRECTORY}:/home/pasturestack/.aws:ro
    {{ end}}
    {{ if eq .Values.REGISTRY_ENVIRONMENT "current"}}
    labels:
      io.rancher.container.create_agent: 'true'
      io.rancher.container.agent.role: environment
    {{ end}}
    cpu_shares: 128
    mem_limit: 128m
    logging:
      driver: json-file
      options:
        max-size: 10m
        max-file: '2'
