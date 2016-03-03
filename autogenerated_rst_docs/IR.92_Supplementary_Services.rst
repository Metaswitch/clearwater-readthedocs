IR.92 Supplementary Services
============================

`GSMA
IR.92 <http://www.gsma.com/newsroom/wp-content/uploads/2013/04/IR.92-v7.0.pdf>`__
defines a set of Supplementary Services (section 2.3). This document
describes Clearwater's support for each.

The services fall into one of four categories.

-  Supported by Clearwater's `built-in MMTel application
   server <Application_Server_Guide.md#the-built-in-mmtel-application-server>`__
-  Supported by Clearwater inherently (i.e. whether or not the MMTel
   application server is enabled) - these services rely on messages or
   headers that Clearwater simply passes through
-  Requiring an external application server
-  Not supported

Supported by Clearwater's Built-In MMTel Application Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following Supplementary Services are supported by Clearwater's
`built-in MMTel Application
Server <Application_Server_Guide.md#the-built-in-mmtel-application-server>`__.

-  Originating Identification Presentation - See the `Privacy Feature
   document <Clearwater_Privacy_Feature.md>`__ for more information.
-  Originating Identification Restriction - See the `Privacy Feature
   document <Clearwater_Privacy_Feature.md>`__ for more information.
-  Call Forwarding Unconditional - See the `Call Diversion Support
   document <Clearwater_Call_Diversion_Support.md>`__ for more
   information.
-  Call Forwarding on not Logged in - See the `Call Diversion Support
   document <Clearwater_Call_Diversion_Support.md>`__ for more
   information.
-  Call Forwarding on Busy - See the `Call Diversion Support
   document <Clearwater_Call_Diversion_Support.md>`__ for more
   information.
-  Call Forwarding on not Reachable - See the `Call Diversion Support
   document <Clearwater_Call_Diversion_Support.md>`__ for more
   information.
-  Call Forwarding on No Reply - See the `Call Diversion Support
   document <Clearwater_Call_Diversion_Support.md>`__ for more
   information.
-  Barring of All Incoming Calls - See the `Call Barring Support
   document <Clearwater_Call_Barring_Support.md>`__ for more
   information.
-  Barring of All Outgoing Calls - See the `Call Barring Support
   document <Clearwater_Call_Barring_Support.md>`__ for more
   information.
-  Barring of Outgoing International Calls - See the `Call Barring
   Support document <Clearwater_Call_Barring_Support.md>`__ for more
   information.

Supported by Clearwater Inherently
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following Supplementary Services are primarily implemented on the
UE, and just require Clearwater to proxy messages and headers, which it
does.

-  Communication Hold
-  Communication Waiting

Requiring an External Application Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following Supplementary Services require an external application
server.

-  Terminating Identification Presentation
-  Terminating Identification Restriction
-  Barring of Outgoing International Calls - ex Home Country -
   Clearwater does not currently have sufficient configuration to know
   the subscriber's home country.
-  Message Waiting Indication - Clearwater proxies SUBSCRIBE and NOTIFY
   messages for the MWI event package (`RFC
   3842 <http://tools.ietf.org/rfc/rfc3842.txt>`__), but requires an
   external application server to handle/generate them.
-  Ad-Hoc Multi Party Conference - Clearwater proxies messages between
   the UE and an external application server that conferences sessions
   together.

Not Supported
~~~~~~~~~~~~~

The following Supplementary Service is not currently supported by
Clearwater.

-  Barring of Incoming Calls - When Roaming - Clearwater does not
   currently support roaming, and so can't support barring on this
   basis.

