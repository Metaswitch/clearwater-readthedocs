# Creating a deployment environment

These instructions make up part of the [automated install process](Automated Install) for Clearwater.  They will take you through creating a deployment environment, which will be used to define the specific settings for a Clearwater deployment.

## Prerequisites

* You must have [installed a Chef client](Installing a Chef client).
* You must have SSH access to the ubuntu user on the chef-client machine.

## Creating a keypair

You need to configure the AWS keypair used to access your Clearwater deployment. You may reuse the one you created when creating your Chef client and server; or you may create a new one (EC2 Dashboard > Network & Security > Key Pairs > Create Key Pair) for finer-grained access rights. The name you give your keypair will be referred to as `<keypair_name>` from this point.

Amazon will give you a `<keypair_name>`.pem file; copy that file to the `/home/ubuntu/.chef/` directory on your Chef client, and make it readable only to your user with `chmod 0700 /home/ubuntu/.chef ; chmod 0400 /home/ubuntu/.chef/<keypair_name>.pem`.

## Creating the environment

Before creating an environment, choose a name (e.g. "clearwater") which will be referred to as `<name>` in the following steps.  Now, on the chef-client machine, create a file in `~/chef/environments/<name>.rb` with the following contents:

    name "<name>"
    description "Clearwater deployment - <name>"
    cookbook_versions "clearwater" => "= 0.1.0"
    override_attributes "clearwater" => {
      "root_domain" => "<zone>",
      "availability_zones" => ["us-east-1a", "us-east-1b"],
      "repo_server" => "http://repo.cw-ngv.com/latest",
      "number_start" => "6505550000",
      "number_count" => 1000,
      "keypair" => "<keypair_name>",
      "keypair_dir" => "/home/ubuntu/.chef/",
      "pstn_number_count" => 0
    }

Note that the value of  "keypair" should *not* include the trailing .pem.

## Uploading the environment

The newly created environment needs to be uploaded to the Chef server before it can be used.

    cd ~/chef
    ./update_chef_server.sh <name>

## Next steps

At this point, your deployment environment is created and can be used to [create a new deployment](Creating a deployment with Chef).
