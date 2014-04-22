The core Clearwater nodes have the ability to elastically scale; in other words, you can grow and shrink your deployment on demand, without disrupting calls or losing data.

This page explains how to use this elastic scaling function when using a deployment created through the automated install process.

## Before scaling your deployment

Before scaling up or down, you should decide how many each of Bono, Sprout, Homestead and Homer nodes you need (ie. your target size). This should be based on your call load profile and measurements of current systems and we recommend scaling up a tier of a given type (sprout, bono, etc) when the average CPU utilization within that tier reaches 60%. The [Deployment Sizing Spreadsheet](http://www.projectclearwater.org/technical/clearwater-performance/) may also prove useful.

## Starting the resize

To resize your deployment, run:

`knife deployment resize -E <env> --sprout-count <n> --bono-count <n> --homer-count <n> --homestead-count <n>`

where the <n> values are how many nodes of each type you need.

If you are scaling up, this will add new nodes, cluster them and update DNS records as needed. Your enlarged deployment will be available immediately (though the DNS records may take a few minutes to propagate).

If you are scaling down, this will put the excess nodes into a quiescing state, in which they move their data to other nodes and attempt to redirect new registrations.

In either case, your registration store will be in a transitional state, which will last until all subscribers have re-registered (i.e. your maximum registration interval, which defaults to five minutes).

## Finishing the rezise

Once enough time has passed for all subscribers to have re-registered, and assuming all Sprout nodes in your deployment have been running *stably* throughout that period, run:
                                                                                      
`knife deployment resize -E <env> --finish`

to complete the resize. If you are scaling down, this will check that all nodes are appropriately quiesced, but will not check the state of the registration store, so you *must* be sure to leave the system in a stable state for the appropriate period first.