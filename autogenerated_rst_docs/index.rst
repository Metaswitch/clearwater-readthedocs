Welcome to Clearwater
=====================

Project Clearwater is an open-source IMS core, developed by `Metaswitch
Networks <http://www.metaswitch.com>`__ and released under the `GNU
GPLv3 <http://www.projectclearwater.org/download/license/>`__. You can
find more information about it on `our
website <http://www.projectclearwater.org/>`__.

Latest Release
--------------

The latest stable release of Clearwater is "`The Year of the
Flood <https://www.goodreads.com/book/show/6080337-the-year-of-the-flood>`__\ ".

Architecture
------------

Clearwater is architected from the ground up to be fully horizontally
scalable, modular and to support running in virtualized environments.
See our `Clearwater Architecture <Clearwater_Architecture.md>`__ page
for a bird's eye view of a Clearwater deployment and a guided tour of
the various functional components that comprise it.

Getting Started
---------------

-  `Installation Instructions <Installation_Instructions.md>`__
-  `Making your first call <Making_your_first_call.md>`__
-  `Running the live tests <Running_the_live_tests.md>`__
-  `A tour of Clearwater <Clearwater_Tour.md>`__

Looking Deeper
--------------

To look at the optional extra features and function of your Clearwater
deployment and for discussions about Clearwater scaling and redundancy,
see `Exploring Clearwater <Exploring_Clearwater.md>`__.

Getting Source Code
-------------------

All the source code is on `GitHub <https://github.com/Metaswitch>`__, in
the following repositories (and their submodules).

-  `chef <https://github.com/Metaswitch/chef>`__ -
   `Chef <http://www.opscode.com/chef/>`__ recipes for Clearwater
   deployment
-  `clearwater-infrastructure <https://github.com/Metaswitch/clearwater-infrastructure>`__
   - General infrastructure for Clearwater deployments
-  `clearwater-logging <https://github.com/Metaswitch/clearwater-logging>`__
   - Logging infrastructure for Clearwater deployments
-  `clearwater-live-test <https://github.com/Metaswitch/clearwater-live-test>`__
   - Live test for Clearwater deployments
-  `clearwater-readthedocs <https://github.com/Metaswitch/clearwater-readthedocs>`__
   - This documentation repository
-  `crest <https://github.com/Metaswitch/crest>`__ - RESTful HTTP
   service built on Cassandra - provides Homer (the Clearwater XDMS) and
   Homestead-prov (the Clearwater provisioning backend)
-  `ellis <https://github.com/Metaswitch/ellis>`__ - Clearwater
   provisioning server
-  `sprout <https://github.com/Metaswitch/sprout>`__ - Sprout and Bono,
   the Clearwater SIP router and edge proxy
-  `homestead <https://github.com/Metaswitch/homestead>`__ - Homestead,
   the Clearwater HSS-cache.
-  `ralf <https://github.com/Metaswitch/ralf>`__ - Ralf, the Clearwater
   CTF.

Contributing
------------

You can contribute by making a GitHub pull request. See our documented
`Pull request process <Pull_request_process.md>`__.

There is more information about contributing to Project Clearwater on
the `community page of our project
website <http://www.projectclearwater.org/community/>`__.

Help
----

If you want help, or want to help others by making Clearwater better,
see the `Support <Support.md>`__ page.

License and Acknowledgements
----------------------------

Clearwater's license is documented in
`LICENSE.txt <https://github.com/Metaswitch/clearwater-docs/blob/master/LICENSE.txt>`__.

It uses other open-source components as acknowledged in
`README.txt <https://github.com/Metaswitch/clearwater-docs/blob/master/README.txt>`__.

.. _1:

.. toctree::
   :caption: Overview
   :maxdepth: 0

   Home <self>
   Clearwater Architecture <Clearwater_Architecture.rst>
   Clearwater Tour <Clearwater_Tour.rst>
   Exploring Clearwater <Exploring_Clearwater.rst>
   Support <Support.rst>
   Troubleshooting and Recovery <Troubleshooting_and_Recovery.rst>

.. _2:

