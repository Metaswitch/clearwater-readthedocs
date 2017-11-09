# Clearwater Configuration Options Reference

This document describes all the Clearwater configuration options that can be set in `/etc/clearwater/shared_config`, `/etc/clearwater/local_config` or `/etc/clearwater/user_settings`.

At a high level, these files contain the following types of configuration options:
* `shared_config` - This file holds settings that are common across the entire deployment. This file should be identical on all nodes (and any changes can be easily synchronised across the deployment as described in [this process](Modifying_Clearwater_settings.md)).
* `local_config` - This file holds settings that are specific to a single node and are not applicable to any other nodes in the deployment. They are entered early on in the node’s life and are not typically changed.
* `user_settings` - This file holds settings that may vary between systems in the same deployment, such as log level (which may be increased on certain nodes to track down specific issues) and performance settings (which may vary if some nodes in your deployment are more powerful than others)

## Modifying Configuration

You should follow [this process](Modifying_Clearwater_settings.md) when changing settings in "Shared Config". For settings in the "Local config" or "User settings" you should:

* Modify the configuration file
* Run `sudo service clearwater-infrastructure restart` to regenerate any dependent configuration files
* Restart the relevant Clearwater service(s) using the following commands as appropriate for the node.
    *   Sprout - `sudo service sprout quiesce`
    *   Bono - `sudo service bono quiesce`
    *   Dime - `sudo service homestead stop && sudo service homestead-prov stop && sudo service ralf stop`
    *   Homer - `sudo service homer stop`
    *   Ellis - `sudo service ellis stop`
    *   Memento - `sudo service memento stop`
    *   Vellum - `sudo service astaire stop && sudo service rogers stop`

## Local Config

This section describes settings that are specific to a single node and are not applicable to any other nodes in the deployment. They are entered early on in the node's life and are not normally changed. These options should be set in `/etc/clearwater/local_config`. Once this file has been created it is highly recommended that you do not change it unless instructed to do so. If you find yourself needing to change these settings, you should destroy and recreate then node instead.

* `local_ip` - this should be set to an IP address which is configured on an interface on this system, and can communicate on an internal network with other Clearwater nodes and IMS core components like the HSS.
* `public_ip` - this should be set to an IP address accessible to external clients (SIP UEs for Bono, web browsers for Ellis). It does not need to be configured on a local interface on the system - for example, in a cloud environment which puts instances behind a NAT.
* `public_hostname` - this should be set to a hostname which resolves to `public_ip`, and will communicate with only this node (i.e. not be round-robined to other nodes). It can be set to `public_ip` if necessary.
* `node_idx` - an index number used to distinguish this node from others of the same type in the cluster (for example, sprout-1 and sprout-2). Optional.
* `etcd_cluster` - this is either blank or a comma separated list of IP addresses, for example `etcd_cluster=10.0.0.1,10.0.0.2`. The setting depends on the node's role:
    * If this node is an etcd master, then it should be set in one of two ways:
        * If the node is forming a new etcd cluster, it should contain the IP addresses of all the nodes that are forming the new cluster as etcd masters (including this node).
        * If the node is joining an existing etcd cluster, it should contain the IP addresses of all the nodes that are currently etcd masters in the cluster.
    * If this node is an etcd proxy, it should be left blank
* `etcd_proxy` - this is either blank or a comma separated list of IP addresses, for example `etcd_proxy=10.0.0.1,10.0.0.2`. The setting depends on the node's role:
    * If this node is an etcd master, this should be left blank
    * If this node is an etcd proxy, it should contain the IP addresses of all the nodes that are currently etcd masters in the cluster.
* `etcd_cluster_key` - this is the name of the etcd datastore clusters that this node should join. It defaults to the function of the node (e.g. a Vellum node defaults to using 'vellum' as its etcd datastore cluster name when it joins the Cassandra cluster). This must be set explicitly on nodes that colocate function.
* `remote_cassandra_seeds` - this is used to connect the Cassandra cluster in your second site to the Cassandra cluster in your first site; this is only necessary in a geographically redundant deployment which is using at least one of Homestead-Prov, Homer or Memento. It should be set to an IP address of a Vellum node in your first site, and it should only be set on the first Vellum node in your second site.
* `scscf_node_uri` - this can be optionally set, and only applies to nodes running an S-CSCF. If it is configured, it almost certainly needs configuring on each S-CSCF node in the deployment.

    If set, this is used by the node to advertise the URI to which requests to this node should be routed. It should be formatted as a SIP URI.

    This will need to be set if the local IP address of the node is not routable by all the application servers that the S-CSCF may invoke. In this case, it should be configured to contain an IP address or host which is routable by all of the application servers – e.g. by using a domain and port on which the sprout can be addressed - `scscf_node_uri=sip:sprout-4.example.net:5054`.

    The result will be included in the Route header on SIP messages sent to application servers invoked during a call.

    If it is not set, the URI that this S-CSCF node will advertise itself as will be `sip:<local_ip>:<scscf_port>` where `<local_ip>` is documented above, and `<scscf_port>` is the port on which the S-CSCF is running, which is 5054 by default.

