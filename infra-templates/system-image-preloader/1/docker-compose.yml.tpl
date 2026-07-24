# SPDX-License-Identifier: MIT
version: '2'
services:
  system-image-preloader:
    image: ghcr.io/pasturestack/system-image-preloader:v0.3.0
    {{ if eq .Values.PRIVILEGED "true"}}
    privileged: true
    {{ end}}
    environment:
      CHECK_CPU_USAGE: '${CHECK_CPU_USAGE}'
      CPU_USAGE_MAX: '${CPU_USAGE_MAX}'
      CPU_USAGE_SLEEP: '${CPU_USAGE_SLEEP}'
      CPU_WAIT_MAX_ATTEMPTS: '${CPU_WAIT_MAX_ATTEMPTS}'
      IMAGE_PULL_MAX_ATTEMPTS: '${IMAGE_PULL_MAX_ATTEMPTS}'
      IMAGE_PULL_RETRY_DELAY_SECONDS: '${IMAGE_PULL_RETRY_DELAY_SECONDS}'
      PLATFORM_AGENT_IMAGE: '${PLATFORM_AGENT_IMAGE}'
      PLATFORM_TLS_VERIFY: '${PLATFORM_TLS_VERIFY}'
      PLATFORM_VERSION: '${PLATFORM_VERSION}'
      RANDOM_SLEEP: '${RANDOM_SLEEP}'
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    {{ if eq .Values.MOUNT_DOCKER_CONFIG "true"}}
      - ${DOCKER_CONFIG_LOCATION}:/root/.docker/config.json:ro
    {{ end}}
    labels:
      io.rancher.container.agent.role: environment
      io.rancher.container.start_once: 'true'
      io.rancher.container.create_agent: 'true'
      io.rancher.scheduler.global: 'true'
    logging:
      driver: json-file
      options:
        max-size: 25m
        max-file: '2'
