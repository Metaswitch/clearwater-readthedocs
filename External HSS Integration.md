# External HSS Integration

All Clearwater deployments include a [Homestead]() cluster.  Homestead presents
an HTTP REST-ful [interface]() to HSS data.  This HSS data can be stored in
either

*   a Cassandra database located on the Homestead cluster or
*   an external HSS, accessible over a standard IMS
    [Cx/Diameter](http://www.3gpp.org/ftp/Specs/html-info/29228.htm) interface.

This page describes

*   how it works
*   how to enable it
*   restrictions.

## How It Works

When Clearwater is deployed without an external HSS, all HSS data is mastered
in Homestead's own Cassandra database.

When Clearwater is deployed with an external HSS, HSS data is queried from the
external HSS via its Cx/Diameter interface and is then cached in the Cassandra
database.

Clearwater uses the following Cx message types.

*   Multimedia-Auth - to retrieve authentication details

*   Server-Assignment - to retrieve Initial Filter Criteria documents and
    register for change notifications

*   Push-Profile - to be notified of changes to Initial Filter Criteria documents

## How to Enable It

This section discusses how to enable support for an external HSS.

### Before you start

Before enabling support for an external HSS, you must

*   [install Clearwater]()
*   install an external HSS - details for this will vary depending on which HSS
    you choose, but there are instructions for
    [OpenIMSCore HSS](OpenIMSCore HSS Integration).

Do not configure any Clearwater subscribers via Ellis!

*   Any subscribers you create before enabling the external HSS will override
    subscribers retrieved from the external HSS, and you will not be able to
    use Ellis to manage them.

*   After enabling the external HSS, you will not be able to create subscribers
    through Ellis at all - they must be created through the HSS's own
    management interface.

### Enabling external HSS support on an existing deployment

To enable external HSS support, for each of your Homestead nodes,

1.  log in over ssh
2.  edit the file
    `/etc/clearwater/config`
3.  find the block (or add it if it does not exist)
```
# HSS configuration
hss_enabled=False
hss_hostname=0.0.0.0
hss_port=3868
```
4.  Modify it to read

```
# HSS configuration
hss_enabled=True
hss_hostname=<address of your HSS>
hss_port=<port of your HSS's Cx interface>
```
6.  save the file and exit the editor
7.  run `sudo service clearwater-infrastructure restart; sudo monit restart homestead` to reload the config and restart Homestead.

### Configuring your external HSS

Homestead will now query the external HSS for subscriber details when they are
required by the rest of the Clearwater deployment, such as when servicing SIP
registrations.

In order to register and make calls, you need to create subscriber records on
your external HSS, and the detailed process for this will depend on which HSS
you have chosen.  Generally, however, you will need to

1. create a public user identity with the desired SIP URI
2. create an associated private user identity with its ID formed by removing
   the `sip:` scheme prefix from the public user ID
3. configure the public user identity's Initial Filter Criteria to include an
   application server named `sip:mmtel.your.home.domain`, where
   `your.home.domain` is replaced with your home domain - this enables MMTEL
   services for this subscriber.

## Restrictions

*   Since Homestead uses the Cx/Diameter interface to the HSS, and this
    interface is read-only, the Homestead API is read-only when external HSS
    integration is enabled.

*   Since Homestead's API is read-only, this means that [Ellis]() can't be used
    alongside a deployment using an external HSS.  Provisioning and subscriber
    management must be performed via the HSS's own management interface.

*   Since Clearwater currently only supports SIP digest authentication,
    details for other authentication method (such as
    [AKA](http://tools.ietf.org/html/rfc3310)) are silently ignored from
    Multimedia-Auth responses.  Other authentication methods may be added in
    future.

*   Homestead currently assumes that private user IDs are formed by removing
    the `sip:` prefix from the public user ID.  This restriction may be relaxed
    in future.

*   While Homestead caches positive results from the external HSS, it does not
    currently cache negative results (e.g. for non-existent users).  Repeated
    requests for a non-existent user will increase the load on the external
    HSS. This restriction may be relaxed in future.
