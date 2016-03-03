Clearwater DNS Usage
====================

DNS is the `Domain Name System <http://en.wikipedia.org/wiki/DNS>`__. It
maps service names to hostnames and then hostnames to IP addresses.
Clearwater uses DNS.

This document describes

-  Clearwater's DNS strategy and requirements
-  how to configure `AWS Route 53 <http://aws.amazon.com/route53/>`__
   and `BIND <https://www.isc.org/downloads/bind/>`__ to meet these.

DNS is also used as part of the
`ENUM <http://tools.ietf.org/rfc/rfc6116.txt>`__ system for mapping
E.164 numbers to SIP URIs. This isn't discussed in this document -
instead see the separate `ENUM <ENUM.md>`__ document.

*If you are installing an All-in-One Clearwater node, you do not need
any DNS records and can ignore the rest of this page.*

Strategy
--------

Clearwater makes heavy use of DNS to refer to its nodes. It uses it for

-  identifying individual nodes, e.g. sprout-1.example.com might resolve
   the IP address of the first sprout node
-  identifying the nodes within a cluster, e.g. sprout.example.com
   resolves to all the IP addresses in the cluster
-  fault-tolerance
-  selecting the nearest site in a multi-site deployments, using
   latency-based routing.

Clearwater also supports using DNS for identifying non-Clearwater nodes.
In particular, it supports DNS for identifying SIP peers using NAPTR and
SRV records, as described in `RFC
3263 <http://tools.ietf.org/rfc/rfc3263.txt>`__.

Resiliency
----------

By default, Clearwater routes all DNS requests through an instance of
`dnsmasq <http://www.thekelleys.org.uk/dnsmasq>`__ running on localhost.
This round-robins requests between the servers in /etc/resolv.conf, as
described in `its
FAQ <http://www.thekelleys.org.uk/dnsmasq/docs/FAQ>`__:

    By default, dnsmasq treats all the nameservers it knows about as
    equal: it picks the one to use using an algorithm designed to avoid
    nameservers which aren't responding.

If the ``signaling_dns_server`` option is set in
``/etc/clearwater/shared_config`` (which is mandatory when using
`traffic separation <Multiple_Network_Support.md>`__), Clearwater will
not use dnsmasq. Instead, resiliency is achieved by being able to
specify up to three servers in a comma-separated list (e.g.
``signaling_dns_server=1.2.3.4,10.0.0.1,192.168.1.1``), and Clearwater
will fail over between them as follows:

-  It will always query the first server in the list first
-  If this returns SERVFAIL or times out (which happens after a
   randomised 500ms-1000ms period), it will resend the query to the
   second server
-  If this returns SERVFAIL or times out, it will resend the query to
   the third server
-  If all servers return SERVFAIL or time out, the DNS query will fail

Clearwater caches DNS responses for several minutes (to reduce the load
on DNS servers, and the latency introduced by querying them). If a cache
entry is stale, but the DNS servers return SERVFAIL or time out when
Clearwater attempts to refresh it, Clearwater will continue to use the
cached value until the DNS servers become responsive again. This
minimises the impact of a DNS server failure on calls.

Requirements
------------

DNS Server
~~~~~~~~~~

Clearwater requires the DNS server to support

-  `RFC 1034 <http://tools.ietf.org/rfc/rfc1034.txt>`__ and `RFC
   1035 <http://tools.ietf.org/rfc/rfc1035.txt>`__ - basic DNS
-  `RFC 2181 <http://tools.ietf.org/rfc/rfc2181.txt>`__ - clarifications
   to DNS
-  `RFC 2782 <http://tools.ietf.org/rfc/rfc2782.txt>`__ - SRV records
-  `RFC 3596 <http://tools.ietf.org/rfc/rfc3596.txt>`__ - AAAA records
   (if IPv6 is required).

Support for latency-based routing and health-checking are required for
multi-site deployments.

