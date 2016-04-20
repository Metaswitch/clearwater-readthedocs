All-in-one OVF Installation
===========================

This pages describes how to install an `all-in-one
image <All_in_one_Images.md>`__ on your own virtualization platform
using `OVF (Open Virtualization
Format) <http://dmtf.org/standards/ovf>`__.

Supported Platforms
-------------------

This process should work on any virtualization platform that supports
OVFs using x86-64 CPUs, but has only been tested on

-  `VMware Player <http://www.vmware.com/products/player/>`__
-  `VirtualBox <https://www.virtualbox.org/>`__
-  `VMware
   ESXi <http://www.vmware.com/products/vsphere-hypervisor/overview.html>`__.

The image uses DHCP to gets its IP configuration, so the virtualization
platform must either serve DHCP natively or be connected to a network
with a DHCP server.

If you install/run the OVF on another platform, please let us know how
you get on on the `mailing
list <http://lists.projectclearwater.org/listinfo/clearwater>`__ so we
can update this page.

Installation Process
--------------------

To install the OVF, you must first download it from
http://vm-images.cw-ngv.com/cw-aio.ova and save it to disk.

Then, you must import it into your virtualization platform. The process
for this varies.

-  On VMware Player, choose **File->Open a Virtual Machine** from the
   menu and select the cw-aio.ova file you downloaded. On the Import
   Virtual Machine dialog that appears, the defaults are normally fine,
   so you can just click **Import**.
-  On VirtualBox, choose **File->Import Appliance...** from the menu. In
   the Appliance Import Wizard, click **Choose...**, select the
   cw-aio.ova file you downloaded and click **Next**. On the next tab,
   you can view the settings and then click **Import**.
-  On VMware ESXi, using the VMware vSphere Client, choose
   **File->Deploy OVF Template...** from the menu. Select the cw-aio.ova
   file you downloaded and click through assigning it a suitable name,
   location and attached network (which must support DHCP) before
   finally clicking **Finish** to create the virtual machine.

Running and Using the Image
---------------------------

Once you've installed the virtual machine, you should start it in the
usual way for your virtualization platform.

If you attach to the console, you should see an Ubuntu loading screen
and then be dropped at a ``cw-aio`` login prompt. The username is
``ubuntu`` and the password is ``cw-aio``. Note that the console is
hard-coded to use a US keyboard, so if you have a different keyboard you
might find that keys are remapped - in particular the ``-`` key.

The OVF provides 3 network services.

-  SSH - username is ``ubuntu`` and password is ``cw-aio``
-  HTTP to ellis for subscriber management - sign-up code is ``secret``.
   You will probably want to change this to a more secure value - see
   `"Modifying Clearwater
   settings" <Modifying_Clearwater_settings.md>`__ for how to do this.
-  SIP to bono for call signaling - credentials are provisioned through
   ellis.

How these network services are exposed can vary depending on the
capabilities of the platform.

-  VMware Player sets up a private network between your PC and the
   virtual machine and normally assigns the virtual machine IP address
   ``192.168.28.128``. To access ellis, you'll need to point your
   browser at http://192.168.28.128. To register over SIP, you'll need
   to configure an outbound proxy of 192.168.28.128 port 5060.

-  VirtualBox uses NAT on the local IP address, exposing SSH on port
   8022, HTTP on port 8080 and SIP on port 8060. To access ellis, you'll
   need to point your browser at http://localhost:8080. To register over
   SIP, you'll need to configure an outbound proxy of localhost port
   8060.

-  VMware ESXi runs the host as normal on the network, so you can
   connect to it directly. To find out its IP address, log in over the
   console and type ``hostname -I``. To access ellis, just point your
   browser at this IP address. To register over SIP, you'll need to
   configure an outbound proxy for this IP address.

Once you've successfully connected to ellis, try `making your first
call <Making_your_first_call.md>`__ - just remember to configure the SIP
outbound proxy as discussed above.
