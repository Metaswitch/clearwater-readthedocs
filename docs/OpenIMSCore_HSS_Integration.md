# OpenIMS HSS Integration

As discussed on the [External HSS Integration](External_HSS_Integration)
page, Clearwater can integrate with an external HSS.

This page describes how to install and configure the [OpenIMSCore](http://www.openimscore.org/) HSS as this external HSS.  It assumes that you have already read the [External HSS Integration](External_HSS_Integration) page.

## Installation with Chef

If you have a deployment environment created by following the [automated install instructions](Automated_Install), then you can create a HSS by running `knife box create -E <env> openimscorehss`. This may take a long time (more than 10 minutes). You should then follow [the configuration instructions below](OpenIMSCore_HSS_Integration/#configuration).

## Installing OpenIMSCore HSS manually

To install OpenIMSCore HSS,

1.  follow the "FHoSS"-related steps in the Quick Install section of the full
    [OpenIMSCore Installation Guide](http://www.openimscore.org/?q=installation_guide)
2.  edit the `/opt/OpenIMSCore/FHoSS/deploy/DiameterPeerHSS.xml` file to
    1.  change the realm attribute to be your Clearwater deployment's home
        domain
    2.  find the Acceptor element and change its bind attribute to be the local
        IP address
3.  follow the FHoSS-related section of the "Start the components" section of
    the
    [OpenIMSCore Installation Guide](http://www.openimscore.org/?q=installation_guide).

## Configuration

### Setting up a SSH tunnel

OpenHSS provides the administration UI over port 8080.  Rather than exposing this configuration interface to the public internet, we recommend configuring an SSH tunnel to access it securely.

In the PuTTY SSH client this is done by by right-clicking on the titlebar, choosing "Change Settings..." then navigating to "Connection->SSH->Tunnels", filling in Source port "8080" and Destination "127.0.0.1:8080", clicking Add and then clicking Apply.

If using Linux/Mac with ssh installed, you can do: ssh -L 8080:localhost:8080 &lt;hss_server&gt;.

### Adding the MMTEL Application Server

To enable the MMTEL application server built into Clearwater for all
subscribers,

1.  access the OpenIMSCore HSS web UI, running on port 8080
2.  log in as hssAdmin/hss
3.  navigate to `Services`->`Application Servers`->`Search`
4.  perform a search with no search string to find all application servers
5.  select default_as
6.  change `server_name` to be `sip:mmtel.your.home.domain`, where
   `your.home.domain` is replaced with your home domain
7.  save your change.

### Configuring Subscribers

To configure a subscriber,

1.  create an IMS subscription
2.  create an associated public user identity
3.  create an associated private user identity, specifying
    1.  the private ID to be the public ID without the `sip:` scheme prefix
    2.  SIP Digest authentication.
4.  add the home domain to the subscriber's visited networks

