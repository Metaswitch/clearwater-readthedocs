Privacy
=======

The Clearwater privacy feature splits into two sections, configuration
and application. For configuration, we've been working from a
combination of `3GPP TS
24.623 <http://www.arib.or.jp/IMT-2000/V730Jul09/5_Appendix/Rel8/24/24623-810.pdf>`__
and `ETSI TS
129.364 <http://www.etsi.org/deliver/etsi_ts/129300_129399/129364/08.00.00_60/ts_129364v080000p.pdf>`__,
which define the XDM documents that store the MMTel services
configuration (currently only OIR,
originating-identity-presentation-restriction, is supported). For
application, we've used 3GPP TS
24.607\ ` <http://www.quintillion.co.jp/3GPP/Specs/24607-910.pdf>`__
which defines the roles of the originating UE, originating AS,
terminating AS and terminating UE. This document is supplemented by
`RFC3323 <http://www.ietf.org/rfc/rfc3323.txt>`__ and
`RFC3325 <http://www.ietf.org/rfc/rfc3325.txt>`__.

For configuration, there's also a communication with Homestead to
determine whether MMTel services should be applied for a call. This uses
a proprietary (JSON) interface based on the inbound filter criteria
definitions.

Configuration
-------------

User-specified configuration is held and validated by the XDM. When a
subscriber is provisioned, Ellis injects a default document into the XDM
for that user, this document turns off OIR by default. After this, if
the user wishes to change their call services configuration, they use
the XCAP interface (Ut) to change their document.

If the user has turned on Privacy by default, then all calls originating
from the user will have identifying headers (e.g. ``User-Agent``,
``Organization``, ``Server``...) stripped out from the originating
request and will have the ``From:`` header re-written as
``"Anonymous" <sip:anonymous@anonymous.invalid\>;tag=xxxxxxx``,
preventing the callee from working out who the caller is. With the
current implementation, there are some headers that are left in the
message that could be used to determine some information about the
caller, see below.

Application
-----------

Originating UE
^^^^^^^^^^^^^^

The originating UE is responsible for adding any per-call Privacy
headers (overriding the stored privacy configuration) if required and
hiding some identifying information (e.g. ``From:`` header).

Application Server
^^^^^^^^^^^^^^^^^^

When receiving a dialog-creating request from an endpoint, Sprout will
ask Homestead which application servers should be used and will parse
the returned iFC configuration. If the configuration indicates that
MMTEL services should be applied, Sprout will continue to act as an
originating and terminating application server on the call as it passes
through.

Once Homestead has indicated that MMTel services should be applied for
the call, Sprout will query the XDM to determine the user's specific
configuration.

Originating Application Server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When acting as an originating AS, the above 3GPP spec states that we
should do the following:

*For an originating user that subscribes to the OIR service in
"temporary mode" with default "restricted", if the request does not
include a Privacy header field, or the request includes a Privacy header
field that is not set to "none", the AS shall insert a Privacy header
field set to "id" or "header" based on the subscription option.
Additionally based on operator policy, the AS shall either modify the
From header field to remove the identification information, or add a
Privacy header field set to "user".*

*For an originating user that subscribes to the OIR service in
"temporary mode" with default "not restricted", if the request includes
a Privacy header field is set to "id" or "header", based on operator
policy, the AS shall either, may modify the From header field to remove
the identification information or add a Privacy header field set to
"user".*

Our implementation of Sprout satisfies the above by injecting the
applicable Privacy headers (i.e. it never actually applies privacy at
this point, only indicates that privacy should be applied later).

Terminating Application Server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When acting as a terminating AS, the 3GPP spec states that we should do
the following:

*If the request includes the Privacy header field set to "header" the AS
shall:*

*a) anonymize the contents of all headers containing private information
in accordance with IETF RFC 3323 [6] and IETF RFC 3325 [7]; and*

*b) add a Privacy header field with the priv-value set to "id" if not
already present in the request.*

*If the request includes the Privacy header field set to "user" the AS
shall remove or anonymize the contents of all "user configurable"
headers in accordance with IETF RFC 3323 [6] and IETF RFC 3325 [7]. In
the latter case, the AS may need to act as transparent back-to-back user
agent as described in IETF RFC 3323 [6].*

Our implementation of Sprout satisfies these requirements but does it by
not fully satisfying the SHOULD clauses of the linked RFCs. In
particular:

-  'header' privacy

   -  We do not perform "Via-Stripping" since we use the Via headers for
      subsequent call routing and don't want to have to hold a
      via-header mapping in state.
   -  Similarly we don't perform "Record-Route stripping" or
      "Contact-stripping".

-  'session' privacy

   -  This is not supported so if the privacy is marked as critical, we
      will reject the call.

-  'user' privacy

   -  We modify the To: header inline here (and do not cache the
      original value) we're assuming that the endpoints are robust
      enough to continue correlating the call based on the tags
   -  We do not anonymize the call-id (for the same reason as the
      Via-stripping above).

-  'id' privacy

   -  This is fully supported.

-  'none' privacy

   -  This is fully supported.

Terminating UE
^^^^^^^^^^^^^^

The terminating UE may use the presence of Privacy headers to determine
if privacy has been applied by OIR or by the originating endpoint
(though this doesn't seem to be very useful information...). It may also
look at the P-Asserted-Identity header to determine the true identity of
the caller (rather than some local ID).

Dialog-Wide Issues
------------------

There are a few issues with our stateless model and privacy that are
worth drawing out here, pending a fuller discussion.

-  We only apply OIR processing and privacy obfuscation to originating
   requests (i.e. not on in-dialog requests or responses)
-  We cannot apply Contact/Via/RR-stripping since to do so would require
   us to restore the headers on not just the response but also on all
   callee in-dialog requests.
-  Similarly for Call-Id obfuscation.
-  Stripping Contact/Via/RR would prevent features such as callee call
   push from working (since they require the callee to send a REFER that
   identifies the caller).

