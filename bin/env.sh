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
