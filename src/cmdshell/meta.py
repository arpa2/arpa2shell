#!/usr/bin/env python2.7
#
# arpa2shell.meta -- an ARPA2 Shell to access other shells.
#
# This meta-shell is used to gain access to other shells.
# Since access control is practiced on a per-command basis,
# there is usually no restrictions on showing a prompt for
# each installed shell to any user.  The meta-shell is
# mostly useful to have an access point for remote access,
# such as from an OpenSSH daemon.
#
# This command assumes that setuptools has been used to
# declare entry_points for the group arpa2shell.Cmd.subclasses
# with a class name in each.  This allows the separate
# installation of arpa2shell packages that can then be
# called from this meta-shell.
#
# The JSON infrastructure would not call the meta-shell
# command, but it may use the same group to find the
# locally installed classes to send JSON messages to.
#
# From: Rick van Rein <rick@openfortress.nl>


import os
import sys

import pkg_resources

import arpa2shell.cmdshell as a2cmd


entrypoint_group = 'arpa2shell.cmd.subclasses'


# Return a map of shells that can be reached.  The return
# value is a dictionary, mapping a shell class name to a class
# that is loaded from the shell's module.
def named_shell_classes ():
	shells = { }
	for cmd in pkg_resources.iter_entry_points (group=entrypoint_group):
		cmd_cls = cmd.load ()
		if not issubclass (cmd_cls, a2cmd.Cmd):
			raise Exception ('%s is not an ARPA2 Shell' % (cmd.name,))
			continue
		shells [cmd.name] = cmd.load ()
	return shells


# The arpa2shell is invoked with packages to load and
# whose Cmd to start, followed by mutual introductions.
# Each of these Cmd instances are assumed to derive
# from arpa2shell.Cmd.
#
def main ():
	arpa2shell = a2cmd.Cmd ()
	shells = named_shell_classes ()
	for (shnm,shcls) in shells.items ():
		cmd = shcls.Cmd ()
		if not isinstance (cmd, a2cmd.Cmd):
			raise Exception ('%s is not an ARPA2 shell' % (shnm,))
		arpa2shell.know_about (shnm, cmd)
		cmd.know_about ('arpa2shell', arpa2shell)
	current_shell = arpa2shell
	while current_shell is not None:
		current_shell.next_shell = None
		current_shell.cmdloop ()
		current_shell.reset ()
		current_shell = current_shell.next_shell


# When this script is called directly, run the main function
#
if __name__ == '__main__':
	main ()
