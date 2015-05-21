# Manual Install Instructions

These instructions will take you through installing a minimal Clearwater system using the latest binary packages provided by the Clearwater project.  For a high level look at the install process, and a discussion of alternative install methods, see [Installation Instructions](Installation_Instructions).

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

## Configure the APT software sources

Configure each machine so that APT can use the Clearwater repository server.

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

Once the above steps have been performed, run the following to re-index your package manager:

    sudo apt-get update

## Determine Machine Roles

At this point, you should decide (if you haven't already) which of the six machines will take on which of the Clearwater roles.

The six roles are:

* ellis
* bono - This role also hosts a restund STUN server
* sprout
* homer
* homestead
* ralf

## Firewall configuration

We need to make sure the Clearwater nodes can all talk to each other.  To do this, you will need to open up some ports in the firewalls in your network.  The ports used by Clearwater are listed in [Clearwater IP Port Usage](Clearwater_IP_Port_Usage).  Configure all of these ports to be open to the appropriate hosts before continuing to the next step.  If you are running on a platform that has multiple physical or virtual interfaces and the option to apply different firewall rules on each, make sure that you open these ports on the correct interfaces.

## Create the per-node configuration.

On each machine create the file `/etc/clearwater/local_config` with the following contents.

    local_ip=<privateIP>
    public_ip=<publicIP>
    public_hostname=<hostname>
    etcd_cluster="<comma separated list of private IPs>"

Note that the `etcd_cluster` variable should be set to a comma separated list that contains the private IP address of the nodes you created above. For example if the nodes had addresses 10.0.0.1 to 10.0.0.6, `etcd_cluster` should be set to `"10.0.0.1,10.0.0.2,10.0.0.3,10.0.0.4,10.0.0.5,10.0.0.6"`

Also create the file `/etc/clearwater/config` with the following contents:

    source /etc/clearwater/shared_config
    source /etc/clearwater/local_config
    [ -f /etc/clearwater/user_settings ] && source /etc/clearwater/user_settings

If this machine will be a Sprout or Ralf node create the file `/etc/chronos/chronos.conf` with the following contents:

    [http]
    bind-address = <privateIP>
    bind-port = 7253
    threads = 50

    [logging]
    folder = /var/log/chronos
    level = 2

    [alarms]
    enabled = true

    [exceptions]
    max_ttl = 600

## Install Clearwater Management Services

Run the following command on each node to install the Clearwater management services.

    sudo apt-get install clearwater-cluster-manager clearwater-config-manager

## Install Node-Specific Software

`ssh` onto each box in turn and follow the appropriate instructions below according to the role the node will take in the deployment:

### Ellis

Install the Ellis package with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install ellis --yes

### Bono

Install the Bono and Restund packages with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install bono restund --yes

### Sprout

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

Install the Ralf package with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install ralf --yes

## SNMP statistics

Sprout, Bono and Homestead nodes expose statistics over SNMP. This function is not installed by default. If you want to enable it follow the instruction in [our SNMP documentation](Clearwater_SNMP_Statistics).

## Provide Shared Configuration

Log onto any node in the deployment and create the file `/etc/clearwater/shared_config` with the following contents:

    # Deployment definitions
    home_domain=<zone>
    sprout_hostname=sprout.<zone>
    hs_hostname=hs.<zone>:8888
    hs_provisioning_hostname=hs.<zone>:8889
    ralf_hostname=ralf.<zone>:10888
    xdms_hostname=homer.<zone>:7888

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

See the [Chef instructions](Installing_a_Chef_client#add-deployment-specific-configuration) for more information on how to fill these in. The values marked `<secret>` **must** be set to secure values to protect your deployment from unauthorized access. To modify these settings after the deployment is created, follow [these instructions](Modifying_Clearwater_settings).

Now run `/usr/share/clearwater/clearwater-config-manager/scripts/upload_shared_config`. This uploads the configuration to a shared database and propagates it around the cluster.

### Setting up S-CSCF configuration

If I-CSCF functionality is enabled, then you will need to set up the S-CSCF configuration. S-CSCF configuration is stored in the `/etc/clearwater/s-cscf.json` file on each sprout node. The file stores the configuration of each S-CSCF, their capabilities, and their relative weighting and priorities.

If you require I-CSCF functionality, log onto your sprout node and create `/etc/clearwater/s-cscf.josn` with the following contents:

    {
       "s-cscfs" : [
           {   "server" : "sip:<sprout_domain>:5054;transport=TCP",
               "priority" : 0,
               "weight" : 100,
               "capabilities" : [<comma separated capabilities>]
           }
       ]
    }

Then upload it to the shared configuration database by running `/usr/share/clearwater/bin/upload_s-cscf_json`. This means that any sprout nodes that you add to the cluster will automatically learn the configuration.

## Provision Telephone Numbers in Ellis

Log onto you Ellis node and provision a pool of numbers in Ellis.  The command given here will generate 1000 numbers starting at `sip:6505550000@<zone>`, meaning none of the generated numbers will be routable outside of the Clearwater deployment.  For more details on creating numbers, see the [create_numbers.py documentation](https://github.com/Metaswitch/ellis/blob/dev/docs/create-numbers.md).

    sudo bash -c "export PATH=/usr/share/clearwater/ellis/env/bin:$PATH ;
                  cd /usr/share/clearwater/ellis/src/metaswitch/ellis/tools/ ;
                  python create_numbers.py --start 6505550000 --count 1000"

On success, you should see some output from python about importing eggs and then the following.

    Created 1000 numbers, 0 already present in database

This command is idempotent, so it's safe to run it multiple times.  If you've run it once before, you'll see the following instead.

    Created 0 numbers, 1000 already present in database

## DNS Records

Clearwater uses DNS records to allow each node to find the others it needs to talk to to carry calls.  At this point, you should create the DNS entries for your deployment before continuing to the next step.  [Clearwater DNS Usage](Clearwater_DNS_Usage) describes the entries that are required before Clearwater will be able to carry service.

Although not required, we also suggest that you configure individual DNS records for each of the machines in your deployment to allow easy access to them if needed.

_Be aware that DNS record creation can take time to propagate, you can check whether your newly configured records have propagated successfully by running `dig <record>` on each Clearwater machine and checking that the correct IP address is returned._

## Where next?

Once you've reached this point, your Clearwater deployment is ready to handle calls.  See the following pages for instructions on making your first call and running the supplied regression test suite.

* [Making your first call](Making_your_first_call)
* [Running the live test suite](Running_the_live_tests)

## Larger-Scale Deployments

If you're intending to spin up a larger-scale deployment containing more than one node of each types, it's recommended that you use the [automated install process](Automated_Install), as this makes scaling up and down very straight-forward.  If for some reason you can't, you can add nodes to the deployment using the [Elastic Scaling Instructions](Clearwater_Elastic_Scaling.md)

### Standalone Application Servers

Gemini and Memento can run integrated into the Sprout nodes, or they can be run as standalone application servers.

To install Gemini or Memento as a standalone server, follow the same process as installing a Sprout node, but don't add them to the existing Sprout DNS cluster.

The `sprout_hostname` setting in `/etc/clearwater/shared_config` on standalone application servers should be set to the cluster of the standalone application servers, for example, `memento.cw-ngv.com`.
