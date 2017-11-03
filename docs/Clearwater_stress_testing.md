# Stress Testing

One of Clearwater's biggest strengths is scalability and in order to demonstrate this, we have easy-to-use settings for running large amounts of SIP stress against a deployment.  This document describes:

- Clearwater's SIP stress nodes, what they do, and (briefly) how they work
- how to kick off your own stress test.

## SIP Stress Nodes

A Clearwater SIP stress node is similar to any other Project Clearwater node, except that instead of having a Debian package like `bono` or `sprout` installed, it has our `clearwater-sip-stress-coreonly` or `clearwater-sip-stress` Debian package installed.

### What they do

Clearwater SIP stress nodes provide a set of SIPp scripts to run against your Sprout cluster. There are two kinds of stress available:

* Our recommended approach is to use scripts which emulate a P-CSCF and send traffic to Sprout, stress testing the IMS Core directly.  The nodes log their success/failure to `/var/log/clearwater-sip-stress` and also print a human-readable summary of the stress (with information about percentage of failed calls, average latency, and so on).
* We also have some older scripts which emulate UEs and send traffic to Bono, stress testing the P-CSCF and the IMS Core together.  The nodes log their success/failure to `/var/log/clearwater-sipp`, but unlike the other scripts, do not print a human-readable summary of the stress.

## Deploying a stress node

These instructions assume you've already [installed a Clearwater deployment](Installation_Instructions.md), either manually or through Chef.

Follow [this process](https://github.com/Metaswitch/crest/blob/dev/docs/Bulk-Provisioning%20Numbers.md) to bulk provision the number of subscribers you want. As a general guideline, we'd expect a small deployment (with one Sprout, Vellum and Dime, each with one full CPU core) to handle at least 30,000 subscribers.

You should also ensure that the `reg_max_expires` setting is set to 1800 rather than the default of 300 - see our [configuration guide](Clearwater_Configuration_Options_Reference.md) for instructions. This matches the assumptions in our load profile of 2 re-registers per hour.

### Chef

If you're using Chef to automate your Clearwater install, create your stress test node by typing `knife box create -V -E ENVIRONMENT sipp --index 1`.

### Manual install

Otherwise, follow these steps to deploy a stress node manually:

* create a new virtual machine and bootstrap it [by configuring access to the Project Clearwater Debian repository](Manual_Install.md#configure-the-apt-software-sources).
* set the following property in `/etc/clearwater/local_config`:
    * `local_ip` - the local IP address of this node
* for our recommended scripts which send stress to Sprout, run `sudo apt-get install clearwater-sip-stress-coreonly` to install the Debian packages.
* for our older scripts which send stress to Bono, run `sudo apt-get install clearwater-sip-stress` to install the Debian packages.

The stress node needs to be able to open connections to Sprout on TCP ports 5052 and 5054, and Sprout needs to be able to open connections to the stress node on TCP port 5082.

## Running stress (IMS core only)

To kick off a stress run, simply run: `/usr/share/clearwater/bin/run_stress <home_domain> <number of subscribers> <duration in minutes>`.

The script will then:

* set up the stress test by sending an initial register for all the subscribers
* report that that initial registration has completed and that the stress test is starting
* send traffic, using a fixed load profile of 1.3 calls/hour for each subscriber (split equally between incoming and outgoing calls) and 2 re-registrations per hour
* after the given duration, wait for all calls to finish and then exit
* print summary output about how the test went

The output will be in this format:

```
Starting initial registration, will take 6 seconds
Initial registration succeeded
Starting test
Test complete

Elapsed time: 00:15:07
Start: 2016-11-16 15:03:29.062755
End: 2016-11-16 15:18:36.414653

Total calls: 1625
Successful calls: 1612 (99.2%)
Failed calls: 13 (0.8%)

Retransmissions: 0

Average time from INVITE to 180 Ringing: 74.0 ms
# of calls with 0-2ms from INVITE to 180 Ringing: 0 (0.0%)
# of calls with 2-20ms from INVITE to 180 Ringing: 0 (0.0%)
# of calls with 20-200ms from INVITE to 180 Ringing: 1572 (96.7384615385%)
# of calls with 200-2000ms from INVITE to 180 Ringing: 45 (2.76923076923%)
# of calls with 2000+ms from INVITE to 180 Ringing: 0 (0.0%)

Total re-REGISTERs: 1800
Successful re-REGISTERs: 1792 (99.5555555556%)
Failed re-REGISTERS: 8 (0.444444444444%)

REGISTER retransmissions: 0

Average time from REGISTER to 200 OK: 15.0 ms

Log files in /var/log/clearwater-sip-stress
```

The summary statistics at the end just come from SIPp, not the Clearwater deployment. If you want to see [our more detailed statistics](Clearwater_SNMP_Statistics.md), you'll need to be running a separate monitoring tool such as [Cacti](Cacti.md) (and we provide the start and end time of the stress run, to let you match up with these external graphs).

### Extra run_stress options

The run-stress script has some command-line options:

* `--initial-reg-rate` - this controls how many REGISTERs/second the script sends in during the initial registration phase (defaulting to 80). On systems that can cope with the load, raising this value will let the test run start faster.
* `--sipp-output` - By default, the script hides the SIPp output and just presents the end-of-run stats. With this option, it will show the SIPp output screen, which may be useful for users familiar with SIPp.
* `--icscf-target TARGET` - Domain/IP and port to target registration stress at. Default is `sprout.{domain}:5052`.
* `--scscf-target TARGET` - Domain/IP and port to target call stress at. Default is `sprout.{domain}:5054`.

## Running stress (IMS core and P-CSCF)

In this mode, each SIP stress node picks a single bono to generate traffic against. This bono is chosen by matching the bono node’s index against the SIP stress node’s index.

This test includes two important scripts.

* `/usr/share/clearwater/infrastructure/scripts/sip-stress`, which generates a `/usr/share/clearwater/sip-stress/users.csv.1` file containing the list of all subscribers we should be targeting - these are calculated from properties in `/etc/clearwater/shared_config`.
* `/etc/init.d/clearwater-sip-stress`, which runs `/usr/share/clearwater/bin/sip-stress`, which in turn runs SIPp specifying `/usr/share/clearwater/sip-stress/sip-stress.xml` as its test script. This test script simulates a pair of subscribers registering every 5 minutes and then making a call every 30 minutes.

The stress test logs to `/var/log/clearwater-sip-stress/sipp.<index>.out`.

There is some extra configuration needed in this mode, so you should:

* set the following properties in `shared_config`:
    * (required) `home_domain` - the home domain of the deployment under test
    * (optional) `bono_servers` - a list of bono servers in this deployment
    * (optional) `stress_target` - the target host (defaults to the `node_idx`-th entry in `bono_servers` or, if there are no `bono_servers`, defaults to `home_domain`)
    * (optional) `base` - the base directory number (defaults to 2010000000)
    * (optional) `count` - the number of subscribers to run on this node (must be even, defaults to 30000)
* optionally, set the following property in `/etc/clearwater/local_config`:
    * node_idx - the node index (defaults to 1)

To apply this config and start stress, run `sudo /usr/share/clearwater/infrastructure/scripts/sip-stress` and `sudo service clearwater-sip-stress restart`.
