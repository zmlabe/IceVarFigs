#!/usr/bin/env bash
set -e

VERSION="${VERSION:-latest}"
IMAGE=icevarfigs:$VERSION

docker build -t "$IMAGE" .
