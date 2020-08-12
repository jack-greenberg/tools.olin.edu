#!/bin/bash

if [ "$1" == "dependencies" ]; then
  docker build \
    -t jackgreenberg/tools-dependencies:latest \
    --target=dependencies \
    .
elif [ "$1" == "cached" ]; then
  docker pull jackgreenberg/tools-dependencies:latest
  docker build \
    --cache-from=jackgreenberg/tools-dependencies:latest \
    -t jackgreenberg/tools-backend:latest \
    .
elif [ "$1" == "all" ]; then
  docker build \
    -t jackgreenberg/tools-dependencies:latest \
    --target=dependencies \
    .

  docker build \
    --cache-from=jackgreenberg/tools-dependencies:latest \
    -t jackgreenberg/tools-backend:latest \
    .
else
  printf "Usage:\n"
  printf "  ./scripts/build-docker.sh <spec>\n"
  printf "\nWhere <spec> is\n"
  printf "* dependencies (only build dependency docker image\n"
  printf "* cached       (build backend image with cache)\n"
  printf "* all          (build dependencies and backend)\n"
fi
