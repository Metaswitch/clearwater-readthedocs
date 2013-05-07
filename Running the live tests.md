# Running the Clearwater Live Tests

The Clearwater team have put together a suite of live tests that can be run over a deployment to confirm that the high level function is working.  These instructions will take you through installing the test suite and running the tests.

## Prerequisites

* You've [installed Clearwater](Installation Instructions)
* You have an Ubuntu Linux machine available to drive the tests
 - If you installed through the automated install process, the chef-client is a perfectly good choice for this task

## Installing dependencies

On your test machine, run

    sudo apt-get install build-essential git --yes
    curl -L https://get.rvm.io | bash -s stable
    source ~/.rvm/scripts/rvm
    rvm autolibs enable
    rvm install 1.9.3
    rvm use 1.9.3

This will install Ruby version 1.9.3 and its dependencies.

## Fetching the code

Run the following to download and install the Clearwater test suite

    git clone git@github.com:Metaswitch/clearwater-live-test.git
    cd clearwater-live-test
    bundle install

## Work out your base domain

If you installed Clearwater manually, your base DNS name will simply be `<zone>`. If you installed using the automated install process, your base DNS name will be `<name>.<zone>`. For the rest of these instructions, the base DNS name will be referred to as `<domain>`.

## Work out your signup code

The tests need your signup code to create a test user.
You set this as `signup_code` during install:
[manually in /etc/clearwater/config](Manual Install)
or [automatically in knife.rb](Installing a Chef client). For the rest of these instructions, the
signup code will be referred to as `<code>`.

## Running the tests

To run the subset of the tests that don't require PSTN interconnect to be configured, simply run

    rake test[<domain>] SIGNUP_CODE=<code>

The suite of tests will be run and the results will be printed on-screen.

## PSTN testing

The live test framework also has the ability to test various aspects of PSTN interconnect.  If you've configured your Clearwater deployment with an IBCF node that connects it to a PSTN trunk, you can test that functionality by picking a real phone (e.g. your mobile) and running

    rake test[<domain>] PSTN=true LIVENUMBER=<your phone #> SIGNUP_CODE=<code>

Which will test call services related to the PSTN and will ring your phone and play an audio clip to you (twice, to cover both TCP and UDP).

## Where next?

Now that you've confirmed that your Clearwater system is operational, you might want to [make a real call](Making your first call) or [explore Clearwater](Exploring Clearwater) to see what else Clearwater offers.
