# Manual Install Instructions

These instructions will take you through installing a minimal Clearwater system using the latest binary packages provided by the Clearwater project.  For a high level look at the install process, and a discussion of alternative install methods, see [Installation Instructions](Installation_Instructions.md).

## Prerequisites

Before starting this process you will need the following:

* Six machines running clean installs of [Ubuntu 14.04 - 64bit server edition](http://releases.ubuntu.com/trusty/).
    * The software has been tested on Amazon EC2 `t2.small` instances (i.e. 1 vCPU, 2 GB RAM), so any machines at least as powerful as one of them will be sufficient.
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

* Ellis
* Bono
* Sprout
* Homer
* Dime
* Vellum

## Firewall configuration

We need to make sure the Clearwater nodes can all talk to each other.  To do this, you will need to open up some ports in the firewalls in your network.  The ports used by Clearwater are listed in [Clearwater IP Port Usage](Clearwater_IP_Port_Usage.md). Configure all of these ports to be open to the appropriate hosts before continuing to the next step.  If you are running on a platform that has multiple physical or virtual interfaces and the option to apply different firewall rules on each, make sure that you open these ports on the correct interfaces.

## Create the per-node configuration.

On each machine create the file `/etc/clearwater/local_config` with the following contents.

    local_ip=<privateIP>
    public_ip=<publicIP>
    public_hostname=<hostname>
    etcd_cluster="<comma separated list of private IPs>"

Note that the `etcd_cluster` variable should be set to a comma separated list that contains the private IP address of the nodes you created above. For example if the nodes had addresses 10.0.0.1 to 10.0.0.6, `etcd_cluster` should be set to `"10.0.0.1,10.0.0.2,10.0.0.3,10.0.0.4,10.0.0.5,10.0.0.6"`

If you are creating a [geographically redundant deployment](Geographic_redundancy.md), then:

* `etcd_cluster` should contain the IP addresses of nodes only in the local site
*  You should set `local_site_name` in `/etc/clearwater/local_config`. The name you choose is arbitrary, but must be the same for every node in the site. This name will also be used in the `remote_site_names`, `sprout_registration_store`, `homestead_impu_store` and `ralf_session_store` configuration options set in shared config (desscribed below).
*  If your deployment uses Homestead-Prov, Homer or Memento:
    * on the first Vellum node in the second site, you should set `remote_cassandra_seeds` to the IP address of a Vellum node in the first site.

## Install Node-Specific Software

`ssh` onto each box in turn and follow the appropriate instructions below according to the role the node will take in the deployment:

### Ellis

Install the Ellis package with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install ellis --yes
    sudo DEBIAN_FRONTEND=noninteractive apt-get install clearwater-management --yes

### Bono

Install the Bono and Restund packages with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install bono restund --yes
    sudo DEBIAN_FRONTEND=noninteractive apt-get install clearwater-management --yes

### Sprout

Install the Sprout package with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install sprout --yes
    sudo DEBIAN_FRONTEND=noninteractive apt-get install clearwater-management --yes


If you want the Sprout nodes to include a Memento Application server, then install the Memento packages with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install memento-as memento-nginx --yes

### Homer

Install the Homer packages with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install homer --yes
    sudo DEBIAN_FRONTEND=noninteractive apt-get install clearwater-management --yes

### Dime

Install the Dime package with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install dime clearwater-prov-tools --yes
    sudo DEBIAN_FRONTEND=noninteractive apt-get install clearwater-management --yes

### Vellum

Install the Vellum packages with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install vellum --yes
    sudo DEBIAN_FRONTEND=noninteractive apt-get install clearwater-management --yes

If you included the Memento Application server on your Sprout nodes, then also install the required packages on Vellum with:

    sudo DEBIAN_FRONTEND=noninteractive apt-get install memento-cassandra --yes

## SNMP statistics

Sprout, Bono, Vellum and Dime nodes expose statistics over SNMP. This function is not installed by default. If you want to enable it follow the instruction in [our SNMP documentation](Clearwater_SNMP_Statistics.md).

## Provide Shared Configuration

Log onto any node in the deployment and run `cw-config download shared_config`. This will download the current `shared_config` in use by your deployment. Edit the downloaded file to add the following contents. The `site_name` should match the value of `local_site_name` in `local_config`; if your deployment is not geographically redundant then you don't need to include it.

    # Deployment definitions
    home_domain=<zone>
    sprout_hostname=sprout.<site_name>.<zone>
    sprout_registration_store=vellum.<site_name>.<zone>
    hs_hostname=hs.<site_name>.<zone>:8888
    hs_provisioning_hostname=hs.<site_name>.<zone>:8889
    homestead_impu_store=vellum.<zone>
    ralf_hostname=ralf.<site_name>.<zone>:10888
    ralf_session_store=vellum.<zone>
    xdms_hostname=homer.<site_name>.<zone>:7888
    chronos_hostname=vellum.<site_name>.<zone>
    cassandra_hostname=vellum.<site_name>.<zone>

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

If you wish to enable the optional external HSS lookups, add the following:

    # HSS configuration
    hss_hostname=<address of your HSS>
    hss_port=3868

If you want to host multiple domains from the same Clearwater deployment, add the following (and configure DNS to route all domains to the same servers):

    # Additional domains
    additional_home_domains=<domain 1>,<domain 2>,<domain 3>...

If you want your Sprout nodes to include Gemini/Memento Application Servers add the following:

    # Application Servers
    gemini=<gemini port>
    memento=<memento port>
    memento_auth_store=vellum.<site_name>.<zone>

See the [Chef instructions](Installing_a_Chef_workstation.md#add-deployment-specific-configuration) for more information on how to fill these in. The values marked `<secret>` **must** be set to secure values to protect your deployment from unauthorized access. To modify these settings after the deployment is created, follow [these instructions](Modifying_Clearwater_settings.md).

If you are creating a [geographically redundant deployment](Geographic_redundancy.md), some of the options require information about all sites to be specified. You need to set the `remote_site_names` configuration option to include the `local_site_name` of each site, replace the `sprout_registration_store`, `homestead_impu_store` and `ralf_session_store` with the values as described in [Clearwater Configuration Options Reference](Clearwater_Configuration_Options_Reference.md), and set the `sprout_chronos_callback_uri` and `ralf_chronos_callback_uri` to deployment wide hostnames. For example, for sites named `siteA` and `siteB`:

    remote_site_names=siteA,siteB
    sprout_registration_store="siteA=vellum-siteA.<zone>,siteB=vellum-siteB.<zone>"
    homestead_impu_store="siteA=vellum-siteA.<zone>,siteB=vellum-siteB.<zone>"
    ralf_session_store="siteA=vellum-siteA.<zone>,siteB=vellum-siteB.<zone>"
    sprout_chronos_callback_uri=sprout.<zone>
    ralf_chronos_callback_uri=ralf.<zone>

Now run the following to upload the configuration to a shared database and propagate it around the cluster (see [Modifying Clearwater settings](Modifying_Clearwater_settings.md) for more details on this).

    sudo cw-config upload shared_config

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

Clearwater uses DNS records to allow each node to find the others it needs to talk to to carry calls.  At this point, you should create the DNS entries for your deployment before continuing to the next step.  [Clearwater DNS Usage](Clearwater_DNS_Usage.md) describes the entries that are required before Clearwater will be able to carry service.

Although not required, we also suggest that you configure individual DNS records for each of the machines in your deployment to allow easy access to them if needed.

_Be aware that DNS record creation can take time to propagate, you can check whether your newly configured records have propagated successfully by running `dig <record>` on each Clearwater machine and checking that the correct IP address is returned._

If you are creating a [geographically redundant deployment](Geographic_redundancy.md), you will also need to set up some DNS overrides. This allow a single hostname to be used across the deployment which can then be resolved to a site specific hostname at the point of use. This is necessary for Chronos and I-CSCF processing:

* Chronos: When a client sets a timer on Chronos, it provides a URI that Chronos can use to inform the client that the timer has popped. This URI should resolve to the clients in the same site as where the timer popped, but the timer could pop in any site.
* I-CSCF: The HSS stores the S-CSCF name. When the I-CSCF learns the S-CSCF name it wants to contact the S-CSCF in the local site, but the HSS will return the same S-CSCF name to the I-CSCFs in different sites.

Details for how to set up this DNS override are detailed [here](Modifying_Clearwater_settings.md), and an example of the JSON file (for siteA) required for a GR deployment with two sites (siteA and siteB) is below:

```
{
  "hostnames": [
    {
      "name": "sprout.<zone>",
      "records": [{"rrtype": "CNAME", "target": "sprout.siteA.<zone>"}]
    },
    {
      "name": "scscf.sprout.<zone>",
      "records": [{"rrtype": "CNAME", "target": "scscf.sprout.siteA.<zone>"}]
    },
    {
      "name": "ralf.<zone>",
      "records": [{"rrtype": "CNAME", "target": "ralf.siteA.<zone>"}]
    }
  ]
}
```

## Chronos configuration

Vellum nodes run the Chronos process, which is our distributed, redundant, reliable timer service (more information [here](https://github.com/Metaswitch/chronos/tree/stable)). Chronos has three types of configuration; configuration that is local to an individual Chronos proces, configuration that covers how a Chronos process clusters with other Chronos processes in the same site, and configuration that covers how a Chronos cluster connects to Chronos clusters in different sites. You don't typically need to set up the first two types of configuration, this is handled automatically. If you are creating a [geographically redundant deployment](Geographic_redundancy.md), you do need to add the GR configuration for Chronos on each Vellum node - details of how to do this are [here](https://github.com/Metaswitch/chronos/blob/stable/doc/configuration.md).

## Where next?

Once you've reached this point, your Clearwater deployment is ready to handle calls.  See the following pages for instructions on making your first call and running the supplied regression test suite.

* [Making your first call](Making_your_first_call.md)
* [Running the live test suite](Running_the_live_tests.md)

## Larger-Scale Deployments

If you're intending to spin up a larger-scale deployment containing more than one node of each types, it's recommended that you use the [automated install process](Automated_Install.md), as this makes scaling up and down very straight-forward.  If for some reason you can't, you can add nodes to the deployment using the [Elastic Scaling Instructions](Clearwater_Elastic_Scaling.md)

### Standalone IMS components and Application Servers

Our IMS components (I-CSCF, S-CSCF, ...) and application servers (Gemini, Memento, ...) can run on the same Sprout node, or they can be run as separate compoments/standalone application servers.

To install a standalone IMS component/application server, you need to:
* Install a Sprout node (following the same process as installing a Sprout node above), but don't add the new node to the Sprout DNS cluster.
* Enable/disable the sproutlets you want to run on this node - see [here](http://clearwater.readthedocs.io/en/latest/Clearwater_Configuration_Options_Reference.html#sproutlet-options) for more details on this. In particular, you should set the ports and the URIs of the sproutlets.
* Once the node is fully installed, add it to the relevant DNS records.

### I-CSCF configuration

The I-CSCF is responsible for sending requests to the correct S-CSCF. It queries the HSS, but if the HSS doesn't have a configured S-CSCF for the subscriber then it needs to select an S-CSCF itself. The I-CSCF defaults to selecting the Clearwater S-CSCF (as configured in `scscf_uri` in `/etc/clearwater/shared/config`).

You can configure what S-CSCFs are available to the I-CSCF by editing the `/etc/clearwater/s-cscf.json` file.

This file stores the configuration of each S-CSCF, their capabilities, and their relative weighting and priorities. The format of the file is as follows:

    {
       "s-cscfs" : [
           {   "server" : "<S-CSCF URI>",
               "priority" : <priority>,
               "weight" : <weight>,
               "capabilities" : [<comma separated capabilities>]
           }
       ]
    }

The S-CSCF capabilities are integers, and their meaning is defined by the operator. Capabilities will have different meanings between networks.

As an example, say you have one S-CSCF that supports billing, and one that doesn't. You can then say that capability 1 is the ability to provide billing, and your s-cscf.json file would look like:

    {
       "s-cscfs" : [
           {   "server" : "sip:scscf1",
               "priority" : 0,
               "weight" : 100,
               "capabilities" : [1]
           },
           {   "server" : "sip:scscf2",
               "priority" : 0,
               "weight" : 100,
               "capabilities" : []
           }
       ]
    }

Then when you configure a subscriber in the HSS, you can set up what capabilities they require in an S-CSCF. These will also be integers, and you should make sure this matches with how you've set up the s-cscf.json file. In this example, if you wanted your subscriber to be billed, you would configure the user data in the HSS to make it mandatory for your subscriber to have an S-CSCF that supports capability 1.

To change the I-CSCF configuration, edit this file on any Sprout node, then upload it to the shared configuration database by running `sudo cw-upload_scscf_json`.

### Shared iFC configuration

If the configuration option `request_shared_ifcs` is set to 'Y', the S-CSCF must be configured with any Shared iFC sets that may be sent to it by the HSS.

You can configure Shared iFC sets on the S-CSCF by editing the `/etc/clearwater/shared_ifcs.xml` file.

This file stores the iFCs in each Shared iFC set. The format of the file is as follows:

    <?xml version="1.0" encoding="UTF-8"?>
    <SharedIFCsSets>
      <SharedIFCsSet>
        <SetID>  <set id>  </SetID>
        <InitialFilterCriteria>
          <iFC>
        </InitialFilterCriteria>
        <InitialFilterCriteria>
          <iFC>
        </InitialFilterCriteria>
      </SharedIFCsSet>
    </SharedIFCsSets>

The `set id` is an integer, and each Shared iFCs set must have a unique `set id`.

The `iFC` is an iFC, in XML format.

There must be exactly one `SharedIFCsSets` element, which can contain multiple `SharedIFCsSet` elements (the minimum number of `SharedIFCsSet` elements is zero).

Each `SharedIFCsSet` element can contain multiple `InitialFilterCriteria` elements (the minimum number of `InitialFilterCriteria` elements is zero), and must contain exactly one unique `SetID` element.

To change the Shared iFC configuration, edit this file on any Sprout node, then upload it to the shared configuration database by running `sudo cw-upload_shared_ifcs_xml`.

To validate the Shared iFC configuration file before uploading it, run the command `cw-validate_shared_ifcs_xml <file_location>` on the Sprout node the file is present on.

To remove the Shared iFC configuration, run the command `sudo cw-remove_shared_ifcs_xml` on any Sprout node.

To view the Shared iFCs being used on any Sprout node, run the command `cw-display_shared_ifcs` on that Sprout node.

### Fallback iFC configuration

If you wish to apply iFCs to any subscribers who have no iFCs triggered on a request (e.g. as a fallback to catch misconfigured subscribers), these iFCs must be configured on the S-CSCF, and the configuration option `apply_fallback_ifcs` set to 'Y'.

You can configure fallback iFCs on the S-CSCF by editing the `/etc/clearwater/fallback_ifcs.xml` file.

This file stores a list of fallback iFCs. The format of the file is as follows:

    <?xml version="1.0" encoding="UTF-8"?>
    <FallbackIFCsSet>
      <InitialFilterCriteria>
        <iFC>
      </InitialFilterCriteria>
    </FallbackIFCsSet>

The `iFC` is an iFC, in XML format.

There must be exactly one `FallbackIFCsSet` element, which can can contain multiple `InitialFilterCriteria` elements (the minimum number of `InitialFilterCriteria` elements is zero).

To change the fallback iFC configuration, edit this file on any Sprout node, then upload it to the shared configuration database by running `sudo cw-upload_fallback_ifcs_xml`.

To validate the fallback iFC configuration file before uploading it, run the command `cw-validate_fallback_ifcs_xml <file_location>` on the Sprout node the file is present on.

To remove the fallback iFC configuration, run the command `sudo cw-remove_fallback_ifcs_xml` on any Sprout node.

To view the Fallback iFCs being used on any Sprout node, run the command `cw-display_fallback_ifcs` on that Sprout node.
