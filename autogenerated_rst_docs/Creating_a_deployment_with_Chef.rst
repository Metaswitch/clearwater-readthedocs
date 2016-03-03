Creating a deployment with Chef
===============================

This is the final stage in creating a Clearwater deployment using the
`automated install process <Automated_Install.md>`__. Here we will
actually create the deployment - commissioning servers and configuring
DNS records.

Prerequisites
-------------

-  You must have `created the chef workstation
   machine <Installing_a_Chef_workstation.md>`__ and have SSH access to
   the ubuntu user on it.
-  You must have `created a deployment
   environment <Creating_a_deployment_environment.md>`__ and know its
   name, ``<name>``.

Creating a Deployment
---------------------

You now have two options - you can create an All-in-One node, where all
the Clearwater components are run on a single machine instance, or a
larger deployment which can potentially have numerous instances of each
component.

Creating an All-in-One ("AIO") node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create a single machine instance running all the Clearwater
components, run the following on the chef workstation machine.

::

    cd ~/chef
    knife box create cw_aio -E <name>

Optional arguments
^^^^^^^^^^^^^^^^^^

The following modifier is available.

-  ``--index <value>`` - Name the new node ``<name>-cw_aio-<value>`` to
   permit distinguishing it from others.

Creating a larger deployment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To kick off construction of the deployment, run the following on the
chef workstation machine.

::

    cd ~/chef
    knife deployment resize -E <name> --ralf-count 1 -V

Follow the on-screen prompts.

This will:

-  Commission AWS instances
-  Install the Clearwater software
-  Configure security groups
-  Configure DNS
-  Start the Clearwater services

Optional arguments
^^^^^^^^^^^^^^^^^^

The following modifiers are available to set the scale of your
deployment.

-  ``--bono-count NUM`` - Create ``NUM`` Bono nodes (default is 1)
-  ``--sprout-count NUM`` - Create ``NUM`` Sprout nodes (default is 1)
-  ``--homer-count NUM`` - Create ``NUM`` Homer nodes (default is 1)
-  ``--homestead-count NUM`` - Create ``NUM`` Homestead nodes (default
   is 1)
-  ``--ralf-count NUM`` - Create ``NUM`` Ralf nodes (default is 0)
-  ``--subscribers NUM`` - Auto-scale the deployment to handle ``NUM``
   subscribers.
-  Due to a known limitation of the install process, Ellis will allocate
   1000 numbers regardless of this value.
-  To bulk provision subscribers (without using Ellis), follow `these
   instructions <https://github.com/Metaswitch/crest/blob/master/src/metaswitch/crest/tools/sstable_provisioning/README.md>`__

More detailed documentation on the available Chef commands is available
`here <https://github.com/Metaswitch/chef/blob/master/docs/knife_commands.mdhttps://github.com/Metaswitch/chef/blob/master/docs/knife_commands.md>`__.

Next steps
----------

Now your deployment is installed and ready to use, you'll want to test
it.

-  `Making your first call <Making_your_first_call.md>`__
-  `Running the live tests <Running_the_live_tests.md>`__

