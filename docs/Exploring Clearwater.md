# Exploring Clearwater

After following the [Install Instructions](Installation Instructions) you will have a Clearwater deployment which is capable of handling on-net calls and has a number of MMTel services available through the built-in TAS.

Clearwater supports many optional extra features that you may chose to add to your deployment.  Descriptions of each feature along with the process to enable it on your system can be found here.

## Integrating Clearwater with existing services

An install of Clearwater will, by default, run with no external requirements and allow simple on-net calls between lines provisioned in Ellis.  Clearwater also supports interoperating with various other SIP core devices to add more functionality and integrate with an existing SIP core.

* [IBCF function](IBCF)
* [Application Server](Application Server Guide)
* [External HSS Integration](External HSS Integration)
* [CDF Integration](CDF Integration)
* [SIP RFCs supported](SIP Interface Specifications)

## Call features

Clearwater has a number of call features provided by its [built-in TAS](Application Server Guide#the-built-in-mmtel-application-server), including:

* [Call barring](Clearwater Call Barring Support)
* [Call diversion](Clearwater Call Diversion Support)
* [Privacy](Clearwater Privacy Feature)

Clearwater's support for all IR.92 Supplementary Services is discussed in [this document](IR.92-Supplementary-Services).

## Scaling and Redundancy

Clearwater is designed from the ground up to scale horizontally across multiple instances to allow it to handle large subscriber counts and to support a high level of redundancy.

* [Scaling Numbers](http://www.projectclearwater.org/technical/clearwater-performance/)
* The local redundancy story is described in the [Clearwater Architecture](Clearwater Architecture) page.
* [Geographic redundancy](Geographic redundancy)

## Operational support

To help you manage your deployment, Clearwater provides:

* [Support for separated management networks](Multiple Network Support)
* [Deployment monitoring](Cacti)
* [Backup](Backups)
* [A troubleshooting guide](Troubleshooting and Recovery) with instructions for viewing the database entries on Sprout and Homestead/Homer.
