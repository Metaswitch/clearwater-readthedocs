# Exploring Clearwater

After following the [Install Instructions](Installation_Instructions.md) you will have a Clearwater deployment which is capable of handling on-net calls and has a number of MMTel services available through the built-in TAS.

Clearwater supports many optional extra features that you may chose to add to your deployment.  Descriptions of each feature along with the process to enable it on your system can be found here.

## Integrating Clearwater with existing services

An install of Clearwater will, by default, run with no external requirements and allow simple on-net calls between lines provisioned in Ellis.  Clearwater also supports interoperating with various other SIP core devices to add more functionality and integrate with an existing SIP core.

* [IBCF function](IBCF.md)
* [Application Server](Application_Server_Guide.md)
* [External HSS Integration](External_HSS_Integration.md)
* [CDF Integration](CDF_Integration.md)
* [SIP RFCs supported](SIP_Interface_Specifications.md)

## Call features

Clearwater has a number of call features provided by its [built-in TAS](Application_Server_Guide.md#the-built-in-mmtel-application-server), including:

* [Call barring](Clearwater_Call_Barring_Support.md)
* [Call diversion](Clearwater_Call_Diversion_Support.md)
* [Privacy](Clearwater_Privacy_Feature.md)

Clearwater's support for all IR.92 Supplementary Services is discussed in [this document](IR.92_Supplementary_Services).

## Scaling and Redundancy

Clearwater is designed from the ground up to scale horizontally across multiple instances to allow it to handle large subscriber counts and to support a high level of redundancy.

* [Scaling Numbers](http://www.projectclearwater.org/technical/clearwater-performance/)
* The local redundancy story is described in the [Clearwater Architecture](Clearwater_Architecture.md) page.
* [Geographic redundancy](Geographic_redundancy.md)

## Operational support

To help you manage your deployment, Clearwater provides:

* [Support for separated management networks](Multiple_Network_Support.md)
* [Deployment monitoring](Cacti.md)
* [Backup](Backups.md)
* [A troubleshooting guide](Troubleshooting_and_Recovery.md) with instructions for viewing the database entries on Sprout and Homestead/Homer.
