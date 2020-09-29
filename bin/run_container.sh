#!/usr/bin/env bash
set -e

VERSION="${VERSION:-latest}"
IMAGE=icevarfigs:$VERSION

docker run --rm -v $(pwd):/usr/local/src/IceVarFigs "$IMAGE" "$@"
