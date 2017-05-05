Clearwater IP Port Usage
========================

The nodes in Clearwater attempt talk to each other over IP. This
document lists the ports that are used by a deployment of Clearwater.

All nodes
---------

All nodes need to allow the following ICMP messages:

::

    Echo Request
    Echo Reply
    Destination Unreachable

They also need the following ports open to the world (``0.0.0.0/0``):

::

    TCP/22 for SSH access

If your deployment uses SNMP monitoring software
(`cacti <http://www.cacti.net/>`__ for example), each node will also
have to open appropriate ports for this service.

-  SNMP

   ::

       UDP/161-162

All nodes also need the following ports open to all other nodes for
`automatic clustering and configuration
sharing <Automatic_Clustering_Config_Sharing.html>`__:

-  etcd

   ::

       TCP/2380
       TCP/4000

All-in-one
----------

All-in-one nodes need the following ports opened to the world

-  Web UI

   ::

       TCP/80
       TCP/443

-  STUN signaling:

   ::

       TCP/3478
       UDP/3478

-  SIP signaling:

   ::

       TCP/5060
       UDP/5060
       TCP/5062

-  RTP forwarding:

   ::

       UDP/32768-65535

Ellis
-----

The Ellis node needs the following ports opened to the world:

-  Web UI

   ::

       TCP/80
       TCP/443

Bono
----

The Bono nodes need the following ports opened to the world:

-  STUN signaling:

   ::

       TCP/3478
       UDP/3478

-  SIP signaling:

   ::

       TCP/5060
       UDP/5060
       TCP/5062

-  RTP forwarding:

   ::

       UDP/32768-65535

They also need the following ports open to all other Bono nodes and to
all the Sprout nodes:

-  Internal SIP signaling:

   ::

       TCP/5058

Sprout
------

The Sprout nodes need the following ports open to all Bono nodes:

-  Internal SIP signaling:

   ::

       TCP/5054
       TCP/5052

They also need the following ports opened to all Vellum nodes:

-  Chronos:

   ::

       TCP/9888

They also need the following ports opened to all Dime nodes:

-  Registration Termination Requests (if using an HSS):

   ::

       TCP/9888

They also need the following ports opened to the world:

-  HTTP interface (if including a Memento AS):

   ::

       TCP/443

Dime
----

The Dime nodes need the following ports open to all the Sprout nodes and
the Ellis node:

-  RESTful interface:

   ::

       TCP/8888

They also need the following ports open to just the Ellis node:

-  RESTful interface:

   ::

       TCP/8889

They also need the following ports open to all the Sprout, Bono and
Vellum nodes:

-  RESTful interface:

   ::

       TCP/10888

Homer
-----

The Homer nodes need the following ports open to all the Sprout nodes
and the Ellis node:

-  RESTful interface:

   ::

       TCP/7888

Vellum
------

The Vellum nodes need the following ports open to all other Vellum
nodes:

-  Chronos:

   ::

       TCP/7253

-  Memcached:

   ::

       TCP/11211

-  Cassandra:

   ::

       TCP/7000

They also need the following ports open to all Sprout and Dime nodes:

-  Chronos:

   ::

       TCP/7253

-  Astaire:

   ::

       TCP/11311

They also need the following ports open to all Homer and Dime nodes (and
all Sprout nodes, if including a Memento AS):

-  Cassandra:

   ::

       TCP/9160

Standalone Application Servers
------------------------------

Standalone Project Clearwater application servers (e.g. Memento and
Gemini) need the following ports open to all Sprout nodes:

-  SIP signaling:

   ::

       TCP/5054

They also need the following ports opened to the world (if they include
a Memento AS):

-  HTTP interface:

   ::

       TCP/443


