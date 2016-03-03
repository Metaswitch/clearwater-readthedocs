Call Diversion
==============

Clearwater allows users to define rules for handling of incoming calls,
by implementing a superset of the IR.92 version of call diversion (which
is itself a cut-down version of the MMTEL call diversion service).

The relevant specifications are

-  `3GPP TS
   24.604 <http://www.etsi.org/deliver/etsi_ts/124600_124699/124604/11.04.00_60/ts_124604v110400p.pdf>`__

   -  the full specification

-  `GSMA PRD
   IR.92 <http://www.gsma.com/newsroom/wp-content/uploads/2013/04/IR.92-v7.0.pdf>`__,
   section 2.3.8

   -  the required subset.

We have implemented all of IR.92 section 2.3.8. We have implemented all
of 3GPP TS 24.604 with the following exceptions.

-  CDIV Notification (notifying the diverting party when a call has been
   diverted) is not supported
-  We only support the default subscription options from table 4.3.1.1
   (most notably, no privacy options).
-  We only support hard-coded values for network provider options from
   table 4.3.1.2, as follows.

   -  We stop ringing the diverting party before/simultaneously with
      trying the diverted-to target (rather than waiting for them to
      start ringing).

      -  Served user communication retention on invocation of diversion
         (forwarding or deflection) = Clear communication to the served
         user on invocation of call diversion
      -  Served user communication retention when diverting is rejected
         at diverted-to user = No action at the diverting user

   -  We don't support CDIV Notification (as above).

      -  Subscription option is provided for "served user received
         reminder indication on outgoing communication that CDIV is
         currently activated" = No
      -  CDIV Indication Timer = irrelevant
      -  CDIVN Buffer Timer = irrelevant

   -  We support up to 5 diversions and then reject the call.

      -  Total number of call diversions for each communication = 5
      -  AS behavior when the maximum number of diversions for a
         communication is reached = Reject the communication

   -  The default no-reply timer before Communication Forwarding on no
      Reply occurs is hard-coded to 20s. This is still overridable on a
      per-subscriber basis.

      -  Communication forwarding on no reply timer = 36s

-  Obviously, the interactions with services that we haven't implemented
   yet have not been implemented! In particular, we haven't implemented
   any interactions with terminating privacy.
-  We've ignored the comment in section 4.2.1.1 which says "It should be
   possible that a user has the option to restrict receiving
   communications that are forwarded" but doesn't provide any function
   for this.

Note that we *have* implemented support for Communication Deflection (in
which the callee sends a 302 response and this triggers forwarding)
despite it not being required by IR.92.
