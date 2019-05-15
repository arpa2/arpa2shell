#!/usr/bin/env python
#
# arpa2id-shell for IdentityHub
#
# This shell allows a variety of commands to add and remove,
# rename and refine users, aliases, pseudonyms as well as
# group memberships and role occupancy.  In short, it allows
# the great variety of identity configurations that ARPA2
# offers to support both that users control their own online
# identity, and that they may Bring Your Own IDentity (BYOID).
#
# Completion is based on word-by-word actions; in some cases,
# regular expressions are used (such as for new domain names);
# in other cases, already known values can be listed by a
# function.  There are also fixed words, indicating a command
# match; this is also used for sub-commands.
#
# From: Rick van Rein <rick@openfortress.nl>


import sys
import re
import string

import cmd
import arpa2cmd


# Regular expressions for fields
#
re_fqdn = re.compile ('^[a-z0-9-_]{1,}(\.[a-z0-9-_]{1,})*$')
re_user = re.compile ('^[a-z0-9_-]{1,}$')
re_alias = re.compile ('^[a-z0-9_-]{1,}\+[a-z0-9_-]{1,}$')
re_role = re_alias
re_group = re_alias

#
# Listing functions for various fields
#

# List the available domains found in LDAP:
# (associatedDomain=d_*) under ou=IdentityHub,o=internetwide.org,ou=ServiceDIT
#
def list_domains (self, d_):
	#TODO#FIXED#
	return [ 'internetwide.org', 'arpa2.net', 'arpa2.org', 'tlspool.org' ]

# List the users for the given domain in LDAP:
# (&(objectClass=inetOrgPerson)(uid=u_*)) under
# associatedDomain=d,ou=IdentityHub,o=internetwide.org,ou=ServiceDIT
#
def list_user (self, u_):
	#TODO#FIXED#
	return [ 'vanrein', 'michiel', 'adriaan', 'tim' ]
#
def list_alias (self, a_):
	#TODO#FIXED#
	return [ 'webmaster', 'pastamaker', 'singer' ]
#
def list_roles (self, r_):
	#TODO#FIXED#
	return [ 'admin' ]
#
def list_groups (self, g_):
	#TODO#FIXED#
	return [ 'hosting', 'diy', 'infra', 'comms' ]

# Overview of possible (sub)command structures
#
matchables = {
	"domain_add":		[ re_fqdn ],
	"domain_del":		[ list_domains ],
	"domain_xfer_away":	[ list_domains ],
	"user_add":		[ list_domains, re_user ],
	"user_del":		[ list_domains, list_user ],
	"user_mov":		[ list_domains, list_user, re_user ],
	"alias_add":		[ list_domains, list_user, re_alias ],
	"alias_del":		[ list_domains, list_user, list_alias ],
	"role_add":		[ list_domains, list_user, re_role ],
	"role_del":		[ list_domains, list_user, list_roles ],
	"role_mov":		[ list_domains, list_user, list_roles, re_role ],
	"group_add":		[ list_domains, re_group ],
	"group_del":		[ list_domains, list_groups ],
	"member_add":		[ list_domains, list_groups, re_user ],
	"member_del":		[ list_domains, list_groups, list_user ],
	"member_name":		[ list_domains, list_groups, list_user, re_alias ],
	# "group_mov":		[ list_domains, list_groups, re_group ],
	# "member_mov":		[ list_domains, list_members, re_user ],
}



