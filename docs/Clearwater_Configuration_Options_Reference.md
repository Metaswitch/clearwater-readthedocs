This document describes all the Clearwater configuration options that can be set in /etc/clearwater/config or /etc/clearwater/user_settings.

To change one of these settings:

* Modify the configuration file
* Run `sudo service clearwater-infrastructure restart` to regenerate any dependent configuration files
* Restart the relevant Clearwater service (e.g. run `sudo service bono stop` and allow monit to restart Bono)

## Core options

This section describes options for the basic configuration of a Clearwater deployment - such as the hostnames of the six node types and external services such as email servers or the Home Subscriber Server. These options should be set in the `/etc/clearwater/config` file (in the format `name=value`, e.g. `local_ip=10.0.0.2`).

* `home_domain` - this is the main SIP domain of the deployment, and determines which SIP URIs Clearwater will treat as local. It will usually be a hostname resolving to all the P-CSCFs (e.g. the Bono nodes). Other domains can be specified through additional_home_domains, but Clearwater will treat this one as the default (for example, when handling `tel:` URIs).
* `sprout_hostname` - a hostname that resolves by DNS round-robin to all Sprout nodes in the cluster.
* `bono_hostname` - a hostname that resolves by DNS round-robin to all Bono nodes in the cluster.
* `hs_hostname` - a hostname that resolves by DNS round-robin to all Homesteads in the cluster. Should include the HTTP port (usually 8888). This is also used (without the port) as the Origin-Realm of the Diameter messages Homestead sends.
* `hs_provisioning_hostname` - a hostname that resolves by DNS round-robin to all Homesteads in the cluster. Should include the HTTP provisioning port (usually 8889). Not needed when using an external HSS.
* `chronos_hostname`  - a hostname that resolves to a Chronos node. Because Chronos nodes pass timers balance timers amongst themselves, this typically just points to the local Chronos node. Should include the port (7253).
* `ralf_hostname` - a hostname that resolves by DNS round-robin to all Ralf nodes in the cluster. Should include the port (usually 9888). This is also used (without the port) as the Origin-Realm of the Diameter messages Ralf sends. Optional if no Ralf nodes exist.
* `cdf_identity` - a Diameter identity that represents the address of an online Charging Function. Subscribers provisioned through Ellis will have this set as their Primary Charging Collection Function on P-Charging-Function-Addresses headers on responses to their successful REGISTERs, and Bono will add similarly in originating requests.
* `xdms_hostname` - a hostname that resolves by DNS round-robin to all Homer nodes in the cluster. Should include the port (usually 7888).
* `local_ip` - this should be set to an IP address which is configured on an interface on this system, and can communicate on an internal network with other Clearwater nodes and IMS core components like the HSS.
* `public_ip` - this should be set to an IP address accessible to external clients (SIP UEs for Bono, web browsers for Ellis). It does not need to be configured on a local interface on the system - for example, in a cloud environment which puts instances behind a NAT.
* `public_hostname` - this should be set to a hostname which resolves to `public_ip`, and will communicate with only this node (i.e. not be round-robined to other nodes). It can be set to `public_ip` if necessary.
* `hss_hostname` - the hostname of your external HSS, if you have one. The port defaults to 3868 - this cannot be set by static configuration, but can be controlled by setting `hss_realm` and having appropriate NAPTR/SRV records for Diameter.
* `signup_key` - this sets the password which Ellis will require before allowing self-sign-up.
* `turn_workaround` - if your STUN/TURN clients are not able to authenticate properly (for example, because they can't send the @ sign), this specifies an additional password which will autenticate clients even without a correct username.
* `smtp_smarthost` - Ellis allows password recovery by email. This sets the SMTP server used to send those emails.
* `smtp_username` - Ellis allows password recovery by email. This sets the username used to log in to the SMTP server.
* `smtp_password` - Ellis allows password recovery by email. This sets the password used to log in to the SMTP server.
* `email_recovery_sender` - Ellis allows password recovery by email. This sets the email address those emails are sent from.
* `ellis_api_key` - sets a key which can be used to authenticate automated requests to Ellis, by setting it as the value of the X-NGV-API header. This is used to expire demo users regularly.

## Advanced options

This section describes optional configuration options, particularly for ensuring conformance with other IMS devices such as HSSes, ENUM servers, application servers with strict requirements on Record-Route headers, and non-Clearwater I-CSCFs. These options should be set in the `/etc/clearwater/config` file (in the format `name=value`, e.g. `icscf=5052`).

* `icscf` - the port which Sprout nodes are providing I-CSCF service on. If not set, Sprout will only provide S-CSCF function.
* `scscf` - the port which Sprout nodes are providing S-CSCF service on. If this not set but `icscf` is, Sprout will only provide I-CSCF function. If neither is set, this will default to 5054 and Sprout will only provide S-CSCF function.
* `homestead_provisioning_port` - the HTTP port the Homestead provisioning interface listens on. Defaults to 8889. Not needed when using an external HSS.
* `sas_server` - the IP address or hostname of your Metaswitch Service Assurance Server for call logging and troubleshooting. Optional.
* `node_idx` - an index number used to distinguish this node from others of the same type in the cluster (for example, sprout-1 and sprout-2). Optional.
* `reg_max_expires` - determines the maximum expires= parameter Sprout will set on Contact headers at registrations, and therefore the amount of time before a UE has to re-register.
* `sub_max_expires` - determines the maximum Expires header Sprout will set in subscription responses, and therefore the amount of time before a UE has to re-subscribe. 
* `upstream_hostname` - the I-CSCF which Bono should pass requests to. Defaults to the sprout_hostname.
* `upstream_port` - the port on the I-CSCF which Bono should pass requests to. Defaults to 5052.
* `sprout_rr_level` - this determines how the Sprout S-CSCF adds Record-Route headers. Possible values are:
  * `pcscf` - a Record-Route header is only added just after requests come from or go to a P-CSCF - that is, at the start of originating handling and the end of terminating handling
  * `pcscf,icscf` - a Record-Route header is added just after requests come from or go to a P-CSCF or I-CSCF - that is, at the start and end of originating handling and the start and end of terminating handling
  * `pcscf,icscf,as` - a Record-Route header is added after requests come from or go to a P-CSCF, I-CSCF or application server - that is, at the start and end of originating handling, the start and end of terminating handling, and between each application server invoked
* `hss_mar_lowercase_unknown` - some Home Subscriber Servers (particularly old releases of OpenIMSCore HSS) expect the string 'unknown' rather than 'Unknown' in Multimedia-Auth-Requests when Clearwater cannot tell what authentication type is expected. Setting this option to 'Y' will make Homestead send requests in this format.
* `enforce_user_phone` - by default, Clearwater will do an ENUM lookup on any SIP URI that looks like a phone number, due to client support for user-phone not being widespread. When this option is set to 'Y', Clearwater will only do ENUM lookups for URIs which have the user=phone parameter.
* `enforce_global_only_lookups` - by default, Clearwater will do ENUM lookups for SIP and Tel URIs containing global and local numbers (as defined in RFC 3966). When this option is set to ‘Y’, Clearwater will only do ENUM lookups for SIP and Tel URIs that contain global numbers. 
* `hs_listen_port` - the Diameter port which Homestead listens on. Defaults to 3868.
* `ralf_listen_port`  - the Diameter port which Ralf listens on. Defaults to 3869 to avoid clashes when colocated with Homestead.
* `alias_list` - this defines additional hostnames and IP addresses which Sprout or Bono will treat as local for the purposes of SIP routing (e.g. when removing Route headers).
* `default_session_expires` - determines the Session-Expires value which Sprout will add to INVITEs, to force UEs to send keepalive messages during calls so they can be tracked for billing purposes.
* `enum_server` - a comma-separated list of DNS servers which can handle ENUM queries.
* `enum_suffix` - determines the DNS suffix used for ENUM requests (after the digits of the number). Defaults to "e164.arpa"
* `enum_file` - if set (to a file path), and if `enum_server` is not set, Sprout will use this local JSON file for ENUM lookups rather than a DNS server. An example file is at http://clearwater.readthedocs.org/en/latest/ENUM/index.html#deciding-on-enum-rules.
* `icscf_uri` - the SIP address of the external I-CSCF integrated with your Sprout node (if you have one).
* `scscf_uri` - the SIP address of the Sprout S-CSCF. This defaults to `sip:$sprout_hostname:$scscf;transport=TCP` - this includes a specific port, so if you need NAPTR/SRV resolution, it must be changed to not include the port.
* `additional_home_domains` - this option defines a set of home domains which Sprout and Bono will regard as locally hosted (i.e. allowing users to register, not routing calls via an external trunk). It is a comma-separated list.
* `hss_realm` - this sets the realm of your external HSS. When this field is set, Homestead will then attempt to set up multiple Diameter connections.
* `billing_realm` - this sets the Destination-Realm on Diameter messages to your external CDR. CDR connections are not based on this but on configuration at the P-CSCF (which sets the P-Charging-Function-Addresses header).
* `diameter_timeout_ms` - determines the number of milliseconds Homestead will wait for a response from the HSS before failing a request. Defaults to 200. `
* `max_peers` - determines the maximum number of Diameter peers which Ralf or Homestead can have open connections to at the same time.
* `num_http_threads` (Ralf/Memento) - determines the number of threads that will be used to process HTTP requests. For Memento this defaults to the number of CPU cores on the system. For Ralf it defaults to 50 times the number of CPU cores (Memento and Ralf use different threading models, hence the different defaults). Note that for Homestead, this can only be set in /etc/clearwater/user_settings.
* `num_http_worker_threads` - determines the number of threads that will be used to process HTTP requests once they have been parsed. Only used by Memento. 
* `ralf_diameteridentity` - determines the Origin-Host that will be set on the Diameter messages Ralf sends. Defaults to public_hostname (with some formatting changes if public_hostname is an IPv6 address).
* `hs_diameteridentity` - determines the Origin-Host that will be set on the Diameter messages Homestead sends. Defaults to public_hostname (with some formatting changes if public_hostname is an IPv6 address).
* `gemini_enabled` - When this field is set to 'Y', then the node (either a Sprout or a standalone application server) will include a Gemini AS. 
* `memento_enabled` - When this field is set to 'Y', then the node (either a Sprout or a standalone application server) will include a Memento AS. 
* `max_call_list_length` - determines the maximum number of complete calls a subscriber can have in the call list store. This defaults to no limit. This is only relevant if the node includes a Memento AS.
* `call_list_store_ttl` - determines how long each call list fragment should be kept in the call list store. This defaults to 604800 seconds (1 week). This is only relevant if the node includes a Memento AS.
* `memento_disk_limit` - determines the maximum size that the call lists database may occupy. This defaults to 20% of disk space. This is only relevant if the node includes a Memento AS. Can be specified in Bytes, Kilobytes, Megabytes, Gigabytes, or a percentage of the available disk. For example:

        memento_disk_limit=10240 # Bytes
        memento_disk_limit=100k  # Kilobytes
        memento_disk_limit=100M  # Megabytes
        memento_disk_limit=100G  # Gigabytes
        memento_disk_limit=45%   # Percentage of available disk

* `memento_threads` - determines the number of threads dedicated to adding call list fragments to the call list store. This defaults to 25 threads. This is only relevant if the node includes a Memento AS.
* `signaling_dns_server` - a comma-separated list of DNS servers for non-ENUM queries. Defaults to 127.0.0.1 (i.e. uses `dnsmasq`)
* `target_latency_us` - Target latency (in microsecs) for requests above which [throttling](http://www.projectclearwater.org/clearwater-performance-and-our-load-monitor/) applies. This defaults to 100000 microsecs
* `max_tokens` - Maximum number of tokens allowed in the token bucket (used by the throttling code). This defaults to 20 tokens
* `init_token_rate` - Initial token refill rate of tokens in the token bucket (used by the throttling code). This defaults to 100.0
* `min_token_rate` - Minimum token refill rate of tokens in the token bucket (used by the throttling code). This defaults to 10.0
* `override_npdi` - Whether the I-CSCF, S-CSCF and BGCF should check for number portability data on requests that already have the 'npdi' indicator. This defaults to false
* `exception_max_ttl` - determines the maximum time before a process exits if it crashes. This defaults to 600 seconds

## Experimental options

This section describes optional configuration options which may be useful, but are not heavily-used or well-tested by the main Clearwater developent team. These options should be set in the `/etc/clearwater/config` file (in the format `name=value`, e.g. `cassandra_hostname=db.example.com`).

* `cassandra_hostname` - if using an external Cassandra cluster (which is a fairly uncommon configuration), a hostname that resolves to one or more Cassandra nodes.
* `ralf_secure_listen_port` - this determines the port Ralf listens on for TLS-secured Diameter connections.
* `hs_secure_listen_port` - this determines the port Homestead listens on for TLS-secured Diameter connections.
* `ellis_cookie_key` - an arbitrary string that enables Ellis nodes to determine whether they should be in the same cluster. This function is not presently used.

## User settings

This section describes settings that may vary between systems in the same deployment, such as log level (which may be increased on certain machines to track down specific issues) and performance settings (which may vary if some servers in your deployment are more powerful than others). These settings are set in `/etc/clearwater/user_settings`, not `/etc/clearwater/config` (in the format `name=value`, e.g. `log_level=5`).

* `log_level` - determines how verbose Clearwater's logging is, from 1 (error logs only) to 5 (debug-level logs). Defaults to 2.
* `log_directory` - determines which folder the logs are created in. This folder must exist, and be owned by the service. Defaults to /var/log/<service> (this folder is created and has the correct permissions set for it by the install scripts of the service).
* `num_pjsip_threads` - determines how many PJSIP transport-layer threads should run at once. Defaults to 1, and it may be dangerous to change this as it is not necessarily thread-safe.
* `num_worker_threads` - for Sprout and Bono nodes, determines how many worker threads should be started to do SIP/IMS processing. Defaults to 50 times the number of CPU cores on the system.
* `upstream_connections` - determines the maximum number of TCP connections which Bono will open to the I-CSCF(s). Defaults to 50.
* `upstream_recycle_connections` - the average number of seconds before Bono will destroy and re-create a connection to Sprout. A higher value means slightly less work, but means that DNS changes will not take effect as quickly (as new Sprout nodes added to DNS will only start to receive messages when Bono creates a new connection and does a fresh DNS lookup).
* `authentication` - by default, Clearwater performs authentication challenges (SIP Digest or IMS AKA depending on HSS configuration). When this is set to 'Y', it simply accepts all REGISTERs - obviously this is very insecure and should not be used in production.
* `num_http_threads` (Homestead) - determines the number of HTTP worker threads that will be used to process requests. Defaults to 50 times the number of CPU cores on the system.
* `impu_cache_ttl` - the number of seconds for which Homestead will cache the SIP Digest from a Multimedia-Auth-Request. Defaults to 0, as Sprout does enough caching to ensure that it can handle an authenticated REGISTER after a challenge, and subsequent challenges should be rare.
* `hss_reregistration_time` - determines how many seconds should pass before Homestead sends a Server-Assignment-Request with type RE_REGISTRATION to the HSS. (On first registration, it will always send a SAR with type REGISTRATION). This determines a minimum value - after this many seconds have passed, Homestead will send the Server-Assignment-Request when the next REGISTER is received. Note that Homestead invalidates its cache of the registration and iFCs after twice this many seconds have passed, so it is not safe to set this to less than half of `reg_max_expires`.
