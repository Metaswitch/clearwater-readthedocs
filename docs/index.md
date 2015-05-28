# Welcome to Clearwater

Project Clearwater is an open-source IMS core, developed by [Metaswitch Networks](http://www.metaswitch.com) and released under the [GNU GPLv3](http://www.projectclearwater.org/download/license/). You can find more information about it on [our website](http://www.projectclearwater.org/).

## Latest Release

The latest stable release of Clearwater is "[East Of Eden](http://www.goodreads.com/book/show/4406.East_of_Eden)", which is named after John Steinbeck's brilliant 1952 novel, a must read once you've finished playing around with Clearwater.

## Architecture

Clearwater is architected from the ground up to be fully horizontally
scalable, modular and to support running in virtualized environments.
See our [Clearwater Architecture](Clearwater_Architecture.md) page for a
bird's eye view of a Clearwater deployment and a guided tour of the
various functional components that comprise it.

## Getting Started

* [Installation Instructions](Installation_Instructions.md)
* [Making your first call](Making_your_first_call.md)
* [Running the live tests](Running_the_live_tests.md)
* [A tour of Clearwater](Clearwater_Tour.md)

## Looking Deeper

To look at the optional extra features and function of your Clearwater deployment and for discussions about Clearwater scaling and redundancy, see [Exploring Clearwater](Exploring_Clearwater.md).

## Getting Source Code

All the source code is on [GitHub](https://github.com/Metaswitch), in the following repositories (and their submodules).

*   [chef](https://github.com/Metaswitch/chef) - [Chef](http://www.opscode.com/chef/) recipes for Clearwater deployment
*   [clearwater-infrastructure](https://github.com/Metaswitch/clearwater-infrastructure) - General infrastructure for Clearwater deployments
*   [clearwater-logging](https://github.com/Metaswitch/clearwater-logging) - Logging infrastructure for Clearwater deployments
*   [clearwater-live-test](https://github.com/Metaswitch/clearwater-live-test) - Live test for Clearwater deployments
*   [clearwater-readthedocs](https://github.com/Metaswitch/clearwater-readthedocs) - This documentation repository
*   [crest](https://github.com/Metaswitch/crest) - RESTful HTTP service built on Cassandra - provides Homer (the Clearwater XDMS) and Homestead-Provisioning (the Clearwater provisioning backend)
*   [ellis](https://github.com/Metaswitch/ellis) - Clearwater provisioning server
*   [sprout](https://github.com/Metaswitch/sprout) - Sprout and Bono, the Clearwater SIP router and edge proxy
*   [homestead](https://github.com/Metaswitch/homestead) - Homestead, the Clearwater HSS-cache.
*   [ralf](https://github.com/Metaswitch/ralf) - Ralf, the Clearwater CTF.

## Contributing

You can contribute by making a GitHub pull request. See our documented [Pull request process](Pull_request_process.md).

There is more information about contributing to Project Clearwater on the [community page of our project website](http://www.projectclearwater.org/community/).

## Help

If you want help, or want to help others by making Clearwater better, see the
[Support](Support.md) page.


## License and Acknowledgements

Clearwater's license is documented in [LICENSE.txt](https://github.com/Metaswitch/clearwater-docs/blob/master/LICENSE.txt).

It uses other open-source components as acknowledged in [README.txt](https://github.com/Metaswitch/clearwater-docs/blob/master/README.txt).