.. toctree::
   :caption: Installation
   :maxdepth: 0

   Installation Instructions <Installation_Instructions.rst>
   All-in-one Images <All_in_one_Images.rst>
   Automated Install <Automated_Install.rst>
   Manual Install <Manual_Install.rst>
   All in one EC2 AMI Installation <All_in_one_EC2_AMI_Installation.rst>
   All-in-one OVF Installation <All_in_one_OVF_Installation.rst>
   Installing a Chef server <Installing_a_Chef_server.rst>
   Installing a Chef workstation <Installing_a_Chef_workstation.rst>
   Creating a deployment environment <Creating_a_deployment_environment.rst>
   Creating a deployment with Chef <Creating_a_deployment_with_Chef.rst>
   Making your first call <Making_your_first_call.rst>
   Configuring the native Android SIP client <Configuring_the_native_Android_SIP_client.rst>
   Configuring Zoiper Android/iOS Client <Configuring_Zoiper_Android_iOS_Client.rst>


.. _3:

.. toctree::
   :caption: Upgrading and Modifying
   :maxdepth: 0

   Upgrading a Clearwater deployment <Upgrading_a_Clearwater_deployment.rst>
   Modifying Clearwater settings <Modifying_Clearwater_settings.rst>
   Clearwater Configuration Options Reference <Clearwater_Configuration_Options_Reference.rst>
   Migrating to Automatic Clustering and Config Sharing <Migrating_To_etcd.rst>


.. _4:

.. toctree::
   :caption: Integration
   :maxdepth: 0

   Configuring an Application Server <Configuring_an_Application_Server.rst>
   External HSS Integration <External_HSS_Integration.rst>
   OpenIMSCore HSS Integration <OpenIMSCore_HSS_Integration.rst>
   CDF Integration <CDF_Integration.rst>
   Clearwater Firewall Configuration <Clearwater_IP_Port_Usage.rst>
   Clearwater DNS Usage <Clearwater_DNS_Usage.rst>
   ENUM <ENUM.rst>
   Voxbone <Voxbone.rst>
   Clearwater SNMP Statistics <Clearwater_SNMP_Statistics.rst>
   SNMP Alarms <SNMP_Alarms.rst>
   Radius Login Authentication <Radius_Authentication.rst>


.. _5:

.. toctree::
   :caption: Features
   :maxdepth: 0

   Application Server Guide <Application_Server_Guide.rst>
   WebRTC support in Clearwater <WebRTC_support_in_Clearwater.rst>
   IR.92 Supplementary Services <IR.92_Supplementary_Services.rst>
   Backups <Backups.rst>
   Clearwater Call Barring Support <Clearwater_Call_Barring_Support.rst>
   Clearwater Call Diversion Support <Clearwater_Call_Diversion_Support.rst>
   Clearwater Elastic Scaling <Clearwater_Elastic_Scaling.rst>
   Clearwater Privacy Feature <Clearwater_Privacy_Feature.rst>
   IBCF <IBCF.rst>
   Multiple Domains <Multiple_Domains.rst>
   Multiple Network Support <Multiple_Network_Support.rst>
   Geographic redundancy <Geographic_redundancy.rst>
   IPv6 <IPv6.rst>
   SIP Interface Specifications <SIP_Interface_Specifications.rst>
   Automatic Clustering and Configuration Sharing <Automatic_Clustering_Config_Sharing.rst>
   Provisioning Subscribers <Provisioning_Subscribers.rst>


.. _6:

.. toctree::
   :caption: Failure Recovery
   :maxdepth: 0

   Permanent Node Failures <Handling_Failed_Nodes.rst>


.. _7:

.. toctree::
   :caption: Development
   :maxdepth: 0

   Clearwater C++ Coding Guidelines <Clearwater_CPP_Coding_Guidelines.rst>
   Clearwater Ruby Coding Guidelines <Clearwater_Ruby_Coding_Guidelines.rst>
   Debugging Bono, Sprout and Homestead with GDB and Valgrind <Debugging_Bono_Sprout_and_Homestead_with_GDB_and_Valgrind.rst>
   Pull request process <Pull_request_process.rst>


.. _8:

.. toctree::
   :caption: Testing
   :maxdepth: 0

   Clearwater stress testing <Clearwater_stress_testing.rst>
   Cacti <Cacti.rst>
   Running the live tests <Running_the_live_tests.rst>


