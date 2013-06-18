One of Clearwater's biggest strengths is scalability and in order to demonstrate this, we have easy-to-use settings for running large amounts of SIP stress against a deployment.  This document describes:
* Clearwater's SIP stress nodes, what they do, and (briefly) how they work
* how to kick off your own stress test.

## SIP Stress Nodes
### What they do

Clearwater SIP stress nodes run a standard SIPp script against your bono cluster.  The bono nodes translate this into traffic for sprout and this generates traffic on homestead and homer.  The nodes log their success/failure to `/var/log/clearwater-sip-stress` and also restart SIPp (after a 30s cool-down) if anything goes wrong.

The SIPp stress starts as soon as the node comes up - this is by design, to avoid you having to manually start 50+ nodes generating traffic.  If you want to stop them from generating traffic, turn the whole node down.

Each SIP stress node picks a single bono to generate traffic against.  This bono is chosen by matching the bono node's index against the SIP stress node's index.  As a result, it's important to always give SIP stress nodes an index.

### How they work

The clearwater-sip-stress package includes two important scripts.

* `/etc/clearwater/scripts/sip-stress`, which generates a `/usr/share/clearwater/sip-stress/users.csv` file containing the list of all subscribers we should be targeting - these are calculated from properties in `/etc/clearwater/config`.
* `/etc/init.d/clearwater-sip-stress`, which runs `/usr/share/clearwater/bin/sip-stress`, which in turn runs SIPp specifying `/usr/share/clearwater/sip-stress/call_load2.xml` as its test script. This test script simulates a pair of subscribers registering every 5 minutes and then making a call every 30 minutes.

## Running Stress

This section describes step-by-step how to run stress.  It includes setting up a new deployment.  It is possible to run stress against an existing deployment but you'll need to reconfigure some things so it's easier just to tear down your existing deployment and start again.

1.  If you haven't done so already, set up chef/knife (as described in [the install guide](https://github.com/Metaswitch/clearwater-docs/wiki/Automated%20Install)).
2.  cd to your chef directory.
3.  Edit your environment (e.g. `environments/stress-test-env.rb`) to override attributes as follows.

    For example (replacing ENVIRONMENT with your environment name and DOMAIN with your Route 53-hosted root domain):

```
    name "ENVIRONMENT"
    description "Stress testing environment"
    cookbook_versions "clearwater" => "= 0.1.0"
    override_attributes "clearwater" => {
        "root_domain" => "DOMAIN",
        "availability_zones" => ["us-east-1a"],
        "repo_server" => "http://repo.cw-ngv.com/latest",
        "number_start" => "2010000000",
        "number_count" => 1000,
        "pstn_number_count" => 0,
        "enum_server" => "enum.ENVIRONMENT.DOMAIN"}
```

4.  Upload your new environment to the chef server by typing `knife environment from file environments/ENVIRONMENT.rb`
5. Create the deployment by typing `knife deployment resize -E stress-test-env`.  If you want more nodes, supply parameters such "--bono-count 5" or "--sprout-count 3" to control this.
6. Follow [this process](https://github.com/Metaswitch/crest/blob/dev/docs/Bulk-Provisioning%20Numbers.md) to bulk provision subscribers. Create 100,000 subscribers per SIPp node.
7. Create an ENUM server.  You need a dedicated ENUM server because the DN range that stress tests use needs to be routed back to your own deployment.  To create an ENUM server, type `knife box create -E ENVIRONMENT enum --index 1`.
8. Add a DNS entry for the ENUM server - `knife dns record create -E ENVIRONMENT enum -z DOMAIN -T A --local enum -p ENVIRONMENT`.
9. Create your stress test node by typing `knife box create -E ENVIRONMENT sipp --index 1`.  If you have multiple bono nodes, you'll need to create multiple stress test nodes by repeating this command with "--index 2", "--index 3", etc. - each stress test node only sends traffic to the bono with the same index.
  * To create multiple nodes, try `for x in {1..20} ; do { knife box create -E ENVIRONMENT sipp --index $x && sleep 2 ; } ; done`.
10. Create a Cacti server for monitoring the deployment, as described in [this document](https://github.com/Metaswitch/clearwater-docs/wiki/Cacti).
11. When you've finished, destroy your deployment with `knife deployment delete -E ENVIRONMENT`.

### Manual (i.e. non-Chef) stress runs

SIP stress nodes can be created manually, instead of via Chef in the process above. To do this, set the following properties in /etc/clearwater/config and install the clearwater-sip-stress Debian package:

* (optional) node_idx - the node index (defaults to 1)
* (optional) bono_servers - a list of bono servers in this deployment
* (optional) stress_target - the target host (defaults to the $node_idx-th entry in $bono_servers or, if there are no $bono_servers, defaults to $home_realm)
* (optional) base - the base directory number (defaults to 2010000000)
* (optional) count - the number of calls to run on this node (defaults to 50000) - note that the SIPp script simulates 2 subscribers per "call".

### Configuring UDP Stress

SIPp supports UDP stress, and this works with Clearwater.  To make a stress test node run UDP stress (rather than the default of TCP)

* open /usr/share/clearwater/bin/sip-stress
* find the line that begins "nice -n-20 /usr/share/clearwater/bin/sipp"
* replace "-t tn" with "-t un"
* save and exit
* restart stress by typing "sudo service clearwater-sip-stress restart".