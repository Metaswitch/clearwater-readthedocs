# SIP Interface Specifications

This document is a review of all the SIP related RFCs referenced by IMS (in particular [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm) [Rel 10](http://www.etsi.org/deliver/etsi_ts/124200_124299/124229/10.10.00_60/ts_124229v101000p.pdf)), particularly how they relate to Clearwater's SIP support.  The bulk of the document goes through the RFCs grouped in the following 4 categories.

*   RFCs already supported by Clearwater (at least sufficient for IMS compliance for Clearwater as a combined P/I/S-CSCF/BGCF/IBCF).
*   RFCs that are relevant to Clearwater but not currently supported.
*   RFCs relevant to media processing, which Clearwater doesn't currently need to handle as it is not involved in the media path.
*   RFCs that are not relevant to Clearwater.

## Supported

The following RFCs are already supported by Clearwater.  Note that a number of these are supported simply because they require no active function from SIP proxies other than forwarding headers unchanged.

### Basic SIP ([RFC 3261](http://www.ietf.org/rfc/rfc3261.txt))

*   This covers the basic SIP protocol including
    *   the 6 basic methods (ACK, BYE, CANCEL, INVITE, OPTIONS and REGISTER)
    *   the 44 basic headers
    *   the transaction and dialog state machines
    *   the function of UACs, UASs, stateful and stateless proxies, and registrars
    *   basic and digest security
    *   transport over UDP and TCP.
*   Clearwater supports this RFC.

### SUBSCRIBE/NOTIFY/PUBLISH messages ([RFC 3265](http://www.ietf.org/rfc/rfc3265.txt) and [RFC 3903](http://www.ietf.org/rfc/rfc3903.txt))

*   These two RFCs define a framework for generating and distributing event notifications in a SIP network.  They cover the SUBSCRIBE and NOTIFY methods and Allow-Events and Event headers ([RFC 3265](http://www.ietf.org/rfc/rfc3265.txt)) and the PUBLISH method and SIP-Etag and SIP-If-Match headers ([RFC 3903](http://www.ietf.org/rfc/rfc3903.txt)).
*   Routing of these messages is largely transparent to proxies, so is largely already supported by proxy function in Clearwater.

### UPDATE method ([RFC 3311](http://www.ietf.org/rfc/rfc3311.txt))

*   Defines UPDATE method used to update session parameters (so can be used as an alternative to reINVITE as a keepalive, for media renegotiation or to signal successful resource reservation).  Often used by ICE enabled endpoints to change media path once ICE probing phase has completed.
*   Supported transparently by Clearwater.

### Privacy header ([RFC 3323](http://www.ietf.org/rfc/rfc3323.txt))

*   Required for privacy service.
*   Clearwater supports this header.

### P-Asserted-Identity and P-Preferred-Identity headers ([RFC 3325](http://www.ietf.org/rfc/rfc3325.txt))

*   Defines headers that allow a UE to select which identity it wants to use on a call-by-call basis.  Ties in with authentication and the P-Associated-URIs header defined in [RFC 3455](http://www.ietf.org/rfc/rfc3455.txt) (see below).
*   Clearwater supports these headers.

### Path header ([RFC 3327](http://www.ietf.org/rfc/rfc3327.txt))

*   Defines handling of registrations from devices which are not adjacent (in SIP routing terms) to the registrar.
*   Supported by Clearwater.

### message/sipfrag MIME type ([RFC 3420](http://www.ietf.org/rfc/rfc3420.txt))

*   [RFC 3420](http://www.ietf.org/rfc/rfc3420.txt) defines an encoding for transporting MIME or S/MIME encoded SIP message fragments in the body of a SIP message.  Use cases for this include status NOTIFYs sent during REFER processing which signal the status of the referral to the referee.
*   Support for this is mandatory according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm), but it does not describe any particular use cases.
*   Transparent to proxy components, so supported by Clearwater.

### P-Access-Network-Info, P-Associated-URI, P-Called-Party-ID, P-Charging-Function-Address, P-Charging-Vector and P-Visited-Network-ID headers ([RFC 3455](http://www.ietf.org/rfc/rfc3455.txt))

*   Defines various private headers specifically for IMS.
*   P-Access-Network-Info is added to incoming messages by the UE or the P-CSCF to provide information about the access network and possibly the UEs location within the network (for example cell).  IMS specifications talk about various uses for this information, including routing emergency calls, an alternative to `phone-context` for interpreting dialled digits, determining the security scheme.  This header is supported by Clearwater.
*   P-Associated-URI is returned by registrar to include the list of alternative user identities defined for the IMS subscription.  This header is supported by Clearwater.
*   P-Called-Party-ID is added to a SIP request by an IMS network to ensure the called UE knows which of the user identities within the IMS subscription was actually called.  This header is supported by Clearwater.
*   P-Charging-Function-Address and P-Charging-Vector headers are related to billing, and are supported by Clearwater.
*   P-Visited-Network-ID is used when roaming to identify the network the user has roamed to. The specs say it is a free-form string, and should be used to check that there is a roaming agreement in place. This header is supported by Clearwater.

### Symmetric SIP response routing ([RFC 3581](http://www.ietf.org/rfc/rfc3581.txt))

*   Defines how SIP responses should be routed to ensure they traverse NAT pinholes.
*   Mandatory for IMS proxy components.
*   Supported by Clearwater nodes.

### Call transfer, multiparty call control (REFER method and related headers) ([RFC 3515](http://www.ietf.org/rfc/rfc3515.txt), [RFC 3891](http://www.ietf.org/rfc/rfc3891.txt), [RFC 3892](http://www.ietf.org/rfc/rfc3892.txt), [RFC 3911](http://www.ietf.org/rfc/rfc3911.txt))

*   Covers REFER method, Refer-To header and event packages for transferring referral state ([RFC 3515](http://www.ietf.org/rfc/rfc3515.txt)), Replaces header ([RFC 3891](http://www.ietf.org/rfc/rfc3891.txt)), Referred-By header ([RFC 3892](http://www.ietf.org/rfc/rfc3892.txt)), Join header ([RFC 3911](http://www.ietf.org/rfc/rfc3911.txt)), Refer-Sub header ([RFC 4488](http://www.ietf.org/rfc/rfc4488.txt)), and the Target-Dialog header ([RFC 4538](http://www.ietf.org/rfc/rfc4538.txt)).
*   Transparent to proxies, so supported by Clearwater - although needs support for GRUUs (see below) to work in all use cases.

### Service-Route header ([RFC 3608](http://www.ietf.org/rfc/rfc3608.txt))

*   In IMS an S-CSCF includes Service-Route header on REGISTER responses, so UE can use to construct Route headers to ensure subsequent requests get to the appropriate S-CSCF.
*   Optional according to TS 24.229(http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   This header is supported by Clearwater.

### ENUM ([RFC 3761](http://www.ietf.org/rfc/rfc3761.txt) and [RFC 4769](http://www.ietf.org/rfc/rfc4769.txt))

*   Defines a mechanism for using DNS look-ups to translate telephone numbers into SIP URIs. ([RFC 3761](http://www.ietf.org/rfc/rfc3761.txt) defines ENUM, [RFC 4769](http://www.ietf.org/rfc/rfc4769.txt) contains IANA registrations for ENUM data.)
*   IMS specifies that ENUM is one mechanisms an S-CSCF can use to translate non-routeable URIs (either Tel URIs or SIP URIs encoding a phone number) into a globally routeable URI (one where the domain name/IP address portion of the URI can safely be used to route the message towards its destination).
*   Clearwater supports this through function in Sprout.

### Event package for MWI ([RFC 3842](http://www.ietf.org/rfc/rfc3842.txt))

*   Defines an event package for notifying UAs of message waiting.
*   Required for UEs and ASs implementing MWI services, transparent to proxy components.
*   Transparent to proxies, so already supported by Clearwater.

### Presence event package ([RFC 3856](http://www.ietf.org/rfc/rfc3856.txt))

*   Defines an event package for monitoring user presence.
*   Required for UEs supporting presence and presence servers.
*   Transparent to proxies, so supported by Clearwater.

### Watcher event template package ([RFC 3857](http://www.ietf.org/rfc/rfc3857.txt))

*   Defines an event package that can be used to subscribe to the list of watchers for another event type.
*   IMS mandates support for this package for subscribing to the list of watchers of a particular presentity, so support is only applicable for SIP UEs supporting presence and presence application servers.
*   Transparent to proxies, so supported by Clearwater.

### Session-expiry ([RFC 4028](http://www.ietf.org/rfc/rfc4028.txt))

*   Covers periodic reINVITE or UPDATE messages used to allow UEs or call stateful proxies to detect when sessions have ended.  Includes Min-SE and Session-Expires headers, which are used to negotiate the frequency of keepalives.
*   Currently supported transparently by Clearwater.  Neither is call stateful, so neither monitors the messages or participates actively in the negotiation.
*   Optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm), so would only need to implement active support if we have a functional need (for example, if in future Clearwater needed some form of dialog tracking in Bono for privacy or quiescing support).

### Early session disposition type ([RFC 3959](http://www.ietf.org/rfc/rfc3959.txt))

*   Defines a new value for the Content-Disposition header to indicate when SDP negotiation applies to early media.
*   Optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   Transparent to proxies so supported by Clearwater.

### Dialog events ([RFC 4235](http://www.ietf.org/rfc/rfc4235.txt))

*   Event package for dialog state.
*   In [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm) only seems to be relevant to E-CSCF and LRF functions.
*   Transparent to proxies, so supported by Clearwater.

### MRFC control ([RFC 4240](http://www.ietf.org/rfc/rfc4240.txt), [RFC 5552](http://www.ietf.org/rfc/rfc5552.txt), [RFC 6230](http://www.ietf.org/rfc/rfc6230.txt), [RFC 6231](http://www.ietf.org/rfc/rfc6231.txt), [RFC 6505](http://www.ietf.org/rfc/rfc6505.txt))

*   These RFCs define three different ways of controlling the function of an MRFC from an AS. [RFC 4240](http://www.ietf.org/rfc/rfc4240.txt) is a simple "play an announcement" service, [RFC 5552](http://www.ietf.org/rfc/rfc5552.txt) uses VoiceXML and [RFC 6230](http://www.ietf.org/rfc/rfc6230.txt)/[RFC 6231](http://www.ietf.org/rfc/rfc6231.txt)/[RFC 6505](http://www.ietf.org/rfc/rfc6505.txt) use SIP/SDP to establish a two-way control channel between the AS and MRFC.
*   IMS allows any of the three mechanisms to be used, or combinations depending on circumstances.
*   All three mechanisms are transparent to proxy components, so supported by Clearwater.

### History-Info ([draft-ietf-sipcore-rfc4244bis](http://datatracker.ietf.org/doc/draft-ietf-sipcore-rfc4244bis/) - not [RFC 4244](http://www.ietf.org/rfc/rfc4244.txt), which is inaccurate wrt real implementations)

*   Primarily aimed at ASs - need to manipulate History-Info headers when diverting calls.  The MMTEL AS built into Sprout already supports this for CDIV.
*   Also, need to proxy History-Info headers transparently.  Clearwater supports this.
*   However, s9.1 says if the incoming H-I is missing or wrong, the intermediary must add an entry on behalf of the previous entity.  Clearwater does not currently do this so if other parts of the network are not compliant, Clearwater will not fill in for them (and should).

### OMS Push-to-Talk over Cellular service ([RFC 4354](http://www.ietf.org/rfc/rfc4354.txt), [RFC 4964](http://www.ietf.org/rfc/rfc4964.txt) and [RFC 5318](http://www.ietf.org/rfc/rfc5318.txt))

*   Covers poc-settings event package ([RFC 4354](http://www.ietf.org/rfc/rfc4354.txt)), P-Answer-State header ([RFC 4964](http://www.ietf.org/rfc/rfc4964.txt)) and P-Refused-URI-List header ([RFC 5318](http://www.ietf.org/rfc/rfc5318.txt))
*   Only required for OMA push-to-talk over cellular service.
*   Optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   Transparent to proxies, so supported by Clearwater.

### Conference event package ([RFC 4575](http://www.ietf.org/rfc/rfc4575.txt))

*   Defines an event package for various events associated with SIP conferences.
*   Mandatory for UEs and IMS application servers providing conference services.
*   Transparent to proxies, so supported by Clearwater.

### Event notification resource lists ([RFC 4662](http://www.ietf.org/rfc/rfc4662.txt))

*   Defines an extension to the SUBSCRIBE/NOTIFY event mechanisms that allow an application to subscribe for events from multiple resources with a single request, by referencing a resource list.
*   In IMS, this is only required for presence events, and is only mandatory for UEs supporting presence or presence servers, otherwise it is optional.
*   Should be transparent to proxies, so supported by Clearwater.

### Consent based Communications ([RFC 5360](http://www.ietf.org/rfc/rfc5360.txt))

*   Defines a framework for obtaining consent for routing traffic towards a SIP entity, including Permission-Missing and Trigger-Consent headers, SIP MESSAGE methods sent via store-and-forward relay to request consents and an event package (ie. a lot of extra SIP!).
*   In theory could be applicable to registrations in IMS (guarding against a user maliciously redirecting their incoming calls or messages to another user's device) or to CDIV type services.
*   Mandatory according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm) - but not clear exactly what is required, could be as simple as just forwarding headers transparently, or it could be required to support consent for registrations.
*   Reading Rel 9, this strongly suggests that the only nodes that need to actually invoke these mechanisms certain types of application servers, such as conference servers or message servers that support message distribution lists (so the function is to guard against people being added to these lists without their consent). Therefore the only function required in the core is to pass the messages and headers through transparently.  Clearwater already supports this minimal set of function.

### Multiple-Recipient MESSAGE requests ([RFC 5365](http://www.ietf.org/rfc/rfc5365.txt))

*   Defines a mechanism for MESSAGE requests to be sent to multiple recipients by specifying the list of recipients in the body of the message.  A message list server then fans the MESSAGE out to the multiple recipients.
*   The function is mandatory in an IMS message list server, but not required anywhere else in the network.
*   Transparent to proxies, so supported by Clearwater.

### Creating multi-party conferences ([RFC 5366](http://www.ietf.org/rfc/rfc5366.txt))

*   Allows a SIP UA to establish a multi-party conference by specifying a resource list in the body of the message used to set up the conference.
*   Mandatory for IMS conference app servers.
*   Transparent to proxies, so supported by Clearwater.

### Referring to multiple resources ([RFC 5368](http://www.ietf.org/rfc/rfc5368.txt))

*   Allows a SIP UA to send a REFER message containing a resource list URI.  One use case for this could be to send a single REFER to a conference server to get it to invite a group of people to a conference.
*   Optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm), and only applicable to UEs and any application servers that can receive REFER requests.
*   Transparent to proxies, so supported by Clearwater.

### P-Served-User header ([RFC 5502](http://www.ietf.org/rfc/rfc5502.txt))

*   Only applicable on the ISC interface - used to clear up some ambiguities about exactly which user the AS should be providing service for.
*   Optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   This header is supported by Clearwater and included on requests sent to application servers.

### Message body handling ([RFC 5621](http://www.ietf.org/rfc/rfc5621.txt))

*   Defines how multiple message bodies can be encoded in a SIP message.
*   Relevant in handling of third-party REGISTERs on ISC where XML encoded data from iFC may be passed to AS.

### SIP outbound support ([RFC 5626](http://www.ietf.org/rfc/rfc5626.txt))

*   Defines mechanisms for clients behind NATs to connect to a SIP network so SIP requests can be routed to the client through the NAT.
*   Mandatory according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   Supported by Clearwater for NAT traversal, except for the Flow-Timer header (which tells the client how often to send keepalives).

### Fixes to Record-Route processing ([RFC 5658](http://www.ietf.org/rfc/rfc5658.txt))

*   Fixes some interoperability issues in basic SIP handling of Record-Route headers, particularly in proxies which have multiple IP addresses.
*   Clearwater used RFC5658 double-record routing in Bono nodes when transitioning between the trusted and untrusted zones on different port numbers.

### Fixes for IPv6 addresses in URIs ([RFC 5954](http://www.ietf.org/rfc/rfc5954.txt))

*   Fixes a minor problem in the ABNF definition in [RFC 3261](http://www.ietf.org/rfc/rfc3261.txt) relating to IPv6 addresses, and clarifies URI comparison rules when comparing IPv6 addresses (in what looks like an obvious way).
*   Mandatory according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   Supported by Clearwater.

### Q.950 codes in Reason header ([RFC 6432](http://www.ietf.org/rfc/rfc6432.txt))

*   Defines how Q.950 codes can be encoded in Reason header.
*   Mandatory for MGCFs, optional for proxy components in IMS.
*   Transparent to proxies anyway, so supported by Clearwater.

### Geolocation ([RFC 4483](http://www.ietf.org/rfc/rfc4483.txt) and [RFC 6442](http://www.ietf.org/rfc/rfc6442.txt))

*   Framework for passing geo-location information within SIP messages.
*   According to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm) only required on an E-CSCF.
*   Supported by Clearwater as headers will be passed transparently.

### Proxy Feature Capabilities (referenced as [draft-ietf-sipcore-proxy-feature-12](http://datatracker.ietf.org/doc/draft-ietf-sipcore-proxy-feature/), but now [RFC 6809](http://www.ietf.org/rfc/rfc6809.txt))

*   Defines a mechanism to allow SIP intermediaries (such as registrars, proxies or B2BUAs) to signal feature capabilities when it would not be appropriate to use the feature tags mechanism in the Contact header as per [RFC 3841](http://www.ietf.org/rfc/rfc3841.txt).
*   Mandatory on P-CSCF according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm), but not clear what this actually means as the IMS specs don't seem to actually define any features to be signalled in these headers.
*   Clearwater will forward these headers if specified by other nodes in the signalling path, so this is supported.

### Alert info URNs ([draft-ietf-salud-alert-info-urns-06](http://datatracker.ietf.org/doc/draft-ietf-salud-alert-info-urns/))

*   Defines family of URNs to be used in Alert-Info header to provide better control over how user is alerted on a UE.
*   Optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   Transparent to proxies, so supported by Clearwater.

### AKA Authentication ([RFC 3310](http://www.ietf.org/rfc/rfc3310.txt))

*   This RFC defines how AKA authentication parameters map into the authentication and authorization headers used for digest authentication.
*   IMS allows AKA authentication as an alternative to SIP digest, although it is not mandatory.
*   Supported in Clearwater since sprint 39 “WALL-E”.

### SIP Instant Messaging ([RFC 3428](http://www.ietf.org/rfc/rfc3428.txt))

*   Defines the use of the SIP MESSAGE method to implement an instant messaging service.
*   Mandatory in proxy components according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   Supported in Clearwater.

### Registration Events ([RFC 3680](http://www.ietf.org/rfc/rfc3680.txt))

*   Defines an event package supported by SIP registrars to notify other devices of registrations.
*   Must be supported by IMS core for the ISC interface, and also needed by some UEs.
*   Supported in Clearwater since sprint 40 "Yojimbo"

### PRACK support ([RFC 3262](http://www.ietf.org/rfc/rfc3262.txt))

*   Defines a mechanism for ensuring the reliability of provisional responses when using an unreliable transport.  Covers the PRACK method and the Rseq and Rack headers.
*   Optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   Supported in Clearwater.

## Relevant to Clearwater but not currently supported

These are the RFCs which are relevant to Clearwater and not yet supported.

### User agent capabilities and caller preferences ([RFC 3840](http://www.ietf.org/rfc/rfc3840.txt) and [RFC 3841](http://www.ietf.org/rfc/rfc3841.txt))

*   User agent capabilities encoded as feature tags in Contact headers during registration ([RFC 3840](http://www.ietf.org/rfc/rfc3840.txt)) and Accept-Contact, Reject-Contact and Request-Disposition headers encode filtering rules to decide which targets subsequent request should be routed/forked to ([RFC 3841](http://www.ietf.org/rfc/rfc3841.txt)).
*   Used for routing of requests to targets with the appropriate features/capabilities in IMS. Mandatory for proxy components.
*   Clearwater's Sprout registrar already supports storing all feature tags, but does not yet support forarding requests based on them.

### Fixes to issues with SIP non-INVITE transactions ([RFC 4320](http://www.ietf.org/rfc/rfc4320.txt))

*   Defines changes to [RFC 3261](http://www.ietf.org/rfc/rfc3261.txt) procedures for handling non-INVITE transactions to avoid some issues - in particular the potential for an O(N^2) storm of 408 responses if a transaction times out.  The main changes are to when/if a 100 Trying responses should be sent, and disallowing 408 responses altogether on non-INVITE transactions.
*   Mandatory for all SIP nodes according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   Clearwater already supports part of this, but probably not all.

### Dialstring URI parameter ([RFC 4967](http://www.ietf.org/rfc/rfc4967.txt))

*   Defines a `user=dialstring` parameter used in SIP URIs to indicate that the user portion of the URI is a dial string (as opposed to a number that definitely identifies a phone as in the `user=phone` case).
*   IMS allows this encoding from UEs initiating calls, but doesn't specify any particular processing within the core of the network.  The intention is that this can be handled by an application server, or captured by filter criteria.
*   Clearwater doesn't currently support this.

### P-Early-Media header ([RFC 5009](http://www.ietf.org/rfc/rfc5009.txt))

*   Used to authorize and control early media.
*   If P-CSCF is not gating media then required function is as simple as
    *   adding P-Early-Media header with `supported` value on requests from clients (or modifying header from clients if already in message)
    *   passing the header through transparently on responses.
*   If P-CSCF is gating media then function is more complex as P-CSCF has to operate on values in P-Early-Media headers sent to/from UEs.
*   Mandatory in a P-CSCF according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   Clearwater doesn't currently support this.

### GRUUs ([RFC 5627](http://www.ietf.org/rfc/rfc5627.txt), plus [RFC 4122](http://www.ietf.org/rfc/rfc4122.txt), [draft-montemurro-gsma-imei-urn-11](http://datatracker.ietf.org/doc/draft-montemurro-gsma-imei-urn/) and [draft-atarius-device-id-meid-urn-01](http://datatracker.ietf.org/doc/draft-atarius-device-id-meid-urn/))

*   [RFC 5627](http://www.ietf.org/rfc/rfc5627.txt) defines mechanisms to assign and propagate a Globally-Routeable User Agent URI for each client that registers with the SIP network.  A GRUU identifies a specific user agent rather than a SIP user, and is routeable from anywhere in the internet.  GRUUs are intended to be used in scenarios like call transfer where URIs are required for individual user agents to ensure the service operates correctly.  Standard Contact headers would seem to do the job in many cases but don't satisfy the globally routeable requirement in all cases, for example where the client is behind certain types of NAT.
*   Assignment and use of GRUUs is mandatory for S-CSCF and UEs in an IMS network. [RFC 4122](http://www.ietf.org/rfc/rfc4122.txt), [draft-montemurro-gsma-imei-urn-11](http://datatracker.ietf.org/doc/draft-montemurro-gsma-imei-urn/) and [draft-atarius-device-id-meid-urn-01](http://datatracker.ietf.org/doc/draft-atarius-device-id-meid-urn/) are referenced from the sections of [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm) that discuss exactly how GRUUs should be constructed.
*   Clearwater currently does not support GRUUs.

### Registration event package for GRUUs ([RFC 5628](http://www.ietf.org/rfc/rfc5628.txt))

*   Defines an extension to the [RFC 3680](http://www.ietf.org/rfc/rfc3680.txt) registration event package to include GRUUs.
*   Mandatory on S-CSCF and UEs in an IMS network.
*   Clearwater does not currently support GRUUs.

### Alternative URIs ([RFC 2806](http://www.ietf.org/rfc/rfc2806.txt), [RFC 2368](http://www.ietf.org/rfc/rfc2368.txt), [RFC 3859](http://www.ietf.org/rfc/rfc3859.txt), [RFC 3860](http://www.ietf.org/rfc/rfc3860.txt), [RFC 3966](http://www.ietf.org/rfc/rfc3966.txt))

*   Various RFCs defining alternatives to SIP URI - Tel URI ([RFC 2806](http://www.ietf.org/rfc/rfc2806.txt) and [RFC 3966](http://www.ietf.org/rfc/rfc3966.txt)), mailto URI ([RFC 2368](http://www.ietf.org/rfc/rfc2368.txt)), pres URI ([RFC 3859](http://www.ietf.org/rfc/rfc3859.txt)), and im URI ([RFC 3860](http://www.ietf.org/rfc/rfc3860.txt)).
*   IMS allows use of Tel URIs
    *   as a public user identity associated with a subscription (although a subscription must have at least on public user identity which is a SIP URI)
    *   as the target URI for a call.
*   Other URIs can be specified as Request URI for a SIP message.
*   Clearwater only supports SIP URIs. 

### P-Media-Authorization header ([RFC 3313](http://www.ietf.org/rfc/rfc3313.txt))

*   According to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm), only required if P-CSCF supporting IMS AKA authentication with IPsec ESP encryption, or SIP digest authentication with TLS encryption.
*   Not supported, as this is P-CSCF only (and Bono doesn't support AKA). 

### Signalling Compression aka SigComp ([RFC 3320](http://www.ietf.org/rfc/rfc3320.txt), [RFC 3485](http://www.ietf.org/rfc/rfc3485.txt), [RFC 3486](http://www.ietf.org/rfc/rfc3486.txt), [RFC 4077](http://www.ietf.org/rfc/rfc4077.txt), [RFC 4896](http://www.ietf.org/rfc/rfc4896.txt), [RFC 5049](http://www.ietf.org/rfc/rfc5049.txt), [RFC 5112](http://www.ietf.org/rfc/rfc5112.txt))

*   [RFC 3320](http://www.ietf.org/rfc/rfc3320.txt) defines basic SigComp (which is not SIP-specific), [RFC 3485](http://www.ietf.org/rfc/rfc3485.txt) defines a static dictionary for use in SigComp compression of SIP and SDP, [RFC 3486](http://www.ietf.org/rfc/rfc3486.txt) defines how to use SigComp with SIP, [RFC 4077](http://www.ietf.org/rfc/rfc4077.txt) defines a mechanism for negative acknowledgements to signal errors in synchronization between the compressor and decompressor, [RFC 4896](http://www.ietf.org/rfc/rfc4896.txt) contains corrections and clarifications to [RFC 3320](http://www.ietf.org/rfc/rfc3320.txt), [RFC 5049](http://www.ietf.org/rfc/rfc5049.txt) contains details and clarifications for SigComp compression of SIP, and [RFC 5112](http://www.ietf.org/rfc/rfc5112.txt) defines a static dictionary for use in SigComp compression of SIP presence bodies.
*   [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm) says that SigComp is mandatory between UEs and P-CSCF if access network is one of the 3GPP or 802.11 types (specifically it says this is mandatory if the UE sends messages with the P-Access-Network-Info set to one of these values - ie. the UE knows that is the type of access network it is being used on). Compression must use the dictionaries defined in both [RFC 3485](http://www.ietf.org/rfc/rfc3485.txt) and [RFC 5112](http://www.ietf.org/rfc/rfc5112.txt).
*   Clearwater does not currently support SigComp (although it would be relatively straightforward to implement it).

### Reason header ([RFC 3326](http://www.ietf.org/rfc/rfc3326.txt))

*   Already supported in Clearwater for responses, would need to add support for passing on CANCEL requests (but pretty easy).
*   Optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).

### Security-Client, Security-Server and Security-Verify headers ([RFC 3329](http://www.ietf.org/rfc/rfc3329.txt))

*   Defines headers that can be used to negotiate authentication mechanisms.
*   Only required if P-CSCF supporting IMS AKA authentication with IPsec ESP encryption, or SIP digest authentication with TLS encryption.
*   Not supported, as these headers are always caught by the P-CSCF (and Bono doesn't support AKA).  

### SMS over IP ([RFC 3862](http://www.ietf.org/rfc/rfc3862.txt) and [RFC 5438](http://www.ietf.org/rfc/rfc5438.txt))

*   Covers CPIM message format used between UEs and AS implementing SMS-GW function ([RFC 3862](http://www.ietf.org/rfc/rfc3862.txt)) and Message Disposition Notifications sent from the SMS-GW to the UE ([RFC 5438](http://www.ietf.org/rfc/rfc5438.txt)).
*   Transported as body in MESSAGE method across IMS core, so transparent to proxy components. Therefore should be supported by Clearwater once we have tested support for MESSAGE methods.

### SIP over SCTP ([RFC 4168](http://www.ietf.org/rfc/rfc4168.txt))

*   Defines how SIP can be transported using SCTP (instead of UDP or TCP).
*   IMS allows SCTP transport within the core of the network, but not between P-CSCF and UEs.
*   Clearwater does not support SCTP transport (nor does PJSIP).  Strictly speaking this is relevant to Clearwater, but it's not clear whether anyone would use it.

### Signalling pre-emption events ([RFC 4411](http://www.ietf.org/rfc/rfc4411.txt))

*   Defines use of the SIP Reason header in BYE messages to signal when a session is being terminated because of a network pre-emption event, for example, if the resources originally acquired for the call were need for a higher priority session.
*   Optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   Not currently supported by Clearwater.

### Resource Priority ([RFC 4412](http://www.ietf.org/rfc/rfc4412.txt))

*   Covers Resource-Priority and Accept-Resource-Priority headers.  Intended to allow UEs to signal high priority calls that get preferential treatment by the network (for example, emergency service use).
*   Not currently supported by Clearwater.
*   Optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).

### Number portability parameters in Tel URI ([RFC 4694](http://www.ietf.org/rfc/rfc4694.txt))

*   Defines additional parameters in Tel URI for signalling related to number portability.
*   Used in IMS in both Tel and SIP URIs for carrier subscription scenarios, and in IMS core for other number portability related scenarios.
*   Optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   Not currently supported by Clearwater.

### Service URNs ([RFC 5031](http://www.ietf.org/rfc/rfc5031.txt))

*   Defines a URN namespace to identify services.  IMS allows UEs to use such service URNs as target URIs when establishing a call.  In particular, it is mandatory for UEs to signal emergency calls using a service URN of the form urn:service:sos possibly with a subtype, and the P-CSCF must be able to handle these requests appropriately, routing to an E-CSCF.
*   Clearwater currently has no support for service URNs.

### Rejecting anonymous requests ([RFC 5079](http://www.ietf.org/rfc/rfc5079.txt))

*   Defines a status code used to reject anonymous requests if required by local policy/configuration.
*   Optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   Not currently supported by Clearwater.

### Subscribing to events on multiple resources ([RFC 5367](http://www.ietf.org/rfc/rfc5367.txt))

*   Allows a SIP node to subscribe to events on multiple resources with a single SUBSCRIBE message by specifying a resource list in the body of the message.
*   Optional for any IMS node that can be the target of a SUBSCRIBE request.
*   Not currently supported by Clearwater.

### Max-Breadth header ([RFC 5393](http://www.ietf.org/rfc/rfc5393.txt))

*   Intended to plug an amplification vulnerability in SIP forking.  Any forking proxy must limit the breadth of forking to breadth specified in this header.
*   According to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm) is mandatory on any node that supports forking.
*   Not currently supported by Clearwater.

### Media feature tag for MIME application subtypes ([RFC 5688](http://www.ietf.org/rfc/rfc5688.txt))

*   Defines a media feature tag to be used with the mechanisms in [RFC 3840](http://www.ietf.org/rfc/rfc3840.txt) and [RFC 3841](http://www.ietf.org/rfc/rfc3841.txt) to direct requests to UAs that support a specific MIME application subtype media stream.
*   According to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm) support for this feature tag is mandatory on S-CSCFs.
*   Not currently supported, but support may drop out of implementing [RFC 3840](http://www.ietf.org/rfc/rfc3840.txt)/[RFC 3841](http://www.ietf.org/rfc/rfc3841.txt) (depending on the what match criteria the tag requires).

### XCAPdiff event package ([RFC 5875](http://www.ietf.org/rfc/rfc5875.txt))

*   Defines an event package allowing applications to get notifications of changes to XCAP documents.
*   Used by IMS at Ut reference point to allow UEs to control service settings.  According to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm), mandatory for XDMS server, but optional for UEs.
*   Not supported by Homer.

### Correct transaction handling of 2xx responses to INVITE ([RFC 6026](http://www.ietf.org/rfc/rfc6026.txt))

*   A fix to basic SIP transaction model to avoid INVITE retransmissions being incorrectly identified as a new transaction and to plug a security hole around the forwarding of uncorrelated responses through proxies.  The change basically adds a new state to the transaction state machine when previously the transaction would have been considered terminated and therefore deleted.
*   This fix is mandatory according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   Not supported by Clearwater, and will probably require PJSIP changes.

### P-Asserted-Service and P-Preferred-Service headers ([RFC 6050](http://www.ietf.org/rfc/rfc6050.txt))

*   Defines a mechanism to allow a UE to signal the service it would like (although this is not binding on the network) and other components to signal between themselves the service being provided.  The UE may optionally include a P-Preferred-Service header on any request specifying the service it wishes to use.  The S-CSCF is responsible for checking that the service requested in P-Preferred-Service is (a) supported for the subscriber and (b) consistent with the actual request.  If the request is allowed, the S-CSCF replaces the P-Preferred-Service with a P-Asserted-Service header.   If either check fails, the S-CSCF may reject the request or it may allow it but ignore the P-Preferred-Service header.  If the UE does not specify a P-Preferred-Service header (or the specified one was not valid) the S-CSCF should work out the requested service by analysing the request parameters, and add a P-Asserted-Service header encoding the result.
*   In IMS networks, header should contain an IMS Communication Service Identifier (ICSI) - defined values are documented at http://www.3gpp.com/Uniform-Resource-Name-URN-list.html - examples include MMTEL (3gpp-service.ims.icsi.mmtel), IPTV (3gpp-service.ims.icsi.iptv), Remote Access (3gpp-service.ims.icsi.ra), and Converged IP Messaging (3gpp-service.ims.icsi.oma.cpm.*   depending on exact service being requested/provided).
*   Mandatory function according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   Not currently supported by Clearwater.

### SIP INFO messages ([RFC 6086](http://www.ietf.org/rfc/rfc6086.txt))

*   Framework for exchanging application specification information within a SIP dialog context.
*   Not currently supported by Clearwater.
*   Optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).

### Indication of support for keepalives ([RFC 6223](http://www.ietf.org/rfc/rfc6223.txt))

*   Adds a parameter to Via headers to allow nodes to agree the type of keepalives to be used to keep NAT pinholes open.
*   Mandatory for UEs and P-CSCFs, optional elsewhere.
*   Not currently supported by Clearwater and would require PJSIP changes.

### Response code for indication of terminated dialog ([RFC 6228](http://www.ietf.org/rfc/rfc6228.txt))

*   Defines a new status code to indicate the termination of an early dialog (ie. a dialog created by a provisional response) prior to sending a final response.
*   According to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm) this parameter is mandatory for all UA components than can send or receive INVITEs, and mandatory for S-CSCF because it has implications on forking proxies.
*   This is not currently supported by Clearwater.

### P-Private-Network-Indication (referenced as [draft-vanelburg-sipping-private-network-indication-02](http://datatracker.ietf.org/doc/draft-vanelburg-sipping-private-network-indication/))

*   Mechanisms for transport of private network information across an IMS core.
*   Optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   Not currently supported by Clearwater.

### Session-ID header (referenced as [draft-kaplan-dispatch-session-id-00](http://datatracker.ietf.org/doc/draft-kaplan-dispatch-session-id/))

*   Defines an end-to-end globally unique session identifier that is preserved even for sessions that traverse B2BUAs).
*   Optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   Not currently supported by Clearwater.

### Interworking with ISDN ([draft-ietf-cuss-sip-uui-06](http://datatracker.ietf.org/doc/draft-ietf-cuss-sip-uui/) and [draft-ietf-cuss-sip-uui-isdn-04](http://datatracker.ietf.org/doc/draft-ietf-cuss-sip-uui-isdn/))

*   Defines mechanisms/encodings for interworking ISDN with SIP.
*   Optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   Not currently supported by Clearwater.

## SDP/Media RFCs

[TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm) references a number of specifications which relate to media function - either SDP negotiation or media transport or both.  Clearwater currently passes SDP transparently and does not get involved in media flows. Unless we change this position, Clearwater can either be considered to support the RFC (because it supports passing SDP with the relevant contents) or that the RFC is not applicable to Clearwater.

The following is a brief explanation of each RFC, and its relevance to IMS.

*   SDP ([RFC 4566](http://www.ietf.org/rfc/rfc4566.txt)) - defines basic SDP protocol.
*   Offer/Answer model for SDP media negotiation ([RFC 3264](http://www.ietf.org/rfc/rfc3264.txt)) - defines how SDP is used to negotiate media.
*   Default RTP/AV profile ([RFC 3551](http://www.ietf.org/rfc/rfc3551.txt)) - defines default mappings from audio and video encodings to RTP payload types.
*   Media Resource Reservation ([RFC 3312](http://www.ietf.org/rfc/rfc3312.txt) and [RFC 4032](http://www.ietf.org/rfc/rfc4032.txt)) - defines additional SDP parameters to signal media resource reservation between two SIP UAs.  [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm) requires UEs, MGCFs and ASs to use these mechanisms, and that P-CSCF should monitor the flows if it is performing IMS-ALG or media gating functions.
*   Mapping of media streams to resource reservation ([RFC 3524](http://www.ietf.org/rfc/rfc3524.txt) and [RFC 3388](http://www.ietf.org/rfc/rfc3388.txt)) - define how multiple media streams can be grouped in SDP and mapped to a single resource reservation. IMS requires UEs to use these encodings when doing resource reservations.
*   Signaling bandwidth required for RTCP ([RFC 3556](http://www.ietf.org/rfc/rfc3556.txt)) - by default RTCP is assumed to consume 5% of session bandwidth, but this is not accurate for some encodings, so this RFC defines explicit signalling of RTCP bandwidth in SDP.  This function is optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   TCP media transport ([RFC 3556](http://www.ietf.org/rfc/rfc3556.txt) and [RFC 6544](http://www.ietf.org/rfc/rfc6544.txt)) - defines how support for TCP media transport is encoded in SDP for basic SDP exchanges and for ICE exchanges. According to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm), media over TCP is optional in most of an IMS network, but mandatory in an IBCF implementing IMS-ALG function.
*   ICE ([RFC 5245](http://www.ietf.org/rfc/rfc5245.txt)) - defines ICE media negotiation used to establish efficient media paths through NATs.  According to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm) support for ICE is optional in most of the IMS network, but mandatory on an IBCF implementing IMS-ALG function.
*   STUN ([RFC 5389](http://www.ietf.org/rfc/rfc5389.txt)) - defines a protocol used to allow UAs to obtain their server reflexive address for use in ICE.
*   TURN ([RFC 5766](http://www.ietf.org/rfc/rfc5766.txt)) - defines extensions to STUN used to relay media sessions via a TURN server to traverse NATs when STUN-only techniques don't work.
*   Indicating support for ICE in SIP ([RFC 5768](http://www.ietf.org/rfc/rfc5768.txt)) - defines a media feature tag used to signal support for ICE.
*   SDP for binary floor control protocol ([RFC 4583](http://www.ietf.org/rfc/rfc4583.txt)) - defines SDP extensions for establishing conferencing binary floor control protocol streams.  Optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   Real-time RTCP feedback ([RFC 4585](http://www.ietf.org/rfc/rfc4585.txt) and [RFC 5104](http://www.ietf.org/rfc/rfc5104.txt)) - defines extensions to RTCP to provide extended real-time feedback on network conditions.  Mandatory for most IMS components handling media (MRFs, IBCFs, MGCFs), but optional for UEs.
*   SDP capability negotiation ([RFC 5939](http://www.ietf.org/rfc/rfc5939.txt)) - defines extensions to SDP to allow for signalling and negotiation of media capabilities (such as alternate transports - SRTP). Mandatory for most IMS components handling media (MRFs, IBCFs, MGCFs), but optional for UEs.
*   SDP transport independent bandwidth signalling ([RFC 3890](http://www.ietf.org/rfc/rfc3890.txt)) - defines extensions to SDP to signal codec-only (ie. independent of transport) bandwidth requirements for a stream. Optional for IMS components handling media.
*   Secure RTP ([RFC 3711](http://www.ietf.org/rfc/rfc3711.txt), [RFC 4567](http://www.ietf.org/rfc/rfc4567.txt), [RFC 4568](http://www.ietf.org/rfc/rfc4568.txt), [RFC 6043](http://www.ietf.org/rfc/rfc6043.txt)) - defines transport of media over a secure variant of RTP, supporting encryption (to prevent eavesdropping) and integrity protecting (to protect against tampering). Keys are either exchanged in SDP negotiation (specified in [RFC 4567](http://www.ietf.org/rfc/rfc4567.txt) and [RFC 4568](http://www.ietf.org/rfc/rfc4568.txt)) or distributed via a separate key management service - termed MIKEY-TICKEY (specified in [RFC 6043](http://www.ietf.org/rfc/rfc6043.txt)).
*   Transcoder invocation using 3PCC ([RFC 4117](http://www.ietf.org/rfc/rfc4117.txt)) - defines how a transcoding service can be inserted into the media path when required using third-party call control flows. According to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm) this is only applicable to app servers and MRFC, and even then is optional.
*   MSRP ([RFC 4975](http://www.ietf.org/rfc/rfc4975.txt)) - defines a protocol for session-based transmission of a sequence of instant messages.  Only applicable to UEs, ASs and MRFCs and optional.
*   SDP for file transfer ([RFC 5547](http://www.ietf.org/rfc/rfc5547.txt)) - defines SDP extensions to support simple file transfers between two IMS nodes.  Optional.
*   Explicit congestion notifications for RTP over UDP ([RFC 6679](http://www.ietf.org/rfc/rfc6679.txt)) - defines RTCP extensions for reporting urgent congestion conditions and reporting congestion summaries. Optional.
*   Setting up audio streams over circuit switched bearers (referenced as [draft-ietf-mmusic-sdp-cs-00](http://datatracker.ietf.org/doc/draft-ietf-mmusic-sdp-cs/)) - defines SDP extensions for negotiating audio streams over a circuit switched network.  Mandatory for ICS capable UEs and SCC-AS, otherwise optional.
*   Media capabilities negotiation in SDP (referenced as [draft-ietf-mmusic-sdp-media-capabilities-08](http://datatracker.ietf.org/doc/draft-ietf-mmusic-sdp-media-capabilities/)) - defines SDP extensions for signalling media capabilities such as encodings and formats.  Mandatory for ICS capable UEs and SCC-AS, otherwise optional.
*   Miscellaneous capabilities negotiation in SDP (referenced as [draft-ietf-mmusic-sdp-miscellaneous-caps-00](http://datatracker.ietf.org/doc/draft-ietf-mmusic-sdp-miscellaneous-caps/)) - defines SDP extensions for signalling some miscellaneous capabilities.  Mandatory for ICS capable UEs and SCC-AS, otherwise optional.

# Not Relevant to Clearwater

### Locating P-CSCF using DHCP ([RFC 3319](http://www.ietf.org/rfc/rfc3319.txt) and [RFC 3361](http://www.ietf.org/rfc/rfc3361.txt))

*   These RFCs describe a mechanism for locating a SIP proxy server using DHCP.  ([RFC 3319](http://www.ietf.org/rfc/rfc3319.txt) defines the mechanism for IPv6/DHCPv6, and [RFC 3361](http://www.ietf.org/rfc/rfc3361.txt) is the IPv4 equivalent - not sure why they happened that way round!).
*   The IMS specifications allows this as one option for a UE to locate a P-CSCF, although there are other options such as manual configuration of a domain name or obtaining it from some access-network specific mechanism.
*   This is irrelevant to Clearwater - there would be no point in Clearwater providing a DHCP server with this function as there will be existing mechanisms used by clients to obtain their own IP addresses.  A service provider might enhance their own DHCP servers to support this function if required.

### Proxy-to-proxy SIP extensions for PacketCable DCS ([RFC 3603](http://www.ietf.org/rfc/rfc3603.txt))

*   Only relevance to IMS is that it defines a billing correlation parameter (bcid) which is passed in the P-Charging-Vector header from DOCSIS access networks.

### Geolocation ([RFC 4119](http://www.ietf.org/rfc/rfc4119.txt) and [RFC 6442](http://www.ietf.org/rfc/rfc6442.txt))

*   Frameworks for passing geo-location information within SIP messages - [RFC 4119](http://www.ietf.org/rfc/rfc4119.txt) encodes geo-location in a message body, [RFC 6442](http://www.ietf.org/rfc/rfc6442.txt) encodes a URI reference where the UEs location can be found.
*   According to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm) only required on an E-CSCF.

### P-User-Database header ([RFC 4457](http://www.ietf.org/rfc/rfc4457.txt))

*   Used when an IMS core has multiple HSSs and an SLF - allows I-CSCF to signal to S-CSCF which HSS to use to avoid multiple SLF look-ups.
*   Optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).
*   Not applicable to Clearwater given its stateless architecture.

### URIs for Voicemail and IVR applications ([RFC 4458](http://www.ietf.org/rfc/rfc4458.txt))

*   Defines conventions for service URIs for redirection services such as voicemail and IVR.
*   Optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm).

### P-Profile-Key header ([RFC 5002](http://www.ietf.org/rfc/rfc5002.txt))

*   Used solely between I-CSCF and S-CSCF to signal the public service identity key to be used when a requested public service identity matches a wildcard entry in the HSS. Purely an optimization to avoid having to do wildcard matching twice for a single request.
*   Optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm)
*   Not applicable to Clearwater's model which doesn't have I-/S-CSCF separation.

### Emergency call requirements and terminology ([RFC 5012](http://www.ietf.org/rfc/rfc5012.txt))

*   Referenced to define some terminology used in IMS architecture for handling emergency calls.

### Answering Modes ([RFC 5373](http://www.ietf.org/rfc/rfc5373.txt))

*   Defines a mechanism for a caller to control the answer mode at the target of the call. Use cases can include invoking some kind of auto-answer loopback.  Covers the Answer-Mode and Priv-Answer-Mode headers.
*   In general is transparent to proxies (provided proxies pass headers through), but the RFC recommends the mechanism is not used in environments that support parallel forking.
*   Optional according to [TS 24.229](http://www.3gpp.org/ftp/Specs/html-info/24229.htm) - and arguably not a good idea because of bad interactions with forking.
