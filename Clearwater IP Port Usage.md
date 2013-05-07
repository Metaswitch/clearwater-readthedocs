# Clearwater IP Port Usage

The nodes in Clearwater attempt talk to each other over IP.  This document lists the ports that are used by a deployment of Clearwater.

## All nodes

All nodes need to allow the following ICMP messages:

    Echo Request
    Echo Reply
    Destination Unreachable

They also need the following ports open to the world (`0.0.0.0/0`):

    TCP/22 for SSH access
    UDP/123 for NTP

If your deployment uses monitoring software ([cacti](http://www.cacti.net/) or [m/monit](http://mmonit.com/) for example), each node will also have to open appropriate ports for those services.

* SNMP (for cacti)

        UDP/161-162

* M/Monit

        TCP/2812

Lastly, to use the statistics interface, the following port should be opened to the world.  Currently statistics are only served from Bono and Sprout nodes, but, in the future, may be served from any node in the system.

* Statistics interface

        TCP/6666

## Ellis

The Ellis node needs the following ports opened to the world:

* Web UI

        TCP/80
        TCP/443

## Bono

The Bono nodes need the following ports open to the world:

* STUN signalling:

        TCP/3478
        UDP/3478

* SIP signalling:

        TCP/5060
        UDP/5060
        TCP/5062

* RTP forwarding:

        UDP/32768-65535

They also need the following ports open to all other Bono nodes and to all the Sprout nodes:

* Internal SIP signalling:

        TCP/5058

## Sprout

The Sprout nodes need the following ports open to all Bono nodes:

* Internal SIP signalling:

        TCP/5058

They also need the following ports opened to all other Sprout nodes:

* Shared registration store:

        TCP/11211
        UDP/11211

## Homestead

The Homestead nodes need the following ports open to all the Sprout nodes and the Ellis node:

* RESTful interface:

        TCP/8888

They also need the following ports opened to all other Homestead nodes:

* Cassandra:

        TCP/7000
        TCP/9160

## Homer

The Homer nodes need the following ports open to all the Sprout nodes and the Ellis node:

* RESTful interface:

        TCP/7888

They also need the following ports opened to all other Homer nodes:

* Cassandra:

        TCP/7000
        TCP/9160
