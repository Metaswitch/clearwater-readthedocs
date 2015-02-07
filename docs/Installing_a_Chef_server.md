# Installing a Chef server

This is the first step in preparing to install a Clearwater deployment using the [automated install](Automated_Install) process.  These instructions will guide you through installing a Chef server on an EC2 instance.

## Prerequisites

* An Amazon EC2 account.
* A DNS root domain configured as a hosted zone with Route53 (Amazon's built-in DNS service, accessible from the EC2 console). This domain will be referred to as `<zone>` in this document.

## Create the instance

Create a `m1.small` AWS EC2 instance running `Ubuntu Server 12.04.1 LTS` using the AWS web interface. The SSH keypair you provide here is referred to below as `<amazon_ssh_key>`. It is easiest if you use the same SSH keypair for all of your instances.

Configure its security group to allow access on ports `TCP/22`, `TCP/4040` and `TCP/4000` (for SSH, Chef WebUI and Chef control respectively).

Configure a DNS entry for this machine, `chef-server.<zone>`. (The precise name isn't important, but we use this consistently in the documentation that follows.) It should have a non-aliased A record pointing at the public IP address of the instance as displayed in the EC2 console.

Once the instance is up and running and you can connect to it over SSH, you may continue to the next steps.

If you make a mistake, simply delete the instance permanently by selecting "Terminate" in the EC2 console, and start again. The terminated instance may take a few minutes to disappear from the console.

## Prepare your package manager

Connect to `chef-server.<zone>` as the `ubuntu` user over SSH.

Install the `add-apt-key` tool.

    sudo apt-get install add-apt-key -y

Under sudo, create `/etc/apt/sources.list.d/opscode.list` with the following content:

    deb http://apt.opscode.com/ precise-0.10 main

Install the GPG key for this repository:

    sudo add-apt-key 83EF826A

Install the Chef keyring and update APT's indexes.

    sudo apt-get update
    sudo apt-get install opscode-keyring -y
    sudo apt-get upgrade -y

Once this is done, you can continue on to install the Chef server.

## Install the Chef server

Do the install.

    sudo apt-get install chef-server -y

When prompted, enter `http://chef-server.<zone>:4000` as the Chef Server URL.  Choose (and remember!) your own passwords for the RabbitMQ server and Web UI when prompted.  **These passwords must be longer than 6 characters and not contain any quote characters**.  These passwords will be referred to in later steps as `<rabbitMQPass>` and `<webUIPass>` respectively.

To check that the install was successful, run

    sudo netstat -plant | grep -e 4040 -e 4000

which should display something like:

    tcp        0      0 0.0.0.0:4040            0.0.0.0:*               LISTEN      16662/merb : chef-s
    tcp        0      0 0.0.0.0:4000            0.0.0.0:*               LISTEN      16556/merb : chef-s

If this is not the case, you probably specified an invalid password during the install.  You can retry the install with

    sudo apt-get purge chef-server
    sudo apt-get install chef-server

## Expose the validator key over SSH

Your chef client will need a valid validator key to be able to spin up instances.  So we can retrieve it from the chef-client later, copy the key from the default location to a folder in the `ubuntu` user's home directory.

    mkdir -p ~/.chef
    sudo cp /etc/chef/validation.pem ~/.chef/
    sudo chown ubuntu:ubuntu ~/.chef/validation.pem

## Next steps

Once your server is installed, you can continue on to [install a chef client](Installing_a_Chef_client).
