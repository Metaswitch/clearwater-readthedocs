Clearwater Tour
===============

This document is a quick tour of the key features of Clearwater, from a
subscriber's point of view.

Self-service account and line creation
--------------------------------------

In a browser, go to the Account Signup tab at
``http://ellis.<domain>/signup.html`` and supply details as requested:

-  Use whatever name you like.
-  Use a real email address, or the password reset function won't work.
-  The signup code to enter in the final box should have been given to
   you by the deployment administrator.
-  Hit "Sign up".

You are now shown a new account with a phone number (which may take a
second or two to show up).

-  The password for each number is only shown once - it is only stored
   encrypted in the system, for security, so cannot be retrieved by the
   system later. It can be reset by the user if they forget it (see
   button towards the right).

Try adding and deleting extra lines. Lines can have non-routable numbers
for a purely on-net service, or PSTN numbers. Make sure you end up with
just a PSTN number assigned to the account.

Address book: for this system there is a single address book which all
numbers are by default added to - see the checkbox by the line.

Connecting an X-Lite client
---------------------------

Now register for the new PSTN line on your newly created account with
your as yet unregistered X-Lite phone.

-  `Download
   X-Lite <http://www.counterpath.com/x-lite-download.html>`__.
-  Install and start X-Lite
-  Navigate to Softphone / Account Settings
-  Account tab:

   -  Account name: Whatever you like.
   -  User ID: "SIP Username" from the line you're adding
   -  Domain: ``<deployment domain>``, e.g., ``ngv.example.com``
   -  Password: "SIP Password" from the line you're adding
   -  Display name: Whatever you like, or omit
   -  Authorization name: ``<SIP Username>@<domain>`` e.g.
      ``6505550611@ngv.example.com``
   -  "Register with domain and receive calls" should be selected
   -  Send outbound via: Domain

-  Topology tab:

   -  Select "Auto-detect firewall traversal method using ICE
      (recommended)"
   -  Server address: ``<domain>``
   -  User name: ``<SIP Username>@<domain>``
   -  Password: "SIP Password" from the line

-  Transport tab:

   -  Signaling transport: TCP

-  hit "OK"
-  phone should register.

We have now registered for the new line.

Connecting an Android phone
---------------------------

See `here <Configuring_the_native_Android_SIP_client.md>`__ for
instructions.

Making calls
------------

-  Make a call using your new line to a PSTN number (eg your regular
   mobile phone number). Clearwater performs an ENUM lookup to decide
   how to route the call, and rings the number.

-  Make a call using a PSTN number (eg your regular mobile phone) to
   your new line. Use the online global address book in Ellis to find
   the number to call.

-  Make a call between X-Lite and the Android client, optionally using
   the address book.

We've gone from no user account, no line, and no service to a configured
user and working line in five minutes. All of this works without any
on-premise equipment, without dedicated servers in a data centre,
without any admin intervention at all.

Supported dialling formats
~~~~~~~~~~~~~~~~~~~~~~~~~~

A brief note on supported dialing formats:

-  Dialling between devices on the Clearwater system. It is easiest to
   always dial the ten digit number, even when calling a PSTN number.
   Seven digit dialling is not supported, and dialing 1+10D is not
   supported. In theory dialling +1-10D if the destination is a
   Clearwater PSTN number should work, but some clients (eg. X-Lite)
   silently strip out the + before sending the INVITE, so only do this
   if you are absolutely sure your client supports it.

-  Dialling out to the PSTN. You must dial as per the NANP. Calls to US
   numbers can use 10D, 1-10D or +1-10D format as appropriate (the
   latter only if your device supports +), and international calls must
   use the 011 prefix (+ followed by country code does not work). If you
   try to make a call using one of these number formats and it doesn't
   connect, then it almost certainly wouldn't connect if you were
   dialling the same number via the configured SIP trunk directly.

WebRTC support
--------------

See `WebRTC support in Clearwater <WebRTC_support_in_Clearwater.md>`__
for how to use a browser instead of a SIP phone as a client.

VoLTE call services
-------------------

Call barring
~~~~~~~~~~~~

-  From Ellis, press the Configure button on the X-Lite PSTN number,
   this will pop up the services management interface.

-  Select the Barring tab and choose the bars you wish to apply to
   incoming/outgoing calls.

-  Click OK then attempt to call X-Lite from the PSTN, see that the call
   is rejected without the called party being notified of anything.

Call diversion
~~~~~~~~~~~~~~

-  From Ellis, press the Configure button on the X-Lite PSTN number,
   this will pop up the services management interface.

-  Select the Barring tab and turn off barring.

-  Select the Redirect tab, enable call diversion and add a new rule to
   unconditionally divert calls to your Android client if using or your
   chosen call diversion destination if not.

-  Click OK then call X-Lite from the PSTN and see that that number is
   not notified but the diverted-to number is, and can accept the call.

Other features
~~~~~~~~~~~~~~

Clearwater also supports privacy, call hold, and call waiting.
