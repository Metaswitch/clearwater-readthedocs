Using Cacti with Clearwater
===========================

`Cacti <http://www.cacti.net/>`__ is an open-source statistics and
graphing solution. It supports gathering statistics via native SNMP and
also via external scripts. It then exposes graphs over a web interface.

We use Cacti for monitoring Clearwater deployment, in particular large
ones running stress.

This document describes how to

-  create and configure a Cacti node
-  point it at your Clearwater nodes
-  view graphs of statistics from your Clearwater nodes.

Setting up a Cacti node (automated)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assuming you've followed the `Automated Chef
install <Automated_Install.md>`__, here are the steps to create and
configure a Cacti node:

1. use knife box create to create a Cacti node -
   ``knife box create -E     <name> cacti``
2. set up a DNS entry for it -
   ``knife dns record create -E <name>     cacti -z <root> -T A --public cacti -p <name>``
3. create graphs for all existing nodes by running
   ``knife cacti update -E <name>``
4. point your web browser at ``cacti.<name>.<root>/cacti/`` (you may
   need to wait for the DNS entry to propagate before this step works)

If you subsequently scale up, running ``knife cacti update -E <name>``
again will create graphs for the new nodes (without affecting the
existing nodes).

Setting up a Cacti node (manual)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you haven't followed our automated install process, and instead just
have an Ubuntu 14.04 machine you want to use to monitor Clearwater,
then:

1. install Cacti on a node by running
   ``sudo apt-get install cacti cacti-spine``
2. accept all the configuration defaults
3. login (admin/admin) and set a new password
4. modify configuration by

   1. going to Devices and deleting "localhost"
   2. going to Settings->Poller and set "Poller Type" to "spine" and
      "Poller Interval" to "Every Minute" - then click Save at the
      bottom of the page
   3. going to Data Templates and, for each of "ucd/net - CPU Usage -
      \*" set "Associated RRA's" to "Hourly (1 Minute Average)" and
      "Step" to 60
   4. going to Graph Templates and change "ucd/net - CPU Usage" to
      disable "Auto Scale"
   5. going to Import Templates and import the
      `Sprout <https://github.com/Metaswitch/chef/blob/master/cookbooks/clearwater/files/default/cacti/templates/cacti_host_template_sprout.xml>`__,
      `Bono <https://github.com/Metaswitch/chef/blob/master/cookbooks/clearwater/files/default/cacti/templates/cacti_host_template_bono.xml>`__
      and
      `SIPp <https://github.com/Metaswitch/chef/blob/master/cookbooks/clearwater/files/default/cacti/templates/cacti_host_template_sipp.xml>`__
      host templates - these define host templates for retrieving
      statistics from our components via SNMP and
      `0MQ <http://www.zeromq.org/>`__. For each template you import,
      select "Select your RRA settings below" and "Hourly (1 Minute
      Average)"

   6. set up the 0MQ-querying script by

      1. ssh-ing into the cacti node
      2. running the following

         ::

             sudo apt-get install -y --force-yes git ruby1.9.3 build-essential libzmq3-dev
             sudo gem install bundler --no-ri --no-rdoc
             git clone https://github.com/Metaswitch/cpp-common.git
             cd cpp-common/scripts/stats
             sudo bundle install

Pointing Cacti at a Node
^^^^^^^^^^^^^^^^^^^^^^^^

Before you point Cacti at a node, make sure the node has the required
packages installed. All nodes need clearwater-snmpd installed
(``sudo apt-get install clearwater-snmpd``). Additionally, sipp nodes
need clearwater-sip-stress-stats
(``sudo apt-get install clearwater-sip-stress-stats``).

To manually point Cacti at a new node,

1. go to Devices and Add a new node, giving a Description and Hostname,
   setting a Host Template of "Bono", "Sprout" or "SIPp" depending on
   the node type), Downed Device Detection to "SNMP Uptime" and SNMP
   Community to "clearwater"
2. click "Create Graphs for this Host" and select the graphs that you
   want - "ucd/net - CPU Usage" is a safe bet, but you might also want
   "Client Counts" and "Bono Latency" (if a bono node), "Sprout Latency"
   (if a sprout node), or "SIP Stress Status" (if a sipp node).
3. click "Edit this Host" to go back to the device, choose "List
   Graphs", select the new graphs and choose "Add to Default Tree" -
   this exposes them on the "graphs" tab you can see at the top of the
   page (although it may take a couple of minutes for them to accumulate
   enough state to render properly).

Viewing Graphs
~~~~~~~~~~~~~~

Graphs can be viewed on the top "graphs" tab. Useful features include

-  the "Half hour" preset, which shows only the last half-hour rather
   than the last day
-  the search box, which matches on graph name
-  the thumbnail view checkbox, which gets you many more graphs on
   screen
-  the auto-refresh interval, configured on the settings panel (the
   default is 5 minutes, so if you're looking for a more responsive UI,
   you'll need to set a smaller value)
-  CSV export, achievable via the icon on the right of the graph.

