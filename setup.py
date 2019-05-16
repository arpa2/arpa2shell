import setuptools
from os import path


#
# Preparation
#
here = path.dirname (path.realpath (__file__))
readme = open (path.join (here, 'README.MD')).read (),
readme_dns = open (path.join (here, 'src', 'arpa2dns', 'README.MD')).read (),


#
# Packaging Instructions -- arpa2shell.cmd, .cmdparser, .amqp
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
	namespace_packages = [ 'arpa2shell', ],
	packages = [
		'arpa2shell',
		'arpa2shell.cmdshell',
		'arpa2shell.cmdparser',
		'arpa2shell.amqp',
	],
	package_dir = {
		'arpa2shell'           : path.join (here, 'src'),
		'arpa2shell.cmdshell'  : path.join (here, 'src', 'cmdshell'),
		'arpa2shell.cmdparser' : path.join (here, 'src', 'cmdparser'),
		'arpa2shell.amqp'      : path.join (here, 'src', 'amqp'),
	},

	# How?
	entry_points = {
		'arpa2shell.cmdshell.subclasses' : [
			'arpa2shell=arpa2shell.cmdshell.meta:Cmd',
		],
		'console_scripts' : [
			'arpa2shell=arpa2shell.cmdshell.meta:main',
			'arpa2client=arpa2shell.amqp.client:main [JSON]',
			'arpa2server=arpa2shell.amqp.server:main [JSON]',
		],
	},

	# Requirements
	install_requires = [ 'enum34', 'six', 'decorator' ],
	extras_require = {
		'JSON' : [ 'gssapi', 'python-qpid-proton' ],
	},

)



#
# Second setup -- for the arpa2dns shell
#
setuptools.setup (

	# What?
	name = 'arpa2shell-dns',
	version = '0.0.0',
	url = 'https://github.com/arpa2/arpa2shell/src/arpa2dns',
	description = 'The ARPA2 Shell for DNS',
	long_description = readme_dns,
	long_description_content_type = 'text/markdown',

	# Who?
	author = 'Rick van Rein (for the ARPA2 Project)',
	author_email = 'rick@openfortress.nl',

	# Where?
	namespace_packages = [ 'arpa2shell', ],
	packages = [
		'arpa2shell',
		'arpa2shell.arpa2dns',
	],
	package_dir = {
		'arpa2shell'           : path.join (here, 'src'),
		'arpa2shell.arpa2dns'  : path.join (here, 'src', 'arpa2dns'),
	},

	# How?
	entry_points = {
		'arpa2shell.cmdshell.subclasses' : [
			'arpa2dns=arpa2shell.arpa2dns.shell:Cmd',
		],
		'console_scripts' : [
			'arpa2dns=arpa2shell.arpa2dns.shell:main',
		],
	},

	# Requirements
	install_requires = [ 'enum34', 'six', 'decorator',
			'libknot' ],

)