## Shared Config

This section describes settings that are common across the entire deployment.

### Core options

This section describes options for the basic configuration of a Clearwater deployment - such as the hostnames of the six node types and external services such as email servers or the Home Subscriber Server. These options should be set in a local copy (in the format `name=value`, e.g. `home_domain=example.com`) by running `cw-config download shared_config`, editing this downloaded copy and then running `cw-config upload shared_config` when finished.

* `home_domain` - this is the main SIP domain of the deployment, and determines which SIP URIs Clearwater will treat as local. It will usually be a hostname resolving to all the P-CSCFs (e.g. the Bono nodes). Other domains can be specified through additional_home_domains, but Clearwater will treat this one as the default (for example, when handling `tel:` URIs).
* `sprout_hostname` - a hostname that resolves by DNS round-robin to the signaling interface of all Sprout nodes in the cluster.
* `sprout_hostname_mgmt` - a hostname that resolves by DNS round-robin to the management interface of all Sprout nodes in the cluster.  Should include the HTTP port (always 9886). For details on the HTTP API exposed on this interface, see https://github.com/Metaswitch/sprout/blob/dev/docs/ManagementHttpAPI.md.
* `hs_hostname` - a hostname that resolves by DNS round-robin to the signaling interface of all Dime nodes in the cluster. Should include the HTTP port (always 8888). This is also used (without the port) as the Origin-Realm of the Diameter messages the homestead process on Dime sends.
* `hs_hostname_mgmt` - a hostname that resolves by DNS round-robin to the management interface of all Dime nodes in the cluster.  Should include the HTTP port (always 8886). For details on the HTTP API exposed on this interface, see https://github.com/Metaswitch/homestead/blob/dev/docs/ManagementHttpAPI.md.
* `hs_provisioning_hostname` - a hostname that resolves by DNS round-robin to the management interface of all Dime nodes in the cluster. Should include the HTTP provisioning port (usually 8889). Not needed when using an external HSS.
* `ralf_hostname` - a hostname that resolves by DNS round-robin to the signaling interface of all Dime nodes in the cluster. Should include the port (usually 9888). This is also used (without the port) as the Origin-Realm of the Diameter messages the ralf process on Dime sends. Optional if ralf is not being used.
* `cdf_identity` - a Diameter identity that represents the address of an online Charging Function. Subscribers provisioned through Ellis will have this set as their Primary Charging Collection Function on P-Charging-Function-Addresses headers on responses to their successful REGISTERs, and Bono will add similarly in originating requests.
* `xdms_hostname` - a hostname that resolves by DNS round-robin to all Homer nodes in the cluster. Should include the port (usually 7888).
* `hss_realm` - this sets the Destination-Realm of your external HSS. When this field is set, the homestead process on Dime will then attempt to set up multiple Diameter connections using an SRV lookup on this realm.
* `hss_hostname` - this sets the Destination-Host of your external HSS, if you have one. The homestead process on Dime will also try and establish a Diameter connection to this host (on port 3868) if no SRV-discovered peers exist.
* `signup_key` - this sets the password which Ellis will require before allowing self-sign-up.
* `turn_workaround` - if your STUN/TURN clients are not able to authenticate properly (for example, because they can't send the @ sign), this specifies an additional password which will authenticate clients even without a correct username.
* `smtp_smarthost` - Ellis allows password recovery by email. This sets the SMTP server used to send those emails.
* `smtp_username` - Ellis allows password recovery by email. This sets the username used to log in to the SMTP server.
* `smtp_password` - Ellis allows password recovery by email. This sets the password used to log in to the SMTP server.
* `email_recovery_sender` - Ellis allows password recovery by email. This sets the email address those emails are sent from.
* `ellis_api_key` - sets a key which can be used to authenticate automated requests to Ellis, by setting it as the value of the X-NGV-API header. This is used to expire demo users regularly.
* `ellis_hostname` - a hostname that resolves to Ellis, if you don't want to use `ellis.home_domain`.  This should match Ellis's SSL certificate, if you are using one.
* `memento_hostname` - a hostname that resolves by DNS round-robin to all Mementos in the cluster (the default is `memento.<home_domain>`).  This should match Memento's SSL certificate, if you are using one.
* `sprout_registration_store` - this is the location of Sprout's registration store. It has the format `<site_name>=<domain>[:<port>][,<site_name>=<domain>[:<port>]]`. In a non-GR deployment, only one domain is provided (and the site name is optional). For a GR deployment, each domain is identified by the site name, and one of the domains must relate to the local site.
* `ralf_session_store` - this is the location of ralf's session store. It has the format `<site_name>=<domain>[:<port>][,<site_name>=<domain>[:<port>]]`. In a non-GR deployment, only one domain is provided (and the site name is optional). For a GR deployment, each domain is identified by the site name, and one of the domains must relate to the local site.
* `homestead_impu_store` - this is the location of homestead's IMPU store. It has the format `<site_name>=<domain>[:<port>][,<site_name>=<domain>[:<port>]]`. In a non-GR deployment, only one domain is provided (and the site name is optional). For a GR deployment, each domain is identified by the site name, and one of the domains must relate to the local site.
* `memento_auth_store` - this is the location of Memento's authorization vector store. It just has the format `<domain>[:port]`. If not present, defaults to the loopback IP.
* `sprout_chronos_callback_uri` - the callback hostname used on Sprout's Chronos timers. If not present, defaults to the host specified in `sprout-hostname`. In a GR deployment, should be set to a deployment-wide Sprout hostname (that will be resolved by using static DNS records in `/etc/clearwater/dns.json`).
* `ralf_chronos_callback_uri` - the callback hostname used on ralf's Chronos timers. If not present, defaults to the host specified in `ralf-hostname`. In a GR deployment, should be set to a deployment-wide Dime hostname (that will be resolved by using static DNS records in `/etc/clearwater/dns.json`).
* `cassandra_hostname` - a hostname that resolves by DNS round-robin to the signaling interface of all Vellum nodes in the local site.
* `chronos_hostname` - a hostname that resolves by DNS round-robin to the signaling interface of all Vellum nodes in the local site.

### Sproutlet options

This section describes optional configuration options for the Clearwater Sproutlets. Sproutlets are built on top of [Sprout](https://github.com/Metaswitch/sprout), and encapsulate the business logic of the I-CSCF/S-CSCF/BGCF, or Project Clearwater's built in Application servers

There are currently eight different Sproutlets:

* S-CSCF - Provides S-CSCF functionality
* I-CSCF - Provides I-CSCF functionality
* BGCF - Provides BGCF functionality
* Gemini - An application server responsible for twinning VoIP clients with a mobile phone hosted on a native circuit-switched network. You can find out more [here](https://github.com/Metaswitch/gemini)
* Memento - An application server responsible for providing network-based call lists. You can find out more [here](https://github.com/Metaswitch/memento)
* CDiv - Provides call diversion functionality
* MMtel - Acts as a basic MMTel AS
* Mangelwurzel - Acts as a basic B2BUA

Each Sproutlet has three configuration options. The options have the same format for each Sproutlet, as listed here, with `<sproutlet>` replaced by the appropriate Sproutlet name:

* `<sproutlet>` - The port that the Sproutlet listens on. The default value depends on the Sproutlet. Some Sproutlets default to 0 (meaning that they are disabled by default). For other Sproutlets, the defaults are:
```
    I-CSCF - 5052
    BGCF - 5053
    S-CSCF - 5054
    MMTel - 5055
```
* `<sproutlet>_prefix` - The identifier prefix for this Sproutlet, used to build the uri, as described below. The default value is simply the Sproutlet name: `<sproutlet>`
* `<sproutlet>_uri` - The full identifier for this Sproutlet, used for routing and receiving requests between nodes. The default value is created using the prefix and the hostname of the parent Sprout node, i.e. `sip:<sproutlet_prefix>.<sprout_hostname>;transport=tcp`. We recommend that you don’t set this yourself anymore, and use the defaults provided.

As a concrete example, below are the S-CSCF options and the default values.

* `scscf=5054`
* `scscf_prefix=scscf`
* `scscf_uri=sip:scscf.<sprout_hostname>;transport=tcp`

### Advanced options

This section describes optional configuration options, particularly for ensuring conformance with other IMS devices such as HSSes, ENUM servers, application servers with strict requirements on Record-Route headers, and non-Clearwater I-CSCFs. These options should be set in a local copy (in the format `name=value`, e.g. `icscf=5052`) by running `cw-config download shared_config`, editing this downloaded copy and then running `cw-config upload shared_config` when finished.

* `homestead_provisioning_port` - the HTTP port the homestead provisioning interface on Dime listens on. Defaults to 8889. Not needed when using an external HSS.
* `sas_server` - the IP address or hostname of your Metaswitch Service Assurance Server for call logging and troubleshooting. Optional.
* `reg_max_expires` - determines the maximum expires= parameter Sprout will set on Contact headers at registrations, and therefore the amount of time before a UE has to re-register - must be less than 2^31 ms (approximately 25 days). Default is 300 (seconds).
* `sub_max_expires` - determines the maximum Expires header Sprout will set in subscription responses, and therefore the amount of time before a UE has to re-subscribe - must be less than 2^31 ms (approximately 25 days).
* `upstream_hostname` - the I-CSCF which Bono should pass requests to. Defaults to `icscf.<sprout_hostname>`.
* `upstream_port` - the port on the I-CSCF which Bono should pass requests to. Defaults to 5052. If set to 0, Bono will use SRV resolution of the `upstream_hostname` hostname to determine a target for traffic.
* `sprout_rr_level` - this determines how the Sprout S-CSCF adds Record-Route headers. Possible values are:
    * `pcscf` - a Record-Route header is only added just after requests come from or go to a P-CSCF - that is, at the start of originating handling and the end of terminating handling
    * `pcscf,icscf` - a Record-Route header is added just after requests come from or go to a P-CSCF or I-CSCF - that is, at the start and end of originating handling and the start and end of terminating handling
    * `pcscf,icscf,as` - a Record-Route header is added after requests come from or go to a P-CSCF, I-CSCF or application server - that is, at the start and end of originating handling, the start and end of terminating handling, and between each application server invoked
* `force_hss_peer` - when set to an IP address or hostname, the homestead process on Dime will create a connection to the HSS using this value, but will still use the `hss_realm` and `hss_hostname` settings for the Destination-Host and Destination-Realm Diameter AVPs. This is useful when your HSS's Diameter configuration does not match the DNS records.
* `hss_mar_scheme_unknown` - if Clearwater cannot tell what authentication type a subscriber is trying to use, this field determines what authentication scheme it requests in the Multimedia-Auth-Request. Default value is 'Unknown'.
* `hss_mar_scheme_digest` - if Clearwater determines a subscriber is trying to use password-based digest authentication, this field determines what authentication scheme it requests in the Multimedia-Auth-Request. Default value is 'SIP Digest'.
* `hss_mar_scheme_akav1` - if Clearwater determines a subscriber is trying to use AKAv1 authentication, this field determines what authentication scheme it requests in the Multimedia-Auth-Request. Default value is 'Digest-AKAv1-MD5'.
* `hss_mar_scheme_akav2` - if Clearwater determines a subscriber is trying to use AKAv2 authentication, this field determines what authentication scheme it requests in the Multimedia-Auth-Request. Default value is 'Digest-AKAv2-SHA-256'.
* `force_third_party_reg_body` - if the HSS does not allow the IncludeRegisterRequest/IncludeRegisterResponse fields (which were added in 3GPP Rel 9) to be configured, setting `force_third_party_reg_body=Y` makes Clearwater behave as though they had been sent, allowing interop with application servers that need them.
* `enforce_user_phone` - by default, Clearwater will do an ENUM lookup on any SIP URI that looks like a phone number, due to client support for user-phone not being widespread. When this option is set to 'Y', Clearwater will only do ENUM lookups for URIs which have the user=phone parameter.
* `enforce_global_only_lookups` - by default, Clearwater will do ENUM lookups for SIP and Tel URIs containing global and local numbers (as defined in RFC 3966). When this option is set to ‘Y’, Clearwater will only do ENUM lookups for SIP and Tel URIs that contain global numbers.
* `hs_listen_port` - the Diameter port on which the homestead process on Dime listens. Defaults to 3868.
* `ralf_listen_port`  - the Diameter port on which the ralf process on Dime listens. Defaults to 3869 to avoid clashes with the homestead process.
* `homestead_diameter_watchdog_timer` - the delay in seconds before a device watchdog message is sent on an unresponsive Diameter connection by the homestead process. Defaults to 6 and must be set to an integer that is at least 6.
* `ralf_diameter_watchdog_timer` - the delay in seconds before a device watchdog message is sent on an unresponsive Diameter connection by the ralf process. Defaults to 6 and must be set to an integer that is at least 6.
* `alias_list` - this defines additional hostnames and IP addresses which Sprout or Bono will treat as local for the purposes of SIP routing (e.g. when removing Route headers).
* `bono_alias_list` - this defines additional hostnames and IP addresses specifically for Bono which will be treated as local for the purposes of SIP routing.
* `default_session_expires` - determines the Session-Expires value which Sprout will add to INVITEs, to force UEs to send keepalive messages during calls so they can be tracked for billing purposes. This cannot be set to a value less than 90 seconds, as specified in [RFC 4028, section 4](https://tools.ietf.org/html/rfc4028#section-4).
* `max_session_expires` - determines the maximum Session-Expires/Min-SE value which Sprout will accept in requests. This cannot be set to a value less than 90 seconds, as specified in [RFC 4028, sections 4 and 5](https://tools.ietf.org/html/rfc4028#section-4).
* `enum_server` - a comma-separated list of DNS servers which can handle ENUM queries.
* `enum_suffix` - determines the DNS suffix used for ENUM requests (after the digits of the number). Defaults to "e164.arpa"
* `enum_file` - if set (to a file path), and if `enum_server` is not set, Sprout will use this local JSON file for ENUM lookups rather than a DNS server. An example file is [on our ENUM page](ENUM.md#deciding-on-enum-rules).
* `external_icscf_uri` - the SIP address of the external I-CSCF integrated with your Sprout node (if you have one).
* `additional_home_domains` - this option defines a set of home domains which Sprout and Bono will regard as locally hosted (i.e. allowing users to register, not routing calls via an external trunk). It is a comma-separated list.
* `billing_realm` - when this field is set, the ralf process on Dime will attempt to set up multiple Diameter connections using an SRV lookup on this realm.  Messages sent on these connections will have:
    * Destination-Realm set to the `billing_realm` value
    * Destination-Host set to the value of the `ccf` parameter in the P-Charging-Function-Addresses SIP header received from the P-CSCF, or from the Primary-Charging-Collection-Function-Name/Secondary-Charging-Collection-Function-Name AVPs received over the Cx interface from the HSS.
* `diameter_timeout_ms` - determines the number of milliseconds homestead will wait for a response from the HSS before failing a request. Defaults to 200.
* `sprout_homestead_timeout_ms` - determines the timeout in milliseconds for which Sprout will wait for Homestead to respond to HTTP requests. Defaults to 550ms + twice the diameter timeout.
* `max_peers` - determines the maximum number of Diameter peers to which the ralf or homestead processes on Dime can have open connections at the same time.
* `num_http_threads` (sprout/homestead/ralf/memento) - determines the number of threads that will be used to process HTTP requests. For Homestead and Memento this defaults to the number of CPU cores on the system. For Sprout and Ralf it defaults to 50 times the number of CPU cores. This is because there are two different threading models, hence the different defaults. On Sprout and Homestead, this can be overriden using the more specific option detailed below.
* `num_http_worker_threads` - determines the number of threads that will be used to process HTTP requests once they have been parsed. Only used by Memento.
* `sprout_http_threads` - determines the number of HTTP threads that will be used to process HTTP requests on Sprout. Defaults to `num_http_threads`.
* `homestead_http_threads` - determines the number of HTTP threads that will be used to process HTTP requests on Homestead. Defaults to `num_http_threads`.
* `num_worker_threads` - The default number of worker threads that should be started to do SIP/IMS processing on Sprout and Bono. Defaults to 50 times the number of CPU cores on the system.
* `sprout_worker_threads` - The number of worker threads Sprout will start. Defaults to `num_worker_threads`
* `ralf_diameteridentity` - determines the Origin-Host that will be set on the Diameter messages ralf sends. Defaults to `public_hostname` (with some formatting changes if public_hostname is an IPv6 address).
* `hs_diameteridentity` - determines the Origin-Host that will be set on the Diameter messages homestead sends. Defaults to `public_hostname` (with some formatting changes if public_hostname is an IPv6 address).
* `max_call_list_length` - determines the maximum number of complete calls a subscriber can have in the call list store. This defaults to no limit. This is only relevant if the node includes a Memento AS.
* `call_list_store_ttl` - determines how long each call list fragment should be kept in the call list store. This defaults to 604800 seconds (1 week). This is only relevant if the node includes a Memento AS.
* `memento_disk_limit` - determines the maximum size that the call lists database may occupy. This defaults to 20% of disk space. This is only relevant if the node includes a Memento AS. Can be specified in Bytes, Kilobytes, Megabytes, Gigabytes, or a percentage of the available disk. For example:

        memento_disk_limit=10240 # Bytes
        memento_disk_limit=100k  # Kilobytes
        memento_disk_limit=100M  # Megabytes
        memento_disk_limit=100G  # Gigabytes
        memento_disk_limit=45%   # Percentage of available disk

* `memento_threads` - determines the number of threads dedicated to adding call list fragments to the call list store. This defaults to 25 threads. This is only relevant if the node includes a Memento AS.
* `memento_notify_url` - If set to an HTTP URL, memento will make a POST request to this URL whenever a subscriber's call list changes.  The body of the POST request will be a JSON document with the subscriber's IMPU in a field named `impu`.  This is only relevant if the node includes a Memento AS.  If empty, no notifications will be sent.  Defaults to empty.
* `signaling_dns_server` - a comma-separated list of DNS servers for non-ENUM queries. Defaults to 127.0.0.1 (i.e. uses `dnsmasq`)
* Throttling options:
    * These options are used as part of the throttling code that allows Clearwater to cope with overload situations. The throttling options are specific to each individual process, e.g. sprout, ralf, homestead, ...
    * `<process>_target_latency_us` - Target latency (in microsecs) for requests above which [throttling](http://www.projectclearwater.org/clearwater-performance-and-our-load-monitor/) applies. This defaults to 10000 microsecs for sprout and 100000 microsecs for other processes. The difference is due to the fact that sprout ignores latency of network requests when calculating message latency. 
    * `<process>_max_tokens` - Maximum number of tokens allowed in the token bucket (used by the throttling code). This defaults to 1000 tokens
    * `<process>_init_token_rate` - Initial token refill rate of tokens in the token bucket (used by the throttling code). This defaults to 250 tokens per second per core
    * `<process>_min_token_rate` - Minimum token refill rate of tokens in the token bucket (used by the throttling code). This defaults to 10.0
    * `<process>_max_token_rate` - Maximum token refill rate of tokens in the token bucket (used by the throttling code). This defaults to 0.0 (no maximum)
    * `<process>_request_queue_timeout` - Maximum time a request can be waiting to be processed before it is rejected (used by the throttling code). This defaults to 4000 millisecs
* `override_npdi` - Whether the I-CSCF, S-CSCF and BGCF should check for number portability data on requests that already have the 'npdi' indicator. This defaults to false
* `exception_max_ttl` - determines the maximum time before a process exits if it crashes. This defaults to 600 seconds
* `check_destination_host` - determines whether the node checks the Destination-Host on a Diameter request when deciding whether it should process the request. This defaults to true.
* `astaire_cpu_limit_percentage` - the maximum percentage of total CPU that Astaire is allowed to consume when resyncing memcached data (as part of a scale-up, scale-down, or following a memcached failure). Note that this only limits the CPU usage of the Astaire process, and does not affect memcached's CPU usage. Must be an integer. Defaults to 5.
* `sip_blacklist_duration` - the time in seconds for which SIP peers are blacklisted when they are unresponsive (defaults to 30 seconds).
* `http_blacklist_duration` - the time in seconds for which HTTP peers are blacklisted when they are unresponsive (defaults to 30 seconds).
* `diameter_blacklist_duration` - the time in seconds for which Diameter peers are blacklisted when they are unresponsive (defaults to 30 seconds).
* `snmp_ip` - the IP address to send alarms to (defaults to being unset). If this is set then Sprout, Dime and Vellum will send alarms - more details on the alarms are [here](SNMP_Alarms.md). This can be a single IP address, or a comma-separated list of IP addresses.
* `snmp_notification_types` - this determines what format SNMP alarms are sent in, and is a comma-separated list of SNMP alarm formats. Valid alarm formats are `rfc3877` and `enterprise` - if both are set, every alarm generates two SNMP INFORMs, one in each format . See the [SNMP alarms documentation](SNMP_Alarms.md) for information about the difference between the formats.
* `impu_cache_ttl` - the number of seconds for which homestead will cache the SIP Digest from a Multimedia-Auth-Request. Defaults to 0, as Sprout does enough caching to ensure that it can handle an authenticated REGISTER after a challenge, and subsequent challenges should be rare.
* `sip_tcp_connect_timeout` - the time in milliseconds to wait for a SIP TCP connection to be established (defaults to 2000 milliseconds).
* `sip_tcp_send_timeout` - the time in milliseconds to wait for sent data to be acknowledgered at the TCP level on a SIP TCP connection (defaults to 2000 milliseconds).
* `session_continued_timeout_ms` - if an Application Server with default handling of 'continue session' is unresponsive, this is the time that Sprout will wait (in milliseconds) before bypassing the AS and moving onto the next AS in the chain (defaults to 2000 milliseconds).
* `session_terminated_timeout_ms` - if an Application Server with default handling of 'terminate session' is unresponsive, this is the time that Sprout will wait (in milliseconds) before terminating the session (defaults to 4000 milliseconds).
* `sas_use_signaling_interface` - When this field is set to 'Y', SAS traffic is routed via the signaling network, rather than the management network.
* `pbxes` - a comma separated list of IP address that Bono considers to be PBXes that are incapable of registering. Non-REGISTER requests from these addresses are passed upstream to Sprout with a `Proxy-Authorization` header. It is strongly recommended that Sprout's `non_register_authentication` option is set to `if_proxy_authorization_present` so that the request will be challenged. Bono also permits requests to these addresses from the core to pass through it.
* `pbx_service_route` - the SIP URI to which Bono routes originating calls from non-registering PBXes (which are identified by the `pbxes` option). This is used to route requests directly to the S-CSCF rather than going via an I-CSCF (which could change the route header and prevent the S-CSCF from processing the request properly). This URI is used verbatim and should almost always include the `lr`, `orig`, and `auto-reg` parameters. If this option is not specified, the requests are routed to the address specified by the `upstream_hostname` and `upstream_port` options.
    * e.g. `sip:sprout.example.com:5054;transport=tcp;lr;orig;auto-reg`
* `non_register_authentication` - controls when Sprout will challenge a non-REGISTER request using SIP Proxy-Authentication. This option is a comma separated list that may contain the values listed below (e.g. `non_register_authentication=if_proxy_authorization_present,initial_req_from_req_digest_endpoint`):
  * `if_proxy_authorization_present`: Sprout will authenticate requests that have a Proxy-Authorization header.
  * `initial_req_from_reg_digest_endpoint`: Sprout will authenticate requests from registered endpoints that use the SIP digest authentication scheme.
* `ralf_threads` - used on Sprout nodes, this determines how many worker threads should be started to do ralf request processing (defaults to 25).
* `impi_store_mode` - used to control how Sprout stores authentication challenges. The default is `impi` which means that challenges are written to a single memcached database table indexed by IMPI. There is another option, `av-impi`, where challenges are also stored in an old table indexed by (IMPI, nonce). This setting can be used to upgrade Clearwater to use the new database table without losing registration state.
* `nonce_count_supported` - when set to 'Y' Clearwater permits authentication responses with a nonce-count greater than 1. By default this option is not enabled. Enabling this option can expose certain security holes if your deployment does not use an HSS (and uses Homestead-Prov instead) and an I-CSCF. Specifically if the option is set and a malicious UE manages to register:
    * Without an HSS there is no way to force it to become deregistered.
    * Without an I-CSCF there is no way to prevent it from registering as different user accounts.
* `disable_tcp_switch` - when set to 'Y', Clearwater disables UDP-to-TCP uplift on SIP messages.  This is useful when creating a deployment where all SIP is sent over UDP.  This option only affects Sprout nodes.
* `sprout_impi_store` - this is the location of Sprout's IMPI store. It has the same format as `sprout_registration_store`. If not provided, Sprout uses the same value configured in `sprout_registration_store`.
* `request_shared_ifcs` - when set to 'Y' Clearwater requests Shared iFC sets from the HSS. Shared iFC sets can be configured on Clearwater in the `/etc/clearwater/shared_ifcs.xml` file. This option is not enabled by default.
* `apply_fallback_ifcs` - when set to 'Y' Clearwater will apply any fallback iFCs specified by the operator in the `/etc/clearwater/fallback_ifcs.xml` file to initial requests who have no applicable iFCs associated with them. This option is not enabled by default.
* `reject_if_no_matching_ifcs` - when set to 'Y' Clearwater will reject any initial requests that don't have any matching iFCs that can be applied to them. This option is not enabled by default.
* `dummy_app_server` - this field allows the name of a dummy application server to be specified. If an iFC contains this dummy application server, then no application server will be invoked when this iFC is triggered.
* `http_acr_logging` when set to 'Y', Clearwater will log the bodies of HTTP requests made to Ralf.  This provides additional diagnostics, but increases the volume of data sent to SAS.
* `dns_timeout` - The time in milliseconds that Clearwater will wait for a response from the DNS server (defaults to 200 milliseconds).
* `homestead_cache_threads` - The number of threads used by Homestead for accessing it's subscriber data cache. Defaults to 50x the number of CPU cores.

### Experimental options

This section describes optional configuration options which may be useful, but are not heavily-used or well-tested by the main Clearwater development team. These options should be set in a local copy (in the format `name=value`, e.g. `ralf_secure_listen_port=12345`) by running `cw-config download shared_config`, editing this downloaded copy and then running `cw-config upload shared_config` when finished.

* `ralf_secure_listen_port` - this determines the port the ralf process on Dime listens on for TLS-secured Diameter connections.
* `hs_secure_listen_port` - this determines the port the homestead process on Dime listens on for TLS-secured Diameter connections.
* `ellis_cookie_key` - an arbitrary string that enables Ellis nodes to determine whether they should be in the same cluster. This function is not presently used.
* `stateless_proxies` - a comma separated list of domain names that are treated as SIP stateless proxies. Stateless proxies are not blacklisted if a SIP transaction sent to them times out. This field should reflect how the servers are identified in SIP. For example if a cluster of nodes is identified by the name 'cluster.example.com', the option should be set to 'cluster.example.com' instead of the hostnames or IP addresses of individual servers.
* `hss_reregistration_time` - determines how many seconds should pass before homestead sends a Server-Assignment-Request with type RE_REGISTRATION to the HSS. (On first registration, it will always send a SAR with type REGISTRATION). This determines a minimum value - after this many seconds have passed, homestead will send the Server-Assignment-Request when the next REGISTER is received. Note that homestead invalidates its cache of the registration and iFCs after twice this many seconds have passed, so it is not safe to set this to less than half of `reg_max_expires`.  The default value of this option is whichever is the greater of the following.

    * 1800.
    * Half of the value of reg_max_expires.

## User settings

This section describes settings that may vary between systems in the same deployment, such as log level (which may be increased on certain machines to track down specific issues) and performance settings (which may vary if some servers in your deployment are more powerful than others). These settings are set in `/etc/clearwater/user_settings` (in the format `name=value`, e.g. `log_level=5`).

* `log_level` - determines how verbose Clearwater's logging is, from 1 (error logs only) to 5 (debug-level logs). Defaults to 2.
* `log_directory` - determines which folder the logs are created in. This folder must exist, and be owned by the service. Defaults to /var/log/<service> (this folder is created and has the correct permissions set for it by the install scripts of the service).
* `max_log_directory_size` - determines the maximum size of each Clearwater process's log_directory in bytes. Defaults to 1GB. If you are co-locating multiple Clearwater processes, you'll need to reduce this value proportionally.
* `upstream_connections` - determines the maximum number of TCP connections which Bono will open to the I-CSCF(s). Defaults to 50.
* `trusted_peers` - For Bono IBCF nodes, determines the peers which Bono will accept connections to and from.
* `ibcf_domain` - For Bono IBCF nodes, allows for a domain alias to be specified for the IBCF to allow for including IBCFs in routes as domains instead of IPs.
* `upstream_recycle_connections` - the average number of seconds before Bono will destroy and re-create a connection to Sprout. A higher value means slightly less work, but means that DNS changes will not take effect as quickly (as new Sprout nodes added to DNS will only start to receive messages when Bono creates a new connection and does a fresh DNS lookup).
* `authentication` - by default, Clearwater performs authentication challenges (SIP Digest or IMS AKA depending on HSS configuration). When this is set to 'Y', it simply accepts all REGISTERs - obviously this is very insecure and should not be used in production.

## DNS Config

This section describes the static DNS config which can be used to override DNS results. These options should be set in a local copy by running `cw-config download dns_json`, editing this downloaded copy and then running `cw-config upload dns_json` when finished. Currently, the only supported record type is CNAME and the only component which uses this is Chronos and the I-CSCF. The file has the format:

    {
      "hostnames": [
        {
          "name": "<hostname 1>",
          "records": [{"rrtype": "CNAME", "target": "<target for hostname 1>"}]
        },
        {
          "name": "<hostname 2>",
          "records": [{"rrtype": "CNAME", "target": "<target for hostname 2>"}]
        }
      ]
    }

## Other configuration options

There is further documentation for Chronos configuration [here](https://github.com/Metaswitch/chronos/blob/dev/doc/configuration.md) and Homer/Homestead-prov configuration [here](https://github.com/Metaswitch/crest/blob/master/docs/development.md#local-settings).
