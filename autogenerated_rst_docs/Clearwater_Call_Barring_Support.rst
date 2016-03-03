Call Barring
============

Clearwater allows users to configure rules for blocking of incoming or
outgoing calls, by implementing the IR.92 version of call barring (which
is itself a cut-down version of the MMTEL call barring service).

The relevant specifications are:

-  `3GPP TS 24.611
   v11.2.0 <http://www.3gpp.org/ftp/Specs/html-info/24611.htm>`__

   -  The full specification

-  `GSMA PRD IR.92, Section
   2.3.9 <http://www.gsma.com/newsroom/wp-content/uploads/2012/06/IR9230.pdf>`__

   -  The required IR.92 subset

Some of the entries in the IR.92 list are not currently applicable for
Clearwater, since Clearwater does not have support for/the concept of
roaming calls. Because of this, the customer may only specify that they
wish to block one of:

-  No outgoing calls
-  All outgoing calls
-  Outgoing calls to international numbers (but see below)

And one of:

-  No incoming calls
-  All incoming calls

International Call detection
----------------------------

The 3GPP specification states that to detect an international number, a
SIP router should discount SIP/SIPS URIs that do not have a
``user=phone`` parameter set on them (this parameter is intended to
distinguish between dialed digits and call-by-name with numeric names)
but X-Lite and other SIP clients never set this parameter. Because of
this behavior, the Clearwater implementation considers all SIP URIs for
international call categorization.

National dialing prefix
-----------------------

Another limitation is that the international call detection algorithm
only checks against a global 'national' dialing prefix (which is fine
unless subscribers are expected to be multi-national within one
Clearwater deployment). There does not appear to be a mechanism in IMS
networks to store a subscriber-specific locale (e.g. in the HSS) so this
would require some smarts to solve. These issues may be addressed in
subsequent development.
