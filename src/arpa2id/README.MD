# ARPA2 Shell for Identity Management

> *The arpa2id shell is a command interface with JSON backend
> over which identities can be managed, including such things as
> aliases, groups, roles and so on.*

Whether on an operating system prompt or in the `arpa2shell`
meta-shell, you can start identity management with the
command

```
arpa2id
```

This is a special shell for doing ARPA2 manipulations.

Once in such an `arpa2id` shell, you can do things like

```
domain_add orvelte.nep Orvelte, Incorporated
user_add orvelte.nep bakker Hij die bakt
user_add orvelte.nep smid Hij die hakt
user_del orvelte.nep bakker
user_del orvelte.nep smid
domain_del orvelte.nep
```

Make sure to hit `<tab>` often, it should work really
pleasantly.  Use `?command` or `help command` to inquire
about a specific command's syntax.

You can run `slapcat` from another shell to see the
changes in the database.  This command is basically
a dump of the contents of the OpenLDAP database in a
standardised exchange format, LDIF.  This is a rogue
utility, bypassing the protocol and authentication,
so it can only be run locally.

The shells are a bit rudimentary, but they are meant to grow
into management utilities.  By that time we should
probably split the words over the underscore characters,
perhaps using the `cmdparser` package that was installed.


