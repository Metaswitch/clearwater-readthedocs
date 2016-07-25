# Installing a Chef Client

These instructions cover commissioning a Chef client node on an EC2 server as part of the [automated install process](Automated_Install.md) for Clearwater.

## Prerequisites

* An Amazon EC2 account.
* A DNS root domain configured with Route53 (Amazon's built-in DNS service, accessible from the EC2 console. This domain will be referred to as `<zone>` in this document.
* You must have [installed a Chef server](Installing_a_Chef_server.md) and thus know the `<chef-user-name>` and `<chef-user-password>` for your server.
* A web-browser with which you can visit the Chef server Web UI.

## Create the instance

Create a `t2.micro` AWS EC2 instance running `Ubuntu Server 14.04.2 LTS` using the AWS web interface.  Configure its security group to allow access on port 22 (for SSH). The SSH keypair you provide here is referred to below as `<amazon_ssh_key>`. It is easiest if you use the same SSH keypair for all of your instances.

Configure a DNS entry for this machine, `chef workstation.<zone>`. (The precise name isn't important, but we use this consistently in the documentation that follows.) It should have a non-aliased A record pointing at the public IP address of the instance as displayed in the EC2 console.

Once the instance is up and running and you can connect to it over SSH, you may continue to the next steps.

If you make a mistake, simply delete the instance permanently by selecting "Terminate" in the EC2 console, and start again. The terminated instance may take a few minutes to disappear from the console.

## Install Ruby 1.9.3

The Clearwater chef plugins use features from Ruby 1.9.3.  To start run the following command.

    curl -L https://get.rvm.io | bash -s stable

This may fail due to missing GPG signatures. If this happens it will suggest a command to run to resolve the problem (e.g. gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3`). Run the command suggested, then run the above command again, which should now succeed).

Next install the required ruby version.

    source ~/.rvm/scripts/rvm
    rvm autolibs enable
    rvm install 1.9.3
    rvm use 1.9.3

At this point, `ruby --version` should indicate that 1.9.3 is in use.

## Installing the Clearwater Chef extensions

On the chef workstation machine, install git and dependent libraries.

    sudo apt-get install git libxml2-dev libxslt1-dev

Clone the Clearwater Chef repository.

    git clone -b stable --recursive git://github.com/Metaswitch/chef.git ~/chef

This will have created a `chef` folder in your home directory, navigate there now.

    cd ~/chef

Finally install the Ruby libraries that are needed by our scripts.

    bundle install

## Creating a Chef user

You will need to configure yourself as a user on the chef server in order to use chef.

*  If you are the person who created the chef server you wil already have added yourself as a user, and will know your username, organization name, and you will have a private key (`<chef-user-name>`, `<org-name>`, `<chef-user-name>.pem` respectively). These will be needed later.
*  If you did not create the chef server, you will need to add an account for yourself. Log SSH on to the chef server and run the following commands, substituting in appropriate values for `USER_NAME`, `FIRST_NAME`, `LAST_NAME`, `PASSWORD` and `ORG_NAME`. We'll refer to the username as `<chef-user-name>` and the organization as `<org-name>`. This will create a `<chef-user-name>.pem` file in the current directory - save it for later.

        sudo chef-server-ctl user-create USER_NAME FIRST_NAME LAST_NAME EMAIL PASSWORD --filename USER_NAME.pem
        sudo chef-server-ctl org-user-add ORG_NAME USER_NAME --admin

## Configure the chef workstation machine

Back on the chef workstation machine, create a `.chef` folder in your home directory.

    mkdir ~/.chef

Copy the `<chef-user-name>.pem` file you saved off earlier to `~/.chef/<chef-user-name.pem>`

Copy the validator key from the chef server to your client. You will need to either copy the Amazon SSH key to the client and use it, or copy the validator

    scp -i <amazon_ssh_key>.pem ubuntu@chef-server.<zone>:<org-name>-validator.pem ~/.chef/

or (on an intermediate box with the SSH key available)

    scp -i <amazon_ssh_key>.pem ubuntu@chef-server.<zone>:<org-name>-validator.pem .
    scp -i <amazon_ssh_key>.pem <org-name>-validator.pem ubuntu@chef workstation.<zone>:~/.chef/

Configure knife using the built in auto-configuration tool.

    knife configure

* Use the default value for the config location.
* The Chef server URL should be `https://chef-server.<zone>/organizations/<org-name>`
* The Chef client name should be `<chef-user-name>`
* The validation client name should be `<org-name>-validator`
* The validation key location should be `~/.chef/<org-name>-validator.pem`.
* The chef repository path should be `~/chef/`

## Obtain AWS access keys

To allow the Clearwater extensions to create AWS instances or configure Route53 DNS entries, you will need to supply your AWS access key and secret access key.  To find your AWS keys, you must be logged in as the main AWS user, not an IAM user. Go to [http://aws.amazon.com](http://aws.amazon.com) and click on `My Account/Console` then `Security Credentials`. From there, under the `Access Credentials` section of the page, click on the `Access Keys` tab to view your access key.  The access key is referred to as `<accessKey>` below. To see your secret access key, just click on the `Show` link under `Secret Access Key`.  The secret access key will be referred to as `<secretKey>` below.

## Add deployment-specific configuration

Now add the following lines to the bottom of your `~/.chef/knife.rb`
file, using the AWS deployment keys are the ones you obtained above.

    # AWS deployment keys.
    knife[:aws_access_key_id]     = "<accessKey>"
    knife[:aws_secret_access_key] = "<secretKey>"

## Test your settings

Test that knife is configured correctly

    knife client list

This should return a list of clients and not raise any errors.

## Next steps

At this point, the Chef server is up and running and ready to manage installs and the chef client is ready to create deployments.  The next step is to [create a deployment environment](Creating_a_deployment_environment.md).
