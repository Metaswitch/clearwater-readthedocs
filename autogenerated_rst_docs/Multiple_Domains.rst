Multiple Domains
================

A single Clearwater deployment can support subscribers in multiple
domains. This document

-  gives some background context
-  describes how to configure multiple domains
-  covers some restrictions on this support.

Background
----------

Clearwater acts as an S-CSCF for one or more home domains. It can only
provide service to users within a home domain for which it is the
S-CSCF. Traffic to or from users in any other home domains must go via
the S-CSCF for those other domains.

Home domains are a routing concept. There is a similar (but distinct)
concept of authentication realms. When a user authenticates, as well as
providing their username and digest, they must also provide a realm,
which describes which user database to authenticate against. Many
clients default their home domain to match their authentication realm.

A single Clearwater deployment can support multiple home domains and
multiple realms.

Configuration
-------------

There are three steps to configuring multiple home domains and/or
multiple realms.

-  Configure the Clearwater deployment to know about all the home
   domains it is responsible for.
-  Add DNS records to point all home domains at the deployment.
-  Create subscribers within these multiple home domains, and optionally
   using multiple different realms.

Configuring the Clearwater Deployment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``/etc/clearwater/shared_config`` file can contain two properties
that are relevant to this function.

-  ``home_domain`` - defines the "default" home domain and must always
   be set
-  ``additional_home_domains`` - optionally defines additional home
   domains

The only difference between the default home domain and the additional
home domains is that the default home domain is used whenever Clearwater
must guess the home domain for a TEL URI, e.g. when filling in the
orig-ioi or term-ioi parameters on the P-Charging-Vector header. This is
fairly minor, and generally you can consider the default home domain and
additional home domains as equivalent.

Adding DNS Records
~~~~~~~~~~~~~~~~~~

The `Clearwater DNS Usage <Clearwater_DNS_Usage.md>`__ document
describes how to configure DNS for a simple single-domain deployment.
This includes creating NAPTR, SRV and A records that resolve the home
domain (or ``<zone>``) to the bono nodes. If you have additional home
domains, you should repeat this for each additional home domain. This
ensures that SIP clients can find the bono nodes without needing to be
explicitly configured with a proxy.

Creating subscribers.
~~~~~~~~~~~~~~~~~~~~~

Once the deployment has multiple domain support enabled, you can create
subscribers in any of the domains, and with any realm.

-  If you use ellis, the
   ```create-numbers.py`` <https://github.com/Metaswitch/ellis/blob/dev/docs/create-numbers.md>`__
   script accepts a ``--realm`` parameter to specify the realm in which
   the directory numbers are created. When a number is allocated in the
   ellis UI, ellis picks any valid number/realm combination.

-  If you
   `bulk-provision <https://github.com/Metaswitch/crest/blob/dev/docs/Bulk-Provisioning%20Numbers.md>`__
   numbers, the home domain and realm can be specified in the input CSV
   file.

-  If you use homestead's `provisioning
   API <https://github.com/Metaswitch/crest/blob/dev/docs/homestead_prov_api.md>`__
   (i.e. without an external HSS), you can specify the home domain and
   realm as parameters.

Alternatively, you can use an external HSS, and configure the
subscribers using its provisioning interface.

Restriction
-----------

Clearwater does not support connections to multiple Diameter realms for
the Cx interface to the HSS or the Rf interface to the CDF - only a
single Diameter realm is supported.
