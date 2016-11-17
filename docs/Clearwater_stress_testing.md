# Stress Testing

One of Clearwater's biggest strengths is scalability and in order to demonstrate this, we have easy-to-use settings for running large amounts of SIP stress against a deployment.  This document describes:
- Clearwater's SIP stress nodes, what they do, and (briefly) how they work
- how to kick off your own stress test.

## SIP Stress Nodes

A Clearwater SIP stress node is similar to any other Project Clearwater node, except that instead of
having a Debian package like `bono` or `sprout` installed, it has our `clearwater-sip-stress` Debian
package installed.

### What they do

Clearwater SIP stress nodes provide a set of SIPp scripts to run against your Sprout cluster. From Sprout's point of view, they look like a P-CSCF.  The nodes log their success/failure to `/var/log/clearwater-sip-stress` and also print a human-readable summary of the stress (with informatin about percentage of failed calls, average latency, and so on).

They follow a fixed load profile, assuming 1.3 calls/hour for each subscriber (split equally between incoming and outgoing calls) and 2 re-registrations per hour.

## Deploying a stress node

Follow [this process](https://github.com/Metaswitch/crest/blob/dev/docs/Bulk-Provisioning%20Numbers.md) to bulk provision the number of subscribers you want. As a general guideline, we'd expect a small deployment (with one Sprout, Homestead and optionally a Ralf node, each with one full CPU core) to handle at least 50,000 subscribers.

You should also ensure that the `reg_max_expires` setting is set to 1800 rather than the default of 300 - see our [configuration guide](Clearwater_Configuration_Options_Reference.md) for instructions. This matches the assumptions in our load profile of 2 re-registers per hour.

If you're using chef, create your stress test node by typing `knife box create -E ENVIRONMENT sipp --index 1`.

Otherwise, follow these steps to deploy a stress node manually:

* create a new virtual machine and bootstrap it [by configuring access to the Project Clearwater Debian repository](Manual_Install.md#configure-the-apt-software-sources).
* set the following properties in /etc/clearwater/local_config:
    * (required) local_ip - the local IP address of this node
    * (optional) node_idx - the node index (defaults to 1)
* run `sudo apt-get install clearwater-sip-stress` to install the Debian package.

The stress node needs to be able to open connections to Sprout on TCP ports 5052 and 5054, and Sprout needs to be able to open connections to the stress node on port 5082.

## Running stress

To kick off a stress run, simply run: `/usr/share/clearwater/bin/run_stress <home_domain> <number of subscribers> <number of minutes>`. 

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

### Extra run_stress options

The run-stress script has some command-line options:

* `--initial-reg-rate` - this controls how many REGISTERs/second the script sends in during the initial registration phase (defaulting to 80). On systems that can cope with the load, raising this value will let the test run start faster.
* `--sipp-output` - By default, the script hides the SIPp outputand just presents the end-of-run stats. With this option, it will show the SIPp output screen, which may be useful for users familiar with SIPp.
* `--target TARGET` - Domain/IP and port to target stress at. Default is sprout.{domain}, with I-CSCF traffic going to port 5052 and S-CSCF traffic to port 5054.

## Restrictions

* The clearwater-sip-stress package currently only targets load at one Sprout node - we're planning to add support for load-balancing in the future.
* The clearwater-sip-stress package acts as a P-CSCF, which means it drives load through Sprout (and therefore through things upstream of Sprout, like Homestead). We don't have tools for stress-testing Bono, because we don't recommend it for production traffic, and it hasn't gone through the same level of testing and hardening that the core Sprout, Homestead and Ralf components have.
* The summary statistics at the end just come from SIPp, not the Clearwater deployment. If you want to monitor Sprout CPU during the stress run, you'll need to be running a separate monitoring tool suchas Cacti (and we provide the start and end time of the stress run, to let you match up with these external graphs).
