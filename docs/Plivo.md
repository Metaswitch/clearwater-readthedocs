# Plivo

[Plivo](http://plivo.com/open-source/) is an open-source framework for voice applications.  It can connect to Clearwater as an [Application Server](Application Server Guide) via the ISC interface.

This documentation describes how to

*   install Plivo
*   configure Plivo to interoperate with Clearwater
*   start Plivo
*   install and run services
*   configure Clearwater to invoke Plivo as an Application Server
*   make a test call
*   troubleshoot problems.

If you followed the Clearwater [Automated Install](Automated Install) instructions, you can install Plivo using chef by running `knife box create -E <environment> plivo` - note that often this takes around an hour to complete.  This automatically installs, configures and starts Plivo, so you can jump straight to [Installing and Running Services](Plivo#installing-and-running-services).

## Installing Plivo

Plivo depends on FreeSWITCH, so you must install both in order to have a working instance.  Fortunately, Plivo offers straight-forward [install instructions](http://docs.plivo.org/get-started/) on both CentOS and Debian-based distributions.  Note that instructions these must be run as root, so you may need to prefix them with `sudo`.

We've tested installing on EC2, using an m1.small instance running Ubuntu 12.04.  The instance must be deployed in a security group with access on

* UDP port 5058 from bono (for SIP/UDP)
* UDP port 5058 from sprout (for SIP/UDP)
* TCP port 5058 from bono (for SIP/TCP)
* TCP port 5058 from sprout (for SIP/TCP)
* UDP ports 32768-65535 from anywhere (for RTP media).

Once the instance is created, install the software using the instructions referred to above.  Note that, at least on an EC2 m1.small instance, the installation process takes longer than the stated 20 minutes - it's often more like an hour.

## Configuring Plivo

Once Plivo and FreeSWITCH are installed, they need to be configured.  For this step, you'll need to know the Plivo node's public IP address - on an EC2 node, you can find this out by issuing the command `curl http://169.254.169.254/latest/meta-data/public-ipv4`.

You'll then need to make the following configuration changes.

*   Edit `/usr/local/freeswitch/conf/vars.xml` to set
    *   `zrtp_secure_media` to `false` (by changing `<X-PRE-PROCESS cmd="set" data="zrtp_secure_media=true"/>` to `<X-PRE-PROCESS cmd="set" data="zrtp_secure_media=false"/>`)
    *   `global_codec_prefs` and `outbound_codec_prefs` to `PCMU,PCMA`
    *   `external_rtp_ip` and `external_sip_ip` to the Plivo node's public IP address
    *   `external_sip_port` to `5058`.
*   Edit `/usr/local/freeswitch/conf/sip_profiles/external.xml` to set `ext-rtp-ip` and `ext-sip-ip` to the Plivo node's public IP address.
*   Edit `/usr/local/freeswitch/conf/sip_profiles/internal.xml` to set `ext-rtp-ip` and `ext-sip-ip` to the Plivo node's public IP address
*   Edit `/usr/local/freeswitch/conf/autoload_configs/switch.conf.xml` to set
    *   `rtp-start-port` to `32768` and `rtp-end-port` to `65535`
    *   `rtp-enable-zrtp` to `false`.
*   Edit `/usr/local/plivo/etc/plivo/default.conf` to change `DEFAULT_HTTP_METHOD` to `GET` - this is easier to handle, and is what our sample applications use.

## Starting Plivo

Before you can start Plivo, you must first start FreeSWITCH.  To do this, run `sudo /usr/local/freeswitch/bin/freeswitch -ncwait`.

To start Plivo, run `sudo service plivo start`.

## Installing and Running Services

By default, when a call comes in Plivo connects to `http:/127.0.0.1:5000/answered/`.  The servicing application must run a web server at this address and respond.

We have 2 sample services for this, written in [Python](http://www.python.org/) using [Flask](http://flask.pocoo.org/) and the [Plivo Python Helper Library](https://github.com/plivo/plivo-python).  They are

*   plivo_conf.py - a conferencing server
*   plivo_vm.py - a voicemail server.

To install these, run

    sudo pip install flask
    sudo pip install plivo==0.4.1 # 0.9 is the default version, but this has API changes
    git clone git@github.com:Metaswitch/plivo-apps.git

To start them, simply run `python plivo-apps/plivo_conf.py` or `sudo python plivo-apps/plivo_vm.py`.  (The VM application must be run under sudo as it needs to access media recordings, and unfortunately Freeswitch stores these in a directory that is only accessible by root.)

Note that plivo_conf.py optionally supports playing back on-hold music while the first attendee is waiting for other attendees to join.  To enable this function, you must source a suitable MP3 music file and host it as `http://localhost/music.mp3`.  To do this using nginx on Ubuntu,

*   install nginx by typing `sudo apt-get install nginx`
*   start nginx by typing `sudo service nginx start`
*   copy your MP3 music file to `/usr/share/nginx/www/music.mp3`.

## Configuring Clearwater

Clearwater invokes Application Servers according to the Initial Filter Criteria (iFCs) configured for each subscriber.  As a result, to cause Clearwater to invoke Plivo, you must

* determine the SIP URI to invoke Plivo
* choose a user for which the Application Server will be invoked
* add an entry to that user's iFC, specifying the SIP URI as the `<ServerName>` element.

The SIP URI is constructed as `sip:<hostname>:5058;transport=tcp`, where `<hostname>` is the public hostname of your Plivo server.  On an EC2 node, you can find this out by issuing the command `curl http://169.254.169.254/latest/meta-data/public-hostname`.

To add an entry to the user's iFC, see the [Configuring an Application Server](https://github.com/Metaswitch/clearwater-docs/wiki/Configuring%20an%20Application%20Server#ifc-configuration) documentation.

## Making a Test Call

Any calls to the user that you selected above should invoke the service.  Create a second user and configure a SIP client for them, as described in the [Making your first call](Making-your-first-call) documentation.  Then call the first user and you should hear the service.

## Troubleshooting Problems

The first thing to check is that your calling user can generally make calls.  Walk through the [Making your first call](Making-your-first-call) process and check this is working.  If not, investigate and fix that first.

The next thing to check is that the call is reaching Plivo correctly.  The application service process you started above outputs access logs whenever it is invoked - make a test call and check whether you see any output from it.  If you don't, [enable detailed tracing from sprout](https://github.com/Metaswitch/clearwater-docs/wiki/Troubleshooting%20and%20Recovery#sprout) and see where sprout is sending the call - check that the IFCs are being retrieved and parsed correctly, and that the destination IP address and port (5058) are correct.  If this doesn't help, check that access to port 5058 is open by logging into your sprout node and typing `( nc -z <hostname> 5058 && echo Connection OK ) || echo Connection failed`, where `<hostname>` is the Plivo server's public hostname - if the connection failed, check whether there is a firewall (or EC2 security group) blocking access.

If the call is reaching Plivo, but the application service process is not responding correctly, you can turn on more debugging from the sample applications by adding the line `app.debug = True` just before the final `app.run(...) line - this will generate more verbose output.

If none of this helps, please try the [mailing list](http://lists.projectclearwater.org/listinfo/clearwater).
