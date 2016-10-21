# Creating a Chef deployment environment

These instructions make up part of the [automated install process](Automated_Install.md) for Clearwater.  They will take you through creating a deployment environment, which will be used to define the specific settings for a Clearwater deployment.

## Prerequisites

* You must have [installed a Chef workstation](Installing_a_Chef_workstation.md).
* You must have SSH access to the ubuntu user on the chef workstation machine.

## Creating a keypair

You need to configure the AWS keypair used to access your Clearwater deployment. You may reuse the one you created when creating your Chef client and server; or you may create a new one (EC2 Dashboard > Network & Security > Key Pairs > Create Key Pair) for finer-grained access rights. The name you give your keypair will be referred to as `<keypair_name>` from this point.

Amazon will give you a `<keypair_name>`.pem file; copy that file to the `/home/ubuntu/.chef/` directory on your Chef client, and make it readable only to your user with `chmod 0700 /home/ubuntu/.chef ; chmod 0400 /home/ubuntu/.chef/<keypair_name>.pem`.

## Creating the environment

Before creating an environment, choose a name (e.g. "clearwater") which will be referred to as `<name>` in the following steps.  Now, on the chef workstation machine, create a file in `~/chef/environments/<name>.rb` with the following contents:

    name "<name>"
    description "Clearwater deployment - <name>"
    cookbook_versions "clearwater" => "= 0.1.0"
    override_attributes "clearwater" => {
      "root_domain" => "<zone>",
      "availability_zones" => ["us-east-1a", "us-east-1b"],
      "repo_servers" => ["http://repo.cw-ngv.com/stable"],
      "number_start" => "6505550000",
      "number_count" => 1000,
      "keypair" => "<keypair_name>",
      "keypair_dir" => "~/.chef/",
      "pstn_number_count" => 0,
      "gr" => false,

      # Signup key. Anyone with this key can create accounts
      # on the deployment. Set to a secure value.
      "signup_key" => "secret",

      # TURN workaround password, used by faulty WebRTC clients.
      # Anyone with this password can use the deployment to send
      # arbitrary amounts of data. Set to a secure value.
      "turn_workaround" => "password",

      # Ellis API key. Used by internal scripts to
      # provision, update and delete user accounts without a password.
      # Set to a secure value.
      "ellis_api_key" => "secret",

      # Ellis cookie key. Used to prevent spoofing of Ellis cookies. Set
      # to a secure value.
      "ellis_cookie_key" => "secret",

      # SMTP credentials as supplied by your email provider.
      "smtp_server" => "localhost",
      "smtp_username" => "",
      "smtp_password" => "",

      # Sender to use for password recovery emails. For some
      # SMTP servers (e.g., Amazon SES) this email address
      # must be validated or email sending will fail.
      "email_sender" => "clearwater@example.com"
    }

Fill in the values appropriate to your deployment using a text editor
as directed.

* The value of `keypair` should *not* include the trailing .pem.

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
    
* For an all-in-one node the root-domain parameter is superfluous and will be ignored.

By default, your deployment will be created in the US East (North Virginia) region.  However, if you want to deploy in another region, you must

*   set the `region` property in the `override_attributes "clearwater"` block (e.g. to `us-west-2`)
*   set the `availability_zones` property correspondingly (e.g. `["us-west-2a", "us-west-2b"]`)
*   open `~/chef/plugins/knife/boxes.rb`, search for `@@default_image`, and comment in the EC2 AMI entry for the region you desire.

These fields override attributes defined and documented in the [chef-base role](https://github.com/Metaswitch/chef/blob/master/roles/chef-base.rb).

If you want to use a different SIP registration period from the default (which is 5 minutes) add a line like `"reg_max_expires" => <timeout_in_secs>,` to the `override_attributes "clearwater"` block.

If you want to test [geographic redundancy function](Geographic_redundancy.md), use `"gr" => true` instead of `"gr" => false`.
This will cause odd-numbered and even-numbered nodes to be treated as separate logical "sites" -
they are not actually in different EC2 regions (cross-region security group rules make that
difficult), but does allow you to see and test GR function.

To modify these settings after the deployment is created, follow [these instructions](Modifying_Clearwater_settings.md).

## Uploading the environment

The newly created environment needs to be uploaded to the Chef server before it can be used.

    cd ~/chef
    knife environment from file environments/<name>.rb

## Next steps

At this point, your deployment environment is created and can be used to [create a new deployment](Creating_a_deployment_with_Chef.md).
