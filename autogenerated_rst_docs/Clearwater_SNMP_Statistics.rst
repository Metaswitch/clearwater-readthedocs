SNMP Statistics
===============

Clearwater provides a set of statistics about the performance of each
Clearwater nodes over SNMP. Currently, this is available on Bono,
Sprout, Ralf and Homestead nodes, and the MMTel, Call Diversion, Memento
and Gemini Application Server nodes.

Configuration
-------------

These SNMP statistics require:

-  the clearwater-snmpd package to be installed for all node types
-  the clearwater-snmp-handler-astaire package to be installed for
   Sprout and Ralf nodes

These packages will be automatically installed when installing through
the Chef automation system; for a manual install, you will need to
install the packages with ``sudo apt-get install``.

Usage
-----

Clearwater nodes provide SNMP statistics over port 161 using SNMP v2c
and community ``clearwater``. The MIB definition file can be downloaded
from
`here <https://github.com/Metaswitch/clearwater-snmp-handlers/blob/master/PROJECT-CLEARWATER-MIB>`__.

Our SNMP statistics are provided through plugins or subagents to the
standard SNMPd packaged with Ubuntu, so querying port 161 (the standard
SNMP port) on a Clearwater node will provide system-level stats like
CPU% as well as any available Clearwater stats.

To load the MIB file, allowing you to refer to MIB objects by name,
first place it in the ``~/.snmp/mibs`` directory. To load the MIB file
for just the current session, run
``export MIBS=+PROJECT-CLEARWATER-MIB``. To load the MIB file every
time, add the line ``mibs +PROJECT-CLEARWATER-MIB`` to a snmp.conf file
in the ``~/.snmp`` directory.

If a statistic is indexed by time period, then it displays the relevant
statistics over:

-  the previous five-second period
-  the current five-minute period
-  the previous five-minute period

For example, a stat queried at 12:01:33 would display the stats
covering:

-  12:01:25 - 12:01:30 (the previous five-second period)
-  12:00:00 - 12:01:33 (the current five-minute period)
-  11:55:00 - 12:00:00 (the previous five-minute period)

All latency values are in microseconds.

| Many of the statistics listed below are stored in SNMP tables
(although the MIB file should be examined to determine exactly which
ones). The full table can be retrieved by using the ``snmptable``
command. For example, the Initial Registrations table for Sprout can be
retrieved by running:
| ``snmptable -v2c -c clearwater <ip> PROJECT-CLEARWATER-MIB::sproutInitialRegistrationTable``

The individual table elements can be accessed using:
``snmpget -v2c -c clearwater <ip> <table OID>.1.<column>.<row>``

| For example, the Initial Registration Stats table has an OID of
``.1.2.826.0.1.1578918.9.3.9``, so the number of initial registration
attempts in the current five-minute period can be retrieved by:
| ``snmpget -v2c -c clearwater <ip> .1.2.826.0.1.1578918.9.3.9.1.2.2``
or by:
| ``snmpget -v2c -c clearwater <ip> PROJECT-CLEARWATER-MIB::sproutInitialRegistrationAttempts.scopeCurrent5MinutePeriod``

| The ``snmpwalk`` command can be used to discover the list of queryable
OIDs beneath a certain point in the MIB tree. For example, you can
retrieve all of the entries in the Sprout Initial Registrations table
using:
| ``snmpwalk -v2c -c clearwater <ip> PROJECT-CLEARWATER-MIB::sproutInitialRegistrationTable``

Running
``snmpwalk -v2c -c clearwater <ip> PROJECT-CLEARWATER-MIB::projectClearwater``
will output a very long list of all available Clearwater stats.

Note that running an 'snmpget' on a table OID will result in a "No Such
Object available on this agent at this OID" message.

Bono statistics
~~~~~~~~~~~~~~~

Bono nodes provide the following statistics:

