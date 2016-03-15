SNMP Alarms
===========

Clearwater nodes report errors over the SNMP interface when they are in
an abnormal state, and clear them when they return to normal. They only
report errors relating to that node - not errors relating to the whole
deployment, which is the role of an external monitoring service.

Error indications come in two forms:

-  For clearly-defined errors not based on thresholds, the Clearwater
   node sets an ITU Alarm MIB from `RFC
   3877 <http://tools.ietf.org/html/3877>`__ and sends an SNMP
   notification to a configured external SNMP manager.

-  For errors based on a threshold set on a statistic (such as latency
   targets or number of failed connections), the Clearwater node
   `exposes that statistic over SNMP <Clearwater_SNMP_Statistics.html>`__.
   A downstream statistics aggregator from the Management and
   Orchestration (MANO) layer monitors these statistics, compares them
   to its configured thresholds, and raises alarms on that basis.

EMS
---

To integrate with an EMS, the EMS must support the following
capabilities of RFC 3877 to obtain the brief description, detailed
description, and severity for the alarm:

-  The EMS must be configured to catch the SNMP INFORM messages used to
   report alarms from Clearwater. It is also recommended that the EMS
   must display the alarm information provided by the following MIBs.

-  Upon receiving a SNMP INFORM message from Clearwater the EMS can
   obtain the alarm data by the following:

   -  The EMS must retrieve the AlarmModelEntry MIB table data
      associated with the current SNMP INFORM message from Clearwater.
      This MIB provides the active/clear state, alarm description, and a
      table index for the ituAlarmEntry MIB.

   -  The EMS must the retrieve the ituAlarmEntry MIB table data
      associated with the current alarm from Clearwater. This MIB
      provides the alarm severity and the additional detailed alarm
      description.

Alarm Models
------------

The alarm models used by Clearwater are defined in
`alarmdefinition.h <https://github.com/Metaswitch/cpp-common/blob/master/include/alarmdefinition.h>`__.

Alarm Resiliency
----------------

Clearwater is designed so that if an EMS receiving alarm notifications
fails and recovers, it will learn about any alarms raised by Clearwater
while it was down, rather than those alarms just being lost. This is due
to the following two features:

-  The process responsible for sending SNMP notifications, the Alarm
   Agent, keeps track of all the currently active error states in a
   table called the Alarm Active Table. Upon restart, an EMS can read
   this table and learn about any SNMP INFORMs it may have missed in its
   downtime.
-  If an EMS does not support reading the Active Alarm Table we can
   still recover the SNMP INFORMs by running
   ``/usr/share/clearwater/bin/sync_alarm.py``. This will cause SNMP
   notifications to be resent to the EMS.

