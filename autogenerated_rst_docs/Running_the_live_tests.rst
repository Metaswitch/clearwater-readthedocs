Running the Clearwater Live Tests
=================================

The Clearwater team have put together a suite of live tests that can be
run over a deployment to confirm that the high level function is
working. These instructions will take you through installing the test
suite and running the tests.

Prerequisites
-------------

-  You've `installed Clearwater <Installation_Instructions.md>`__
-  You have an Ubuntu Linux machine available to drive the tests
-  If you installed through the automated install process, the chef
   workstation is a perfectly good choice for this task

Installing dependencies
-----------------------

On your test machine, run

::

    sudo apt-get install build-essential git --yes
    curl -L https://get.rvm.io | bash -s stable
    source ~/.rvm/scripts/rvm
    rvm autolibs enable
    rvm install 1.9.3
    rvm use 1.9.3

This will install Ruby version 1.9.3 and its dependencies.

Fetching the code
-----------------

Run the following to download and install the Clearwater test suite

::

    git clone -b stable --recursive git@github.com:Metaswitch/clearwater-live-test.git
    cd clearwater-live-test
    bundle install

Make sure that you have an SSH key - if not, see the `GitHub
instructions <https://help.github.com/articles/generating-ssh-keys>`__
for how to create one.

Work out your signup code
-------------------------

The tests need your signup code to create a test user. You set this as
``signup_key`` during install: `manually in
/etc/clearwater/shared\_config <Manual_Install.md>`__ or `automatically
in knife.rb <Installing_a_Chef_workstation.md>`__. For the rest of these
instructions, the signup code will be referred to as ``<code>``.

Running the tests against an All-in-One node
--------------------------------------------

Work out your All-in-One node's identity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This step is only required if you installed an All-in-One node, either
from an AMI or an OVF. If you installed manually or using the automated
install process, just move on to the next step.

If you installed an All-in-One node from an Amazon AMI, you need the
public DNS name that EC2 has assigned to your node. This will look
something like ``ec2-12-34-56-78.compute-1.amazonaws.com`` and can be
found on the EC2 Dashboard on the "instances" panel. If you installed an
All-in-One node from an OVF image, you need the IP address that was
assigned to the node via DHCP. You can find this out by logging into the
node's console and typing ``hostname -I``.

For the rest of these instructions, the All-in-One node's identity will
be referred to as ``<aio-identity>``.

Run the tests
~~~~~~~~~~~~~

To run the subset of the tests that don't require PSTN interconnect to
be configured, simply run

::

    rake test[example.com] SIGNUP_CODE=<code> PROXY=<aio-identity> ELLIS=<aio-identity>

The suite of tests will be run and the results will be printed
on-screen.

Running the tests against a full deployment
-------------------------------------------

Work out your base domain
~~~~~~~~~~~~~~~~~~~~~~~~~

-  If you installed Clearwater manually, your base DNS name will simply
   be ``<zone>``.
-  If you installed using the automated install process, your base DNS
   name will be ``<name>.<zone>``.

For the rest of these instructions, the base DNS name will be referred
to as ``<domain>``.

Running the tests
~~~~~~~~~~~~~~~~~

To run the subset of the tests that don't require PSTN interconnect to
be configured, simply run

::

    rake test[<domain>] SIGNUP_CODE=<code>

The suite of tests will be run and the results will be printed
on-screen. If your deployment doesn't have DNS entries for the Bono and
Ellis domain, then these can be passed to rake by adding the ``PROXY``
and ``ELLIS`` parameters, e.g.

::

    rake test[<domain>] SIGNUP_CODE=<code> PROXY=<Bono domain> ELLIS=<Ellis domain>

PSTN testing
------------

The live test framework also has the ability to test various aspects of
PSTN interconnect. If you've configured your Clearwater deployment with
an IBCF node that connects it to a PSTN trunk, you can test that
functionality by picking a real phone (e.g. your mobile) and running

::

    rake test[<domain>] PSTN=true LIVENUMBER=<your phone #> SIGNUP_CODE=<code>

Which will test call services related to the PSTN and will ring your
phone and play an audio clip to you (twice, to cover both TCP and UDP).

Where next?
-----------

Now that you've confirmed that your Clearwater system is operational,
you might want to `make a real call <Making_your_first_call.md>`__ or
`explore Clearwater <Exploring_Clearwater.md>`__ to see what else
Clearwater offers.
