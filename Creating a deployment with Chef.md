# Creating a deployment with Chef

This is the final stage in creating a Clearwater deployment using the [automated install process](Automated Install).  Here we will actually create the deployment - commissioning servers and configuring DNS records.

## Prerequisites

* You must have [created the chef client machine](Installing a Chef client) and have SSH access to the ubuntu user on it.
* You must have [created a deployment environment](Creating a deployment environment) and know its name, `<name>`.

## Creating the deployment

To kick off construction of the deployment, run the following on the chef-client machine.

    cd ~/chef
    knife deployment resize -E <name> -V

Follow the on-screen prompts.

This will:

* Commission AWS instances
* Install the Clearwater software
* Configure security groups
* Configure DNS
* Start the Clearwater services

## Restart Cassandra

The automated install of Cassandra on the Homer and Homestead instances is not clean (this is a known bug) and requires the Cassandra service to be restarted before Homer or Homestead becomes functional.  This command will stop the Cassandra instances, causing Monit to restart them.

    knife ssh -i ~/.chef/<keypair>.pem "chef_environment:<name> AND (role:homer OR role:homestead)" "sudo service cassandra stop"

## Optional arguments

The following modifiers are available to set the scale of your deployment.

* `--bono-count NUM` - Create `NUM` Bono nodes (default is 1)
* `--sprout-count NUM` - Create `NUM` Sprout nodes (default is 1)
* `--homer-count NUM` - Create `NUM` Homer nodes (default is 1)
* `--homestead-count NUM` - Create `NUM` Homestead nodes (default is 1)
* `--subscribers NUM` - Auto-scale the deployment to handle `NUM` subscribers.
  - Due to a known limitation of the install process, Ellis will allocate 1000 numbers regardless of this value.
  - To bulk provision subscriber (without using Ellis), follow [these instructions]() @@@ TODO Link this

## Next steps

Now your deployment is installed and ready to use, you'll want to test it.

* [Making your first call](Making your first call)
* [Running the live tests](Running the live tests)
