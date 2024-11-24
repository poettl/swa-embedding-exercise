#!/bin/sh
docker build -t earlybird-embedding .
docker run --rm earlybird-embedding