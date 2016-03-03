Configuring an Application Server
=================================

This document explains how to configure an application server for use in
a Clearwater deployment.

Network configuration
---------------------

Each application server must be able to communicate with Sprout and Bono
in both directions.

-  The application server must be able to contact all sprout and bono
   nodes on the trusted SIP ports, 5054 and 5058 (respectively, for both
   TCP and UDP).

-  All sprout and bono nodes must be able to contact the application
   server on the port and protocol configured in your subscribers' iFCs
   (typically TCP and UDP port 5060).

-  The application server must also be able to exchange SIP messages (in
   both directions) with any other application server that may appear in
   the signaling path of any call going through it.

-  Since the application server is in the trusted zone, it should *not*
   be accessible to untrusted SIP entities.

If Clearwater and your application server are both in the Amazon EC2
cloud, you can achieve all of these by placing the application server in
the ``<deployment>-sprout`` security group.

Application server configuration
--------------------------------

No special application server configuration is required.

-  Your application server should be prepared to accept SIP messages
   from any of your deployment's bono or sprout nodes, and from any SIP
   entity that may appear in the signaling path of any call going
   through it.

-  If your application server needs to spontaneously originate calls, it
   should do this via Sprout's trusted interface:
   ``sprout.<deployment-domain>:5054`` over either TCP or UDP.

The headers set by Clearwater are described in the `Application Server
Guide <Application_Server_Guide>`__.

iFC configuration
-----------------

To configure a subscriber to invoke your application server, you must
configure the appropriate iFCs for that subscriber. You can do this via
the Ellis UI, the Homestead API, or if you are using an HSS, directly in
the HSS.

Web UI configuration via Ellis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ellis allows you to specify a mapping between application server names
and XML nodes. This is done by editing the
``/usr/share/clearwater/ellis/web-content/js/app-servers.json`` file,
which is in
`JSON <http://en.wikipedia.org/wiki/JSON#Data_types.2C_syntax_and_example>`__
format. An example file would be:

::

    {
    "MMTEL" : "<InitialFilterCriteria><Priority>0</Priority><TriggerPoint><ConditionTypeCNF></ConditionTypeCNF><SPT><ConditionNegated>0</ConditionNegated><Group>0</Group><Method>INVITE</Method><Extension></Extension></SPT></TriggerPoint><ApplicationServer><ServerName>sip:mmtel.example.com</ServerName><DefaultHandling>0</DefaultHandling></ApplicationServer></InitialFilterCriteria>", 
    "Voicemail" : "<InitialFilterCriteria><Priority>1</Priority><TriggerPoint><ConditionTypeCNF></ConditionTypeCNF><SPT><ConditionNegated>0</ConditionNegated><Group>0</Group><Method>INVITE</Method><Extension></Extension></SPT></TriggerPoint><ApplicationServer><ServerName>sip:vm.example.com</ServerName><DefaultHandling>0</DefaultHandling></ApplicationServer></InitialFilterCriteria>"
    }

Once this is saved, the list of application server names will appear in
the Ellis UI (on the 'Application Servers' tab of the Configure dialog),
and selecting or deselecting them will add or remove the relevant XML
from Homestead. This change takes effect immediately. If an node in the
iFC XML is not included in app-servers.json, Ellis will leave it
untouched.

Direct configuration via cURL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also configure iFCs directly using Homestead.

Here is an example of how to use ``curl`` to configure iFCs directly.
This configures a very basic iFC, which fires on INVITEs only, with no
conditions on session case. See an iFC reference for more details, e.g.,
`3GPP TS
29.228 <http://www.3gpp.org/ftp/Specs/archive/29_series/29.228/29228-b70.zip>`__
appendices B and F.

To simplify the following commands, define the following variables - set
the user, application server(s), and Homestead name as appropriate for
your deployment.

::

    user=sip:6505550269@example.com
    as_hostnames="as1.example.com mmtel.example.com" # the list of zero or more application servers to invoke - don't forget mmtel
    hs_hostname=hs.example.com:8888

Be careful - the user must be *exactly* right, including the ``sip:``
prefix, and also ``+1`` if and only if it is a PSTN line. We have seen
problems with PSTN lines; if the above syntax does not work, try
URL-encoding the user, e.g., for +16505550269@example.com write
``user=sip%3A%2B16505550269%40example.com``.

To retrieve the current configuration, invoke ``curl`` as follows. You
must be able to access $hs\_hostname; check your firewall configuration.

::

    curl http://$hs_hostname:8889/public/$user/service_profile

This will return a 303 if the user exists, with the service profile URL
in the Location header, e.g.

::

    Location: /irs/<irs-uuid>/service_profiles/<service-profile-uuid>

Then invoke ``curl`` as follows, using the values from the Location
header retrieved above:

::

    curl http://$hs_hostname:8889/irs/<irs-uuid>/service_profiles/<service-profile-uuid>/filter_criteria

To update the configuration, invoke ``curl`` as follows. The first stage
builds the new XML document and the second pushes it to the server.

::

    { cat <<EOF
    <?xml version="1.0" encoding="UTF-8"?>
    <ServiceProfile>
    EOF
    for as_hostname in $as_hostnames ; do
      cat <<EOF
      <InitialFilterCriteria>
        <Priority>1</Priority>
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
    } | curl -X PUT http://$hs_hostname:8889/irs/<irs-uuid>/service_profiles/<service-profile-uuid>/filter_criteria --data-binary @-

The subscriber will now have the desired configuration. You can confirm
this by running the retrieval command again.
