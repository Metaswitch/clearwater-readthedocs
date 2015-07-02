Clearwater provides a set of statistics about the performance of each Clearwater nodes over SNMP. Currently, this is available on Bono, Sprout, Ralf and Homestead nodes.

## Configuration

These SNMP statistics require:

* the clearwater-snmp-handler-homestead package to be installed for Homestead nodes
* the clearwater-snmp-handler-chronos and clearwater-snmp-handler-astaire packages to be installed for Sprout and Ralf nodes
    
These packages will be automatically installed when installing through the Chef automation system; for a manual install, you will need to install the packages with `sudo apt-get install`.

## Usage

Clearwater nodes provide SNMP statistics over port 161 using SNMP v2c and community `clearwater`. The MIB definition file can be downloaded from [here](https://github.com/Metaswitch/clearwater-snmp-handlers/blob/master/PROJECT-CLEARWATER-MIB).

Our SNMP statistics are provided through plugins or subagents to the standard SNMPd packaged with Ubuntu, so querying port 161 (the standard SNMP port) on a Clearwater node will provide system-level stats like CPU% as well as any available Clearwater stats.

If a statistic is indexed by time period, then it displays the relevant statistics over:

* the previous five-second period
* the current five-minute period
* the previous five-minute period

For example, a stat queried at 12:01:33 would display the stats covering:

* 12:01:25 - 12:01:30 (the previous five-second period)
* 12:00:00 - 12:01:33 (the current five-minute period)
* 11:55:00 - 12:00:00 (the previous five-minute period)

All latency values are in microseconds.

### Bono statistics

Bono nodes provide the following statistics:

* The standard SNMP CPU and memory usage statistics (see http://net-snmp.sourceforge.net/docs/mibs/ucdavis.html for details)
* The average latency, variance, highest latency and lowest latency for SIP requests, indexed by time period.
* The number of parallel TCP connections to each Sprout node.
* The number of incoming requests, indexed by time period.
* The number of requests rejected due to overload, indexed by time period.
* The average request queue size, variance, highest queue size and lowest queue size, indexed by time period.

### Sprout statistics

Sprout nodes provide the following statistics:

* The standard SNMP CPU and memory usage statistics (see http://net-snmp.sourceforge.net/docs/mibs/ucdavis.html for details)
* The average latency, variance, highest latency and lowest latency for SIP requests, indexed by time period.
* The average latency, variance, highest latency and lowest latency for requests to Homestead, indexed by time period.
* The average latency, variance, highest latency and lowest latency for requests to Homestead's `/impi/<private ID>/av` endpoint, indexed by time period.
* The average latency, variance, highest latency and lowest latency for requests to Homestead's `/impi/<private ID>/registration-status` endpoint, indexed by time period.
* The average latency, variance, highest latency and lowest latency for requests to Homestead's `/impu/<public ID>/reg-data` endpoint, indexed by time period.
* The average latency, variance, highest latency and lowest latency for requests to Homestead's `/impu/<public ID>/location` endpoint, indexed by time period.
* The average latency, variance, highest latency and lowest latency for requests to Homer, indexed by time period.
* The number of parallel TCP connections to each Homestead node.
* The number of parallel TCP connections to each Homer node.
* The number of incoming SIP requests, indexed by time period.
* The number of requests rejected due to overload, indexed by time period.
* The average request queue size, variance, highest queue size and lowest queue size, indexed by time period.
* The number of Memcached buckets needing to be synchronized and buckets already resynchronized during the current Astaire resynchronization operation (overall, and for each peer).
* The number of Memcached entries, and amount of data (in bytes) already resynchronized during the current Astaire resynchronization operation.
* The transfer rate (in bytes/second) of data during this resynchronization, over the last 5 seconds (overall, and per bucket).
* The number of remaining nodes to query during the current Chronos scaling operation.
* The number of timers, and number of invalid timers, processed over the last 5 seconds.

### Ralf statistics

Ralf nodes provide the following statistics:

* The standard SNMP CPU and memory usage statistics (see http://net-snmp.sourceforge.net/docs/mibs/ucdavis.html for details).
* The number of Memcached buckets needing to be synchronized and buckets already resynchronized during the current Astaire resynchronization operation (overall, and for each peer).
* The number of Memcached entries, and amount of data (in bytes) already resynchronized during the current Astaire resynchronization operation.
* The transfer rate (in bytes/second) of data during this resynchronization, over the last 5 seconds (overall, and per bucket).
* The number of remaining nodes to query during the current Chronos scaling operation.
* The number of timers, and number of invalid timers, processed over the last 5 seconds.

### Homestead Statistics

Homestead nodes provide the following statistics:

* The standard SNMP CPU and memory usage statistics (see http://net-snmp.sourceforge.net/docs/mibs/ucdavis.html for details)
* The average latency, variance, highest call latency and lowest latency on HTTP requests over the past five seconds.
* The average latency, variance, highest latency and lowest latency on the Cx interface over the past five seconds.
* The average latency, variance, highest latency and lowest latency on Multimedia-Auth Requests on the Cx interface over the past five seconds.
* The average latency, variance, highest latency and lowest latency on Server-Assignment, User-Authorization and Location-Information Requests on the Cx interface over the past five seconds.
* The number of incoming requests over the past five seconds.
* The number of requests rejected due to overload over the past five seconds.
* The total number of Diameter requests with an invalid Destination-Realm or invalid Destination-Host over the last 5 seconds.
