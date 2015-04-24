This page discusses how to change settings on a Clearwater system. Most settings can be changed on an existing deployment (e.g. security keys and details of external servers), but some are so integral to the system (e.g. the SIP home domain) that the best way to change it is to recreate the Clearwater deployment entirely.

## Reconfiguring existing deployments

*This will have a service impact of up to five minutes.*

The following settings can safely be changed without entirely recreating the system. If you want to change a setting not in this list, go to the "Starting from scratch" section instead.

All nodes:

```
mmonit_hostname
mmonit_username
mmonit_password
```

Sprout:

```
sas_server
enum_server
reg_max_expires
chronos_hostname
hs_hostname
xdms_hostname
additional_home_domains
```

Bono:

```
sas_server
enum_server
cdf_address
```

Ellis:

```
hs_provisioning_hostname
xdms_hostname
smtp_smarthost
smtp_username
smtp_password
email_recovery_sender
signup_key
ellis_api_key
ellis_cookie_key
```

Homestead:

```
hss_hostname
hss_port
```

To change one of these settings:

*   Edit `/etc/clearwater/config` on each affected node, and change to the new value
*   Run `sudo service clearwater-infrastructure restart` to ensure that the configuration changes are applied consistently across the node
*   Restart the individual component by running the appropriate one of the following commands to stop the service and allow monit to restart it.

    *   Sprout - `sudo service sprout quiesce`
    *   Bono - `sudo service bono quiesce`
    *   Homestead - `sudo service homestead stop`
    *   Homer - `sudo service homer stop`
    *   Ralf -`sudo service ralf stop`
    *   Ellis - `sudo service ellis stop`

## Starting from scratch

*This will have a service impact of up to half an hour.*

If other settings (such as the Clearwater home domain) are being changed, we recommend that users delete their old deployment and create a new one from scratch, either [with Chef](Creating_a_deployment_with_Chef) or [manually](Manual_Install). This ensures that the new settings are consistently applied.
