# ARPA2 Shell to edit Resource Records in DNS

> *This shell manages a master DNS node.  We generally send
> the same DNS commands to multiple masters and let them work
> in parallel, with the exception of key management operations
> which must be co-ordinated so the signers produce exchangeable
> signatures.*

This shell assumes that Knot DNS is running.
If this is true you can start the DNS shell, either from an
operating system prompt or from the meta-shell `arpa2shell` with
the command

```
arpa2dns
```

In the DNS shell, you can do things like (more to come)

```
zone add orvelte.nep ns1.orvelte.nep. admin.orvelte.nep.
dane config pkix-end pubkey sha512
dane add orvelte.nep _tcp 443 web 666999aaabbbcccdddeeefff
acme add orvelte.nep www 1122334455
zone del orvelte.nep
exit
```

If you hadn't deleted the zone, you could have queried it
with commands like

```
kdig @localhost _443._tcp.web.orvelte.nep tlsa
kdig @localhost _acme-challenge.www.orvelte.nep txt
```

But alas, you had to go and delete that zone.  That ought
to teach you, following up orders without thinking about
their consequences ;-)

**ENUM support.**
There is some special support for ENUM.  Any place that
receive a zone can also process +ddddd form numbers,
which will be mapped to the ENUM form d.d.d.d.d.e164.arpa
before working with it:

```
zone add +12345 ns1.example.com admin@example.com
enum add +12345          1 E2U+xmpp     xmpp:1\\1@jabber.nep
enum add +12345 wildcard 1 E2U+xmpp xmpp:1\\1+\\2@jabber.nep
enum del +12345          1 E2U+xmpp     xmpp:1\\1@jabber.nep
enum del +12345 wildcard 1 E2U+xmpp xmpp:1\\1+\\2@jabber.nep
zone del +12345
```

The form without `wildcard` simply adds an NAPTR to reference
the service field and URI for the indicated number; the form
with `wildcard` adds an NAPTR for all numbers with additional
digits, like `+123456789`.  The `\\1` variable expands to
the matched domain minus the skip (here set to 1) and the
`\\2` variable expands to the wildcarded part.

On an operating system's commandline could query for

```
kdig @localhost         5.4.3.2.1.e164.arpa naptr
kdig @localhost 9.8.7.6.5.4.3.2.1.e164.arpa naptr
```


## Learning about DNS Cache Timing

When publishing security-bound information, such as the
records `DNSKEY`, `DS`, `TLSA`, `SSHFP` it can be important
to not make such claims too early or too late.  Having to
figure out how long to wait can be rather tedious, but a
general structure might be
[min(DNS) and max(DNS)](https://github.com/arpa2/DNS-mixer/blob/master/doc/min-max-DNS.MD)
as we intend to build it into the anticipated
[DNS mixer](https://github.com/arpa2/DNS-mixer/blob/master/doc/dns-mixer-from-partial-masters.md)
component.

Until we have a DNS mixer, we can at least satisfy ourselves
by returning cache delays from knowledge central, which is
the DNS shell.  So, even simple update returns cache delay
times:

```
shell$ docker run -it demo-dns
# /etc/init.d/knot start
# arpa2dns
arpa2dns> ?
arpa2dns> ?record
arpa2dns> record add orvelte.nep www 7200 AAAA 2001:db8:1::80
Cache-Update-Delay: 3600
arpa2dns> record add orvelte.nep www 7200 AAAA 2001:db8:2::80
Cache-Update-Delay: 7200
arpa2dns> quit
# kdig +short @::1 www.orvelte.nep aaaa
2001:db8:1::80
2001:db8:2::80
# exit
shell$ 
```

Note the two responses, and how they are different.  The
first record is a freshly added `AAAA` record that will
take the negative caching time to come through.  This is
the lowest of the SOA minimum and the SOA TTL, in this
case 3600 seconds from now.  The second addition is made
to an existing record that has a cache time of 7200, and
since that may already be loaded somewhere it may take
that long for the second record added to come through.
(I am aware that the shell could try to combine these,
and we probably will, at some point.)

For security-related operations, this is a great asset.
When you post something that ends up as a security
instruction, you always risk breaking things if the
instruction is expected but not yet found.  The same
holds when you remove things.  In those cases, it is
really helpful to have a timer for the records added
or removed, to know when they are globally available,
or globally retracted.  This facility takes away a
lot of complexity related to caching in DNS.


## Current and Future Work

This DNS demonstration takes in zone changes and publishes
them with DNSSEC signatures on everything.  For now, there
is one master.  Future versions will also support multiple
masters that sign independently, with only the DNSSEC keys
as shared state.  Yes, DNSSEC can do that :-)


