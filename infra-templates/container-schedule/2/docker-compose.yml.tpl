# SPDX-License-Identifier: MIT
version: '2'
services:
  container-schedule:
    image: ghcr.io/pasturestack/container-cron:v0.6.0
    restart: always
    command: container-cron{{- if eq .Values.ENABLE_DEBUG "true" }} --debug{{- end }}{{- if eq .Values.ENABLE_METRICS "true" }} --metrics{{- end }}
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    expose:
      - '9191'
    labels:
      io.rancher.scheduler.global: 'true'
      io.rancher.container.hostname_override: container_name
    logging:
      driver: json-file
      options:
        max-size: 25m
        max-file: '2'