class Cmd (arpa2cmd.Cmd):

	prompt = 'arpa2kv> '
	intro = 'Shell to the ARPA2 Keys `n\' Values.  Like Rock `n\' Roll, but better.'

	def do_EOF (self, line):
		return True

	do_exit = do_EOF

	do_quit = do_EOF

	def completenames (self, text, *ignored):
		return [ w + ' '
			for w in cmd.Cmd.completenames (self, text, *ignored) ]

	def completedefault (self, text, line, begidx, endidx):
		words = string.split (line.lstrip () + 'x')
		last_word = words [-1] [:-1]
		try:
			to_match = matchables.get (words [0], []) [len (words)-2]
			if type (to_match) == type (re_user):
				mtch = to_match.match (last_word)
				if mtch is not None:
					# Confirm
					return [ last_word + ' ' ]
				else:
					# Beep
					return [ ]
			else:
				# Assume a function to be called, usually list_xxx
				cmpl = to_match (self, last_word)
				return [ c + ' ' for c in cmpl if c.startswith (last_word) ]
		except Exception, e:
			# Beep
			return [ ]

	def do_domain_add (self, line):
		"""domain_add DOMAIN.TLD
		   Add DOMAIN.TLD to the managed portfolio of domain names.
		"""
		sys.stdout.write ("do_domain_add: " + line + "\n")
		pass

	def do_domain_del (self, line):
		"""domain_del DOMAIN.TLD
		   Remove DOMAIN.TLD from the managed portfolio of domain names.
		"""
		sys.stdout.write ("do_domain_del: " + line + "\n")
		pass

	def do_domain_xfer_away (self, line):
		"""domain_xfer_away DOMAIN.TLD
		   Transfer ownership of DOMAIN.TLD to another party.
		"""
		sys.stdout.write ("do_domain_xfer_away: " + line + "\n")
		pass

	def do_user_add (self, line):
		"""user_add DOMAIN.TLD USERNAME
		   Add a new user USERNAME@DOMAIN.TLD to a managed domain.
		"""
		sys.stdout.write ("do_user_add: " + line + "\n")
		pass

	def do_user_del (self, line):
		"""user_del DOMAIN.TLD USERNAME
		   Remove a user USERNAME@DOMAIN.TLD from a managed domain.
		"""
		sys.stdout.write ("do_user_del: " + line + "\n")
		pass

	def do_user_mov (self, line):
		"""user_mov DOMAIN.TLD USERNAME NEWNAME
		   Rename a user USERNAME@DOMAIN.TLD to NEWNAME@DOMAIN.TLD.
		"""
		sys.stdout.write ("do_user_mov: " + line + "\n")
		pass

	def do_alias_add (self, line):
		"""alias_add DOMAIN.TLD USERNAME NEWALIAS
		   Introduce USERNAME+NEWALIAS@DOMAIN.TLD as an alias for USERNAME@DOMAIN.TLD.
		"""
		sys.stdout.write ("do_alias_add: " + line + "\n")
		pass

	def do_alias_del (self, line):
		"""alias_del DOMAIN.TLD USERNAME ALIAS
		   Remove an alias USERNAME+ALIAS@DOMAIN.TLD as from a managed domain.
		"""
		sys.stdout.write ("do_alias_del: " + line + "\n")
		pass

	def do_role_add (self, line):
		"""role_add DOMAIN.TLD USERNAME NEWROLE
		   Add a role NEWROLE@DOMAIN.TLD to USERNAME@DOMAIN.TLD
		"""
		sys.stdout.write ("do_role_add: " + line + "\n")
		pass

	def do_role_del (self, line):
		"""role_del DOMAIN.TLD USERNAME ROLENAME
		   Remove a role ROLENAME@DOMAIN.TLD from USERNAME@DOMAIN.TLD.
		"""
		sys.stdout.write ("do_role_del: " + line + "\n")
		pass

	def do_role_mov (self, line):
		"""role_mov DOMAIN.TLD ROLENAME NEWROLENAME
		   Rename ROLENAME@DOMAIN.TLD to NEWROLENAME@DOMAIN.TLD.
		"""
		sys.stdout.write ("do_role_mov: " + line + "\n")
		pass

	def do_group_add (self, line):
		"""group_add DOMAIN.TLD GROUPNAME
		   Add GROUPNAME@DOMAIN.TLD as a group.
		"""
		sys.stdout.write ("do_group_add: " + line + "\n")
		pass

	def do_group_del (self, line):
		"""group_del DOMAIN.TLD GROUPNAME
		   Remove GROUPNAME@DOMAIN.TLD as a group.
		"""
		sys.stdout.write ("do_group_del: " + line + "\n")
		pass

	def do_group_mov (self, line):
		"""group_mov DOMAIN.TLD GROUPNAME NEWGROUPNAME
		   Rename GROUPNAME@DOMAIN.TLD into NEWGROUPNAME@DOMAIN.TLD.
		"""
		sys.stdout.write ("do_group_mov: " + line + "\n")
		pass

	def do_member_add (self, line):
		"""member_add DOMAIN.TLD GROUPNAME USERNAME
		   Add USERNAME@DOMAIN.TLD as a member to GROUPNAME@DOMAIN.TLD.
		"""
		sys.stdout.write ("do_member_add: " + line + "\n")
		pass

	def do_member_del (self, line):
		"""member_del DOMAIN.TLD GROUPNAME USERNAME
		   Remove USERNAME@DOMAIN.TLD as a member from GROUPNAME@DOMAIN.TLD.
		"""
		sys.stdout.write ("do_member_del: " + line + "\n")
		pass

	def do_member_name (self, line):
		"""member_name DOMAIN.TLD GROUP USER MEMBER
		   Let USER@DOMAIN.TLD act in GROUP@DOMAIN.TLD as GROUP+MEMBER@DOMAIN.TLD.
		"""
		sys.stdout.write ("do_member_name: " + line + "\n")
		pass




if __name__ == '__main__':
	arpa2kv = Cmd ()
	arpa2kv.cmdloop ()

