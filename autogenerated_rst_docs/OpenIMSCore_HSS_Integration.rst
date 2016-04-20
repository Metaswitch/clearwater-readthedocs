OpenIMS HSS Integration
=======================

As discussed on the `External HSS
Integration <External_HSS_Integration.md>`__ page, Clearwater can
integrate with an external HSS.

This page describes how to install and configure the
`OpenIMSCore <http://www.openimscore.org/>`__ HSS as this external HSS.
It assumes that you have already read the `External HSS
Integration <External_HSS_Integration.md>`__ page.

Installation with Chef
----------------------

If you have a deployment environment created by following the `automated
install instructions <Automated_Install.md>`__, then you can create a
HSS by running ``knife box create -E <env> openimscorehss``. You should
then follow `the configuration instructions
below <OpenIMSCore_HSS_Integration.md/#configuration>`__.

Installing OpenIMSCore HSS manually
-----------------------------------

To install OpenIMSCore HSS,

1. Follow the "Adding this PPA to your system" steps at
   https://launchpad.net/~rkd-u/+archive/ubuntu/fhoss

2. Run ``sudo apt-get update; sudo apt-get install openimscore-fhoss``

3. Answer the installation questions appropriately, including providing
   the IMS home domain, your local IP, and the MySQL root password
   (which you will have to provide both when installing MySQL and when
   intalling the HSS).

Configuration
-------------

Logging in
~~~~~~~~~~

OpenIMSCore HSS provides the administration UI over port 8080. The admin
username is hssAdmin.

-  If the HSS was installed using Chef, the hssAdmin password will be
   `the signup\_key setting from
   knife.rb <Installing_a_Chef_client/index.html#add-deployment-specific-configuration>`__.
-  If the HSS was installed manually, the hssAdmin password will be
   "hss". This can be changed by editing
   ``/usr/share/java/fhoss-0.2/conf/tomcat-users.xml`` and running
   ``sudo service openimscore-fhoss restart``.

Adding the MMTEL Application Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable the MMTEL application server built into Clearwater for all
subscribers,

1. access the OpenIMSCore HSS web UI, running on port 8080
2. log in as hssAdmin
3. navigate to ``Services``->``Application Servers``->``Search``
4. perform a search with no search string to find all application
   servers
5. select default\_as
6. change ``server_name`` to be ``sip:mmtel.your.home.domain``, where
   ``your.home.domain`` is replaced with your home domain
7. save your change.

Configuring Subscribers
~~~~~~~~~~~~~~~~~~~~~~~

To configure a subscriber,

1. create an IMS subscription
2. create an associated public user identity
3. create an associated private user identity, specifying

   1. the private ID to be the public ID without the ``sip:`` scheme
      prefix
   2. SIP Digest authentication.

4. add the home domain to the subscriber's visited networks

