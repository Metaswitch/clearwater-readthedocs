WebRTC support in Clearwater
============================

Clearwater supports WebRTC clients. This article explains how to do
this, using a common WebRTC client as an example.

**This has been tested using Chrome 26 and some previous versions. It
has not been tested on other browsers. WebRTC is under active
development, so as a result of browser updates clients may not work.**

**Be aware that the sipML5 client can't be logged in to multiple numbers
simultaneously in the same browser.**

Instructions
------------

In the instructions below, <domain> is your Clearwater domain.

-  Configure a line in ellis.
-  Check the camera is not in use: check the camera light is off. If it
   is on, close the app that is using it (e.g., Skype, or a phone
   client).
-  Visit http://sipml5.org/ and click on the button to start the live
   demo. If the website is down, you can also use
   http://doubango.org/sipml5/.
-  By default sipML5 uses a SIP<->WebRTC gateway run by sipml5.org.
   Clearwater supports WebRTC directly. To tell sipML5 to speak WebRTC
   directly to Clearwater:

   -  Click on the "expert mode" button to open the "expert mode" tab,
      and fill in the following field:

      -  WebSocket Server URL: ws://<domain>:5062

   -  Click Save.
   -  Go back to the calls tab.

-  Fill in the fields as follows:

   -  Display name: <whatever you like, e.g., your name>
   -  Private identity: <phone number>@<domain>
   -  Public identity: sip:<phone number>@<domain>
   -  Password: <password as displayed in ellis>
   -  Realm: <domain>

-  Now click Log In. This sometimes takes a few seconds. If it fails
   (e.g., due to firewall behaviour), click Log Out then Log In again.

Some firewalls or proxies may not support WebSockets (the technology
underlying WebRTC). If this is the case, logging in will not work
(probably it will time out). Clearwater uses port 5062 for WebSockets.

Once you have this set up on two tabs, or two browsers, you can make
calls between them as follows:

-  Entering the phone number
-  Press the Call button.
-  Accept the local request to use the camera/mic.
-  Remote browser rings.
-  Accept the remote request to use the camera/mic.
-  Click Answer.
-  Talk.
-  Click Hang up on either end.

Video can be disabled on the 'expert mode' tab.

**Note:** Clearwater does not transcode media between WebRTC and
non-WebRTC clients, so such calls are not possible. Transcoding will be
supported in future.

Known sipML5 bugs
-----------------

At the time of writing, the following sipML5 bugs are known:

-  Calls where one or both ends do not have a webcam do not always
   complete correctly. It is best to ensure both ends have a webcam,
   even if audio-only calls are being made.
-  Hang up doesn't work - you have to hang up on both ends.

Using STUN and TURN
-------------------

**Note:** The above uses a default (non-Clearwater) STUN server, and no
TURN server. Clearwater has its own STUN and TURN servers which can be
used to support clients behind NATs and firewalls, but at the time of
writing (April 2013) there are some difficulties with the WebRTC spec
that make the Clearwater TURN server inaccessible to compliant browsers.
These are being tracked.

If one or both clients are behind a symmetric firewall, you must use
TURN. Configure this as follows:

-  On the 'expert mode' tab, fill in the following field with your SIP
   username and the TURN workaround password set by your administrator
   (``turn_workaround`` in `Installing a Chef
   workstation <Installing_a_Chef_workstation.md>`__). This is a
   workaround for Chrome WebRTC `issue
   1508 <https://code.google.com/p/webrtc/issues/detail?id=1508>`__
   which will be fixed in Chrome 28 (not yet released).

   -  ICE Servers: [{url:"turn:<phone
      number>%40<domain>@<domain>",credential:"<password>"}]

Testing TURN
------------

To test TURN when one or both of the clients are running under Windows
7, find the IP of the remote client, and block direct communication
between them as follows:

-  Control Panel > Windows Firewall > Advanced Settings > Inbound Rules
   > New Rule > Custom > All Programs > Any Protocol > specify remote IP
   address > Block the connection > (give it a name).
-  Do the same for outbound.

