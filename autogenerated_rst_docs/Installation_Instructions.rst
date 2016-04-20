Installation Instructions
=========================

These pages will guide you through installing a Clearwater deployment
from scratch.

Installation Methods
--------------------

What are my choices?
~~~~~~~~~~~~~~~~~~~~

1. All-in-one image, either using an
   `AMI <https://aws.amazon.com/amis/>`__ on `Amazon
   EC2 <http://aws.amazon.com/ec2/>`__ or an
   `OVF <http://dmtf.org/standards/ovf>`__ image on a private
   virtualization platform such as `VMware <http://www.vmware.com/>`__
   or `VirtualBox <https://www.virtualbox.org/>`__. This is the
   recommended method for trying Clearwater out.

   This installation method is very easy but offers no redundancy or
   scalability and relatively limited performance. As a result, it is
   great for familiarizing yourself with Clearwater before moving up to
   a larger-scale deployment using one of the following methods.

2. An automated install, using the
   `Chef <http://www.opscode.com/chef/>`__ orchestration system. This is
   the recommended install for spinning up large scale deployments since
   it can handle creating an arbitrary sized deployment in a single
   command.

   This installation method does have its limitations though. It is
   currently only supported on Amazon's EC2 cloud and assumes that DNS
   is being handled by Amazon's Route53 and that Route53 controls the
   deployment's root domain. It also requires access to a running Chef
   server. Setting this up is non-trivial but only needs to be done
   once, after which multiple deployments can be spun up very easily.

3. A manual install, using Debian packages and hand configuring each
   machine. This is the recommended method if chef is not supported on
   your virtualization platform or your DNS is not provided by Amazon's
   Route53.

   This install can be performed on any collection of machines (at least
   5 are needed) running Ubuntu 14.04 as it makes no assumptions about
   the environment in which the machines are running. On the other hand,
   it requires manually configuring every machine, firewalls and DNS
   entries, meaning it is not a good choice for spinning up a
   large-scale deployment.

4. Installing from source. If you are running on a non-Ubuntu-based OS,
   or need to test a code fix or enhancement you've made, you can also
   install Clearwater from source, building the code yourself.
   Per-component instructions are provided that cover the route from
   source code to running services. Familiarity with performing a manual
   install on Ubuntu will help with configuring your network correctly
   after the software is installed.

   If you install from source, especially on a non-Ubuntu OS, we'd love
   to hear about your experience, good or bad.

Installation Steps
------------------

The installation process for a full Clearwater deployment (i.e. not an
all-in-one) can be described at a high level as follows:

-  Sourcing enough machines to host the deployment (minimum is 6) and
   installing an OS on them all. `Ubuntu
   14.04 <http://releases.ubuntu.com/trusty/>`__ is the recommended and
   tested OS for hosting Clearwater.
-  Preparing each machine to allow installation of the Clearwater
   software.
-  Installing the Clearwater software onto the machines.
-  Configuring firewalls to allow the various machines to talk to each
   other as required.
-  Configuring DNS records to allow the machines to find each other and
   to expose the deployment to clients.

Detailed Instructions
~~~~~~~~~~~~~~~~~~~~~

Once you've decided on your install method, follow the appropriate link
below.

-  `All-in-one Images <All_in_one_Images.md>`__
-  `Automated Install <Automated_Install.md>`__
-  `Manual Install <Manual_Install.md>`__
-  For source installs, see the per-component instructions
   (`Sprout/Bono <https://github.com/Metaswitch/sprout/blob/master/docs/Development.md>`__,
   `Ellis <https://github.com/Metaswitch/ellis/blob/master/docs/development.md>`__,
   `Homer/Homestead <https://github.com/Metaswitch/crest/blob/master/docs/development.md>`__).

If you hit problems during this process, see the `Troubleshooting and
Recovery <Troubleshooting_and_Recovery.md>`__ steps.

If you want to deploy with IPv6 addresses, see the `IPv6 <IPv6.md>`__
notes.

Next Steps
----------

Once you have installed your deployment, you'll want to test that it
works.

-  `Making your first call <Making_your_first_call.md>`__
-  `Running the live test suite <Running_the_live_tests.md>`__

