# Installation Instructions

These pages will guide you through installing a Clearwater deployment from scratch.

## Installation Steps

At a high level, the following steps will need to be performed to install a Clearwater deployment:

* Sourcing enough machines to host the deployment (minimum is 5) and installing an OS on them all.  [Ubuntu 12.04](http://releases.ubuntu.com/precise/) is the recommended and tested OS for hosting Clearwater.
* Preparing each machine to allow installation of the Clearwater software.
* Installing the Clearwater software onto the machines.
* Configuring firewalls to allow the various machines to talk to each other as required.
* Configuring DNS records to allow the machines to find each other and to expose the deployment to clients.

## Installation Methods

### What are my choices?

1. A manual install, using Debian packages and hand configuring each machine.  This is the recommended method for your first install.

   This install can be performed on any collection of machines (at least 5 are needed) running Ubuntu 12.04 as it makes no assumptions about the environment in which the machines are running.  On the other hand, it requires manually configuring every machine, firewalls and DNS entries, meaning it is not a good choice for spinning up a large-scale deployment.

2. An automated install, using the [Chef](http://www.opscode.com/chef/) orchestration system.  This is the recommended install for spinning up large scale deployments since it can handle creating an arbitrary sized deployment in a single command.

   This installation method does have its limitations though.  It is currently only supported on Amazon's EC2 cloud and assumes that DNS is being handled by Amazon's Route53 and that Route53 controls the deployment's root domain.  It also requires access to a running Chef server.  Setting this up is non-trivial but only needs to be done once, after which multiple deployments can be spun up at will.

3. Installing from source.  If you are running on a non-Ubuntu-based OS, or need to test a code fix or enhancement you've made, you can also install Clearwater from source, building the code yourself.  Per-component instructions are provided that cover the route from source code to running services.  Familiarity with performing a manual install on Ubuntu will help with configuring your network correctly after the software is installed.

   If you install from source, especially on a non-Ubuntu OS, we'd love to hear about your experience, good or bad.

### Detailed Instructions

Once you've decided on your install method, follow the appropriate link below.

* [Manual Install](Manual Install)
* [Automated Install](Automated Install)
* For source installs, see the per-component instructions ([Sprout/Bono](https://github.com/Metaswitch/sprout/blob/master/docs/Development.md), [Ellis](https://github.com/Metaswitch/ellis/blob/master/docs/development.md), [Homer/Homestead](https://github.com/Metaswitch/crest/blob/master/docs/development.md)).

If you hit problems during this process, see the [Troubleshooting and Recovery](Troubleshooting and Recovery) steps.

## Next Steps

Once you have installed your deployment, you'll want to test that it works.

* [Making your first call](Making your first call)
* [Running the live test suite](Running the live tests)