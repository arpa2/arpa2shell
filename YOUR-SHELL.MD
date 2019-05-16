# Programming an ARPA2 Shell

> *This is a small manual, mostly references to documentation elsewhere,
> that can help you get going with a new ARPA2 Shell.*

The ARPA2 Shell infrastructure helps to create shells for a specific
purpose, for which operators need to enter commands that feels logical
to them.  So not *write a file with the following rights* but rather
*install a certificate for a given service name* or even *switch on the
automatic construction of a certificate for a given service name* if
that is the available service level.

The services offered by an ARPA2 Shell are many:

  * A commandline that can be run as a console, for instance after
    SSH login;
  * Syntax enforcement for your commands; automatic translation of
    those syntaxes to JSON message formats;
  * Access Control Lists for every command, so  you can welcome anyone
    to the prompt as long as they authenticate;
  * JSON entrances for all shells, so automation is much easier to get
    right (no scraping of specific formats);
  * JSON output scraped from command output in a standard manner,
    picking up extra variables from "output headers" that are reminiscent
    of email headers;
  * End-to-end protection of JSON messaging with GSS-API;
  * Dynamic routing of JSON messages with AMQP 1.0;
  * A meta-shell named `arpa2shell` that can switch to your
    purpose-specific shell from this meta-shell or from any other shell
    that it found;
  * A meta-server named `arpa2amqpd` that listens to an AMQP 1.0 router
    for JSON messages protected GSS-API.


## Subclassing the arpa2shell

ARPA2 Shells are a subclass if the standard Python `cmd.Cmd`, but with
annotations and extras through intermediate inheritance relations.
The extras are obtained with

```
from arpa2shell import cmdshell, cmdparser
```

which, if your shell is part of the `arpa2shell` name space,
should be preceded with

```
from __future__ import absolute_import
```

You can now create a class with

```
@cmdparser.CmdClassDecorator()
class Cmd (arpa2shell.cmdshell.Cmd):

    version = (1,2)
    prompt = 'arpa2xxx>'
    intro = 'Kiss Editing.  You can sign any message with triple X signatures.'
```

The initialiser needs to invoke the `arpa2shell`,

```
    def __init__ (self):
        arpa2shell.Cmd.__init__ (self)
        ...
```

