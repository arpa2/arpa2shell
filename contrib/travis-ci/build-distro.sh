#!/bin/bash
#
# Build distribution with the $PYTHON and $PIP executables
#
# From: Rick van Rein <rick@openfortress.nl>



info() {
	echo
	# Red=31, Bright=1
	echo '[31;1m'"$@"'[0m'
}

cmd_ok() {
	# Green=32, Bright=1
	echo '[32;1mbash$ '"$@"'[0m'
	"$@"
}

maybe_exit() {
	EXITVAL=${1:-$?}
	if [ $EXITVAL -ne 0 ]
	then
		info Error exit value $EXITVAL
		exit $EXITVAL
	fi
}

cmd() {
	# Green=32, Bright=1			# Yellow=33
	echo '[32;1mbash$ '"$@"'[0m (dir is [33m'`pwd`'[0m)'
	"$@"
	maybe_exit
	# EXITVAL=$?
	# maybe_exit $EXITVAL
}

cmake_depend() {
	PKG="$1"
	DIR="/builds/arpa2/$PKG"
	cmd mkdir -p "$DIR"
	pushd "$DIR"
	info Building CMake project $PKG
	cmd mkdir build
	cmd cd build
	cmd cmake -D DEBUG:BOOL=OFF ..
	cmd make
	cmd make install
	popd
}


info Changing to distribution
cmd pwd
cmd cd /io

info 'Upgrading wheel (hoping to parse Markdown in README files)'
cmd_ok ${PYTHON:-python} -c 'import wheel; print (wheel.__version__)'
cmd_ok ${PIP:-pip} install -U wheel
cmd_ok ${PYTHON:-python} -c 'import wheel; print (wheel.__version__)'

info 'Preparing build environment'
cmd mkdir -p build dist
cmd rm -rf build/* dist/*

info 'Creating distribution files, source and "binary" wheels'
cmd ${PYTHON:-python} setup.py sdist bdist_wheel

info 'Local installation, directly from setup.py'
cmd ${PYTHON:-python} setup.py install

info Forking shell script
cat > /tmp/script <<SCRIPTEND
help
ping
ping6
quit
SCRIPTEND

info 'Trying shell scripts'
for A2SH in arpa2shell arpa2dns arpa2id arpa2reservoir arpa2acl
do
	cmd_ok arpa2shell < /tmp/script
done

info Successful result from $0
cmd exit 0
