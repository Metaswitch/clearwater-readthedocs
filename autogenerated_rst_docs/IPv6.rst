IPv6
====

`IPv6 <http://en.wikipedia.org/wiki/IPv6>`__ is the new version of IP.
The most obvious difference from IPv4 is the addresses.

-  IPv4 addresses are 4 bytes, represented in decimal, separated by
   dots, e.g. ``166.78.3.224``
-  IPv6 addresses are 16 bytes, represented in hexadecimal, with each
   pair of bytes separated by colons, e.g
   ``2001:0db8:85a3:0000:0000:8a2e:0370:7334``.

Clearwater can operate over either IPv4 or IPv6, but not both
simultaneously (known as "dual-stack").

This document describes

-  how to configure Clearwater to use IPv6
-  function currently missing on IPv6.

Configuration
-------------

As discussed in the Clearwater `installation
instructions <Installation_Instructions.md>`__, there are several ways
to install Clearwater, and which way you choose affects how you must
configure IPv6.

Manual Install
~~~~~~~~~~~~~~

The process to configure Clearwater for IPv6 is very similar to IPv4.
The key difference is to use IPv6 addresses in the
``/etc/clearwater/local_config`` file rather than IPv4 addresses when
following the `manual install instructions <Manual_Install>`__.

Note also that you must configure your DNS server to return IPv6
addresses (AAAA records) rather than (or as well as) IPv4 addresses (A
records). For more information on this, see the `Clearwater DNS usage
documentation <Clearwater_DNS_Usage.md>`__.

Automated Install
~~~~~~~~~~~~~~~~~

Configuring Clearwater for IPv6 via the `automated install
process <Automated_Install.md>`__ is not yet supported (and Amazon EC2
does not yet support IPv6).

All-in-one Images
~~~~~~~~~~~~~~~~~

Clearwater `all-in-one images <All_in_one_Images.md>`__ support IPv6.

Since all-in-one images get their IP configuration via DHCP, the DHCP
server must be capable of returning IPv6 addresses. Not all
virtualization platforms support this, but we have successfully tested
on OpenStack.

Once the all-in-one image determines it has an IPv6 address, it
automatically configures itself to use it. Note that since Clearwater
does not support dual-stack, all-in-one images default to using their
IPv4 address in preference to their IPv6 address if they have both. To
force IPv6, create an empty ``/etc/clearwater/force_ipv6`` file and
reboot.

Missing Function
----------------

The following function is not yet supported on IPv6.

-  Automated install
-  SIP/WebSockets (WebRTC)

