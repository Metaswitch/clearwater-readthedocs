# IBCF

The Clearwater IBCF (Interconnect Border Gateway Function) provides an interface point between a Clearwater deployment and one or more trusted SIP trunks.

The IBCF does not currently provide all of the functions of an IMS compliant IBCF - in particular it does not support topology hiding or an H.248 interface to control a Transition Gateway.

To use the IBCF function you must install and configure at least one IBCF node, set up the ENUM configuration appropriately, and set up BGCF (Breakout Gateway Control Function) routing configuration on the Sprout nodes.

## Install and Configure an IBCF

Install and configure an IBCF node with the following steps.

- Install the node as if installing a Bono node, either [manually](Manual Install) or [using Chef](Automated Install).  If using Chef, use the `ibcf` role, for example

        knife box create -E <name> ibcf

- Edit the /etc/clearwater/user_settings file (creating it if it does not already exist) and add or update the line defining the IP addresses of SIP trunk peer nodes.

        trusted_peers="<trunk 1 IP address>,<trunk 2 IP address>,<trunk 3 IP address>, ..."

- Restart the Bono daemon.

        monit restart bono

## ENUM Configuration

The number ranges that should be routed over the SIP trunk must be set up in the ENUM configuration to map to a SIP URI owned by the SIP trunk provider, and routable to that provider.  For example, you would normally want to map a dialed number to a URI of the form `<number>@<domain>`.

This can either be achieved by defining rules for each number range you want to route over the trunk, for example

    *.0.1.5 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@<trunk IP address>!" .
    *.0.1.5.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@<trunk IP address>!" .

or by defining a default mapping to the trunk and exceptions for number ranges you want to keep on-net, for example

    * IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@<trunk IP address>!" .
    *.3.2.1.2.4.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@<local domain>!" .
    *.3.2.1.2.4.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@<local domain>!" .

Refer to the [ENUM guide](ENUM) for more about how to configure ENUM.

## BGCF Configuration

BGCF (Border Gateway Control Function) configuration is stored in the bgcf.json file in `/etc/clearwater` on each sprout node.  The file stores mappings from SIP trunk IP addresses and/or host names to IBCF host names, and these mappings control which IBCF nodes are used to route to a particular destination. Multiple nodes can be specified; in this case the message will be routed through the nodes in turn.

The file is in JSON format, for example.

    {
        "routes" : [
            {   "name" : "<route 1 descriptive name>",
                "domain" : "<SIP trunk IP address or host name>",
                "route" : ["<IBCF host name>"]
            },
            {   "name" : "<route 2 descriptive name>",
                "domain" : "<SIP trunk IP address or host name>",
                "route" : ["<IBCF host name>", "<IBCF host name>"]
            }
        ]
    }

There can be only one route to any given SIP trunk IP address or host name.  If there are multiple routes with the same destination IP address or host name, only the first will be used.