Support for `RFC 2915 <http://tools.ietf.org/rfc/rfc2915.txt>`__ (NAPTR
records) is also suggested, but not required. NAPTR records specify the
transport (UDP, TCP, etc.) to use for a particular service - without it,
UEs will default (probably to UDP).

AWS Route 53 supports all these features except NAPTR. BIND supports all
these features except latency-based routing (although there is a
`patch <http://www.caraytech.com/geodns/>`__ for this) and
health-checking.

DNS Records
~~~~~~~~~~~

Clearwater requires the following DNS records to be configured.

-  bono

   -  ``bono-1.<zone>``, ``bono-2.<zone>``... (A and/or AAAA) - per-node
      records for bono
   -  ``<zone>`` (A and/or AAAA) - cluster record for bono, resolving to
      all bono nodes - used by UEs that don't support RFC 3263
      (NAPTR/SRV)
   -  ``<zone>`` (NAPTR, optional) - specifies transport requirements
      for accessing bono - service ``SIP+D2T`` maps to
      ``_sip._tcp.<zone>`` and ``SIP+D2U`` maps to ``_sip._udp.<zone>``
   -  ``_sip._tcp.<zone>`` and ``_sip._udp.<zone>`` (SRV) - cluster SRV
      records for bono, resolving to port 5060 on each of the per-node
      records

-  sprout

   -  ``sprout-1.<zone>``, ``sprout-2.<zone>``... (A and/or AAAA) -
      per-node records for sprout
   -  ``sprout.<zone>`` (A and/or AAAA) - cluster record for sprout,
      resolving to all sprout nodes - used by P-CSCFs that don't support
      RFC 3263 (NAPTR/SRV)
   -  ``sprout.<zone>`` (NAPTR, optional) - specifies transport
      requirements for accessing sprout - service ``SIP+D2T`` maps to
      ``_sip._tcp.sprout.<zone>``
   -  ``_sip._tcp.sprout.<zone>`` (SRV) - cluster SRV record for sprout,
      resolving to port 5054 on each of the per-node records
   -  ``icscf.sprout.<zone>`` (NAPTR, only required if using sprout as
      an I-CSCF) - specifies transport requirements for accessing sprout
      - service ``SIP+D2T`` maps to ``_sip._tcp.icscf.sprout.<zone>``
   -  ``_sip._tcp.icscf.sprout.<zone>`` (SRV, only required if using
      sprout as an I-CSCF) - cluster SRV record for sprout, resolving to
      port 5052 on each of the per-node records

-  homestead

   -  ``homestead-1.<zone>``, ``homestead-2.<zone>``... (A and/or AAAA)
      - per-node records for homestead
   -  ``hs.<zone>`` (A and/or AAAA) - cluster record for homestead,
      resolving to all homestead nodes

-  homer

   -  ``homer-1.<zone>``, ``homer-2.<zone>``... (A and/or AAAA) -
      per-node records for homer
   -  ``homer.<zone>`` (A and/or AAAA) - cluster record for homer,
      resolving to all homer nodes

-  ralf

   -  ``ralf-1.<zone>``, ``ralf-2.<zone>``... (A and/or AAAA) - per-node
      records for ralf
   -  ``ralf.<zone>`` (A and/or AAAA) - cluster record for ralf,
      resolving to all ralf nodes

-  ellis

   -  ``ellis-1.<zone>`` (A and/or AAAA) - per-node record for ellis
   -  ``ellis.<zone>`` (A and/or AAAA) - "cluster"/access record for
      ellis

-  standalone application server (e.g. gemini/memento)

   -  ``<standalone name>-1.<zone>`` (A and/or AAAA) - per-node record
      for each standalone application server
   -  ``<standalone name>.<zone>`` (A and/or AAAA) - "cluster"/access
      record for the standalone application servers

Of these, the following must be resolvable by UEs - the others need only
be resolvable within the core of the network. If you have a NAT-ed
network, the following must resolve to public IP addresses, while the
others should resolve to private IP addresses.

