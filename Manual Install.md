# Manual Install Instructions

These instructions will take you through installing a minimal Clearwater system using the latest binary packages provided by the Clearwater project.  For a high level look at the install process, and a discussion of alternative install methods, see [Installation Instructions](Installation Instructions).

## Prerequisites

Before starting this process you will need the following:

* Five machines running clean installs of [Ubuntu 12.04 - 64bit server edition](http://releases.ubuntu.com/precise/).
    * The software has been tested on Amazon EC2 `m1.small` instances, so any machines at least as powerful as one of them will be sufficient.
    * Each machine will take on a separate role in the final deployment.  The system requirements for each role are the same thus the allocation of roles to machines can be arbitrary.
    * The firewalls of these devices must be independently configurable.  This may require some attention when commissioning the machines.  For example, in Amazon's EC2, they should all be created in separate security groups.
* A publicly accessible IP address of each of the above machines and a private IP address for each of them (these may be the same address depending on the machine environment).  These will be referred to as `<publicIP>` and `<privateIP>` below.
* The FQDN of the machine, which resolves to the machine's private IP address (if the machine has no FQDN, you should instead use the private IP).  Referred to as `<hostname>` below.
* SSH access to the above machines to a user called `ubuntu` authorised to use sudo.  If your system does not come with such a user pre-configured, add one with `sudo adduser ubuntu` and then authorize them to use sudo with `sudo adduser ubuntu sudo`.
* A DNS root zone in which to install your repository and the ability to configure records within that zone.  This root zone will be referred to as `<zone>` below.
* If you are not using the Project Clearwater provided Debian repository, you will need to know the URL (and, if applicable, the public GPG key) of your repository.

## Bootstrapping the Machines

There are a few steps that are common to all the Clearwater node installs - configuring the APT software sources and supplying the IP addresses/DNS hostnames to use for communicating within the deployment.

The following steps should be followed on all the machines that will make up the Clearwater deployment.

### Configuring the APT software sources

The machines need to be configured so that APT can use the Clearwater repository server and the [DataStax](http://www.datastax.com/) Cassandra repository.

#### Project Clearwater

Under sudo, create `/etc/apt/sources.list.d/clearwater.list` with the following contents:

    deb http://repo.cw-ngv.com/stable binary/

_Note: If you are not installing from the provided Clearwater Debian repository, replace the URL in this file to point to your Debian package repository._

Once this is created install the signing key used by the Clearwater server with:

    curl -L http://repo.cw-ngv.com/repo_key | sudo apt-key add -

You should check the key fingerprint with:

    sudo apt-key finger

The output should contain the following - check the fingerprint carefully.

    pub   4096R/22B97904 2013-04-30
          Key fingerprint = 9213 4604 DE32 7DF7 FEB7  2026 111D BE47 22B9 7904
    uid                  Project Clearwater Maintainers <maintainers@projectclearwater.org>
    sub   4096R/46EC5B7F 2013-04-30

#### DataStax

Under sudo, create `/etc/apt/sources.list.d/cassandra.list` with the following contents:

    deb http://debian.datastax.com/community stable main

Once this is created install the PGP signing key used by the DataStax server with:

    curl -L http://debian.datastax.com/debian/repo_key | sudo apt-key add -

#### Finishing up

Once the above steps have been performed, run the following to re-index your package manager:

    sudo apt-get update

### Configuring the inter-node hostnames/IP addresses

On each machine, create the file `/etc/clearwater/config` with the following contents:

    # Deployment definitions
    home_domain=<zone>
    sprout_hostname=sprout.<zone>
    hs_hostname=hs.<zone>:8888
    xdms_hostname=homer.<zone>:7888

    # Local IP configuration
    local_ip=<privateIP>
    public_ip=<publicIP>
    public_hostname=<hostname>

    # Email server configuration
    smtp_smarthost=<smtp server>
    smtp_username=<username>
    smtp_password=<password>
    email_recovery_sender=clearwater@example.org

    # Keys
    signup_key=<secret>
    turn_workaround=<secret>
    ellis_api_key=<secret>
    ellis_cookie_key=<secret>

See the [Chef instructions](Installing a Chef client#add-deployment-specific-configuration)
for more information on how to fill these in. The values marked
`<secret>` **must** be set to secure values to protect your deployment
from unauthorized access.

## Crash monitoring

Clearwater can be configured to upload crash reports to the Clearwater
repository server. This is useful for diagnosing problems. The crash
report contains, among other things, the entire contents of the
crashed process. This may include sensitive data such as usernames,
passwords, the content of any SIP messages passing through the server,
DNS hostnames, and many other potentially-sensitive items.

**Crash monitoring is disabled by default. You should not enable it
unless you are sure that your system has no sensitive information on
it, and you are happy for all data within a Clearwater process to be
sent to the Clearwater maintainers.**

To enable crash monitoring, simply install the relevant package on
each box in your deployment:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install clearwater-crash-monitor --yes

To remove it, remove the package and confirm that the
`clearwater-crash-monitoring` process is no longer running.

## Node specific installation instructions

At this point, you should decide (if you haven't already) which of the five machines will take on which of the Clearwater roles.

The five roles are:

* ellis
* bono - This role also hosts a restund STUN server
* sprout
* homer
* homestead

Once this is determined, `ssh` onto each box in turn and follow the appropriate instructions below:

### Ellis

Install the Ellis package with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install ellis --yes

Provision a pool of numbers in Ellis.  The command given here will generate 1000 numbers starting at `sip:6505550000@<zone>`, meaning none of the generated numbers will be routeable outside of the Clearwater deployment.  For more details on creating numbers, see the [create_numbers.py documentation]().

    sudo bash -c "export PATH=/usr/share/clearwater/ellis/env/bin:$PATH ;
                  cd /usr/share/clearwater/ellis/src/metaswitch/ellis/tools/ ;
                  python create_numbers.py --start 6505550000 --count 1000"

On success, you should see some output from python about importing eggs and then the following.

    Created 1000 numbers, 0 already present in database

This command is idempotent, so it's safe to run it multiple times.  If you've run it once before, you'll see the following instead.

    Created 0 numbers, 1000 already present in database

### Bono

Install the Bono and Restund packages with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install bono restund --yes

### Sprout

Install the Sprout package with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install sprout --yes

### Homer

Install the Homer and Cassandra packages with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install python-cql dsc1.1=1.1.9-1 cassandra=1.1.9 --yes
    sudo DEBIAN_FRONTEND=noninteractive apt-get install homer --yes

### Homestead

Install the Homestead and Cassandra packages with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install python-cql dsc1.1=1.1.9-1 cassandra=1.1.9 --yes
    sudo DEBIAN_FRONTEND=noninteractive apt-get install homestead --yes

## DNS Records

Clearwater uses DNS records to allow each node to find the others it needs to talk to to carry calls.  At this point, you should create the DNS entries for your deployment before continuing to the next step.  [Clearwater DNS Usage](Clearwater DNS Usage) describes the entries that are required before Clearwater will be able to carry service.

Although not required, we also suggest that you configure individual DNS records for each of the machines in your deployment to allow easy access to them if needed.

_Be aware that DNS record creation can take time to propagate, you can check whether your newly configured records have propagated successfully by running `dig <record>` on each Clearwater machine and checking that the correct IP address is returned._

## Firewall configuration

Lastly, we need to make sure the Clearwater nodes can all talk to each other.  To do this, you will need to open up some ports in the firewalls in your network.  The ports used by Clearwater are listed in [Clearwater IP Port Usage](Clearwater IP Port Usage).  Configure all of these ports to be open to the appropriate hosts before continuing to the next step.

## Where next?

Once you've reached this point, your Clearwater deployment is ready to handle calls.  See the following pages for instructions on making your first call and running the supplied regression test suite.

* [Making your first call](Making your first call)
* [Running the live test suite](Running the live tests)
