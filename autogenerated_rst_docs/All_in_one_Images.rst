All-in-one Images
=================

While Clearwater is designed to be massively horizontally scalable, it
is also possible to install all Clearwater components on a single node.
This makes installation much simpler, and is useful for familiarizing
yourself with Clearwater before moving up to a larger-scale deployment
using one of the `other installation
methods <Installation_Instructions.md>`__.

This page describes the all-in-one images, their capabilities and
restrictions and the installation options available.

Images
------

All-in-one images consist of

-  Ubuntu 14.04, configured to use DHCP
-  bono, sprout, homestead, homer and ellis
-  Clearwater auto-configuration scripts.

On boot, the image retrieves its IP configuration over DHCP and the
auto-configuration scripts then configure the bono, sprout, homestead,
homer and ellis software to match.

The image is designed to run on a virtual machine with a single core,
2GB RAM and 8GB of disk space. On EC2, this is an t2.small.

Capabilities and Restrictions
-----------------------------

Since the all-in-one images include all of bono, sprout, homestead,
homer and ellis, they are capable of almost anything a full deployment
is capable of.

The key restrictions of all-in-one images are

-  hard-coded realm - the all-in-one image uses a hard-coded realm of
   ``example.com`` so your SIP URI might be
   ``sip:6505551234@example.com`` - by default, SIP uses this realm for
   routing but ``example.com`` won't resolve to your host so you need to
   configure an outbound proxy on all your SIP clients (more details
   later)
-  performance - since all software runs on a single virtual machine,
   performance is significantly lower than even the smallest scale
   deployment
-  scalability - there is no option to scale up and add more virtual
   machines to boost capacity - for this, you must create a normal
   deployment
-  fault-tolerance - since everything runs on a single virtual machine,
   if that virtual machine fails, the service as a whole fails.

Installation Options
--------------------

All-in-one images can be installed on EC2 or on your own virtualization
platform, as long as it supports `OVF (Open Virtualization
Format) <http://dmtf.org/standards/ovf>`__.

-  To install on EC2, follow the `all-in-one EC2 AMI installation
   instructions <All_in_one_EC2_AMI_Installation.md>`__.
-  To install on your own virtualization platform, follow the
   `all-in-one OVF installation
   instructions <All_in_one_OVF_Installation.md>`__.

Manual Build
------------

If your virtualization platform is not EC2 and doesn't support OVF, you
may still be able to manually build an all-in-one node. To do so,

1. install `Ubuntu 14.04 - 64bit server
   edition <http://releases.ubuntu.com/trusty/>`__
2. find the ``preseed/late_command`` entry in the `all-in-one image's
   install
   script <https://github.com/Metaswitch/clearwater-vm-images/blob/master/ubuntu-ovf/ubuntu-server.seed>`__
   - as of writing this is as follows, but please check the linked file
   for the latest version

   ::

        d-i preseed/late_command string in-target bash -c '{ echo "#!/bin/bash" ; \
                                                    echo "set -e" ; \
                                                    echo "repo=... # filled in by make_ovf.sh" ; \
                                                    echo "curl -L https://raw.githubusercontent.com/Metaswitch/clearwater-infrastructure/master/scripts/clearwater-aio-install.sh | sudo bash -s clearwater-auto-config-generic $repo" ; \
                                                    echo "python create_numbers.py --start 6505550000 --count 1000" ; \
                                                    echo "rm /etc/rc2.d/S99zclearwater-aio-first-boot" ; \
                                                    echo "poweroff" ; } > /etc/rc2.d/S99zclearwater-aio-first-boot ; \
                                                  chmod a+x /etc/rc2.d/S99zclearwater-aio-first-boot'

3. run the command (stripping the
   ``d-i preseed/late_command string in-target`` prefix, filling in the
   repo variable - the default is ``http://repo.cw-ngv.com/stable``, and
   stripping the ``\``) - this will create an
   ``/etc/rc2.d/S99zclearwater-aio-first-boot`` script
4. run the ``/etc/rc2.d/S99zclearwater-aio-first-boot`` script - this
   will install the all-in-one software and then shutdown (ready for an
   image to be taken)
5. restart the node.


