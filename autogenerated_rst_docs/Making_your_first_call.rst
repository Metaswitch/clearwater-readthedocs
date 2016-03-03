Making calls through Clearwater
===============================

These instructions will take you through the process of making a call on
a Clearwater deployment.

Prerequisites
-------------

-  You've `installed Clearwater <Installation_Instructions.md>`__
-  You have access to two SIP clients.
-  If you have installed Clearwater on VirtualBox using the All-In-One
   image you must use `Zoiper <http://www.zoiper.com/en>`__ as one of
   your clients. For the other client (or for other install modes) you
   may use any standard SIP client, we've tested with the following:

   -  `X-Lite <http://www.counterpath.com/x-lite.html>`__
   -  `Bria <http://www.counterpath.com/bria.html‎>`__
   -  `Jitsi <https://jitsi.org/>`__
   -  `Blink <http://icanblink.com/>`__
   -  `Stock Android SIP
      client <Configuring_the_native_Android_SIP_client.md>`__
   -  `Zoiper Android/iOS SIP
      client <Configuring_Zoiper_Android_iOS_Client.md>`__
   -  Media5-fone iOS SIP client (on iPhone 4 and 4S)

-  You have access to a web-browser. We've tested with:
-  Google Chrome

Work out your base domain
-------------------------

If you installed Clearwater manually, your base DNS name will simply be
``<zone>``. If you installed using the automated install process, your
base DNS name will be ``<name>.<zone>``. If you installed an All-in-One
node, your base name will be ``example.com``.

For the rest of these instructions, the base DNS name will be referred
to as ``<domain>``.

Work out your All-in-One node's identity
----------------------------------------

This step is only required if you installed an All-in-One node, either
from an AMI or an OVF. If you installed manually or using the automated
install process, just move on to the next step.

If you installed an All-in-One node from an Amazon AMI, you need the
public DNS name that EC2 has assigned to your node. This will look
something like ``ec2-12-34-56-78.compute-1.amazonaws.com`` and can be
found on the EC2 Dashboard on the "instances" panel.

If you installed an All-in-One node from an OVF image in VMPlayer or
VMWare, you need the IP address that was assigned to the node via DHCP.
You can find this out by logging into the node's console and typing
``hostname -I``.

If you installed an All-in-One node from an OVF in VirtualBox, you
simply need ``localhost``.

For the rest of these instructions, the All-in-One node's identity will
be referred to as ``<aio-identity>``.

Work out your Ellis URL
-----------------------

If you installed Clearwater manually or using the automated install
process, your Ellis URL will simply be ``http://ellis.<domain>``. If you
installed an All-in-One node, your Ellis URL will be
``http://<aio-identity>``.

Create a number for your client
-------------------------------

In your browser, navigate to the Ellis URL you worked out above.

Sign up as a new user, using the signup code you set as ``signup_key``
when `configuring your
deployment <Installing_a_Chef_workstation.md#add-deployment-specific-configuration>`__.

Ellis will automatically allocate you a new number and display its
password to you. Remember this password as it will only be displayed
once. From now on, we will use ``<username>`` to refer to the SIP
username (e.g. ``6505551234``) and ``<password>`` to refer to the
password.

Configure your client
---------------------

Client configuration methods vary by client, but the following
information should be sufficient to allow your client to register with
Clearwater.

-  SIP Username: ``<username>``
-  SIP Password: ``<password>``
-  SIP Domain: ``<domain>``
-  Authorization Name: ``<username>@<domain>``
-  Transport: ``TCP``
-  STUN/TURN/ICE:
-  Enabled: ``true``
-  Server: ``<domain>`` (or ``<aio-identity>`` on an All-in-One node)
-  Username: ``<username>@<domain>``
-  Password: ``<password>``

*Extra configuration to use an All-in-One node*

If you are using an All-in-One node, you will also need to configure an
outbound proxy at your client.

-  Outbound Proxy address: ``<aio-identity>``
-  Port: 5060 (or 8060 if installed in VirtualBox)

Once these settings have been applied, your client will register with
Clearwater. Note that X-Lite may need to be restarted before it will set
up a STUN connection.

Configure a second number and client
------------------------------------

Create a new number in Ellis, either by creating a new Ellis user, or by
clicking the ``Add Number`` button in the Ellis UI to add one for the
existing user.

Configure a second SIP client with the new number's credentials as
above.

Make the call
-------------

From one client (Zoiper if running an All-in-One node in VirtualBox),
dial the ``<username>`` of the other client to make the call. Answer the
call and check you have two-way media.

Next steps
----------

Now that you've got a basic call working, check that all the features of
your deployment are working by running the `live
tests <Running_the_live_tests.md>`__ or `explore
Clearwater <Exploring_Clearwater.md>`__ to see what else Clearwater
offers.
