Installing a Chef server
========================

This is the first step in preparing to install a Clearwater deployment
using the `automated install <Automated_Install.md>`__ process. These
instructions will guide you through installing a Chef server on an EC2
instance.

Prerequisites
-------------

-  An Amazon EC2 account.
-  A DNS root domain configured as a hosted zone with Route53 (Amazon's
   built-in DNS service, accessible from the EC2 console). This domain
   will be referred to as ``<zone>`` in this document.

Create the instance
-------------------

Create a ``t2.small`` AWS EC2 instance running
``Ubuntu Server 14.04.2 LTS`` using the AWS web interface. The SSH
keypair you provide here is referred to below as ``<amazon_ssh_key>``.
It is easiest if you use the same SSH keypair for all of your instances.

Configure its security group to allow access SSH, HTTP, and HTTPS
access.

Configure a DNS entry for this machine, ``chef-server.<zone>``. (The
precise name isn't important, but we use this consistently in the
documentation that follows.) It should have a non-aliased A record
pointing at the public IP address of the instance as displayed in the
EC2 console.

Once the instance is up and running and you can connect to it over SSH,
you may continue to the next steps.

If you make a mistake, simply delete the instance permanently by
selecting "Terminate" in the EC2 console, and start again. The
terminated instance may take a few minutes to disappear from the
console.

Install and configure the Chef server
-------------------------------------

The `chef documentation <http://docs.chef.io/install_server.html>`__
explains how to install and configure the chef server. These
instructions involve setting up a user and an organization.

-  The user represents you as a user of chef. Pick whatever user name
   and password you like. We refer to these as ``<chef-user-name>`` and
   ``<chef-user-password>``
-  Organizations allow different groups to use the same chef server, but
   be isolated from one another. You can choose any organization name
   you like (e.g. "clearwater"). We refer to this as ``<org-name>``

Follow steps 1-6 in the `chef
docs <http://docs.chef.io/install_server.html>`__.

Once you have completed these steps, copy the ``<chef-user-name>.pem``
file off of the chef server - you will need it when installing a chef
workstation.

Next steps
----------

Once your server is installed, you can continue on to `install a chef
workstation <Installing_a_Chef_workstation.md>`__.
