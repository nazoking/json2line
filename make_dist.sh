#!/bin/bash
set -e
PACKAGE=json2line

BASE=$(readlink -f $(which $0))
echo $BASE

if [ -e MANIFEST ]; then
  rm MANIFEST
fi
VERSION=`python setup.py --version`
echo VERSION=[$VERSION]
python test.py
if [ "x" != "x`git tag -l v$VERSION`" ]; then
  echo VERSION $VERSION is already exists
  exit -1
fi
python setup.py sdist
pip install dist/$PACKAGE-$VERSION.tar.gz

