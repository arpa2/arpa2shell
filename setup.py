import setuptools
from os import path


#
# Preparation
#
here = path.dirname (path.realpath (__file__))


#
# Packaging Instructions -- arpa2shell.cmd, .cmdparser, .amqp
#
readme = open (path.join (here, 'README.MD')).read ()
setuptools.setup (

	# What?
	name = 'arpa2shell',
	version = '0.0.3',
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
	install_requires = [ 'enum34 ; python_version < "3"', 'six' ],
	extras_require = {
		'JSON' : [ 'gssapi', 'python-qpid-proton' ],
	},

)



#
# Additional setup -- for the arpa2dns shell
#
readme_dns = open (path.join (here, 'src', 'arpa2dns', 'README.MD')).read ()
setuptools.setup (

	# What?
	name = 'arpa2shell-dns',
	version = '0.0.3',
	url = 'https://github.com/arpa2/arpa2shell/tree/master/src/arpa2dns',
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
	install_requires = [ 'arpa2shell', 'libknot' ],

)



#
# Additional setup -- for the arpa2id shell
#
# BIG TODO: Not a cmdparser shell yet, so no integration with arpa2shell
#
readme_id = open (path.join (here, 'src', 'arpa2id', 'README.MD')).read ()
setuptools.setup (

	# What?
	name = 'arpa2shell-id',
	version = '0.0.3',
	url = 'https://github.com/arpa2/arpa2shell/tree/master/src/arpa2id',
	description = 'The ARPA2 Shell for Identity Management',
	long_description = readme_id,
	long_description_content_type = 'text/markdown',

	# Who?
	author = 'Rick van Rein (for the ARPA2 Project)',
	author_email = 'rick@openfortress.nl',

	# Where?
	namespace_packages = [ 'arpa2shell', ],
	packages = [
		'arpa2shell',
		'arpa2shell.arpa2id',
	],
	package_dir = {
		'arpa2shell'           : path.join (here, 'src'),
		'arpa2shell.arpa2id'   : path.join (here, 'src', 'arpa2id'),
	},

	# How?
	entry_points = {
		#NOTYET# 'arpa2shell.cmdshell.subclasses' : [
		#NOTYET# 	'arpa2id=arpa2shell.arpa2id.shell:Cmd',
		#NOTYET# ],
		'console_scripts' : [
			'arpa2id=arpa2shell.arpa2id.shell:main',
		],
	},

	# Requirements
	install_requires = [ 'arpa2shell', 'python-ldap' ],

)



#
# Additional setup -- for the arpa2reservoir shell
#
# BIG TODO: Not a cmdparser shell yet, so no integration with arpa2shell
#
readme_reservoir = open (path.join (here, 'src', 'arpa2reservoir', 'README.MD')).read ()
setuptools.setup (

	# What?
	name = 'arpa2shell-reservoir',
	version = '0.0.3',
	url = 'https://github.com/arpa2/arpa2shell/tree/master/src/arpa2reservoir',
	description = 'The ARPA2 Shell for Reservoir data Management',
	long_description = readme_reservoir,
	long_description_content_type = 'text/markdown',

	# Who?
	author = 'Rick van Rein (for the ARPA2 Project)',
	author_email = 'rick@openfortress.nl',

	# Where?
	namespace_packages = [ 'arpa2shell', ],
	packages = [
		'arpa2shell',
		'arpa2shell.arpa2reservoir',
	],
	package_dir = {
		'arpa2shell'                : path.join (here, 'src'),
		'arpa2shell.arpa2reservoir' : path.join (here, 'src', 'arpa2reservoir'),
	},

	# How?
	entry_points = {
		'arpa2shell.cmdshell.subclasses' : [
			'arpa2reservoir=arpa2shell.arpa2reservoir.shell:Cmd',
		],
		'console_scripts' : [
			'arpa2reservoir=arpa2shell.arpa2reservoir.shell:main',
		],
	},

	# Requirements
	install_requires = [ 'arpa2shell', 'python-ldap' ],

)



#
# Additional setup -- for the arpa2acl shell
#
readme_acl = open (path.join (here, 'src', 'arpa2acl', 'README.MD')).read ()
setuptools.setup (

	# What?
	name = 'arpa2shell-acl',
	version = '0.0.3',
	url = 'https://github.com/arpa2/arpa2shell/tree/master/src/arpa2acl',
	description = 'The ARPA2 Shell for ACL Management',
	long_description = readme_acl,
	long_description_content_type = 'text/markdown',

	# Who?
	author = 'Rick van Rein (for the ARPA2 Project)',
	author_email = 'rick@openfortress.nl',

	# Where?
	namespace_packages = [ 'arpa2shell', ],
	packages = [
		'arpa2shell',
		'arpa2shell.arpa2acl',
	],
	package_dir = {
		'arpa2shell'           : path.join (here, 'src'),
		'arpa2shell.arpa2acl'  : path.join (here, 'src', 'arpa2acl'),
	},

	# How?
	entry_points = {
		'arpa2shell.cmdshell.subclasses' : [
			'arpa2acl=arpa2shell.arpa2acl.shell:Cmd',
		],
		'console_scripts' : [
			'arpa2acl=arpa2shell.arpa2acl.shell:main',
		],
	},

	# Requirements
	install_requires = [ 'arpa2shell', 'python-ldap' ],

)
