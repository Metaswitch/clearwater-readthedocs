Exploring Clearwater
====================

After following the `Install
Instructions <Installation_Instructions.html>`__ you will have a
Clearwater deployment which is capable of handling on-net calls and has
a number of MMTel services available through the built-in TAS.

Clearwater supports many optional extra features that you may chose to
add to your deployment. Descriptions of each feature along with the
process to enable it on your system can be found here.

Integrating Clearwater with existing services
---------------------------------------------

An install of Clearwater will, by default, run with no external
requirements and allow simple on-net calls between lines provisioned in
Ellis. Clearwater also supports interoperating with various other SIP
core devices to add more functionality and integrate with an existing
SIP core.

-  `IBCF function <IBCF.html>`__
-  `Application Server <Application_Server_Guide.html>`__
-  `External HSS Integration <External_HSS_Integration.html>`__
-  `CDF Integration <CDF_Integration.html>`__
-  `SIP RFCs supported <SIP_Interface_Specifications.html>`__

Call features
-------------

Clearwater has a number of call features provided by its `built-in
TAS <Application_Server_Guide.html#the-built-in-mmtel-application-server>`__,
including:

-  `Call barring <Clearwater_Call_Barring_Support.html>`__
-  `Call diversion <Clearwater_Call_Diversion_Support.html>`__
-  `Privacy <Clearwater_Privacy_Feature.html>`__

Clearwater's support for all IR.92 Supplementary Services is discussed
in `this document <IR.92_Supplementary_Services.md>`__.

Scaling and Redundancy
----------------------

Clearwater is designed from the ground up to scale horizontally across
multiple instances to allow it to handle large subscriber counts and to
support a high level of redundancy.

-  `Scaling
   Numbers <http://www.projectclearwater.org/technical/clearwater-performance/>`__
-  The local redundancy story is described in the `Clearwater
   Architecture <Clearwater_Architecture.html>`__ page.
-  `Geographic redundancy <Geographic_redundancy.html>`__

Operational support
-------------------

To help you manage your deployment, Clearwater provides:

-  `Command-line/scriptable provisioning
   tools <Provisioning_Subscribers.html>`__
-  `Support for separated management
   networks <Multiple_Network_Support.html>`__
-  `Deployment monitoring <Cacti.html>`__
-  `Backup <Backups.html>`__
-  `A troubleshooting guide <Troubleshooting_and_Recovery.html>`__ with
   instructions for viewing the database entries on Sprout and
   Homestead/Homer.