The you can add commands.  These may include syntax specifications
as defined for the
[cmdparser](https://pypi.org/project/cmdparser/)
package, that we extended with the JSON entrance that supports the
level of automation that we require.  We have actually posted this
as a PR after talking to the owner, but it appears that maintenance
of the package has ceased.  We now include `cmdparser` as a
sub-package of `arpa2shell` and might change that back into the
external package when it adds our JSON extensions.  The only
difference you will see is the `import` statement that we use.

```
    @cmdparser.CmdMethodDecorator()
    def do_kiss (self, args, fields):
        """
        kiss ( send [ <xcount> ] | receive ) <target>

        Add or remove kisses from the specified target.
        The `<xcount>` specifies...
        """
        subcmd = args [1]
        target = fields ['target']
        xcount = args [2] if subcmd == 'send' else 0
        if subcmd == 'send':
            ...
        if subcmd == 'receive':
            ...
```

This indicates how you can harvest the output that has been
parsed to do the things that the shell must do.  The grammar
is processed with the decorator preceding the call.

Your users can now ask for help with `?kiss` and they would
be shown the grammar to use.

The grammar definition
[translates to JSON](PROTOCOL.MD),
in this case one might send

```
{
   "do_" : [ "kiss", "send" ],
   "target" : "bakker@orvelte.nep",
   "xcount" : "3"
}
```

Note how the `"do_"` string is used for the keywords of the
grammar, and how the variables `<target>` and `<xcount>` end up
in words of their own.

The `cmdparser` module offers much more, in terms of syntax for
variables and their tab-based completion.  Just
[read the documentation](https://pypi.org/project/cmdparser/)
for details.

Do not start your commands with `arpa2`, so do not start your
function names with `do_arpa2` as for example in `do_arpa2kiss`.
The names starting with `arpa2` will be used as shell names,
and commands will be automatically added to allow switching
between shells.

You may define a `reset(self)` function on your shell that will
reset the state of the shell after it has run.  This is
called when the meta-shell causes switching from one shell
to another.  The shell instance will remain, but you can
choose to remove parts of the state.  For instance, a path
in the filesystem or an object in LDAP that you were
focussing on, or perhaps a password that was memorised.  If
you don't specify a `reset(self)` function then the object
will not be cleaned in any way when switching shells.

You should define a `main` function of some sort, let's call
it like that for simplicity.  A common formulation is this:

```
def main ():
    shell = Cmd ()
    shell.cmdloop ()

if __name__ == '__main__':
    main ()
```

This will help to start the command from the shell, or when
the module is loaded directly (as you may want to do during
development and testing).


## Invoking your Shell

There are two ways of invoking your shell.  Assuming you have packaged
it with a `console_scripts` entry-point named `arpa2xxx`, you would be
able to run `arpa2xxx` from any command line.  If all you require is
this one shell, you are done.

In many cases, a hosting environment runs more than one shell, each
catering to their own specific aspects of the environment.  This
means that you don't need to address ACL aspects (except perhaps
creating the right structures for them) and the operator does not
need to learn your original way of specifying them, but can rely
on a generic mechanism to handle ACL aspects.

For such an environment, the meta-shell `arpa2shell` can be called
and it in turn allows switching to your shell with a simple `arpa2xxx`
command.  Moreover, your shell and the others that are locally
installed will be cross-linked, so the operator can enter the `arpa2xxx`
command to enter your shelll from all the other shells as well.
You might see the `arpa2shell` as the constructor of this setup as
well as a shell that you get to see before you jumped into the
first shell of your choosing.

To allow your shell to be found by the `arpa2shell` meta-shell, it
should register an entry-point named `arpa2shell.cmd.subclasses`
as described below under packaging.


## Running the JSON daemon for your Shell

The JSON daemon is linked to the same packaging entry-point named
`arpa2shell.cmd.subclasses` as the `arpa2shell` mechanism.  So, if
`arpa2shell` can find your Shell class, then so can the JSON daemon.

The JSON daemon never runs for one shell alone, but it registers
all the shells with the AMQP 1.0 backbone.  Remember that any ACL
control is part of the commands, and your Shell as a whole will
be openly exposed.  Well, openly... it requires GSS-API for end-to-end
protection, but anyone getting through that is welcomed, because they
are authenticated users and can therefore be subjected to the ACL.


## Packaging your Shell

The name `arpa2shell` is a namespace.  Because of this, you will
use `from arpa2shell import` statements to get hold of its parts.
The value of this is that various ARPA2 Shells can be distributed
in their own packages.  The suggested package naming would be
`arpa2shell-xxx` if it is called as `arpa2xxx` from the operating
system prompt or from the `arpa2shell` meta-shell and the other
shells that start through them.

Independent of naming, you may decide to add your shell to the
[Git repository for ARPA2 Shells](https://github.com/arpa2/arpa2shell)
and extend the setup instructions to build the necessary wheels.
Keeping the shells separately packaged helps to reduce the
runtime dependencies, and it helps to install precisely those
shells that are locally of use on a hosting system.

In any case, you should add the entry-point that helps the
`arpa2shell` meta-shell and the JSON daemon to find your
shell, but also a script to call from the operating system
command line if you prefer to start the shell directly,
so without going through the meta-shell `arpa2shell`.

```
setuptools.setup (
    name = 'arpa2xxx',
    version = '0.0.0',
    url = 'https://github.com/arpa2/arpa2shell/arpa2xxx',
    description = ...,
    long_description = ...,
    long_description_content_type = 'text/markdown',
    ...
    namespace_packages = [ 'arpa2shell' ],
    packages = [ 'arpa2shell.arpa2xxx' ],
    package_dir = {
        'arpa2shell.arpa2xxx' : path.join (here, 'src', 'arpa2xxx'),
    },
    ...
    entry_points = {
        'arpa2shell.cmd.subclasses' : [
            'arpa2xxx' : 'arpa2shell.arpa2xxx:Cmd' ],
	'console_scripts' : [
            'arpa2xxx' : 'arpa2shell.arpa2xxx:main' ],
    },
    ...
)
```
