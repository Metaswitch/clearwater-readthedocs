Upgrading a Clearwater Deployment
=================================

This article explains how to upgrade a Project Clearwater deployment.

Quick Upgrade
-------------

The quickest way to upgrade is to simply upgrade all your nodes in any
order. There is no need to wait for one node to finish upgrading before
moving onto the next.

This is recommended if you:

-  Do not have a fault-tolerant deployment (e.g. the All-in-One image,
   or a deployment with one node of each type) OR
-  Do not need to provide uninterrupted service to users of your system.

Note that during a quick upgrade your users may be unable to register,
or make and receive calls. If you do have a fault-tolerant deployment
and need uninterrupted service, see "Seamless Upgrade" below.

Manual Install
~~~~~~~~~~~~~~

If you installed your system using the `Manual Install
Instructions <Manual_Install.md>`__, run
``sudo apt-get update -o Dir::Etc::sourcelist="sources.list.d/clearwater.list" -o Dir::Etc::sourceparts="-" -o APT::Get::List-Cleanup="0" && sudo apt-get install clearwater-infrastructure && sudo clearwater-upgrade``
on each node.

Chef Install
~~~~~~~~~~~~

If you installed your deployment with
`chef <Creating_a_deployment_with_Chef.md>`__:

-  Follow the instructions to `update the Chef
   server <https://github.com/Metaswitch/chef#updating-the-chef-server>`__
-  Run
   ``sudo apt-get update -o Dir::Etc::sourcelist="sources.list.d/clearwater.list" -o Dir::Etc::sourceparts="-" -o APT::Get::List-Cleanup="0" && sudo apt-get install clearwater-infrastructure && sudo chef-client && sudo clearwater-upgrade``
   on each node.

Seamless Upgrade
----------------

If your deployment contains at least two nodes of each type (excluding
Ellis) it is possible to perform a *seamless upgrade* that does not
result in any loss of service.

To achieve this the nodes must be upgraded one at a time and in a
specific order: first all Ralf nodes (if present), then Homestead,
Homer, Sprout, Memento (if present), Gemini (if present), Bono, and
finally Ellis.

For example if your deployment has two Homesteads, two Homers, two
Sprouts, two Bonos, and one Ellis, you should upgrade them in the
following order:

-  Homestead-1
-  Homestead-2
-  Homer-1
-  Homer-2
-  Sprout-1
-  Sprout-2
-  Bono-1
-  Bono-2
-  Ellis

Manual Install
~~~~~~~~~~~~~~

If you installed your system using the `Manual Install
Instructions <Manual_Install.md>`__ run
``sudo apt-get update -o Dir::Etc::sourcelist="sources.list.d/clearwater.list" -o Dir::Etc::sourceparts="-" -o APT::Get::List-Cleanup="0" && sudo apt-get install clearwater-infrastructure && sudo clearwater-upgrade``
on each node in the order described above.

Chef Install
~~~~~~~~~~~~

If you installed your deployment with
`chef <Creating_a_deployment_with_Chef.md>`__:

-  Follow the instructions to `update the Chef
   server <https://github.com/Metaswitch/chef#updating-the-chef-server>`__
-  Run
   ``sudo apt-get update -o Dir::Etc::sourcelist="sources.list.d/clearwater.list" -o Dir::Etc::sourceparts="-" -o APT::Get::List-Cleanup="0" && sudo apt-get install clearwater-infrastructure && sudo chef-client && sudo clearwater-upgrade``
   on each node in the order described above.

