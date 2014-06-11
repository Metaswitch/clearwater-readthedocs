Clearwater provides a set of statistics about the performance of each Clearwater nodes over SNMP. Currently (as of release 43) this is only available on Bono, Sprout and Homestead nodes.

## Configuration

These SNMP statistics require the clearwater-snmp-handler-bono, clearwater-snmp-handler-sprout or clearwater-snmp-handler-homestead packages to be installed for Bono, Sprout and Homestead nodes respectively. These packages will be automatically installed when installing through the Chef automation system; for a manual install, you will need to run `sudo apt-get install clearwater-snmp-handler-bono` on Bono nodes, `sudo apt-get install clearwater-snmp-handler-sprout` on Sprout nodes and `sudo apt-get install clearwater-snmp-handler-homestead` on Homestead nodes.

## Usage

Clearwater nodes provide SNMP statistics over port 161 using SNMP v2c and community `clearwater`. The MIB definition file can be downloaded from [here](https://github.com/Metaswitch/clearwater-snmp-handlers/blob/master/PROJECT-CLEARWATER-MIB), or (for Clearwater nodes on relases before Halo, when the MIB file was updated to support IPv6) [here](https://github.com/Metaswitch/clearwater-snmp-handlers/blob/release-48/PROJECT-CLEARWATER-MIB).

### Bono statistics

Bono nodes provide the following statistics:

* The standard SNMP CPU and memory usage statistics (see http://net-snmp.sourceforge.net/docs/mibs/ucdavis.html for details)
* The average latency, variance, highest call latency and lowest call latency (all in microseconds) seen over the past five seconds.
* The number of parallel TCP connections to each Sprout node.
* The number of incoming requests over the past five seconds.
* The number of requests rejected due to overload over the past five seconds.
* The average request queue size, variance, highest queue size and lowest queue size seen over the past five seconds.


### Sprout statistics

Sprout nodes provide the following statistics:

* The standard SNMP CPU and memory usage statistics (see http://net-snmp.sourceforge.net/docs/mibs/ucdavis.html for details)
* The average latency, variance, highest call latency and lowest call latency (all in microseconds) seen over the past five seconds.
* The average latency, variance, highest latency and lowest latency (all in microseconds) seen on the Cx interface over the past five seconds.
* The average latency, variance, highest latency and lowest latency (all in microseconds) seen on Multimedia-Auth Requests on the Cx interface over the past five seconds.
* The average latency, variance, highest latency and lowest latency (all in microseconds) seen on Server-Assignment Requests on the Cx interface over the past five seconds.
* The average latency, variance, highest latency and lowest latency (all in microseconds) seen on User-Authorization Requests on the Cx interface over the past five seconds.
* The average latency, variance, highest latency and lowest latency (all in microseconds) seen on Location-Information Requests on the Cx interface over the past five seconds.
* The average latency, variance, highest latency and lowest latency (all in microseconds) between Sprout and the Homer XDMS over the past five seconds.
* The number of parallel TCP connections to each Homestead node.
* The number of parallel TCP connections to each Homer node.
* The number of incoming requests over the past five seconds.
* The number of requests rejected due to overload over the past five seconds.
* The average request queue size, variance, highest queue size and lowest queue size seen over the past five seconds.


### Homestead Statistics

Homestead nodes provide the following statistics:

* The standard SNMP CPU and memory usage statistics (see http://net-snmp.sourceforge.net/docs/mibs/ucdavis.html for details)
* The average latency, variance, highest call latency and lowest call latency (all in microseconds) seen over the past five seconds.
* The average latency, variance, highest latency and lowest latency (all in microseconds) seen on the Cx interface over the past five seconds.
* The average latency, variance, highest latency and lowest latency (all in microseconds) seen on Multimedia-Auth Requests on the Cx interface over the past five seconds.
* The average latency, variance, highest latency and lowest latency (all in microseconds) seen on Server-Assignment, User-Authorization and Location-Information Requests on the Cx interface over the past five seconds.
* The number of incoming requests over the past five seconds.
* The number of requests rejected due to overload over the past five seconds.
