Voxbone
=======

`Voxbone <http://www.voxbone.com/>`__ provides local, geographical,
mobile and toll free phone numbers and converts incoming calls and SMSs
to SIP INVITE and MESSAGE flows.

Clearwater supports these flows, and this document describes how to
configure Voxbone and Clearwater to work together, and then how to test
and troubleshoot.

Configuration
-------------

There are 3 configuration steps.

1. Configure Clearwater's IBCF to trust Voxbone's servers.
2. Create a subscriber on Clearwater.
3. Associate the subscriber with a number on Voxbone.

Configuring IBCF
~~~~~~~~~~~~~~~~

An IBCF (Interconnection Border Control Function) interfaces between the
core network and one or must trusted SIP trunks. We will configure
Voxbone to send all its traffic to the IBCF, but we first need to
configure the IBCF to accept traffic from Voxbone.

Clearwater's bono component acts as an IBCF. To make things simpler
later on, you should configure *all* of your bono nodes to act as IBCFs.

The IP addresses you need to specify as trusted peers are

-  all the `Voxbone signaling IP
   addresses <http://www.voxbone.com/network-ipaddressesranges.jsf>`__ -
   as of writing, these are

   -  81.201.82.45
   -  81.201.84.195
   -  81.201.83.45
   -  81.201.86.45
   -  81.201.85.45

-  the `Voxbone SMS IP
   addresses <https://www.voxbone.com/members/faq-voxsms.jsf#faq-voxsms09>`__
   - as of writing, these are

   -  81.201.82.10
   -  81.201.82.11
   -  81.201.82.12.

The process for configuring trusted peers is described as part of `the
IBCF documentation <IBCF.md#install-and-configure-an-ibcf>`__.

If you don't want to configure all your bono nodes as IBCF nodes, you
can do so, but will need to take extra steps when configuring Voxbone to
ensure that calls are routed to the correct node.

Creating a subscriber
~~~~~~~~~~~~~~~~~~~~~

Creating a subscriber for Voxbone use is done exactly `as you would
normally do
so <Making_your_first_call.md#create-a-number-for-your-client>`__.

Associating the subscriber on Voxbone
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For each telephone number you own, Voxbone allows you to configure a SIP
URI to which incoming calls will be sent.

-  If, as recommended earlier, all your bono nodes are configured as
   IBCFs, you can simply use the SIP URI of the subscriber you created
   above.

-  If only one (or a subset) of your bono nodes are configured as IBCFs,
   you must ensure that calls are routed to this node by replacing the
   domain name of the SIP URI with the IP address or domain name of the
   IBCF node. For example, if your SIP URI was
   ``1234567890@example.com`` but your IBCF node was ``1.2.3.4``, you
   must use ``1234567890@1.2.3.4``.

If you are also using the VoxSMS service for receiving SMSes, you
additionally need to configure a VoxSMS SIP URI using the same SIP URI
as above.

Testing
-------

The Voxbone web UI allows you to make a test call. Alternatively, you
can make a normal call through the PSTN to your Voxbone number.

The only way to test SMS function is to actually send an SMS to your
Voxbone number.

Troubleshooting
---------------

If your call or SMS doesn't get through, there are three things to
check.

-  Does the SIP message actually reach the IBCF? You can check this
   using network capture (e.g. ``tcpdump``) on the IBCF? If not, the
   problem is likely to either be that the SIP URI's domain doesn't
   resolve to your IBCF, or that security groups or firewall rules are
   blocking traffic to it.

-  Is the SIP message trusted? You can again check this with network
   capture - if you see a ``403 Forbidden`` response, this indicates
   that the IBCF does not trust the sender of the message. Check the
   ``trusted_peers`` entry in your ``/etc/clearwater/user_settings``
   file and that you have restarted bono since updating it.

-  Would the call go through if it were sent on-net? Try making a call
   to the subscriber from another subscriber on Clearwater and check
   that it goes through (or follow the `standard troubleshooting
   process <Troubleshooting_and_Recovery.md>`__).


