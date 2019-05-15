import setuptools
from os import path


#
# Preparation
#
here = path.dirname (path.realpath (__file__))
srcdir = path.join (here, 'src')
readme = open (path.join (here, 'README.MD')).read (),


#
# Packaging Instructions
#
setuptools.setup (

# What?
name = 'arpa2shell',
version = '0.0.0',
url = 'https://github.com/arpa2/arpa2shell',
description = 'The ARPA2 Shell Collection',
long_description = readme,
long_description_content_type = 'text/markdown',

# Who?
author = 'Rick van Rein (for the ARPA2 Project)',
author_email = 'rick@openfortress.nl',

# Where?
packages = [ 'arpa2shell', 'arpa2shell.cmdparser' ],
package_dir = {
	'arpa2shell'           : path.join (here, 'src'             ),
	'arpa2shell.cmdparser' : path.join (here, 'src', 'cmdparser'),
}

)
