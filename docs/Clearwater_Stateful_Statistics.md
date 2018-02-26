# Stateful Statistics

Clearwater is designed to be as stateless as possible, simplifying redundancy, and making it ideal for virtualised and cloud-based deployment. However, through use of our distributed timer store, Chronos, Clearwater is able to maintain a number of stateful statistics. As components use timers to maintain stateful functionality without actually remaining independently aware of state, we can form statistics based on these, rather than needing each main process to maintain and report state. Currently Vellum nodes expose stateful statistics. To see the full list of statistics available, check [here](https://clearwater.readthedocs.io/en/stable/Clearwater_SNMP_Statistics/index.html); stateful statistics are marked as '(stateful)' to distinguish them.


## Configuration

These statistics are accessible in the same manner as our standard SNMP statistics. Detail on how to configure nodes and access the statistics can be found [here](https://clearwater.readthedocs.io/en/stable/Clearwater_SNMP_Statistics/index.html).

## Usage

As these statistics are representative of deployment wide state, their usage is slightly different to the standard per-node SNMP statistics. They key difference is that, due to the redundancy design in Chronos, the statistics are subject to a replication factor (which is by default set to 2). To accurately report the statistics from a whole single site deployment, the individual values should be gathered from each node in the deployment, and then the sum total should be divided by the replication factor.

e.g. Consider a deployment with three Vellum nodes. If ten registrations are set up, the nodes might report the following statistics:

* Node 1 :-  6 Registrations
* Node 2 :-  7 Registrations
* Node 3 :-  7 Registrations


This does not mean that the number of registrations has doubled, nor is it representative of the number of registrations that each node actually handled. It is simply directly the number of timers held on each node tagged as registrations.
To then calculate the number of registrations actually active in the deployment, one takes the total and divides it by the replication factor, in this example 2.

> (Node 1 + Node 2 + Node 3) / Replication-factor = (6 + 7 + 7) / 2  = 10 Active registrations

Note: These statistics may be inaccurate in systems with a failing node. As such they should be considered unreliable while any alarms are raised, particularly those relating to Chronos.

For a deployment which contains more that one site, the statistics must be summed across all sites in the deployment, as by default Chronos is not geographically redundant.

e.g. Consider a deployment with two sites, each of which contains three Vellum nodes. If ten registrations are set up in Site 1, and 8 in Site 2, the nodes could report the following statistics:

Site 1
* Node 1 :- 6 Registrations
* Node 2 :- 7 Registrations
* Node 3 :- 7 Registrations

Site 2
* Node 1 :- 6 Registrations
* Node 2 :- 6 Registrations
* Node 3 :- 4 Registrations

To calculate the number of registrations actually active in the deployement, the total in each site should be divided by the replication factor, and then the registrations for each site should be summed.

> ((6 + 7 + 7) / 2 ) + ((6 + 6 + 4) /  2) = 10 + 8 = 18 Active registrations

Note: These statistics may be inaccurate in systems with a failing site. As such they should be considered unreliable for the length of the re-registration period after a site fails.

## Technical details

For a more technical overview of how these statistics are handled within Chronos, see [here.](https://github.com/Metaswitch/chronos/blob/dev/doc/statistics_structures.md)
