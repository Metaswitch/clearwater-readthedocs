External HSS Integration
========================

All Clearwater deployments include a
`Homestead <https://github.com/Metaswitch/crest>`__ cluster. Homestead
presents an HTTP RESTful
`interface <https://github.com/Metaswitch/homestead/blob/dev/docs/homestead_api.md>`__
to HSS data. This HSS data can be stored in either

-  a Cassandra database located on the Homestead cluster
-  an external HSS, accessible over a standard IMS
   `Cx/Diameter <http://www.3gpp.org/ftp/Specs/html-info/29228.htm>`__
   interface.

This page describes

-  how it works
-  how to enable it
-  restrictions.

How It Works
------------

When Clearwater is deployed without an external HSS, all HSS data is
mastered in Homestead's own Cassandra database.

When Clearwater is deployed with an external HSS, HSS data is queried
from the external HSS via its Cx/Diameter interface and is then cached
in the Cassandra database.

Clearwater uses the following Cx message types.

-  Multimedia-Auth - to retrieve authentication details
-  Server-Assignment - to retrieve Initial Filter Criteria documents and
   register for change notifications
-  Push-Profile - to be notified of changes to Initial Filter Criteria
   documents
-  User-Authorization - to retrieve S-CSCF details on initial
   registrations
-  Location-Information - to retrieve S-CSCF details on calls
-  Registration-Termination - to be notified of de-registrations

How to Enable It
----------------

This section discusses how to enable support for an external HSS.

Before you start
~~~~~~~~~~~~~~~~

Before enabling support for an external HSS, you must

-  `install Clearwater <Installation_Instructions.md>`__
-  install an external HSS - details for this will vary depending on
   which HSS you choose, but there are instructions for `OpenIMSCore
   HSS <OpenIMSCore_HSS_Integration.md>`__.

Do not configure any Clearwater subscribers via Ellis!

-  Any subscribers you create before enabling the external HSS will
   override subscribers retrieved from the external HSS, and you will
   not be able to use Ellis to manage them.
-  After enabling the external HSS, you will not be able to create
   subscribers through Ellis at all - they must be created through the
   HSS's own management interface.

Enabling external HSS support on an existing deployment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable external HSS support, you will need to modify the contents of
``/etc/clearwater/shared_config`` so that the block that reads

::

    # HSS configuration
    hss_hostname=0.0.0.0
    hss_port=3868

instead reads

::

    # HSS configuration
    hss_hostname=<address of your HSS>
    hss_realm=<realm your HSS is located in>
    hss_port=<port of your HSS's Cx interface>

Both hss\_hostname and hss\_realm are optional. If a realm is
configured, homestead will try NAPTR/SRV resolution on the realm to find
and connect to (2 by default) diameter peers in the realm. If a hostname
is also configured, this will be used in the Destination-Host field on
the diameter messages, so that the messages will be routed to that host.
If just a hostname is configured, homestead will just attempt to create
and maintain a single connection to that host.

`This process <Modifying_Clearwater_settings>`__ explains how to modify
these settings and ensure that all nodes pick up the changes.

Configuring your external HSS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Homestead will now query the external HSS for subscriber details when
they are required by the rest of the Clearwater deployment, such as when
servicing SIP registrations.

In order to register and make calls, you need to create subscriber
records on your external HSS, and the detailed process for this will
depend on which HSS you have chosen. Generally, however, you will need
to

1. create a public user identity with the desired SIP URI
2. create an associated private user identity with its ID formed by
   removing the ``sip:`` scheme prefix from the public user ID
3. configure the public user identity's Initial Filter Criteria to
   include an application server named ``sip:mmtel.your.home.domain``,
   where ``your.home.domain`` is replaced with your home domain - this
   enables MMTEL services for this subscriber.

Allowing one subscriber to have two private identities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you try to use an `Android SIP
client <Configuring_the_native_Android_SIP_client.md#instructions-1>`__
that doesn't contain an **Authentication username** field, the client
will default to a username like **``1234``** (rather than
**``1234@example.com``** - the IMS standard form). To register a
subscriber you will have to configure your external HSS so that the
subscriber you are trying to register has two private identities
(**``1234``** and **``1234@example.com``**).

The detailed process for this will depend on which HSS you have chosen.
Generally, however, you will need to

1. create a subscriber as usual- with public user identity
   "sip:*<username>*\ @\ *<server>*"
2. create two new private identities, one having identity
   "*<username>*\ " and the other with identity
   "*<username>*\ @\ *<server>*"
3. associate the public user identity that was created in step 1:
   "sip:*<username>*\ @\ *<server>*" to both of the private identities
   created in step 2.

This should allow the SIP client to register with that subscriber.

Restrictions
------------

-  Since Homestead uses the Cx/Diameter interface to the HSS, and this
   interface is read-only, the Homestead API is read-only when external
   HSS integration is enabled.
-  Since Homestead's API is read-only, this means that
   `Ellis <https://github.com/Metaswitch/ellis>`__ can't be used
   alongside a deployment using an external HSS. Provisioning and
   subscriber management must be performed via the HSS's own management
   interface.
-  Clearwater currently only supports `SIP
   digest <http://tools.ietf.org/html/rfc3261#section-22.4>`__ or
   `AKA <http://tools.ietf.org/html/rfc3310>`__ authentication; details
   for other authentication methods are silently ignored from
   Multimedia-Auth responses. Other authentication methods may be added
   in future.
-  Homestead currently assumes that private user IDs are formed by
   removing the ``sip:`` prefix from the public user ID. This
   restriction may be relaxed in future.
-  While Homestead caches positive results from the external HSS, it
   does not currently cache negative results (e.g. for non-existent
   users). Repeated requests for a non-existent user will increase the
   load on the external HSS. This restriction may be relaxed in future.

