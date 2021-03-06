# The ARPA2 Shell Collection

> *ARPA2 Shells are the control programs for hosts that implement
> parts of the InternetWide Architecture.  They may integrate with
> components like LDAP, Kerberos or databases to setup and control 
> those components.  The shells have an interactive interface and
> a JSON access path.*

To operate a node in your infrastructure, you might use the basic
commands relating to the various programs that make them do what
they are supposed to do.  Or you might use a wrapper shell that
is designed to make functionality available at a conceptual level.
This is the intention of the ARPA2 Shells.

As part of doing something, an infrastructural node may need to
order co-operation from another node.  This too can be done using
traditional techniques, for instance accessing a shell and sending
a command. then scraping the output.  This tends to be tedious and
errorprone.  The ARPA2 Shells facilitate a JSON access channel to
accommodate such commands in an automation-friendly manner, and
indeed the shells can calll on each other.


## Access Control

A vital part in the design of the ARPA2 Shell system is that they
exercise access control not on the sessions, but on the individual
commands.  This is a bit like file access permissions, but now
applied to operations.  Here it helps that the operations aim to
be conceptual, rather than mechanical.  Instead of granting the
permission to write a file, you would be granting the permission
to add and remove users under a domain.

An interesting result of this detailed level of access control is
that we can open the system to anyone.  The shells and their JSON
interfaces are open to any user anywhere, both internal and external,
but before they can succeed in running a certain command they need
to be qualified to run just that command.  In other words, anyone
accessing our shells can get a prompt -- but they may still be
impotent when it comes to issuing commands.  This openness is of
importance with our intended pluggable infrastructure, where
third parties can plugin service under our domain and we allow
them a limited degree of control.


## Command Syntax implies JSON Scheme

The commands issued have a clear syntax, of which the ARPA2 Shells
are aware.  This is inherited from the `cmdparser.cmdparser` package
by Andy Pearce.  We extended this package with a JSON interface,
using the same grammar to form a JSON scheme.  We are still hoping
to integrate our work into the original package, but have ceased
waiting and instead forked the package.  You can use our package
`arpa2shell.cmdparser` as a drop-in replacement for the original
`cmdparser.cmdparser` package in its 1.0.1 version.

Read more:

  * [Backbone Innovations](http://internetwide.org/blog/2018/11/22/backbone-innovations.html)
  * [Protocol for ARPA2 Messaging over AMQP](PROTOCOL.MD)
  * [Using GSS-API with AMQP](GSS-API.MD)


## Generic Modules

The class `arpa2shell.Cmd` is a generic class from which the
ARPA2 Shells all inherit.  It provides them with a few general
facilities by which their behaviour is more general.  We may
also add a few other general things in the `arpa2shell` module,
such as LDAP access, or sending JSON commands to that interface
of other ARPA2 Shells.

Shells install as entry points into the `arpa2shell` or other
packages, and the generic shell installs as an `arpa2shell`
command.  This command might be started as a shell anywhere,
but will most commonly be used to service an OpenSSH login
or other (remote) console access attempts.

The `arpa2shell` does not process commands on its own, but it
can launch other shells.  This allows switching back and forth
between command environments that setup different aspects of
the infrastructure.  It is also possible to prefix a command
for a subshell with that subshell's name.  The result is that
ARPA2 Shells can focus on one aspect alone, while operators
still have control over as many of these aspects as they need
on any particular node.


## Choosing GSS-API and AMQP 1.0

ARPA2 Shells can send commands to subshells, but they should
not do this directly.  Instead, they should rely on a switching
backbone that grants optimum flexibility to the operator and
domain owners.  This is established by messaging through AMQP 1.0,
where access control is achieved through GSS-API with credential
forwarding.

We use GSS-API as an end-to-end encryption/authentication layer,
not TLS.  This might sound obnoxious, but it is grown out of a
true need.  TLS does not protect end-to-end traffic, but instead
a single client-server connection.  Since we intend to allow any
user to access any shell, we need to account for deep linking into
our infrastructure.  Again, the objective is to support external
components diving into whatever parts of the infrastructure and
simply control their usage of conceptual commands.

The choice to transport over AMQP 1.0 is for the same reason;
having end-to-end protection, we can now allow for flexible
routing of messages between infrastructural nodes, at least
for the passing of JSON messages.  This is best done with a
flexible infrastructure.  It is true that AMQP 1.0 is more
complex than its predecessors, but the upgrade to 1.0 enables
the routing of messages between domains, and that is in the
interest of externally provided services being plugged into
our infrastructure.

Read more:

  * [Tetralogy of a Free Internet](http://internetwide.org/blog/2016/06/24/iwo-phases.html)


## Multiple Shells in one Setup

Operators may install multiple shells on one machine, and
to simplify that we support multiple shells in one Git repository.
This is not required, other repositories can add their own shells
under the `arpa2shell` name space.

The `setup.py` builds and distributes multiple software
packages at once.  You normally want to install the ones that
make sense locally, so keep an eye on that.  We may split up
the `setup.py` later if that makes sense.

The currently supported shells are:

  * The basic shell `arpa2shell`
  * The basic client `arpa2client` for JSON / GSS-API / AMQP 1.0
  * The basic server `arpa2server` for JSON / GSS-API / AMQP 1.0
  * [arpa2dns](src/arpa2dns/README.MD) for DNS management
  * [arpa2id](src/arpa2id/README.MD) for Identity management
