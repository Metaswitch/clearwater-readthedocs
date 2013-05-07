Configuring an Application Server
=================================

This document explains how to configure an application server for use
in a Clearwater deployment.

Network configuration
=====================

Each application server must be able to communicate with Sprout and
Bono in both directions.

 * The application server must be able to contact all sprout and bono
   nodes on the trusted SIP port, 5058 (both TCP and UDP).

 * All sprout and bono nodes must be able to contact the application
   server on the port and protocol configured in your subscribers'
   iFCs (typically TCP and UDP port 5060).

 * The application server must also be able to exchange SIP messages
   (in both directions) with any other SIP entity that may appear in
   the signalling path of any call going through it.

 * Since the application server is in the trusted zone, it should
   *not* be accessible to untrusted SIP entities.

If Clearwater and your application server are both in the Amazon EC2
cloud, you can achieve all of these by placing the application server
in the `<deployment>-sprout` security group.

Application server configuration
================================

No special application server configuration is required.

 * Your application server should be prepared to accept SIP messages
   from any of your deployment's bono or sprout nodes, and from any
   SIP entity that may appear in the signalling path of any call going
   through it.

 * If your application server needs to spontaneously originate calls,
   it should do this via Sprout's trusted interface:
   `sprout.<deployment-domain>:5058` over either TCP or UDP.

The headers set by Clearwater are described in the [Application Server
Guide](Application Server Guide.md).

iFC configuration
=================

To configure a subscriber to invoke your application server, you must
configure the appropriate iFCs for that subscriber. You can do this
via the Homestead API, or if you are using an HSS, directly in the
HSS.

Ellis does not currently provide a GUI for altering the iFCs, but you
can configure them directly using Homestead.

Example
-------

Here is an example of how to use `curl` to configure iFCs directly.

To simplify the following commands, define the following variables -
set the user, application server(s), and Homestead name as appropriate
for your deployment:

    user=sip:6505550269@example.com
    as_hostnames="as1.example.com mmtel.example.com" # the list of zero or more application servers to invoke - don't forget mmtel
    hs_hostname=hs.example.com:8888

To retrieve the current configuration, invoke `curl` as follows.

    curl -H "NGV-API-Key: <API-key>" http://$hs_hostname/filtercriteria/$user

To update the configuration, invoke `curl` as follows.  The first stage builds the new XML document and the second pushes it to the server.

    { cat <<EOF
    <?xml version="1.0" encoding="UTF-8"?>
    <ServiceProfile>
    EOF
    for as_hostname in $as_hostnames ; do
      cat <<EOF
      <InitialFilterCriteria>
        <TriggerPoint>
          <ConditionTypeCNF>0</ConditionTypeCNF>
          <SPT>
            <ConditionNegated>0</ConditionNegated>
            <Group>0</Group>
            <Method>INVITE</Method>
            <Extension></Extension>
          </SPT>
        </TriggerPoint>
        <ApplicationServer>
          <ServerName>sip:$as_hostname</ServerName>
          <DefaultHandling>0</DefaultHandling>
        </ApplicationServer>
      </InitialFilterCriteria>
    EOF
    done
    cat <<EOF
    </ServiceProfile>
    EOF
    } | curl -X PUT -H "NGV-API-Key: <API-key>" http://$hs_hostname/filtercriteria/$user --data-binary @-

The subscriber will now have the desired configuration. You can confirm this by running the retrieval command again.
