# ARPA2 Shell for Reservoir

> *The arpa2reservoir shell is used for management of nested
> data structures with metadata in LDAP and the actual data
> in an object store.*

Shells for poking around can be started as desired in the
same way on an operating system shell or in the meta-shell
`arpa2shell` with:

```
arpa2reservoir
```

Note that the set of domains is independent from those
used in `arpa2id`.  They reside in different parts
of the tree, to help with situations where not all
domains have the same service, where subdomains have
additional service, where customers take out only one
but not both the services, and so on.

Once on an `arpa2reservoir` shell, you can do things like
adding domains, Resource Collections underneath domains,
and since both the domain and each Resource Collection
count as a Resource Index, you can use `index add` to
link to a Resource Collection throug its UUID (shown
symbolically below, as it is a random value).  You can
start at a domain's Resource Index with `index domain`
and the traverse locally added names with `index path`.
There may be cycles, such as the `buurman` below that
points from `Smid` to `Bakker` and back again.  The
paths are always finite-sized so you can make any
steps that seem good.

```
domain add orvelte.nep
collection add orvelte.nep Ambachten
collection add orvelte.nep Kunstenaars
collection add orvelte.nep Bakker
collection add orvelte.nep Brood
collection add orvelte.nep Banket
collection add orvelte.nep Smid
collection add orvelte.nep Hoefijzers
collection add orvelte.nep Schilden
collection add orvelte.nep Zwaarden
index domain orvelte.nep
index add {UUID_Kunstenaars} kunst
index add {UUID_Ambachten} ambacht
index path kunst
index add {UUID_Schilden} schilden
index add {UUID_Zwaarden} zwaarden
index add {UUID_Banket} banket
index add {UUID_Bakker} bakker
index add {UUID_Smid} smid
inded domain orvelte.nep
index path ambacht
index add {UUID_Schilden} schilden
index add {UUID_Zwaarden} zwaarden
index add {UUID_Hoefijzers} hoefijzers
index add {UUID_Brood} brood
index add {UUID_Banket} banket
index add {UUID_Bakker} bakker
index add {UUID_Smid} smid
index domain orvelte.nep
index collection {UUID_Smid}
index add {UUID_Schilden} schilden
index add {UUID_Zwaarden} zwaarden
index add {UUID_Hoefijzers} hoefijzers
index add {UUID_Bakker} buurman
index add {UUID_Kunstenaars} kunst
index add {UUID_Ambachten} ambacht
index path buurman
index add {UUID_Brood} brood
index add {UUID_Banket} banket
index add {UUID_Smid} buurman
index add {UUID_Kunstenaars} kunst
index add {UUID_Ambachten} ambacht
index domain orvelte.nep
index path kunst bakker brood
resource add file=/tmp/recept-krentemik.txt type=text/plain name=Recept_Krentemik
```

Make sure to hit `<tab>` often, it should work really
pleasantly.  Use `?command` or `help command` to inquire
about a specific command's syntax.

You can also use the `arpa2acl` shell to set the ACL for
the two kinds of Reservoir Index objects: the client's
domain as represented under the Reservoir root and the
various Reservoir Collections underneath the domain.
Resource are one step further down; these do not have
individual ACL settings but follow Resource Collections.

The shells are a bit rudimentary, but they may grow
into management utilities.  By that time we should
probably split the words over the underscore characters,
perhaps using the `cmdparser` package that was installed.
