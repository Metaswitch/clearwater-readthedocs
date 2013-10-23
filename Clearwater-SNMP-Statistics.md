Clearwater provides a set of statistics about the performance of each Clearwater nodes over SNMP. Currently (as of release 33) this is only available on Bono and Sprout nodes.

## Configuration

These SNMP statistics require the clearwater-snmp-handler-bono or clearwater-snmp-handler-sprout packages to be installed for Bono and Sprout nodes respectively. These packages will be automatically installed when installing through the Chef automation system; for a manual install, you will need to run `sudo apt-get install clearwater-snmp-handler-bono` on Bono nodes and `clearwater-snmp-handler-sprout` on Sprout nodes.

## Usage

Clearwater nodes provide SNMP statistics over port 161.

### Bono statistics

Bono nodes provide the following statistics:

* The standard SNMP CPU and memory usage statistics (see http://net-snmp.sourceforge.net/docs/mibs/ucdavis.html for details)
* The average latency, variance, highest call latency and lowest call latency (all in microseconds) seen over the past five minutes.
* The number of parallel TCP connections to each Sprout node.


### Sprout statistics

Sprout nodes provide the following statistics:

* The standard SNMP CPU and memory usage statistics (see http://net-snmp.sourceforge.net/docs/mibs/ucdavis.html for details)
* The average latency, variance, highest call latency and lowest call latency (all in microseconds) seen over the past five minutes.
* The average latency, variance, highest latency and lowest latency (all in microseconds) seen on the Cx interface over the past five minutes.
* The average latency, variance, highest latency and lowest latency (all in microseconds) seen on Multimedia-Auth Requests on the Cx interface over the past five minutes.
* The average latency, variance, highest latency and lowest latency (all in microseconds) seen on Server-Assignment Requests on the Cx interface over the past five minutes.
* The average latency, variance, highest latency and lowest latency (all in microseconds) between Sprout and the Homer XDMS over the past five minutes.
* The number of parallel TCP connections to each Homestead node.
* The number of parallel TCP connections to each Homer node.