#!/bin/bash
#
# Script based on https://github.com/pypa/python-manylinux-demo

set -e -x

# Install system packages required by our libraries
#NONEED# yum search ldap
#NONEED# yum search gssapi
#NONEED# yum search riak
#NONEED# yum install -y gssapi openldap

# Compile wheels
for PYBIN in /opt/python/*/bin; do
    # "${PYBIN}/pip" install -r /io/dev-requirements.txt
    "${PYBIN}/pip" wheel /io/ -w /io/wheelhouse/
done

# Show where the intermediates have gone
echo Show where the intermediates have gone
ls -l /io/wheelhouse/

# Bundle external shared libraries into the wheels
for whl in /io/wheelhouse/*.whl; do
    auditwheel repair "$whl" --plat $PLAT -w /io/wheelhouse/
done

# Show where the output has gone
echo Show where the output has gone
ls -l /io/wheelhouse/

# Install packages and test
for PYBIN in /opt/python/*/bin/; do
    "${PYBIN}/pip" install arpa2shell --no-index -f /io/wheelhouse
    #TODO:TRYIT# (cd "$HOME"; "${PYBIN}/nosetests" pymanylinuxdemo)
done
