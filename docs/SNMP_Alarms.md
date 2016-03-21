# SNMP Alarms

Clearwater nodes report errors over the SNMP interface when they are in an abnormal
state, and clear them when they return to normal. They only report errors relating to
that node - not errors relating to the whole deployment, which is the role of an external
monitoring service.

Error indications come in two forms:

*   For clearly-defined errors not based on thresholds, the Clearwater node sets an
    ITU Alarm MIB from [RFC 3877](http://tools.ietf.org/html/3877) and sends an SNMP
    notification to a configured external SNMP manager.

*   For errors based on a threshold set on a statistic (such as latency targets or
    number of failed connections), the Clearwater node [exposes that statistic over
    SNMP](Clearwater_SNMP_Statistics.md). A downstream statistics aggregator from the Management and
    Orchestration (MANO) layer monitors these statistics, compares them to its
    configured thresholds, and raises alarms on that basis.

## EMS

To integrate with an EMS, the EMS must support the following capabilities of RFC 3877 to
obtain the brief description, detailed description, and severity for the alarm:

*   The EMS must be configured to catch the SNMP INFORM messages used to
    report alarms from Clearwater. It is also recommended that the EMS must
    display the alarm information provided by the following MIBs.

*   Upon receiving a SNMP INFORM message from Clearwater the EMS can obtain the
    alarm data by the following:

    *   The EMS must retrieve the AlarmModelEntry MIB table data associated
        with the current SNMP INFORM message from Clearwater. This MIB provides the
        active/clear state, alarm description, and a table index for the ituAlarmEntry
        MIB.

    *   The EMS must the retrieve the ituAlarmEntry MIB table data associated
        with the current alarm from Clearwater. This MIB provides the alarm
        severity and the additional detailed alarm description.

## Alarm Models

The alarm models used by Clearwater are defined in [alarmdefinition.h](https://github.com/Metaswitch/cpp-common/blob/master/include/alarmdefinition.h).

## Alarm Resiliency

Since prompt, accurate notifications of alarms are important for running a reliable telecoms network, Clearwater is designed so that if an EMS or an internal Clearwater component responsible for alarm notifications fails and recovers, the EMS will learn about any alarms raised by Clearwater during the outage, rather than those alarms just being lost. The exact behaviour is as follows:

- On startup (including after reboots), Clearwater nodes will detect whether each of their alarms should be raised or not (and at what severity), and send corresponding SNMP INFORMs to the EMS. This will happen within a minute.
    - If there is no call traffic, the correct state of some alarms cannot be determined – in this case, the node will neither raise nor clear an alarm until there is call traffic and it can determine the correct state.
- If the EMS suffers an outage, but remembers previous alarm state when it recovers, no operator intervention is required. Clearwater nodes send SNMP INFORMs, which require acknowledgement by the EMS, and these will be retransmitted until they are acknowledged.
    - Note that if the alarm changes state multiple times during an outage (e.g. if it is raised but then cleared, or raised once at major severity and then again at critical severity), only the latest state will be transmitted to the EMS on connection recovery.
- If the EMS suffers an outage and loses previous alarm state, there are two ways to recover:
    - The process responsible for sending SNMP notifications, the Alarm Agent, keeps track of all the currently active error states in a table called the Alarm Active Table (defined in [RFC 3877](https://tools.ietf.org/html/rfc3877)). Upon restart, an EMS can read this table and learn about any SNMP INFORMs it may have missed in its downtime.
    - If an EMS does not support reading the Active Alarm Table, the operator can still recover the SNMP INFORMs by running `/usr/share/clearwater/bin/sync_alarm.py` on each node. This will cause SNMP notifications to be resent to the EMS.

Clearwater nodes also regularly re-detect and re-transmit alarm state internally. This is so that if the alarm agent is failed when an alarmable condition is detected, the alarm will still reach the EMS less than a minute after the component recovers. If the alarm agent fails, it will be automatically restarted, but it will lose its alarm state. However, each internal component which detects alarms will retransmit them on a 30-second timer – so within a minute, they will have retransmitted their alarm state to the alarm agent, it will have sent corresponding SNMP INFORMs to the EMS, and both the alarm agent and the EMS will have a complete picture of the current alarm state. 
