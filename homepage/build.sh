#!/bin/sh

# Builds a docker image of the homepage app.

set -e

VERSION=`python setup.py --version`
rm -rf homepage/site_media
python setup.py sdist
mkdir -p dist/image
mv dist/homepage-${VERSION}.tar.gz dist/image/homepage.tar.gz

# Only copy the requirements.txt if it's different from the
# on in the dist directory.
rsync --checksum requirements.txt dist/image/

cp Dockerfile dist/image/
docker build -t homepage dist/image/
# Tag with the appropriate version
docker tag homepage asia.gcr.io/ianlewis-org/homepage:${VERSION}

# Export to Container Registry
gcloud docker -- push asia.gcr.io/ianlewis-org/homepage:${VERSION}
