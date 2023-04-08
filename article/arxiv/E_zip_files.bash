#!/bin/bash

VERSION=$1
mkdir -p zip-files
zip -r zip-files/arxiv-$VERSION.zip files/
