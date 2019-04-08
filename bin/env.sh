#!/bin/bash

_WORKDIR=~/.x123
_CONFIG=~/.x123config
_RESOURCES=$_WORKDIR/resources
_HELM_RESOURCES=$_RESOURCES/helm

_K3S_DOCKER_COMPOSE=$_RESOURCES/k3s-docker-compose.yaml
_K3S_TMP=/tmp/k3s
_K3S_DATA=$_K3S_TMP/data
_K3S_MANIFESTS=$_K3S_TMP/manifests
_K3S_IMAGES=$_K3S_TMP/images

# colors
# https://misc.flogisoft.com/bash/tip_colors_and_formatting
F_RED="\e[31m"
F_GREEN="\e[32m"
F_YELLOW="\e[33m"
F_LIGHT_RED="\e[91m"
F_LIGHT_GRAY="\e[37m"
F_DARK_GRAY="\e[90m"


RESET="\e[0m"
BOLD="\e[1m"
BLINK="\e[5m"
