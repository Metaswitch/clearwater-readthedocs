Elastic Scaling
===============

The core Clearwater nodes have the ability to elastically scale; in
other words, you can grow and shrink your deployment on demand, without
disrupting calls or losing data.

This page explains how to use this elastic scaling function when using a
deployment created through the `automated <Automated_Install.html>`__ or
`manual <Manual_Install.html>`__ install processes. Note that, although
the instructions differ between the automated and manual processes, the
underlying operations that will be performed on your deployment are the
same - the automated process simply uses chef to drive this rather than
issuing the commands manually.

Before scaling your deployment
------------------------------

Before scaling up or down, you should decide how many Bono, Sprout,
Dime, Vellum and Homer nodes you need (i.e. your target size). This
should be based on your call load profile and measurements of current
systems, though based on experience we recommend scaling up a tier of a
given type (sprout, bono, etc.) when the average CPU utilization within
that tier reaches ~60%.

Performing the resize
---------------------

If you did an Automated Install
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To resize your automated deployment, run:

::

    knife deployment resize -E <env> --bono-count <n> --sprout-count <n> --dime-count <n> --vellum-count <n> --homer-count <n>

Where the ``<n>`` values are how many nodes of each type you need. Once
this command has completed, the resize operation has completed and any
nodes that are no longer needed will have been terminated.

More detailed documentation on the available Chef commands is available
`here <https://github.com/Metaswitch/chef/blob/master/docs/knife_commands.md>`__.

If you did a Manual Install
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're scaling up your deployment, follow the following process:

1. Spin up new nodes, following the `standard install
   process <Manual_Install.html>`__, but with the following modifications:

   -  Set the ``etcd_cluster`` so that it only includes nodes that are
      already in the deployment and that are running as etcd masters (so
      it does not include any nodes being added).
   -  Stop when you get to the "Provide Shared Configuration" step. The
      nodes will learn their configuration from the existing nodes.

2. Wait until the new nodes have fully joined the existing deployment.
   To check if a node has joined the deployment:

   -  Run ``cw-check_cluster_state``. This should report that the
      cluster is stable and, if this is a Vellum node, it should also
      report that this node is in all of its clusters.
   -  Run ``sudo cw-check_config_sync``. This reports when the node has
      learned its configuration.

3. Update DNS to contain the new nodes.

If you're scaling down your deployment, follow the following process:

1. Update DNS to contain only the nodes that will remain after the
   scale-down.
2. On each node that is about to be turned down:

   -  Run the appropriate command from the following (based on the node
      type) to stop processes from automatically restarting.

      -  Bono - ``monit unmonitor -g bono``
      -  Sprout - ``monit unmonitor -g sprout``
      -  Dime -
         ``monit unmonitor -g homestead && monit unmonitor -g homestead-prov && monit unmonitor -g ralf``
      -  Vellum - n/a
      -  Homer - ``monit unmonitor -g homer``
      -  Memento - ``monit unmonitor -g sprout``
      -  Ellis - ``monit unmonitor -g ellis``

   -  Start the main processes quiescing.

      -  Bono - ``sudo service bono quiesce``
      -  Sprout - ``sudo service sprout quiesce``
      -  Dime -
         ``sudo service homestead stop && sudo service homestead-prov stop && sudo service ralf stop``
      -  Vellum - n/a
      -  Homer - ``sudo service homer stop``
      -  Memento - ``sudo service sprout quiesce``
      -  Ellis - ``sudo service ellis stop``

   -  If the node you are turning down is a Vellum node, or another node
      configured to act as an etcd master, also do the following:

      -  ``sudo monit unmonitor -g clearwater_cluster_manager``
      -  ``sudo monit unmonitor -g clearwater_config_manager``
      -  ``sudo monit unmonitor -g clearwater_queue_manager``
      -  ``sudo monit unmonitor -g etcd``
      -  ``sudo service clearwater-etcd decommission``

      This will cause the node to leave its existing clusters.

3. Once the above steps have completed, turn down the nodes.


