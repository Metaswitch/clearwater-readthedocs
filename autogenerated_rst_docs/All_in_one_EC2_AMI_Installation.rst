All-in-one EC2 AMI Installation
===============================

This pages describes how to launch and run an `all-in-one
image <All_in_one_Images.md>`__ in Amazon's EC2 environment.

Launch Process
--------------

Project Clearwater's all-in-one node is already available as a pre-built
AMI, which can be found in the Community AMIs list on the US East region
of EC2. Launching this follows exactly the same process as for other EC2
AMIs.

Before you launch the node, you will need an EC2 keypair, and a security
group configured to provide access to the `required
ports <Clearwater_IP_Port_Usage.md>`__.

To launch the node

-  From the EC2 console, make sure you're in the US East region, then
   select "Instances", "Launch instance" and then "Classic Wizard"
-  Select the "Community AMIs" tab, and search for "Clearwater"
-  Press "Select" for the Clearwater all-in-one AMI. Take the most
   recent version unless you have a good reason not to.
-  Choose the Instance Type you require (the node runs fine for basic
   functional testing on an t2.small)
-  From the remaining pages of parameters, the only ones that need to be
   set are Name (give the node whatever convenient name you wish),
   keypair and security group.

On the last page, press "Launch", and wait for the node to be started by
EC2.

Running and Using the Image
---------------------------

Once the node has launched, you can SSH to it using the keypair you
supplied at launch time, and username ``ubuntu``.

You can then try `making your first call <Making_your_first_call.md>`__
and `running the live tests <Running_the_live_tests.md>`__ - for these
you will need the signup key, which is ``secret``. You will probably
want to change this to a more secure value - see `"Modifying Clearwater
settings" <Modifying_Clearwater_settings.md>`__ for how to do this.
