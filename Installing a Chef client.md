# Installing a Chef Client

These instructions cover commissioning a Chef client node on an EC2 server as part of the [automated install process](Automated Install) for Clearwater.

## Prerequisites

* An Amazon EC2 account.
* A DNS root domain configured with Route53, this domain will be referred to as `<zone>` in this document.
* You must have [installed a Chef server](Installing a Chef server) and thus know the `<webUIPass>` for your server.
* A web-browser with which you can visit the Chef server Web UI.

## Create the instance

Create a `m1.small` AWS EC2 instance running `Ubuntu Server 12.04.1 LTS` using the AWS web interface.  Configure its security group to allow access on port 22 (for SSH).

Configure a DNS entry for this machine, `chef-client.<zone>`.

Once the instance is up and running and you can connect to it over SSH, you may continue to the next steps.

## Prepare APT

Connect to `chef-client.<zone>` as the `ubuntu` user over SSH.

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

Once this is done, you can continue on to install the Chef client software.

## Install the Chef client software

Install the Chef client tool.

    sudo apt-get install chef -y

During the install you will be prompted for the Chef server URL, enter `http://chef-server.<zone>:4000`.

## Install Ruby 1.9.3

The Clearwater chef plugins use features from Ruby 1.9.3.  Run the following to install it.

    curl -L https://get.rvm.io | bash -s stable
    source ~/.rvm/scripts/rvm
    rvm autolibs enable
    rvm install 1.9.3
    rvm use 1.9.3

At this point, `ruby --version` should indicate that 1.9.3 is in use.

## Create a Chef client for the chef-client machine

In a browser of your choice, navigate to `http://chef-server.<zone>:4040` to access the Web UI of the server.  Log in using `admin` and `<webUIPass>` and follow the on-screen instructions to change the WebUI password (you can 'change' it to its current value if you don't want to remember a new password).

Go to the `Clients` tab at the top of the screen and click `Create`, use `chef-client` for the name, __tick the `Admin` box__ and click `Create Client`.  On the next screen, you'll be presented with an RSA keypair, __copy the private half before moving away from this screen__.  Once you've copied the key, you can close your browser tab.

If you forgot to tick the admin box or forgot to copy the private key before closing the browser tab, delete the newly created client with the `delete` link and create a new one.

## Configure the chef-client machine

Back on the chef-client machine, create a `.chef` folder in your home directory.

    mkdir ~/.chef

Create `~/.chef/chef-client.pem` and paste the private key from the server into it.

Copy the validator key from the chef server to your client

    scp ubuntu@chef-server.<zone>:.chef/validation.pem ~/.chef/

Configure knife using the built in auto-configuration tool.

    knife configure

* Use the default value for the config location.
* The Chef server URL should be `http://chef-server.<zone>:4000`
* The Chef client name should be `chef-client`
* Use the default value for the validation client name.
* The validation key location should be `~/.chef/validation.pem`.
* The chef repository path should be `~/chef/`

## Obtain AWS access keys

To allow the Clearwater extensions to create AWS instances or configure Route53 DNS entries, you will need to supply your AWS access key and secret access key.  To find your AWS keys, go to [http://aws.amazon.com](http://aws.amazon.com) and click on `My Account/Console` then `Security Credentials`. From there, under the `Access Credentials` section of the page, click on the `Access Keys` tab to view your access key.  The access key is referred to as `<accessKey>` below. To see your secret access key, just click on the `Show` link under `Secret Access Key`.  The secret access key will be referred to as `<secretKey>` below.

## Add deployment-specific configuration

Now add the following lines to the bottom of your `~/.chef/knife.rb`
file.

    # AWS deployment keys.
    knife[:aws_access_key_id]     = "<accessKey>"
    knife[:aws_secret_access_key] = "<secretKey>"

    # Signup key. Anyone with this key can create accounts
    # on the deployment. Set to a secure value.
    knife[:signup_key]        = "secret"

    # TURN workaround password, used by faulty WebRTC clients.
    # Anyone with this password can use the deployment to send
    # arbitrary amounts of data. Set to a secure value.
    knife[:turn_workaround]   = "password"

    # Ellis API key. Used by internal scripts to
    # provision, update and delete user accounts without a password.
    # Set to a secure value.
    knife[:ellis_api_key]     = "secret"

    # Ellis cookie key. Used to prevent spoofing of Ellis cookies. Set
    # to a secure value.
    knife[:ellis_cookie_key]  = "secret"

    # SMTP credentials as supplied by your email provider.
    knife[:smtp_server]       = "localhost"
    knife[:smtp_username]     = ""
    knife[:smtp_password]     = ""

    # Sender to use for password recovery emails. For some
    # SMTP servers (e.g., Amazon SES) this email address
    # must be validated or email sending will fail.
    knife[:email_sender]      = "clearwater@example.com"

    # MMonit server credentials, if any.
    knife[:mmonit_server]     = "0.0.0.0"
    knife[:mmonit_username]   = ""
    knife[:mmonit_password]   = ""

Fill in the values appropriate to your deployment using a text editor
as directed.

* The AWS deployment keys are the ones you obtained above.

* The keys and passwords marked "Set to a secure value" above should
  be set to secure random values, to protect your deployment from
  unauthorised access. An easy way to generate a secure random key on
  a Linux system is as follows:

        head -c6 /dev/random | base64

  The `signup_key` must be supplied by new users when they create an
  account on the system.

  The `turn_workaround` must be supplied by certain WebRTC clients
  when using TURN. It controls access to media relay function.

  The `ellis_api_key` and `ellis_cookie_key` are used internally.

* The SMTP credentials are required only for password recovery.
  If you leave them unchanged, this function will not work.

* The M/Monit credentials are only required if you have an
  [M/Monit](http://mmonit.com/) server. Otherwise you can leave them
  unchanged.

## Test your settings

Test that knife is configured correctly

    knife client list

This should return a list of clients and not raise any errors.

## Installing the Clearwater Chef extensions

On the chef-client machine, install git and dependent libraries.

    sudo apt-get install git libxml2-dev libxslt1-dev

Clone the Clearwater Chef repository.

@@@ TODO Use real URL and branch name

    git clone git@bitbucket.org:metaswitch/chef.git -b dev ~/chef

This will have created a `chef` folder in your home directory, navigate there now.

    cd ~/chef

Fetch the submodules used by the Clearwater Chef extensions.

    git submodule update --init

Finally install the Ruby libraries that are needed by our scripts.

    bundle install

## Next steps

At this point, the Chef server is up and running and ready to manage installs and the chef client is ready to create deployments.  The next step is to [create a deployment environment](Creating a deployment environment).
