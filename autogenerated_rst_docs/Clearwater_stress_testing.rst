Stress Testing
==============

One of Clearwater's biggest strengths is scalability and in order to
demonstrate this, we have easy-to-use settings for running large amounts
of SIP stress against a deployment. This document describes: -
Clearwater's SIP stress nodes, what they do, and (briefly) how they work
- how to kick off your own stress test.

SIP Stress Nodes
----------------

A Clearwater SIP stress node is similar to any other Project Clearwater
node, except that instead of having a Debian package like ``bono`` or
``sprout`` installed, it has our ``clearwater-sip-stress`` Debian
package installed.

What they do
~~~~~~~~~~~~

Clearwater SIP stress nodes run a standard SIPp script against your bono
cluster. The bono nodes translate this into traffic for sprout and this
generates traffic on homestead and homer. The nodes log their
success/failure to ``/var/log/clearwater-sip-stress`` and also restart
SIPp (after a 30s cool-down) if anything goes wrong.

The SIPp stress starts as soon as the node comes up - this is by design,
to avoid you having to manually start 50+ nodes generating traffic. If
you want to stop them from generating traffic, turn the whole node down.

Each SIP stress node picks a single bono to generate traffic against.
This bono is chosen by matching the bono node's index against the SIP
stress node's index. As a result, it's important to always give SIP
stress nodes an index.

How they work
~~~~~~~~~~~~~

The clearwater-sip-stress package includes two important scripts.

-  ``/usr/share/clearwater/infrastructure/scripts/sip-stress``, which
   generates a ``/usr/share/clearwater/sip-stress/users.csv.1`` file
   containing the list of all subscribers we should be targeting - these
   are calculated from properties in ``/etc/clearwater/shared_config``.
-  ``/etc/init.d/clearwater-sip-stress``, which runs
   ``/usr/share/clearwater/bin/sip-stress``, which in turn runs SIPp
   specifying ``/usr/share/clearwater/sip-stress/call_load2.xml`` as its
   test script. This test script simulates a pair of subscribers
   registering every 5 minutes and then making a call every 30 minutes.

The stress test logs to
``/var/log/clearwater-sip-stress/sipp.<index>.out``.

Running Stress
--------------

Using Chef
~~~~~~~~~~

This section describes step-by-step how to run stress using Chef
automation. It includes setting up a new deployment. It is possible to
run stress against an existing deployment but you'll need to reconfigure
some things so it's easier just to tear down your existing deployment
and start again.

1. If you haven't done so already, set up chef/knife (as described in
   `the install guide <Automated_Install.md>`__).
2. cd to your chef directory.
3. Edit your environment (e.g. ``environments/ENVIRONMENT.rb``) to
   override attributes as follows.

   For example (replacing ENVIRONMENT with your environment name and
   DOMAIN with your Route 53-hosted root domain):

   ::

       name "ENVIRONMENT"
       description "Stress testing environment"
       cookbook_versions "clearwater" => "= 0.1.0"
       override_attributes "clearwater" => {
           "root_domain" => "DOMAIN",
           "availability_zones" => ["us-east-1a"],
           "repo_server" => "http://repo.cw-ngv.com/latest",
           "number_start" => "2010000000",
           "number_count" => 1000,
           "pstn_number_count" => 0}

4. Upload your new environment to the chef server by typing
   ``knife environment from file environments/ENVIRONMENT.rb``
5. Create the deployment by typing
   ``knife deployment resize -E ENVIRONMENT``. If you want more nodes,
   supply parameters such "--bono-count 5" or "--sprout-count 3" to
   control this.
6. Follow `this
   process <https://github.com/Metaswitch/crest/blob/dev/docs/Bulk-Provisioning%20Numbers.md>`__
   to bulk provision subscribers. Create 30000 subscribers per SIPp
   node.
7. Create your stress test node by typing
   ``knife box create -E ENVIRONMENT sipp --index 1``. If you have
   multiple bono nodes, you'll need to create multiple stress test nodes
   by repeating this command with "--index 2", "--index 3", etc. - each
   stress test node only sends traffic to the bono with the same index.

-  To create multiple nodes, try
   ``for x in {1..20} ; do { knife box create -E ENVIRONMENT sipp --index $x && sleep 2 ; } ; done``.
-  To modify the number of calls/hour to simulate, edit/add
   ``count=<number>`` to ``/etc/clearwater/shared_config``, then run
   ``sudo /usr/share/clearwater/infrastructure/scripts/sip-stress`` and
   ``sudo service clearwater-sip-stress restart``.

8. Create a Cacti server for monitoring the deployment, as described in
   `this document <Cacti.md>`__.
9. When you've finished, destroy your deployment with
   ``knife deployment delete -E ENVIRONMENT``.

Manual (i.e. non-Chef) stress runs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SIP stress can also be run against a deployment that has been installed
manually (as per the `Manual Install
instructions <Manual_Install.md>`__).

Firstly follow `this
process <https://github.com/Metaswitch/crest/blob/dev/docs/Bulk-Provisioning%20Numbers.md>`__
to bulk provision subscribers. Work out how many stress nodes you want,
and create 30000 subscribers per SIPp node.

To create a new SIPp node, create a new virtual machine and bootstrap it
`by configuring access to the Project Clearwater Debian
repository <Manual_Install.md#configure-the-apt-software-sources>`__.

Then set the following properties in /etc/clearwater/local\_config:

-  (required) local\_ip - the local IP address of this node
-  (optional) node\_idx - the node index (defaults to 1)

Set the following properties in /etc/clearwater/shared\_config:

-  (required) home\_domain - the home domain of the deployment under
   test
-  (optional) bono\_servers - a list of bono servers in this deployment
-  (optional) stress\_target - the target host (defaults to the
   :math:`node_idx-th entry in `\ bono\_servers or, if there are no
   :math:`bono_servers, defaults to `\ home\_realm)
-  (optional) base - the base directory number (defaults to 2010000000)
-  (optional) count - the number of subscribers to run on this node
   (must be even, defaults to 30000)

Finally, run ``sudo apt-get install clearwater-sip-stress`` to install
the Debian package. Stress will start automatically after the package is
installed.

Configuring UDP Stress
~~~~~~~~~~~~~~~~~~~~~~

SIPp supports UDP stress, and this works with Clearwater. To make a
stress test node run UDP stress (rather than the default of TCP)

-  open /usr/share/clearwater/bin/sip-stress
-  find the line that begins "nice -n-20 /usr/share/clearwater/bin/sipp"
-  replace "-t tn" with "-t un"
-  save and exit
-  restart stress by typing "sudo service clearwater-sip-stress
   restart".

