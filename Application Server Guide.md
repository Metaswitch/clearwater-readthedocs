Application Server Guide
========================

You can add new call features or functionality to calls by adding an
application server.  Clearwater supports application servers through
the standard IMS interface ISC. This article explains the
features and limitations of this support. See [Configuring an
Application Server](Configuring an Application Server) for details of
how to configure Clearwater to use this function.

What is an application server?
==============================

An application server (AS) is a server which is brought into or
notified of a call by the network in order to provide call features or
other behaviour.

In IMS, an application server is a SIP entity which is invoked by the
S-CSCF for each dialog, both originating and terminating, as
configured by the initial filter criteria (iFCs) of the relevant
subscribers. The application server may reject or accept the call
itself, redirect it, pass it back to the S-CSCF as a proxy, originate
new calls, or perform more complex actions (such as forking) as a
B2BUA. It may choose to remain in the signalling path, or drop out.

The application server communicates with the IMS core via the ISC
interface. This is a SIP interface. The details are given in [3GPP TS
24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm), especially
s5.4 (the S-CSCF side) and s5.7 (the AS side). Further useful
information can be found in [3GPP TS
23.228](http://www.3gpp.org/ftp/Specs/html-info/23228.htm). Section
references below are to 3GPP TS 24.229 unless otherwise specified.

Clearwater interfaces
=====================

**This section describes the goal, not the current state of Clearwater. See [below](#current-limitations) for the current limitations.**

In Clearwater most S-CSCF function, including the ISC interface, is
implemented in Sprout. Sprout invokes application servers over the ISC
interface, as specified in the iFCs.

 * Per the IMS specs, this invocation occurs on dialog-initiating requests such as INVITE, SUBSCRIBE, MESSAGE, etc, and according to the triggers within the iFCs (s5.4.3.2, s5.4.3.3):
   * When specified, Sprout will route the message to the AS; the AS can either route it onward, act as a B2BUA for e.g. call diversion, or give a final response. Handling of dead ASs (408, 5xx, or no response, not preceded by a 1xx response) follows the spec: per the iFC, either the response is treated as final or the AS is bypassed. Clearwater does not attempt to avoid dead ASs on subsequent calls.
   * Clearwater has full support for chained iFCs. The original dialog is tracked by Sprout using an ODI token in the Route header.
   * Service trigger points (i.e., conditions) are implemented, but the only conditions allowed are SIP method and service case. Conditions based on SIP headers, SDP lines, registration parameters, and request URIs are not implemented - they will always evaluate to false.
 * No per-AS configuration is required; ASs are invoked simply by their URI appearing in the iFCs.
 * AS invocation also occurs on REGISTER - this is called third-party registration (3GPP TS 24.229 s5.4.1.7 and 7A):
   * When a UE registers with Sprout, if the iFCs require it, it passes a third-party registration onto an AS.
   * Message body handling for third-party registration, per 3GPP TS 24.229 s5.4.1.7A: including optionally service info, a copy of the registration, and a copy of the response.
   * Network-initiated deregister. If the third-party registration fails and the iFC requests it, we must deregister the UE.

Supported SIP headers
---------------------

The following SIP headers are supported on the ISC interface:

 * All standard RFC3261 headers and relevant flows, including `To`, `From`, `Route`, `Contact`, etc. Also `Privacy` (per RFC3323) and `Path` (per RFC3327).
 * `P-Asserted-Identity` - bare minimal support only: we set it to the same value as `From:` on the outbound ISC interface, and never strip it. Full support will be added in future phases. This header is needed by originating ASs, particularly in cases where privacy is requested (see RFC3325). Full support would involve setting it in P-CSCF (bono), and ensuring it is set/stripped in the right places. The proposed minimal support has the limitation that ASs which don't understand `P-Served-User` won't work correctly when privacy is invoked. See 3GPP TS 24.229 s5.7.1.3A.
 * `P-Served-User`. This is needed for proper support of AS chains, to avoid service-interaction tangles. It is set by Sprout and set/stripped in the appropriate places.

Limitations
-----------

 * Trust:
   - Some ISC signaling is trust-dependent. For Clearwater, all ASs are trusted - we think support for untrusted ASs is unlikely to be required.
 * Change of request URI:
   - 3GPP TS 24.229 s5.4.3.3 step 3 allows a terminating AS to change the request URI to another URI that matches it (i.e., is canonically equal or an alias) without interrupting the interpretation of the iFCs.
   - Clearwater only supports this for URIs which are canonically equal; it does not support changing to an alias URI (i.e., a different public identity belonging to the same alias group of the same private identity, per 3GPP TS 24.229 s3.1, 3GPP TS 29.228 sB.2.1).
 * `Request-Disposition: no-fork` (3GPP TS 24.229 s5.4.3.3 step 10, s5.7.3, RFC 3841)
   - Clearwater ignores this directive - it always INVITEs all registered endpoints.

Current limitations
-------------------

**The initial (May 2013) release of Clearwater has only a partial implementation of the ISC interface. The specific additional limitations of this partial implementation are as follows:**

 * Initial filter criteria (iFCs):
   - Clearwater currently supports iFCs with zero or one criteria only. Any subsequent criteria may be ignored. It does not support AS chains.
   - Clearwater currently ignores the conditions of each iFC; instead it invokes the named application server if and only if the method is INVITE.
 * Dead AS handling is not currently implemented.
 * AS invocation on REGISTER and deregister is not currently implemented.
 * Headers:
   - Clearwater does not currently set `P-Asserted-Identity` or `P-Served-User`.
 * UDP:
   - Clearwater currently supports UDP access only for application servers.
   - Clearwater currently inserts itself into the signalling path (`Record-Route`) on either side of an external AS. This is forced by the UDP limitation.

Future phases
-------------

The following features may be implemented by Clearwater in future phases:

 * Registration event package 3GPP TS 24.229 s5.4.2.1.1/2. Required in order to get full registration information to the AS (because third-party registration is a tiny subset).
 * Billing: both billing headers within ISC, and AS communicating with the billing system via Rf/Ro.
 * `P-Access-Network-Info`: should be passed (from the UE) and stripped in the appropriate places, and possibly set by bono.
 * `History-Info` draft-ietf-sipcore-rfc4244bis (not RFC4244, which is inaccurate wrt real implementations).
 * `user=dialstring` handling (RFC4967). The specs (3GPP TS 24.229 s5.4.3.2, esp step 10) are quite clear that this is handed off to an AS or handled in a deployment-specific way, as for various other URI formats, so there is nothing to do here.
 * `P-Asserted-Service` / `P-Preferred-Service` (RFC6050, TS 23.228 s4.13), i.e., IMS Communication Services and ICSIs.
 * IMS debug package, IMS logging.
 * Full support for ISC service trigger point conditions: conditions on SIP headers, SDP lines, registration parameters, and request URIs.
 * Support for untrusted ASs.
 * Support for terminating ASs changing to an alias URI.
 * Support for `Request-Disposition: no-fork`, which should pick a single endpoint to INVITE.

Exclusions
----------

Clearwater implements the ISC interface only. An AS may also expect to communicate over several other interfaces:

 * AS interrogates HSS over Sh. If the AS requires this it can access the HSS directly, bypassing Clearwater's Homestead cache. It is not supported in deployments without an HSS.
 * AS interrogates SRF over Dh. Typical Clearwater deployments do not include an SRF.
 * UE retrieves and edits AS configuration via Ut. An AS is free to provide this or any other configuration interface it chooses. Homer does not provide a generic Ut interface for ASs to store configuration information.

The built-in MMTEL application server
=====================================

Clearwater has a built-in application server,
`mmtel.<deployment-domain>`, which implements a subset of the MMTEL
services defined in [GSMA PRD
IR.92](http://www.gsma.com/newsroom/wp-content/uploads/2012/03/ir9250.pdf),
[ETSI TS
129.364](http://webapp.etsi.org/workprogram/Report_WorkItem.asp?WKI_ID=42062)
and [3GPP TS
24.623](http://www.3gpp.org/ftp/Specs/html-info/24623.htm):

 * Originating Identification Presentation (OIP)
 * Originating Identification Restriction (OIR)
 * Communication Diversion (CDIV)
 * Communication Barring (CB)

The built-in MMTEL application server is invoked only for calls
configured to use it. To use it, simply configure a subscriber's iFCs
to indicate the use of `mmtel.<deployment-domain>` as an application
server. The MMTEL application server can be used on its own, or as one
of a chain of application servers handling a call.  The default iFCs
configured by Ellis specify that the built-in MMTEL application server
should be used for all originating and terminating calls.
