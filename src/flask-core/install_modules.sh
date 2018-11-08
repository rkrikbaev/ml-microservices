#! /bin/bash

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get upgrade -y

PACKAGES=$(xargs <<EOF
apt-utils
build-essential
curl
git
python3-dev
python3-setuptools
locales
gfortran
swig
libagg-dev
libffi-dev
libatlas-base-dev
libfreetype6-dev
liblapack-dev
libncurses5-dev
libopenblas-dev
libpq-dev
libxft-dev
libxml2-dev
libxslt-dev
zlib1g-dev
libpng-dev
ttf-bitstream-vera
EOF
)

apt-get install -y $PACKAGES
apt-get clean

ln -sr ./src/conf.d/config.conf ./src/flask-core/app
ln -sr ./src/conf.d/config.conf ./src/tf-core/app
ln -sr ./src/conf.d/config.conf ./src/script-server/app
