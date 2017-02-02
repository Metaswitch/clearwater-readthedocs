Off-net Calling with BGCF and IBCF
==================================

The Clearwater IBCF (Interconnection Border Control Function) provides
an interface point between a Clearwater deployment and one or more
trusted SIP trunks.

The IBCF does not currently provide all of the functions of an IMS
compliant IBCF - in particular it does not support topology hiding or an
H.248 interface to control a Transition Gateway.

To use the IBCF function you must install and configure at least one
IBCF node, set up the ENUM configuration appropriately, and set up BGCF
(Breakout Gateway Control Function) routing configuration on the Sprout
nodes.

Install and Configure an IBCF
-----------------------------

Install and configure an IBCF node with the following steps.

-  Install the node as if installing a Bono node, either
   `manually <Manual_Install.html>`__ or `using
   Chef <Automated_Install.html>`__. If using Chef, use the ``ibcf`` role,
   for example

   ::

       knife box create -E <env> ibcf

-  Edit the /etc/clearwater/user\_settings file (creating it if it does
   not already exist) and add or update the line defining the IP
   addresses of SIP trunk peer nodes.

   ::

       trusted_peers="<trunk 1 IP address>,<trunk 2 IP address>,<trunk 3 IP address>, ..."

-  Restart the Bono daemon.

   ::

       service stop bono (allow monit to restart Bono)

ENUM Configuration
------------------

The number ranges that should be routed over the SIP trunk must be set
up in the ENUM configuration to map to a SIP URI owned by the SIP trunk
provider, and routable to that provider. For example, you would normally
want to map a dialed number to a URI of the form ``<number>@<domain>``.

This can either be achieved by defining rules for each number range you
want to route over the trunk, for example

::

    *.0.1.5 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@<trunk IP address>!" .
    *.0.1.5.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@<trunk IP address>!" .

or by defining a default mapping to the trunk and exceptions for number
ranges you want to keep on-net, for example

::

    * IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@<trunk IP address>!" .
    *.3.2.1.2.4.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@<local domain>!" .
    *.3.2.1.2.4.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@<local domain>!" .

You can also use ENUM to provide number portability information, for
example

::

    *.3.2.1.2.4.2 IN NAPTR 1 1 "u" "E2U+pstn:tel" "!(^.*$)!sip:\\1;npdi;rn=+242123@<local domain>!" .
    *.3.2.1.2.4.2.1 IN NAPTR 1 1 "u" "E2U+pstn:tel" "!(^.*$)!sip:\\1;npdi@<local domain>!" .

Refer to the `ENUM guide <ENUM.html>`__ for more about how to configure
ENUM.

BGCF Configuration
------------------

BGCF (Border Gateway Control Function) configuration is stored in the
``bgcf.json`` file in ``/etc/clearwater`` on each Sprout node (both I-
and S-CSCF). The ``bgcf.json`` file stores two types of mappings.

-  The first maps from SIP trunk IP addresses and/or domain names to
   IBCF SIP URIs
-  The second maps from a telephone number (contained in the ``rn``
   parameter of a Tel URI, the ``rn`` parameter in a SIP URI, a TEL URI
   or the user part of a SIP URI with a user=phone parameter) to an IBCF
   SIP URI using prefix matching on the number.

These mappings control which IBCF nodes are used to route to a
particular destination. Each entry can only apply to one type of
mapping.

Multiple nodes to route to can be specified. In this case, Route headers
are added to the message such that it is sent to the first node and the
first node sends it to the second node and so on; the message is not
tried at the second node if it fails at the first node.

The ``bgcf.json`` file is in JSON format, for example.

::

    {
        "routes" : [
            {   "name" : "<route 1 descriptive name>",
                "domain" : "<SIP trunk IP address or domain name>",
                "route" : ["<IBCF SIP URI>"]
            },
            {   "name" : "<route 2 descriptive name>",
                "domain" : "<SIP trunk IP address or domain name>",
                "route" : ["<IBCF SIP URI>", "<IBCF SIP URI>"]
            },
            {   "name" : "<route 3 descriptive name>",
                "number" : "<Telephone number>",
                "route" : ["<IBCF SIP URI>", "<IBCF SIP URI>"]
            }
        ]
    }

There can be only one route set for any given SIP trunk IP address or
domain name. If there are multiple routes with the same destination IP
address or domain name, only the first will be used. Likewise, there can
only be one route set for any given telephone number; if there are
multiple routes with the same telephone number only the first will be
used.

A default route set can be configured by having an entry where the
domain is set to ``"*"``. This will be used by the BGCF if it is trying
to route based on the the domain and there's no explicit match for the
domain in the configuration, or if it is trying to route based on a
telephone number and there's no explicit match for the number in the
configuration.

After making a change to this file you should run
``sudo cw-upload_bgcf_json`` to ensure the change is synchronized to
other Sprout nodes on your system (including nodes added in the future).
