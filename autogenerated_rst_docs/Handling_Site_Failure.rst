Dealing with Complete Site Failure
----------------------------------

In a geographically redundant deployment, you may encounter the
situation where an entire site has permanently failed (e.g. because the
location of that geographic site has been physically destroyed). This
article covers:

-  How to recover from this situation
-  The likely impact of a site failure

More information about Clearwater's geographic redundancy support is
available
`here <http://clearwater.readthedocs.io/en/latest/Geographic_redundancy.html>`__
and information on how to configure a geographically redundant
deployment is available
`here <http://clearwater.readthedocs.io/en/latest/Configuring_GR_deployments.html>`__.

Recovery
~~~~~~~~

If you are using any of Homestead-Prov, Homer or Memento, to recover
from this situation all you need to do is remove the failed Vellum nodes
from Cassandra cluster.

::

    * From any Vellum node in the remaining site, run `cw-remove_site_from_cassandra <site ID - the name of the failed site>`

If you are not using any of Homestead-Prov, Homer or Memento, you do not
need to do anything to recover the single remaining site.

You should now have a working single-site cluster, which can continue to
run as a single site, or be safely paired with a new remote site
(details on how to set up a new remote site are
`here <http://clearwater.readthedocs.io/en/latest/Configuring_GR_deployments.html#removing-a-site-from-a-gr-deployment>`__).

Impact
~~~~~~

This section considers the probable impact on a subscriber of a total
outage of a region in a 2-region geographically-redundant deployment. It
assumes that the deployments in both regions have sufficient capacity to
cope with all subscribers (or the deployments scale elastically).

The subscriber interacts with Clearwater through 3 interfaces, and these
each have a different user experience.

-  SIP to Bono for calls
-  HTTP to Homer for direct call service configuration
-  HTTP to Ellis for web-UI-based provisioning

For the purposes of the following descriptions, we label the two regions
A and B, and the deployment in region A has failed.

SIP to Bono
^^^^^^^^^^^

If the subscriber is connected to a Bono node in region A, their TCP
connection fails. The behavior is client-specific, but we assume that
the client will attempt to re-register with the region A Bono, fail to
connect, and attempt connections to the other Bonos returned by DNS
domain query until they locate a Bono node in region B, at which point
their re-register succeeds and service is restored.

If the subscriber is connected to a Bono node in region B, their TCP
connection does not fail, they do not need to re-register and their
service is unaffected.

Realistically however, if 50% of subscribers all re-registered almost
simultaneously (due to their TCP connection dropping and their DNS being
timed out), it's unlikely that Bono would be able to keep up.

HTTP to Homer
^^^^^^^^^^^^^

If the subscriber was using a Homer node in region A, their requests
would fail until their DNS timed out, and they retried to a Homer in
region B. If the subscriber was using a Homer node in region B, they
would see no failures.

HTTP to Ellis
^^^^^^^^^^^^^

Ellis is not geographically redundant. If Ellis was deployed in region
A, all subscriber provisioning would fail until region A was recovered.
If Ellis was deployed in region B, there would be no outage.
