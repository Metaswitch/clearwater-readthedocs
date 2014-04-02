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


## All-in-one

All-in-one nodes need the following ports opened to the world

* Web UI

        TCP/80
        TCP/443

* STUN signalling:

        TCP/3478
        UDP/3478

* SIP signalling:

        TCP/5060
        UDP/5060
        TCP/5062

* RTP forwarding:

        UDP/32768-65535

* Statistics interface:
      
        TCP/6665
        TCP/6666
        TCP/6667
        TCP/6668
        TCP/6669
        
## Ellis

The Ellis node needs the following ports opened to the world:

* Web UI

        TCP/80
        TCP/443

## Bono

The Bono nodes need the following ports opened to the world:

* STUN signalling:

        TCP/3478
        UDP/3478

* SIP signalling:

        TCP/5060
        UDP/5060
        TCP/5062

* RTP forwarding:

        UDP/32768-65535

* Statistics interface:

        TCP/6669

They also need the following ports open to all other Bono nodes and to all the Sprout nodes:

* Internal SIP signalling:

        TCP/5058

## Sprout

The Sprout nodes need the following ports open to all Bono nodes:

* Internal SIP signalling:

        TCP/5054
        TCP/5052 (if I-CSCF function is enabled)

They also need the following ports opened to all other Sprout nodes:

* Shared registration store:

     For releases using a memcached store - that is all releases up to release 28 (Lock, Stock and Two Smoking Barrels) and from release 32 (Pulp Fiction) onwards

        TCP/11211
        
     For releases using an Infinispan store - that is releases 29 (Memento) and 30 (No Country for Old Men)

        TCP/7800

The following ports need to be open to all homestead nodes:

* Registration Termination Requests (if using an HSS):

        TCP/9888

They also need the following ports opened to the world:

* Statistics interface:

        TCP/6666

## Homestead

The Homestead nodes need the following ports open to all the Sprout nodes and the Ellis node:

* RESTful interface:

        TCP/8888

They also need the following ports open to just the Ellis node:

* RESTful interface:

        TCP/8889

They also need the following ports opened to all other Homestead nodes:

* Cassandra:

        TCP/7000
        TCP/9160

They also need the following ports opened to the world:

* Statistics interface:

        TCP/6667
        TCP/6668

## Homer

The Homer nodes need the following ports open to all the Sprout nodes and the Ellis node:

* RESTful interface:

        TCP/7888

They also need the following ports opened to all other Homer nodes:

* Cassandra:

        TCP/7000
        TCP/9160

They also need the following ports opened to the world:

* Statistics interface:

        TCP/6665