-  bono

   -  ``<zone>`` (A and/or AAAA)
   -  ``<zone>`` (NAPTR, optional)
   -  ``_sip._tcp.<zone>`` and ``_sip._udp.<zone>`` (SRV)

-  ellis

   -  ``ellis.<zone>`` (A and/or AAAA)

-  memento

   -  ``memento.<zone>`` (A and/or AAAA)

If you are not deploying with some of these components, you do not need
the DNS records to be configured for them. For example, if you are using
a different P-CSCF (and so don't need bono), you don't need the bono DNS
records. Likewise, if you are deploying with an external HSS (and so
don't need ellis), you don't need the ellis DNS records.

Configuration
-------------

Clearwater can work with any DNS server that meets the `requirements
above <#dns-server>`__. However, most of our testing has been performed
with

-  `AWS Route 53 <http://aws.amazon.com/route53/>`__ - see
   `configuration instructions <#aws-route-53>`__
-  `BIND <https://www.isc.org/downloads/bind/>`__ - see `configuration
   instructions <#bind>`__.

The Clearwater nodes also need to know the identity of their DNS server.
Ideally, this is done via `DHCP <http://en.wikipedia.org/wiki/DHCP>`__
within your virtualization infrastructure. Alternatively, you can
`configure it manually <#client-configuration>`__.

The UEs need to know the identity of the DNS server too. In a testing
environment, you may be able to use DHCP or manual configuration. In a
public network, you will need to register the ``<zone>`` domain name you
are using and arranging for an NS record for ``<zone>`` to point to your
DNS server.

AWS Route 53
~~~~~~~~~~~~

Clearwater's `automated install <Automated_Install.md>`__ automatically
configures AWS Route 53. There is no need to follow the following
instructions if you are using the automated install.

The official `AWS Route 53
documentation <http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html>`__
is a good reference, and most of the following steps are links into it.

To use AWS Route 53 for Clearwater, you need to

-  `create a
   domain <http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/CreatingNewDNS.html>`__
-  `create record
   sets <http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/RRSchanges_console.html>`__
   for each of the non-geographically-redundant `records Clearwater
   requires <#dns-records>`__.

For the geographically-redundant records, you need to

-  `create a
   health-check <http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/health-checks-creating-deleting.html>`__
   for each of your sites
-  `create latency-based-routing
   records <http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/HowToLatencyRRS.html>`__
   for each of your sites
-  associate each site's records with its health-check.

Note that AWS Route 53 does not support NAPTR records.

BIND
~~~~

To use BIND, you need to

-  install it
-  create an entry for your "zone" (DNS suffix your deployment uses)
-  configure the zone with a "zone file"
-  restart BIND.

Note that BIND does not support latency-based routing or
health-checking.

Installation
^^^^^^^^^^^^

To install BIND on Ubuntu, issue ``sudo apt-get install bind9``.

Creating Zone Entry
^^^^^^^^^^^^^^^^^^^

To create an entry for your zone, edit the
``/etc/bind/named.conf.local`` file to add a line of the following form,
replacing ``<zone>`` with your zone name.

::

    zone "<zone>" IN { type master; file "/etc/bind/db.<zone>"; };

Configuring Zone
^^^^^^^^^^^^^^^^

Zones are configured through "zone files" (defined in `RFC
1034 <http://tools.ietf.org/rfc/rfc1034.txt>`__ and `RFC
1035 <http://tools.ietf.org/rfc/rfc1035.txt>`__).

If you followed the instructions above, the zone file for your zone is
at ``/etc/bind/db.<zone>``.

For Clearwater, you should be able to adapt the following example zone
file by correcting the IP addresses and duplicating (or removing)
entries where you have more (or fewer) than 2 nodes in each tier.

::

    $TTL 5m ; Default TTL

    ; SOA, NS and A record for DNS server itself
    @                 3600 IN SOA  ns admin ( 2014010800 ; Serial
                                              3600       ; Refresh
                                              3600       ; Retry
                                              3600       ; Expire
                                              300 )      ; Minimum TTL
    @                 3600 IN NS   ns
    ns                3600 IN A    1.0.0.1 ; IPv4 address of BIND server
    ns                3600 IN AAAA 1::1    ; IPv6 address of BIND server

    ; bono
    ; ====
    ;
    ; Per-node records - not required to have both IPv4 and IPv6 records
    bono-1                 IN A     2.0.0.1
    bono-2                 IN A     2.0.0.2
    bono-1                 IN AAAA  2::1
    bono-2                 IN AAAA  2::2
    ;
    ; Cluster A and AAAA records - UEs that don't support RFC 3263 will simply
    ; resolve the A or AAAA records and pick randomly from this set of addresses.
    @                      IN A     2.0.0.1
    @                      IN A     2.0.0.2
    @                      IN AAAA  2::1
    @                      IN AAAA  2::2
    ;
    ; NAPTR and SRV records - these indicate a preference for TCP and then resolve
    ; to port 5060 on the per-node records defined above.
    @                      IN NAPTR 1 1 "S" "SIP+D2T" "" _sip._tcp
    @                      IN NAPTR 2 1 "S" "SIP+D2U" "" _sip._udp
    _sip._tcp              IN SRV   0 0 5060 bono-1
    _sip._tcp              IN SRV   0 0 5060 bono-2
    _sip._udp              IN SRV   0 0 5060 bono-1
    _sip._udp              IN SRV   0 0 5060 bono-2

    ; sprout
    ; ======
    ;
    ; Per-node records - not required to have both IPv4 and IPv6 records
    sprout-1               IN A     3.0.0.1
    sprout-2               IN A     3.0.0.2
    sprout-1               IN AAAA  3::1
    sprout-2               IN AAAA  3::2
    ;
    ; Cluster A and AAAA records - P-CSCFs that don't support RFC 3263 will simply
    ; resolve the A or AAAA records and pick randomly from this set of addresses.
    sprout                 IN A     3.0.0.1
    sprout                 IN A     3.0.0.2
    sprout                 IN AAAA  3::1
    sprout                 IN AAAA  3::2
    ;
    ; NAPTR and SRV records - these indicate TCP support only and then resolve
    ; to port 5054 on the per-node records defined above.
    sprout                 IN NAPTR 1 1 "S" "SIP+D2T" "" _sip._tcp.sprout
    _sip._tcp.sprout       IN SRV   0 0 5054 sprout-1
    _sip._tcp.sprout       IN SRV   0 0 5054 sprout-2
    ;
    ; Per-node records for I-CSCF (if enabled) - not required to have both
    ; IPv4 and IPv6 records
    sprout-3               IN A     3.0.0.3
    sprout-3               IN AAAA  3::3
    ;
    ; Cluster A and AAAA records - P-CSCFs that don't support RFC 3263 will simply
    ; resolve the A or AAAA records and pick randomly from this set of addresses.
    icscf.sprout           IN A     3.0.0.3
    icscf.sprout           IN AAAA  3::3
    ;
    ; NAPTR and SRV records for I-CSCF (if enabled) - these indicate TCP
    ; support only and then resolve to port 5052 on the per-node records
    ; defined above.
    icscf.sprout           IN NAPTR 1 1 "S" "SIP+D2T" "" _sip._tcp.icscf.sprout
    _sip._tcp.icscf.sprout IN SRV   0 0 5052 sprout-3

    ; homestead
    ; =========
    ;
    ; Per-node records - not required to have both IPv4 and IPv6 records
    homestead-1            IN A     4.0.0.1
    homestead-2            IN A     4.0.0.2
    homestead-1            IN AAAA  4::1
    homestead-2            IN AAAA  4::2
    ;
    ; Cluster A and AAAA records - sprout picks randomly from these.
    hs                     IN A     4.0.0.1
    hs                     IN A     4.0.0.2
    hs                     IN AAAA  4::1
    hs                     IN AAAA  4::2
    ;
    ; (No need for NAPTR or SRV records as homestead doesn't handle SIP traffic.)

    ; homer
    ; =====
    ;
    ; Per-node records - not required to have both IPv4 and IPv6 records
    homer-1                IN A     5.0.0.1
    homer-2                IN A     5.0.0.2
    homer-1                IN AAAA  5::1
    homer-2                IN AAAA  5::2
    ;
    ; Cluster A and AAAA records - sprout picks randomly from these.
    homer                  IN A     5.0.0.1
    homer                  IN A     5.0.0.2
    homer                  IN AAAA  5::1
    homer                  IN AAAA  5::2
    ;
    ; (No need for NAPTR or SRV records as homer doesn't handle SIP traffic.)

    ; ralf
    ; =====
    ;
    ; Per-node records - not required to have both IPv4 and IPv6 records
    ralf-1                IN A     6.0.0.1
    ralf-2                IN A     6.0.0.2
    ralf-1                IN AAAA  6::1
    ralf-2                IN AAAA  6::2
    ;
    ; Cluster A and AAAA records - sprout and bono pick randomly from these.
    ralf                  IN A     6.0.0.1
    ralf                  IN A     6.0.0.2
    ralf                  IN AAAA  6::1
    ralf                  IN AAAA  6::2
    ;
    ; (No need for NAPTR or SRV records as ralf doesn't handle SIP traffic.)

    ; ellis
    ; =====
    ;
    ; ellis is not clustered, so there's only ever one node.
    ;
    ; Per-node record - not required to have both IPv4 and IPv6 records
    ellis-1                IN A     7.0.0.1
    ellis-1                IN AAAA  7::1
    ;
    ; "Cluster"/access A and AAAA record
    ellis                  IN A     7.0.0.1
    ellis                  IN AAAA  7::1

Restarting
^^^^^^^^^^

To restart BIND, issue ``sudo service bind9 restart``. Check
/var/log/syslog for any error messages.

Client Configuration
~~~~~~~~~~~~~~~~~~~~

Clearwater nodes need to know the identity of their DNS server. Ideally,
this is achieved through DHCP. There are two main situations in which it
might need to be configured manually.

-  When DNS configuration is not provided via DHCP.
-  When incorrect DNS configuration is provided via DHCP.

Either way, you must

-  create an ``/etc/dnsmasq.resolv.conf`` file containing the desired
   DNS configuration (probably just the single line
   ``nameserver <IP address>``)
-  add ``RESOLV_CONF=/etc/dnsmasq.resolv.conf`` to
   ``/etc/default/dnsmasq``
-  run ``service dnsmasq restart``.

(As background,
`dnsmasq <http://www.thekelleys.org.uk/dnsmasq/doc.html>`__ is a DNS
forwarder that runs on each Clearwater node to act as a cache. Local
processes look in ``/etc/resolv.conf`` for DNS configuration, and this
points them to localhost, where dnsmasq runs. In turn, dnsmasq takes its
configuration from ``/etc/dnsmasq.resolv.conf``. By default, dnsmasq
would use ``/var/run/dnsmasq/resolv.conf``, but this is controlled by
DHCP.)

IPv6 AAAA DNS lookups
~~~~~~~~~~~~~~~~~~~~~

Clearwater can be installed on an IPv4-only system, an IPv6-only system,
or a system with both IPv4 and IPv6 addresses (though the Clearwater
software does not use both IPv4 and IPv6 at the same time).

Normally, systems with both IPv4 and IPv6 addresses will prefer IPv6,
performing AAAA lookups first and only trying an A record lookup if that
fails. This may cause problems (or be inefficient) if you know that all
your Clearwater DNS records are A records.

In this case, you can configure a preference for A lookups by editing
``/etc/gai.conf`` and commenting out the line
``precedence ::ffff:0:0/96 100`` (as described at
http://askubuntu.com/questions/32298/prefer-a-ipv4-dns-lookups-before-aaaaipv6-lookups).
