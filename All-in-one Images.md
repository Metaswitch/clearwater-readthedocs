# All-in-one Images

While Clearwater is designed to be massively horizontally scalable, it is also possible to install all Clearwater components on a single node.  This makes installation much simpler, and is useful for familiarizing yourself with Clearwater before moving up to a larger-scale deployment using one of the [other installation methods](Installation Instructions).

This page describes the all-in-one images, their capabilities and restrictions and the installation options available.

## Images

All-in-one images consist of
*   Ubuntu 12.04, configured to use DHCP
*   bono, sprout, homestead, homer and ellis
*   Clearwater auto-configuration scripts.

On boot, the image retrieves its IP configuration over DHCP and the auto-configuration scripts then configure the bono, sprout, homestead, homer and ellis software to match.

The image is designed to run on a virtual machine with a single core, 1.7GB RAM and 8GB of disk space.  On EC2, this is an m1.small.

## Capabilities and Restrictions

Since the all-in-one images include all of bono, sprout, homestead, homer and ellis, they are capable of almost anything a full deployment is capable of.

The key restrictions of all-in-one images are
*   hard-coded realm - the all-in-one image uses a hard-coded realm of `example.com` so your SIP URI might be `sip:6505551234@example.com` - by default, SIP uses this realm for routing but `example.com` won't resolve to your host so you need to configure an outbound proxy on all your SIP clients (more details later)
*   performance - since all software runs on a single virtual machine, performance is significantly lower than even the smallest scale deployment
*   scalability - there is no option to scale up and add more virtual machines to boost capacity - for this, you must create a normal deployment
*   fault-tolerance - since everything runs on a single virtual machine, if that virtual machine fails, the service as a whole fails.

## Installation Options

All-in-one images can be installed on EC2 or on your own virtualization platform, as long as it supports [OVF (Open Virtualization Format)](http://dmtf.org/standards/ovf).

*   To install on EC2, follow the [all-in-one EC2 AMI installation instructions](All-in-one EC2 AMI Installation).
*   To install on your own virtualization platform, follow the [all-in-one OVF installation instructions](All-in-one OVF Installation).

