#!/usr/bin/env bash
# Build and deploy a new S3 version
# Argument 1 (required): Version id (v1, v2, ...)
set -o errexit
set -o nounset
set -o xtrace
S3_VER=${1} make -e -f k8s.mak s3