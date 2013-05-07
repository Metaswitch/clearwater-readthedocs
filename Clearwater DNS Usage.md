# Clearwater DNS Usage

Clearwater uses DNS records to allow the individual devices in the deployment to discover each other.

Below `<root>` is used to represent the DNS root domain which is hosting your deployment.  For a manual deployment this is just `<zone>`, for an automated install, this will be `<name>.<zone>`.

## Required DNS entries

The following A records are required for Clearwater function:

* `<root>` - Public IP addresses of all of the Bono nodes
* `sprout.<root>` - Private IP addresses of all of the Sprout nodes
* `hs.<root>` - Private IP addresses of all of the Homestead nodes
* `homer.<root>` - Private IP addresses of all of the Homer nodes
* `ellis.<root>` - Public IP address of the Ellis node
