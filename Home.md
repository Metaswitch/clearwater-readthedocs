# Welcome to Clearwater

Project Clearwater is an open-source IMS core, developed by [Metaswitch Networks](http://www.metaswitch.com) and released under the [GNU GPLv3](http://www.projectclearwater.org/download/license/). You can find more information about it on [our website](http://www.projectclearwater.org/).

## Latest Release

The latest stable release of Clearwater is "Reservoir Dogs".

## Architecture

Clearwater is architected from the ground up to be fully horizontally
scalable, modular and to support running in virtualized environments.
See our [[Clearwater Architecture]] page for a
bird's eye view of a Clearwater deployment and a guided tour of the
various functional components that comprise it.

## Getting Started

* [[Installation Instructions]]
* [[Making your first call]]
* [[Running the live tests]]
* [[A tour of Clearwater|Clearwater Tour]]

## Looking Deeper

To look at the optional extra features and function of your Clearwater deployment and for discussions about Clearwater scaling and redundancy, see [[Exploring Clearwater]].

## Getting Source Code

All the source code is on [github](https://github.com/Metaswitch), in the following repositories (and their submodules).

*   [chef](https://github.com/Metaswitch/chef) - [Chef](http://www.opscode.com/chef/) recipes for Clearwater deployment
*   [clearwater-infrastructure](https://github.com/Metaswitch/clearwater-infrastructure) - General infrastructure for Clearwater deployments
*   [clearwater-logging](https://github.com/Metaswitch/clearwater-logging) - Logging infrastructure for Clearwater deployments
*   [clearwater-live-test](https://github.com/Metaswitch/clearwater-live-test) - Live test for Clearwater deployments
*   [clearwater-docs](https://github.com/Metaswitch/clearwater-docs) - This documentation repository
*   [crest](https://github.com/Metaswitch/crest) - RESTful HTTP service built on Cassandra - provides Homer and Homestead.
*   [ellis](https://github.com/Metaswitch/ellis) - Clearwater provisioning server
*   [sprout](https://github.com/Metaswitch/sprout) - sprout and bono, the Clearwater SIP router and edge proxy

## Contributing

You can contribute by making a Github pull request. See our documented [[Pull request process]].

There is more information about contributing to Project Clearwater on the [community page of our project website](http://www.projectclearwater.org/community/).

## Help

If you want help, or want to help others by making Clearwater better, see the
[[Support]] page.


## License and Acknowledgements

Clearwater's license is documented in [LICENSE.txt](https://github.com/Metaswitch/clearwater-docs/blob/master/LICENSE.txt).

It uses other open-source components as acknowledged in [README.txt](https://github.com/Metaswitch/clearwater-docs/blob/master/README.txt).