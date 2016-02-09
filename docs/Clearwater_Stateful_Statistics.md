Despite being designed as an inherently stateless system, Clearwater is able to provide a number of deployment wide stateful statistics. This is done through utilisation of our distributed timer store, Chronos. As components use timers to maintain stateful functionality without actually remaining independently aware of state, we can use those same timers to convey statistics. Currently, only Sprout and Ralf expose any stateful statistics.

## Configuration

These statistics behave in the same manner as our standard SNMP statistics. Detail on how to configure nodes and access the statistics can be found [here](https://clearwater.readthedocs.org/en/stable/Clearwater_SNMP_Statistics/index.html).

## Usage

As these statistics are representative of deployment wide state, their usage is slightly different to the standard per-node SNMP statistics. They key difference is that, due to the redundancy design in Chronos, the statistics are subject to a replication factor (which is by default set to 2). To accurately report the statistics from a whole deployment, the individual values should be gathered from each node in the deployment, and then the sum total should be divided by the replication factor.

e.g. Consider a deployment with three Sprout nodes. If ten registrations are set up, the nodes might report the following statistics:

* Node 1 :-  6 Registrations
* Node 2 :-  7 Registrations
* Node 3 :-  7 Registrations

This does not mean that the number of registrations has doubled, nor is it representative of the number of registrations that each node actually handled. It is simply directly the number of timers held on each node tagged as registrations.  
To then calculate the number of registrations actually active in the deployment, one takes the total and divides it by the replication factor, in this example 2.
> (Node 1 + Node 2 + Node 3) / Replication-factor  
> (  6    +   7    +   7   ) / 2  => 10 Active registrations

## Sprout statistics

Sprout nodes provide the following statistics:

* The average count, variance, and high and low watermarks for the number of registrations, indexed by time period.
* The average count, variance, and high and low watermarks for the number of bindings, indexed by time period.
* The average count, variance, and high and low watermarks for the number of subscriptions, indexed by time period.

## Ralf statistics

Ralf nodes provide the following statistics:

* The average count, variance, and high and low watermarks for the number of calls, indexed by time period.
