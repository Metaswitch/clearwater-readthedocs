# Automated Install Instructions

These instructions will take you through preparing for an automated install  of Clearwater using Chef.  For a high level look at the install process, and a discussion of the various install methods, see [Installation Instructions](Installation Instructions).  The automated install is the suggested method for installing a large-scale deployment of Clearwater.

The automated install is only supported for deployments running in Amazon's EC2 cloud, where DNS is being provided by Amazon's Route53 service.  If your proposed deployment doesn't meet these requirements, you should use the [Manual Install](Manual Install) instructions instead.

## The Install Process

The automated install system is made up of two phases:

* A series of steps that need to be performed once, before any deployment is created.
* A simpler set of instructions that will actually create the deployment.

Once the first phase has been completed, multiple deployments (of various sizes) can be created by repeating the second phase multiple times.

The first phase:

* [Installing a Chef server](Installing a Chef server)
 - This server will track the created Clearwater nodes and allow the client access to them.
* [Configuring a Chef client](Installing a Chef client)
 - This machine will be the one on which deployments will be defined and managed.

The second phase:

* [Creating a deployment environment](Creating a deployment environment)
 - The automated install supports the existence and management of multiple deployments simultaneously, each deployment lives in an environment to keep them separate.
* [Creating the deployment](Creating a deployment with Chef)
 - Actually provisioning the servers, installing the Clearwater software and configuring DNS.

## Next steps

Once you've followed the instructions above, your Clearwater deployment is ready for use.  Be aware that the newly created DNS entries may take some time to propagate fully through your network and until propagation is complete, your deployment may not function correctly.  This propagation usually takes no more than 5 minutes.

To test the deployment, you can try making some real calls, or run the provided live test framework.

* [Making your first call](Making your first call)
* [Running the live test framework](Running the live tests)
