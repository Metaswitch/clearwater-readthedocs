## Dealing with Complete Site Failure

In a geographically redundant deployment, you may encounter the situation where
an entire site has permanently failed (e.g. because the location of that
geographic site has been physically destroyed).

To recover from this situation:

* Remove the failed Vellum nodes from the Cassandra cluster
    * From any Vellum node in the remaining site:
        * identify the Host ID of failed Vellum nodes using`cw-run_in_signaling_namespace nodetool status`
        * for each failed Vellum node, run `cw-run_in_signaling_namespace nodetool removenode <id>`

You should now have a working single-site cluster, which can continue to run as
a single site, or be safely paired with a new remote site.
