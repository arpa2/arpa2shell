# Installing the ARPA2 Shell Collection

> *Installation is simple, because the ARPA2 Shells have no
> binary components.  All we need to do is iterate over Python2
> and Python3 to build generic distribution packages for each.*



## Having all Software

Test your **wheel version** by running

```
python  -c 'import wheel; print (wheel.__version__)'
python3 -c 'import wheel; print (wheel.__version__)'
```

If you `wheel` is <= 0.30 as may be the case with Debian,
you will not be able to upload the Markdown properly, so

```
pip  install -U wheel
pip3 install -U wheel
```

We will also use `virtualenv` below, so

```
pip install virtualenv
pip3 install virtualenv
```

## Installation Cycle

Now, **clean your environment** by removing the code and
upping all versions:

```
rm -rf build dist
vi src/*/__init__.py setup.py
```


## Local Testing

```
rm -rf /tmp/venv2 /tmp/venv3
python  -m virtualenv /tmp/venv2
python3 -m virtualenv /tmp/venv2
/tmp/venv2/bin/activate
	python  setup.py install
	deactivate
/tmp/venv3/bin/activate
	python3 setup.py install
	deactivate
```

## Package Crafting

The **easiest package build and install** is through `.egg` format,

```
python3 setup.py bdist_egg
easy_install3 dist/arpa2shell-*-py3.*.egg
```

To **build all packages** for the various ARPA2 Shells, run

```
python  setup.py sdist bdist_wheel
python3 setup.py sdist bdist_wheel
```

You will find the built packages in `dist/`


To upload to PyPi, first **have the code** for doing so,

```
python3 -m pip install --user --upgrade twine
```


Now make a **test repo upload** with

```
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```


Then **test** the various shells, counting on dependencies to be resolved:

```
rm -rf /tmp/venv2 /tmp/venv3
python  -m virtualenv /tmp/venv2
python3 -m virtualenv /tmp/venv3
. /tmp/venv2/bin/activate
	pip install --index-url https://test.pypi.org/simple/ arpa2shell-dns
	#NOTYET# arpa2dns
	arpa2shell
		ping
		ping6
		exit
	deactivate
	#WONTWORK# pip install arpa2shell[JSON]
. /tmp/venv3/bin/activate
	pip3 install --index-url https://test.pypi.org/simple/ arpa2shell-dns
	#NOTYET# arpa2dns
	arpa2shell
		ping
		ping6
		exit
	deactivate
	#WONTWORK# pip install arpa2shell[JSON]
```


Read more:

  * [Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/)
