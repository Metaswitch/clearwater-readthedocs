# Manual Install Instructions

These instructions will take you through installing a minimal Clearwater system using the latest binary packages provided by the Clearwater project.  For a high level look at the install process, and a discussion of alternative install methods, see [Installation Instructions](Installation_Instructions.md).

## Prerequisites

Before starting this process you will need the following:

* Six machines running clean installs of [Ubuntu 12.04 - 64bit server edition](http://releases.ubuntu.com/precise/).
    * The software has been tested on Amazon EC2 `m1.small` instances, so any machines at least as powerful as one of them will be sufficient.
    * Each machine will take on a separate role in the final deployment.  The system requirements for each role are the same thus the allocation of roles to machines can be arbitrary.
    * The firewalls of these devices must be independently configurable.  This may require some attention when commissioning the machines.  For example, in Amazon's EC2, they should all be created in separate security groups.
    * On Amazon EC2, we've tested both within a [VPC](http://aws.amazon.com/vpc/) and without.  If using a VPC, we recommend using the "VPC with a Single Public Subnet" model (in the "VPC Wizard") as this is simplest.
* A publicly accessible IP address of each of the above machines and a private IP address for each of them (these may be the same address depending on the machine environment).  These will be referred to as `<publicIP>` and `<privateIP>` below.  (If running on Amazon EC2 in a VPC, you must explicitly add this IP address by ticking the "Automatically assign a public IP address" checkbox on creation.)
* The FQDN of the machine, which resolves to the machine's public IP address (if the machine has no FQDN, you should instead use the public IP).  Referred to as `<hostname>` below.
* SSH access to the above machines to a user authorised to use sudo.  If your system does not come with such a user pre-configured, add a user with `sudo adduser <username>` and then authorize them to use sudo with `sudo adduser <username> sudo`.
* A DNS zone in which to install your deployment and the ability to configure records within that zone.  This zone will be referred to as `<zone>` below.
* If you are not using the Project Clearwater provided Debian repository, you will need to know the URL (and, if applicable, the public GPG key) of your repository.

## Bootstrapping the Machines

There are a few steps that are common to all the Clearwater node installs - configuring the APT software sources and supplying the IP addresses/DNS hostnames to use for communicating within the deployment.

The following steps should be followed on all the machines that will make up the Clearwater deployment.

### Configuring the APT software sources

The machines need to be configured so that APT can use the Clearwater repository server.

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

#### Finishing up

Once the above steps have been performed, run the following to re-index your package manager:

    sudo apt-get update

### Configuring the inter-node hostnames/IP addresses

On each machine, create the file `/etc/clearwater/config` with the following contents:

    # Deployment definitions
    home_domain=<zone>
    sprout_hostname=sprout.<zone>
    chronos_hostname=<privateIP>:7253
    hs_hostname=hs.<zone>:8888
    hs_provisioning_hostname=hs.<zone>:8889
    ralf_hostname=ralf.<zone>:10888
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

If you wish to enable the optional I-CSCF function, also add the following:

    # I-CSCF/S-CSCF configuration
    icscf=5052
    upstream_hostname=<sprout_hostname>
    upstream_port=5052

If you wish to enable the optional external HSS lookups, add the following:

    # HSS configuration
    hss_hostname=<address of your HSS>
    hss_port=3868

If you want to host multiple domains from the same Clearwater deployment, add the following (and configure DNS to route all domains to the same servers):

    # Additional domains
    additional_home_domains=<domain 1>,<domain 2>,<domain 3>...

If you want your Sprout nodes to include Gemini/Memento Application Servers add the following:

    # Application Servers
    gemini_enabled='Y'
    memento_enabled='Y'

See the [Chef instructions](Installing_a_Chef_client.md#add-deployment-specific-configuration)
for more information on how to fill these in. The values marked
`<secret>` **must** be set to secure values to protect your deployment
from unauthorized access.

To modify these settings after the deployment is created, follow [these instructions](Modifying_Clearwater_settings.md).

## Node specific installation instructions

At this point, you should decide (if you haven't already) which of the six machines will take on which of the Clearwater roles.

The six roles are:

* ellis
* bono - This role also hosts a restund STUN server
* sprout
* homer
* homestead
* ralf

Once this is determined, `ssh` onto each box in turn and follow the appropriate instructions below:

### Ellis

Install the Ellis package with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install ellis --yes

Provision a pool of numbers in Ellis.  The command given here will generate 1000 numbers starting at `sip:6505550000@<zone>`, meaning none of the generated numbers will be routable outside of the Clearwater deployment.  For more details on creating numbers, see the [create_numbers.py documentation](https://github.com/Metaswitch/ellis/blob/dev/docs/create-numbers.md).

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

Set up the Chronos configuration file, following [these instructions](https://github.com/Metaswitch/chronos/blob/dev/doc/configuration.md)

Install the Sprout package with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install sprout --yes

If you want the Sprout nodes to include a Memento Application server, then install the memento packages with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install clearwater-cassandra --yes
    sudo DEBIAN_FRONTEND=noninteractive apt-get install memento memento-nginx --yes

### Homer

Install the Homer and Cassandra packages with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install clearwater-cassandra --yes
    sudo DEBIAN_FRONTEND=noninteractive apt-get install homer --yes

### Homestead

Install the Homestead and Cassandra packages with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install clearwater-cassandra --yes
    sudo DEBIAN_FRONTEND=noninteractive apt-get install homestead homestead-prov --yes

### Ralf

Set up the Chronos configuration file, following [these instructions](https://github.com/Metaswitch/chronos/blob/dev/doc/configuration.md)

Install the Ralf package with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install ralf --yes

## SNMP statistics

Sprout, Bono and Homestead nodes expose statistics over SNMP. This function is not installed by default - see [our SNMP documentation](Clearwater_SNMP_Statistics.md) for information on how to enable it.

## DNS Records

Clearwater uses DNS records to allow each node to find the others it needs to talk to to carry calls.  At this point, you should create the DNS entries for your deployment before continuing to the next step.  [Clearwater DNS Usage](Clearwater_DNS_Usage.md) describes the entries that are required before Clearwater will be able to carry service.

Although not required, we also suggest that you configure individual DNS records for each of the machines in your deployment to allow easy access to them if needed.

_Be aware that DNS record creation can take time to propagate, you can check whether your newly configured records have propagated successfully by running `dig <record>` on each Clearwater machine and checking that the correct IP address is returned._

## Firewall configuration

We need to make sure the Clearwater nodes can all talk to each other.  To do this, you will need to open up some ports in the firewalls in your network.  The ports used by Clearwater are listed in [Clearwater IP Port Usage](Clearwater_IP_Port_Usage.md).  Configure all of these ports to be open to the appropriate hosts before continuing to the next step.  If you are running on a platform that has multiple physical or virtual interfaces and the option to apply different firewall rules on each, make sure that you open these ports on the correct interfaces.

### Setting up S-CSCF configuration

If I-CSCF functionality is enabled, then you will need to set up the S-CSCF configuration. S-CSCF configuration is stored in the `s-cscf.json` file in `/etc/clearwater` on each sprout node. The file stores the configuration of each S-CSCF, their capabilities, and their relative weighting and priorities.

The file is in stored in JSON format, an example is:

    {
       "s-cscfs" : [
           {   "server" : "sip:<sprout_domain>:5054;transport=TCP",
               "priority" : 0,
               "weight" : 100,
               "capabilities" : [<comma separated capabilities>]
           }
       ]
    }

## Where next?

Once you've reached this point, your Clearwater deployment is ready to handle calls.  See the following pages for instructions on making your first call and running the supplied regression test suite.

* [Making your first call](Making_your_first_call.md)
* [Running the live test suite](Running_the_live_tests.md)

## Larger-Scale Deployments

If you're intending to spin up a larger-scale deployment containing more than one node of each types, it's recommended that you use the [automated install process](Automated_Install.md), as this makes scaling up and down very straight-forward.  If for some reason you can't, you'll need to configure DNS correctly and cluster the nodes in the Sprout, Homestead, Homer and Ralf tiers.

### Configuring DNS

When configuring DNS for a multi-node deployment, it's crucial that

*   each node's `public_hostname` property (in `/etc/clearwater/config`) resolves to an IP address that belongs solely to that node (not to the cluster)
*   the `sprout_hostname`, `hs_hostname`, `ralf_hostname` and `xdms_hostname` properties resolve to the set of all IP addresses in that tier so, for example, the value of `sprout_hostname` resolves to the IP addresses of all sprout nodes.

### Clustering Sprout

Sprout uses [memcached](http://memcached.org) as its registration datastore, and [Chronos](https://github.com/Metaswitch/chronos) as its timer service. After initially installing the Sprout nodes, you must reconfigure them to ensure they cluster together.

To do this for memcached:

*   edit `/etc/clearwater/cluster_settings` file on each node to contain a single line of the form
`servers=<Sprout-1 IP address>:11211,<Sprout-2 IP address>:11211,...` (e.g. `servers=10.0.0.1:11211,10.0.0.2:11211`), ensuring the order of the IP addresses is identical on each node.
*   force Sprout to reload its configuration with `sudo service sprout reload`.

To do this for Chronos, follow the instructions in <https://github.com/Metaswitch/chronos/blob/dev/doc/clustering.md>:

*   edit `/etc/chronos/chronos.conf` to include a node entry for each Sprout node in the cluster.
*   ensure that the `localhost` entry in `/etc/chronos/chronos.conf` is set to the local IP address and not the word 'localhost'.
*   force Chronos to reload its configuration with `sudo service chronos reload`.

If the Sprout nodes include the Memento Application server, then you must reconfigure the Cassandra processes on these nodes to cluster together. To do this, follow the [instructions on the Cassandra website](http://www.datastax.com/documentation/cassandra/1.2/cassandra/initialize/initializeTOC.html).

The clustering process might cause you to lose the memento schema.  To restore it, the simplest process is, on one sprout node, to uninstall memento (using `sudo apt-get purge memento`) and then reinstall it (using `sudo apt-get install memento`).  As part of the installation process, the schema is reinjected into Cassandra.

### Clustering Homestead and Homer

Homestead and homer use [Cassandra](http://cassandra.apache.org/) as their datastore.

After installing the homestead and homer nodes, you must reconfigure the Cassandra processes on these nodes to cluster together.  To do this, follow the [instructions on the Cassandra website](http://www.datastax.com/documentation/cassandra/1.2/cassandra/initialize/initializeTOC.html).  Note that we generally cluster homestead Cassandra instances separately from homer Cassandra instances, rather than as one big cluster.

The clustering process might cause you to lose the homestead or homer schema.  To restore it, the simplest process is, on one homestead node and on one homer node, to uninstall homestead/homer (using `sudo apt-get purge homestead` or `sudo apt-get purge homer`) and then reinstall it (using `sudo apt-get install homestead` or `sudo apt-get install homer`).  As part of the installation process, the schema is reinjected into Cassandra.

### Clustering Ralf

Ralf, like Sprout, uses Memcached as a local data store, with the same support for redundancy and dynamic scaling.  To configure the Memcached cluster,

*   edit `/etc/clearwater/cluster_settings` file on each node to contain a single line of the form
`servers=<Ralf IP address:11211>,<Ralf IP address:11211>,...` ensuring the order of the IP addresses is identical on each node
*   force Ralf to reload its configuration with `sudo service sprout reload`.

Ralf also makes use of the Chronos timer service cluster.  To ensure that the Ralfs are correctly clustered.

*   edit `/etc/chronos/chronos.conf` to include a node entry for each Ralf node in the cluster.
*   ensure that the `localhost` entry in `/etc/chronos/chronos.conf` is set to the local IP address and not the word 'localhost'.
*   force Chronos to reload its configuration with `sudo service chronos reload`.

### Standalone Application Servers

Gemini and Memento can run integrated into the Sprout nodes, or they can be run as standalone application servers.

To install Gemini or Memento as a standalone server, follow the same process as installing a Sprout node. Make sure not to cluster the new standalone Sprout nodes with the existing Sprout nodes, and don't add them to the existing Sprout DNS cluster.

The `sprout_hostname` setting in `/etc/clearwater/config` on standalone application servers should be set to the cluster of the standalone application servers, for example, `memento.cw-ngv.com`.