-  The standard SNMP CPU and memory usage statistics (see
   http://net-snmp.sourceforge.net/docs/mibs/ucdavis.html for details)
-  The average latency, variance, highest latency and lowest latency for
   SIP requests, indexed by time period.
-  The number of parallel TCP connections to each Sprout node.
-  The number of incoming requests, indexed by time period.
-  The number of requests rejected due to overload, indexed by time
   period.
-  The average request queue size, variance, highest queue size and
   lowest queue size, indexed by time period.

Sprout statistics
~~~~~~~~~~~~~~~~~

Sprout nodes provide the following statistics:

-  The standard SNMP CPU and memory usage statistics (see
   http://net-snmp.sourceforge.net/docs/mibs/ucdavis.html for details)
-  The average latency, variance, highest latency and lowest latency for
   SIP requests, indexed by time period.
-  The average latency, variance, highest latency and lowest latency for
   requests to Homestead, indexed by time period.
-  The average latency, variance, highest latency and lowest latency for
   requests to Homestead's ``/impi/<private ID>/av`` endpoint, indexed
   by time period.
-  The average latency, variance, highest latency and lowest latency for
   requests to Homestead's ``/impi/<private ID>/registration-status``
   endpoint, indexed by time period.
-  The average latency, variance, highest latency and lowest latency for
   requests to Homestead's ``/impu/<public ID>/reg-data`` endpoint,
   indexed by time period.
-  The average latency, variance, highest latency and lowest latency for
   requests to Homestead's ``/impu/<public ID>/location`` endpoint,
   indexed by time period.
-  The average latency, variance, highest latency and lowest latency for
   requests to Homer, indexed by time period.
-  The number of attempts, successes and failures for AKA
   authentications on register requests, indexed by time period (AKA
   authentication attempts with a correct response but that fail due to
   the sequence number in the nonce being out of sync are counted as
   successes).
-  The number of attempts, successes and failures for SIP digest
   authentications on register requests, indexed by time period
   (authentication attempts with a correct response but that fail due to
   being stale are counted as failures).
-  The number of attempts, successes and failures for authentications on
   non-register requests, indexed by time period.
-  The number of attempts, successes and failures for initial
   registrations, indexed by time period (registrations that fail due to
   failed authentication are counted in the authentication stats and not
   here).
-  The number of attempts, successes and failures for re-registrations,
   indexed by time period (registrations that fail due to failed
   authentication are counted in the authentication stats and not here).
-  The number of attempts, successes and failures for de-registrations,
   indexed by time period (registrations that fail due to failed
   authentication are counted in the authentication stats and not here).
-  The number of attempts, successes and failures for third-party
   initial registrations, indexed by time period (registrations that
   fail due to failed authentication are counted in the authentication
   stats and not here).
-  The number of attempts, successes and failures for third-party
   re-registrations, indexed by time period (registrations that fail due
   to failed authentication are counted in the authetication stats and
   not here).
-  The number of attempts, successes and failures for third-party
   de-registrations, indexed by time period (registrations that fail due
   to failed authentication are counted in the authentication stats and
   not here).
-  The number of requests routed by the S-CSCF according to a route
   pre-loaded by an app server, indexed by time period.
-  The number of parallel TCP connections to each Homestead node.
-  The number of parallel TCP connections to each Homer node.
-  The number of incoming SIP requests, indexed by time period.
-  The number of requests rejected due to overload, indexed by time
   period.
-  The average request queue size, variance, highest queue size and
   lowest queue size, indexed by time period.
-  The number of Memcached buckets needing to be synchronized and
   buckets already resynchronized during the current Astaire
   resynchronization operation (overall, and for each peer).
-  The number of Memcached entries, and amount of data (in bytes)
   already resynchronized during the current Astaire resynchronization
   operation.
-  The transfer rate (in bytes/second) of data during this
   resynchronization, over the last 5 seconds (overall, and per bucket).
-  The number of remaining nodes to query during the current Chronos
   scaling operation.
-  The number of timers, and number of invalid timers, processed over
   the last 5 seconds.
-  The total number of timers being managed by a Chronos node at the
   current time.
-  The weighted average of total timer count, variance, highest timer
   count, lowest timer count, indexed by time period.
-  The number of attempts, successes and failures for incoming SIP
   transactions for the ICSCF, indexed by time period and request type.
-  The number of attempts, successes and failures for outgoing SIP
   transactions for the ICSCF, indexed by time period and request type.
-  The number of attempts, successes and failures for incoming SIP
   transactions for the SCSCF, indexed by time period and request type.
-  The number of attempts, successes and failures for outgoing SIP
   transactions for the SCSCF, indexed by time period and request type.
-  The number of attempts, successes and failures for incoming SIP
   transactions for the BGCF, indexed by time period and request type.
-  The number of attempts, successes and failures for outgoing SIP
   transactions for the BGCF, indexed by time period and request type.
-  The permitted request rate (PRR) is an estimate for the sustainable
   request rate without causing large latency. Sprout provides a
   weighted average permitted request rate, variance, highest PRR, and
   lowest PRR, indexed by time period.
-  The value of the smoothed latency at the last permitted request rate
   update.
-  The value of the target (maximum permissible) latency at the last
   permitted request rate update.
-  The number of penalties experienced at the last permitted request
   rate update.
-  The current permitted request rate.
-  The number of incoming INVITE transactions for the S-CSCF that were
   cancelled before a 1xx response was seen, indexed by time period.
-  The number of incoming INVITE transactions for the S-CSCF that were
   cancelled after a 1xx response was seen, indexed by time period
   (these INVITE cancellation statistics can be used to distinguish
   between the case where an INVITE was cancelled because the call rang
   but wasn't answered and the case where it failed due to network
   issues and never got through in the first place).

Ralf statistics
~~~~~~~~~~~~~~~

Ralf nodes provide the following statistics:

-  The standard SNMP CPU and memory usage statistics (see
   http://net-snmp.sourceforge.net/docs/mibs/ucdavis.html for details).
-  The number of Memcached buckets needing to be synchronized and
   buckets already resynchronized during the current Astaire
   resynchronization operation (overall, and for each peer).
-  The number of Memcached entries, and amount of data (in bytes)
   already resynchronized during the current Astaire resynchronization
   operation.
-  The transfer rate (in bytes/second) of data during this
   resynchronization, over the last 5 seconds (overall, and per bucket).
-  The number of remaining nodes to query during the current Chronos
   scaling operation.
-  The number of timers, and number of invalid timers, processed over
   the last 5 seconds.

Homestead Statistics
~~~~~~~~~~~~~~~~~~~~

Homestead nodes provide the following statistics:

-  The standard SNMP CPU and memory usage statistics (see
   http://net-snmp.sourceforge.net/docs/mibs/ucdavis.html for details)
-  The average latency, variance, highest call latency and lowest
   latency on HTTP requests, indexed by time period.
-  The average latency, variance, highest latency and lowest latency on
   the Cx interface, indexed by time period.
-  The average latency, variance, highest latency and lowest latency on
   Multimedia-Auth Requests on the Cx interface, indexed by time period.
-  The average latency, variance, highest latency and lowest latency on
   Server-Assignment, User-Authorization and Location-Information
   Requests on the Cx interface, indexed by time period.
-  The number of incoming requests, indexed by time period.
-  The number of requests rejected due to overload, indexed by time
   period.
-  The total number of Diameter requests with an invalid
   Destination-Realm or invalid Destination-Host, indexed by time
   period.
-  The number of Multimedia-Authorization-Answers with a given
   result-code received over the Cx interface, indexed by time period.
-  The number of Server-Assignment-Answers with a given result-code
   received over the Cx interface, indexed by time period.
-  The number of User-Authorization-Answers with a given result-code
   received over the Cx interface, indexed by time period.
-  The number of Location-Information-Answers with a given result-code
   received over the Cx interface, indexed by time period.
-  The number of Push-Profile-Answers with a given result-code sent over
   the Cx interface, indexed by time period.
-  The number of Registration-Termination-Answers with a given
   result-code sent over the Cx interface, indexed by time period.

Call Diversion App Server Statistics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Call Diversion App Server nodes provide the following statistics:

-  The number of attempts, successes and failures for incoming SIP
   transactions, indexed by time period and request type.
-  The number of attempts, successes and failures for outgoing SIP
   transactions, indexed by time period and request type.

Memento App Server Statistics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Memento App Server nodes provide the following statistics:

-  The number of attempts, successes and failures for incoming SIP
   transactions, indexed by time period and request type.
-  The number of attempts, successes and failures for outgoing SIP
   transactions, indexed by time period and request type.

MMTel App Server Statistics
~~~~~~~~~~~~~~~~~~~~~~~~~~~

MMTel App Server nodes provide the following statistics:

-  The number of attempts, successes and failures for incoming SIP
   transactions, indexed by time period and request type.
-  The number of attempts, successes and failures for outgoing SIP
   transactions, indexed by time period and request type.

Gemini App Server Statistics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Gemini App Server nodes provide the following statistics:

-  The number of attempts, successes and failures for incoming SIP
   transactions, indexed by time period and request type.
-  The number of attempts, successes and failures for outgoing SIP
   transactions, indexed by time period and request type.

