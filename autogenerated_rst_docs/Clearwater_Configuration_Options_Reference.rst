Clearwater Configuration Options Reference
==========================================

This document describes all the Clearwater configuration options that
can be set in /etc/clearwater/shared\_config,
/etc/clearwater/local\_config or /etc/clearwater/user\_settings.

You should follow `this process <Modifying_Clearwater_settings>`__ when
changing most of these settings. However for settings in the "Local
settings" or "User settings" you should:

-  Modify the configuration file
-  Run ``sudo service clearwater-infrastructure restart`` to regenerate
   any dependent configuration files
-  Restart the relevant Clearwater service(s) using the following
   commands as appropriate for the node.

   -  Sprout - ``sudo service sprout quiesce``
   -  Bono - ``sudo service bono quiesce``
   -  Homestead -
      ``sudo service homestead stop && sudo service homestead-prov stop``
   -  Homer - ``sudo service homer stop``
   -  Ralf -``sudo service ralf stop``
   -  Ellis - ``sudo service ellis stop``
   -  Memento - ``sudo service memento stop``

Local Settings
--------------

This section describes settings that are specific to a single node and
are not applicable to any other nodes in the deployment. They are
entered early on in the node's life and are not normally changed. These
options should be set in ``/etc/clearwater/local_config``. Once this
file has been created it is highly recommended that you do not change it
unless instructed to do so. If you find yourself needing to change these
settings, you should destroy and recreate then node instead.

-  ``local_ip`` - this should be set to an IP address which is
   configured on an interface on this system, and can communicate on an
   internal network with other Clearwater nodes and IMS core components
   like the HSS.
-  ``public_ip`` - this should be set to an IP address accessible to
   external clients (SIP UEs for Bono, web browsers for Ellis). It does
   not need to be configured on a local interface on the system - for
   example, in a cloud environment which puts instances behind a NAT.
-  ``public_hostname`` - this should be set to a hostname which resolves
   to ``public_ip``, and will communicate with only this node (i.e. not
   be round-robined to other nodes). It can be set to ``public_ip`` if
   necessary.
-  ``node_idx`` - an index number used to distinguish this node from
   others of the same type in the cluster (for example, sprout-1 and
   sprout-2). Optional.
-  ``etcd_cluster`` - this is a comma separated list of IP addresses,
   for example ``etcd_cluster=10.0.0.1,10.0.0.2``. It should be set on
   one of two ways:
-  If the node is forming a new deployment, it should contain the IP
   addresses of all the nodes that are forming the new deployment
   (including this node).
-  If the node is joining an existing deployment, it should contain the
   IP addresses of all the nodes that are currently in the deployment.
-  ``etcd_cluster_key`` - this is the name of the etcd datastore
   clusters that this node should join. It defaults to the function of
   the node (e.g. a Homestead node defaults to using 'homestead' as its
   etcd datastore cluster name when it joins the Cassandra cluster).
   This must be set explicitly on nodes that colocate function.

Core options
------------

This section describes options for the basic configuration of a
Clearwater deployment - such as the hostnames of the six node types and
external services such as email servers or the Home Subscriber Server.
These options should be set in the ``/etc/clearwater/shared_config``
file (in the format ``name=value``, e.g. ``home_domain=example.com``).

-  ``home_domain`` - this is the main SIP domain of the deployment, and
   determines which SIP URIs Clearwater will treat as local. It will
   usually be a hostname resolving to all the P-CSCFs (e.g. the Bono
   nodes). Other domains can be specified through
   additional\_home\_domains, but Clearwater will treat this one as the
   default (for example, when handling ``tel:`` URIs).
-  ``sprout_hostname`` - a hostname that resolves by DNS round-robin to
   all Sprout nodes in the cluster.
-  ``bono_hostname`` - a hostname that resolves by DNS round-robin to
   all Bono nodes in the cluster.
-  ``hs_hostname`` - a hostname that resolves by DNS round-robin to all
   Homesteads in the cluster. Should include the HTTP port (usually
   8888). This is also used (without the port) as the Origin-Realm of
   the Diameter messages Homestead sends.
-  ``hs_provisioning_hostname`` - a hostname that resolves by DNS
   round-robin to all Homesteads in the cluster. Should include the HTTP
   provisioning port (usually 8889). Not needed when using an external
   HSS.
-  ``ralf_hostname`` - a hostname that resolves by DNS round-robin to
   all Ralf nodes in the cluster. Should include the port (usually
   9888). This is also used (without the port) as the Origin-Realm of
   the Diameter messages Ralf sends. Optional if no Ralf nodes exist.
-  ``cdf_identity`` - a Diameter identity that represents the address of
   an online Charging Function. Subscribers provisioned through Ellis
   will have this set as their Primary Charging Collection Function on
   P-Charging-Function-Addresses headers on responses to their
   successful REGISTERs, and Bono will add similarly in originating
   requests.
-  ``xdms_hostname`` - a hostname that resolves by DNS round-robin to
   all Homer nodes in the cluster. Should include the port (usually
   7888).
-  ``hss_realm`` - this sets the Destination-Realm of your external HSS.
   When this field is set, Homestead will then attempt to set up
   multiple Diameter connections using an SRV lookup on this realm.
-  ``hss_hostname`` - this sets the Destination-Host of your external
   HSS, if you have one. Homestead will also try and establish a
   Diameter connection to this host (on port 3868) if no SRV-discovered
   peers exist.
-  ``signup_key`` - this sets the password which Ellis will require
   before allowing self-sign-up.
-  ``turn_workaround`` - if your STUN/TURN clients are not able to
   authenticate properly (for example, because they can't send the @
   sign), this specifies an additional password which will authenticate
   clients even without a correct username.
-  ``smtp_smarthost`` - Ellis allows password recovery by email. This
   sets the SMTP server used to send those emails.
-  ``smtp_username`` - Ellis allows password recovery by email. This
   sets the username used to log in to the SMTP server.
-  ``smtp_password`` - Ellis allows password recovery by email. This
   sets the password used to log in to the SMTP server.
-  ``email_recovery_sender`` - Ellis allows password recovery by email.
   This sets the email address those emails are sent from.
-  ``ellis_api_key`` - sets a key which can be used to authenticate
   automated requests to Ellis, by setting it as the value of the
   X-NGV-API header. This is used to expire demo users regularly.
-  ``ellis_hostname`` - a hostname that resolves to Ellis, if you don't
   want to use ``ellis.home_domain``. This should match Ellis's SSL
   certificate, if you are using one.
-  ``memento_hostname`` - a hostname that resolves by DNS round-robin to
   all Mementos in the cluster (the default is
   ``memento.<home_domain>``). This should match Memento's SSL
   certificate, if you are using one.

Advanced options
----------------

This section describes optional configuration options, particularly for
ensuring conformance with other IMS devices such as HSSes, ENUM servers,
application servers with strict requirements on Record-Route headers,
and non-Clearwater I-CSCFs. These options should be set in the
``/etc/clearwater/shared_config`` file (in the format ``name=value``,
e.g. ``icscf=5052``).

-  ``icscf`` - the port which Sprout nodes are providing I-CSCF service
   on. If not set, Sprout will only provide S-CSCF function.
-  ``scscf`` - the port which Sprout nodes are providing S-CSCF service
   on. If this not set but ``icscf`` is, Sprout will only provide I-CSCF
   function. If neither is set, this will default to 5054 and Sprout
   will only provide S-CSCF function.
-  ``homestead_provisioning_port`` - the HTTP port the Homestead
   provisioning interface listens on. Defaults to 8889. Not needed when
   using an external HSS.
-  ``sas_server`` - the IP address or hostname of your Metaswitch
   Service Assurance Server for call logging and troubleshooting.
   Optional.
-  ``reg_max_expires`` - determines the maximum expires= parameter
   Sprout will set on Contact headers at registrations, and therefore
   the amount of time before a UE has to re-register - must be less than
   2^31 ms (approximately 25 days). Default is 300 (seconds).
-  ``sub_max_expires`` - determines the maximum Expires header Sprout
   will set in subscription responses, and therefore the amount of time
   before a UE has to re-subscribe - must be less than 2^31 ms
   (approximately 25 days).
-  ``upstream_hostname`` - the I-CSCF which Bono should pass requests
   to. Defaults to the sprout\_hostname.
-  ``upstream_port`` - the port on the I-CSCF which Bono should pass
   requests to. Defaults to 5052. If set to 0, Bono will use SRV
   resolution of the ``upstream_hostname`` hostname to determine a
   target for traffic.
-  ``sprout_rr_level`` - this determines how the Sprout S-CSCF adds
   Record-Route headers. Possible values are:

   -  ``pcscf`` - a Record-Route header is only added just after
      requests come from or go to a P-CSCF - that is, at the start of
      originating handling and the end of terminating handling
   -  ``pcscf,icscf`` - a Record-Route header is added just after
      requests come from or go to a P-CSCF or I-CSCF - that is, at the
      start and end of originating handling and the start and end of
      terminating handling
   -  ``pcscf,icscf,as`` - a Record-Route header is added after requests
      come from or go to a P-CSCF, I-CSCF or application server - that
      is, at the start and end of originating handling, the start and
      end of terminating handling, and between each application server
      invoked

-  ``force_hss_peer`` - when set to an IP address or hostname, Homestead
   will create a connection to the HSS using this value, but will still
   use the ``hss_realm`` and ``hss_hostname`` settings for the
   Destination-Host and Destination-Realm Diameter AVPs. This is useful
   when your HSS's Diameter configuration does not match the DNS
   records.
-  ``hss_mar_lowercase_unknown`` - some Home Subscriber Servers
   (particularly old releases of OpenIMSCore HSS) expect the string
   'unknown' rather than 'Unknown' in Multimedia-Auth-Requests when
   Clearwater cannot tell what authentication type is expected. Setting
   this option to 'Y' will make Homestead send requests in this format.
-  ``hss_mar_force_digest`` - if Clearwater cannot tell what
   authentication type a subscriber is trying to use, this forces it to
   assume 'SIP Digest' and report that in the Multimedia-Auth-Request,
   rather than 'Unknown'.
-  ``hss_mar_force_aka`` - if Clearwater cannot tell what authentication
   type a subscriber is trying to use, this forces it to assume
   'Digest-AKA-v1' and report that in the Multimedia-Auth-Request,
   rather than 'Unknown'.
-  ``force_third_party_reg_body`` - if the HSS does not allow the
   IncludeRegisterRequest/IncludeRegisterResponse fields (which were
   added in 3GPP Rel 9) to be configured, setting
   ``force_third_party_reg_body=Y`` makes Clearwater behave as though
   they had been sent, allowing interop with application servers that
   need them.
-  ``enforce_user_phone`` - by default, Clearwater will do an ENUM
   lookup on any SIP URI that looks like a phone number, due to client
   support for user-phone not being widespread. When this option is set
   to 'Y', Clearwater will only do ENUM lookups for URIs which have the
   user=phone parameter.
-  ``enforce_global_only_lookups`` - by default, Clearwater will do ENUM
   lookups for SIP and Tel URIs containing global and local numbers (as
   defined in RFC 3966). When this option is set to ‘Y’, Clearwater will
   only do ENUM lookups for SIP and Tel URIs that contain global
   numbers.
-  ``hs_listen_port`` - the Diameter port which Homestead listens on.
   Defaults to 3868.
-  ``ralf_listen_port`` - the Diameter port which Ralf listens on.
   Defaults to 3869 to avoid clashes when colocated with Homestead.
-  ``alias_list`` - this defines additional hostnames and IP addresses
   which Sprout or Bono will treat as local for the purposes of SIP
   routing (e.g. when removing Route headers).
-  ``default_session_expires`` - determines the Session-Expires value
   which Sprout will add to INVITEs, to force UEs to send keepalive
   messages during calls so they can be tracked for billing purposes.
   This cannot be set to a value less than 90 seconds, as specified in
   `RFC 4028, section
   4 <https://tools.ietf.org/html/rfc4028#section-4>`__.
-  ``max_session_expires`` - determines the maximum
   Session-Expires/Min-SE value which Sprout will accept in requests.
   This cannot be set to a value less than 90 seconds, as specified in
   `RFC 4028, sections 4 and
   5 <https://tools.ietf.org/html/rfc4028#section-4>`__.
-  ``enum_server`` - a comma-separated list of DNS servers which can
   handle ENUM queries.
-  ``enum_suffix`` - determines the DNS suffix used for ENUM requests
   (after the digits of the number). Defaults to "e164.arpa"
-  ``enum_file`` - if set (to a file path), and if ``enum_server`` is
   not set, Sprout will use this local JSON file for ENUM lookups rather
   than a DNS server. An example file is at
   http://clearwater.readthedocs.org/en/stable/ENUM/index.html#deciding-on-enum-rules.
-  ``icscf_uri`` - the SIP address of the external I-CSCF integrated
   with your Sprout node (if you have one).
-  ``scscf_uri`` - the SIP address of the Sprout S-CSCF. This defaults
   to ``sip:$sprout_hostname:$scscf;transport=TCP`` - this includes a
   specific port, so if you need NAPTR/SRV resolution, it must be
   changed to not include the port.
-  ``additional_home_domains`` - this option defines a set of home
   domains which Sprout and Bono will regard as locally hosted (i.e.
   allowing users to register, not routing calls via an external trunk).
   It is a comma-separated list.
-  ``billing_realm`` - this sets the Destination-Realm on Diameter
   messages to your external CDR. CDR connections are not based on this
   but on configuration at the P-CSCF (which sets the
   P-Charging-Function-Addresses header).
-  ``diameter_timeout_ms`` - determines the number of milliseconds
   Homestead will wait for a response from the HSS before failing a
   request. Defaults to 200.
-  ``max_peers`` - determines the maximum number of Diameter peers which
   Ralf or Homestead can have open connections to at the same time.
-  ``num_http_threads`` (Ralf/Memento) - determines the number of
   threads that will be used to process HTTP requests. For Memento this
   defaults to the number of CPU cores on the system. For Ralf it
   defaults to 50 times the number of CPU cores (Memento and Ralf use
   different threading models, hence the different defaults). Note that
   for Homestead, this can only be set in
   /etc/clearwater/user\_settings.
-  ``num_http_worker_threads`` - determines the number of threads that
   will be used to process HTTP requests once they have been parsed.
   Only used by Memento.
-  ``ralf_diameteridentity`` - determines the Origin-Host that will be
   set on the Diameter messages Ralf sends. Defaults to public\_hostname
   (with some formatting changes if public\_hostname is an IPv6
   address).
-  ``hs_diameteridentity`` - determines the Origin-Host that will be set
   on the Diameter messages Homestead sends. Defaults to
   public\_hostname (with some formatting changes if public\_hostname is
   an IPv6 address).
-  ``gemini_enabled`` - When this field is set to 'Y', then the node
   (either a Sprout or a standalone application server) will include a
   Gemini AS.
-  ``memento_enabled`` - When this field is set to 'Y', then the node
   (either a Sprout or a standalone application server) will include a
   Memento AS.
-  ``max_call_list_length`` - determines the maximum number of complete
   calls a subscriber can have in the call list store. This defaults to
   no limit. This is only relevant if the node includes a Memento AS.
-  ``call_list_store_ttl`` - determines how long each call list fragment
   should be kept in the call list store. This defaults to 604800
   seconds (1 week). This is only relevant if the node includes a
   Memento AS.
-  ``memento_disk_limit`` - determines the maximum size that the call
   lists database may occupy. This defaults to 20% of disk space. This
   is only relevant if the node includes a Memento AS. Can be specified
   in Bytes, Kilobytes, Megabytes, Gigabytes, or a percentage of the
   available disk. For example:

   ::

       memento_disk_limit=10240 # Bytes
       memento_disk_limit=100k  # Kilobytes
       memento_disk_limit=100M  # Megabytes
       memento_disk_limit=100G  # Gigabytes
       memento_disk_limit=45%   # Percentage of available disk

-  ``memento_threads`` - determines the number of threads dedicated to
   adding call list fragments to the call list store. This defaults to
   25 threads. This is only relevant if the node includes a Memento AS.
-  ``memento_notify_url`` - If set to an HTTP URL, memento will make a
   POST request to this URL whenever a subscriber's call list changes.
   The body of the POST request will be a JSON document with the
   subscriber's IMPU in a field named ``impu``. This is only relevant if
   the node includes a Memento AS. If empty, no notifications will be
   sent. Defaults to empty.
-  ``signaling_dns_server`` - a comma-separated list of DNS servers for
   non-ENUM queries. Defaults to 127.0.0.1 (i.e. uses ``dnsmasq``)
-  ``target_latency_us`` - Target latency (in microsecs) for requests
   above which
   `throttling <http://www.projectclearwater.org/clearwater-performance-and-our-load-monitor/>`__
   applies. This defaults to 100000 microsecs
-  ``max_tokens`` - Maximum number of tokens allowed in the token bucket
   (used by the throttling code). This defaults to 20 tokens
-  ``init_token_rate`` - Initial token refill rate of tokens in the
   token bucket (used by the throttling code). This defaults to 250
   tokens per second per core
-  ``min_token_rate`` - Minimum token refill rate of tokens in the token
   bucket (used by the throttling code). This defaults to 10.0
-  ``override_npdi`` - Whether the I-CSCF, S-CSCF and BGCF should check
   for number portability data on requests that already have the 'npdi'
   indicator. This defaults to false
-  ``exception_max_ttl`` - determines the maximum time before a process
   exits if it crashes. This defaults to 600 seconds
-  ``check_destination_host`` - determines whether the node checks the
   Destination-Host on a Diameter request when deciding whether it
   should process the request. This defaults to true.
-  ``astaire_cpu_limit_percentage`` - the maximum percentage of total
   CPU that Astaire is allowed to consume when resyncing memcached data
   (as part of a scale-up, scale-down, or following a memcached
   failure). Note that this only limits the CPU usage of the Astaire
   process, and does not affect memcached's CPU usage. Must be an
   integer. Defaults to 5.
-  ``sip_blacklist_duration`` - the time in seconds for which SIP peers
   are blacklisted when they are unresponsive (defaults to 30 seconds).
-  ``http_blacklist_duration`` - the time in seconds for which HTTP
   peers are blacklisted when they are unresponsive (defaults to 30
   seconds).
-  ``diameter_blacklist_duration`` - the time in seconds for which
   Diameter peers are blacklisted when they are unresponsive (defaults
   to 30 seconds).
-  ``snmp_ip`` - the IP address to send alarms to (defaults to being
   unset). If this is set then Sprout, Ralf, Homestead and Chronos will
   send alarms - more details on the alarms are
   `here <http://clearwater.readthedocs.org/en/stable/SNMP_Alarms/index.html>`__.
   This can be a single IP address, or a comma-separated list of IP
   addresses.
-  ``impu_cache_ttl`` - the number of seconds for which Homestead will
   cache the SIP Digest from a Multimedia-Auth-Request. Defaults to 0,
   as Sprout does enough caching to ensure that it can handle an
   authenticated REGISTER after a challenge, and subsequent challenges
   should be rare.
-  ``sip_tcp_connect_timeout`` - the time in milliseconds to wait for a
   SIP TCP connection to be established (defaults to 2000 milliseconds).
-  ``sip_tcp_send_timeout`` - the time in milliseconds to wait for sent
   data to be acknowledgered at the TCP level on a SIP TCP connection
   (defaults to 2000 milliseconds).
-  ``session_continued_timeout_ms`` - if an Application Server with
   default handling of 'continue session' is unresponsive, this is the
   time that Sprout will wait (in milliseconds) before bypassing the AS
   and moving onto the next AS in the chain (defaults to 2000
   milliseconds).
-  ``session_terminated_timeout_ms`` - if an Application Server with
   default handling of 'terminate session' is unresponsive, this is the
   time that Sprout will wait (in milliseconds) before terminating the
   session (defaults to 4000 milliseconds).
-  ``pbxes`` - a comma separated list of IP address that Bono considers
   to be PBXes that are incapable of registering. Non-REGISTER requests
   from these addresses are passed upstream to Sprout with a
   ``Proxy-Authorization`` header. It is strongly recommended that
   Sprout's ``non_register_authentication`` option is set to
   ``if_proxy_authorization_present`` so that the request will be
   challenged. Bono also permits requests to these addresses from the
   core to pass through it.
-  ``pbx_service_route`` - the SIP URI to which Bono routes originating
   calls from non-registering PBXes (which are identified by the
   ``pbxes`` option). This is used to route requests directly to the
   S-CSCF rather than going via an I-CSCF (which could change the route
   header and prevent the S-CSCF from processing the request properly).
   This URI is used verbatim and should almost always include the
   ``lr``, ``orig``, and ``auto-reg`` parameters. If this option is not
   specified, the requests are routed to the address specified by the
   ``upstream_hostname`` and ``upstream_port`` options.

   -  e.g.
      ``sip:sprout.example.com:5054;transport=tcp;lr;orig;auto-reg``

-  ``non_register_authentication`` - controls when Sprout will challenge
   a non-REGISTER request using SIP Proxy-Authentication. Possible
   values are ``never`` (meaning Sprout will never challenge) or
   ``if_proxy_authorization_present`` (meaning Sprout will only
   challenge requests that have a Proxy-Authorization header).
-  ``ralf_threads`` - used on Sprout nodes, this determines how many
   worker threads should be started to do Ralf request processing
   (defaults to 25).

Experimental options
--------------------

This section describes optional configuration options which may be
useful, but are not heavily-used or well-tested by the main Clearwater
development team. These options should be set in the
``/etc/clearwater/shared_config`` file (in the format ``name=value``,
e.g. ``cassandra_hostname=db.example.com``).

-  ``cassandra_hostname`` - if using an external Cassandra cluster
   (which is a fairly uncommon configuration), a hostname that resolves
   to one or more Cassandra nodes.
-  ``ralf_secure_listen_port`` - this determines the port Ralf listens
   on for TLS-secured Diameter connections.
-  ``hs_secure_listen_port`` - this determines the port Homestead
   listens on for TLS-secured Diameter connections.
-  ``ellis_cookie_key`` - an arbitrary string that enables Ellis nodes
   to determine whether they should be in the same cluster. This
   function is not presently used.
-  ``stateless_proxies`` - a comma separated list of domain names that
   are treated as SIP stateless proxies. Stateless proxies are not
   blacklisted if a SIP transaction sent to them times out. This field
   should reflect how the servers are identified in SIP. For example if
   a cluster of nodes is identified by the name 'cluster.example.com',
   the option should be set to 'cluster.example.com' instead of the
   hostnames or IP addresses of individual servers.
-  ``hss_reregistration_time`` - determines how many seconds should pass
   before Homestead sends a Server-Assignment-Request with type
   RE\_REGISTRATION to the HSS. (On first registration, it will always
   send a SAR with type REGISTRATION). This determines a minimum value -
   after this many seconds have passed, Homestead will send the
   Server-Assignment-Request when the next REGISTER is received. Note
   that Homestead invalidates its cache of the registration and iFCs
   after twice this many seconds have passed, so it is not safe to set
   this to less than half of ``reg_max_expires``. The default value of
   this option is whichever is the greater of the following.

   -  1800.
   -  Half of the value of reg\_max\_expires.

User settings
-------------

This section describes settings that may vary between systems in the
same deployment, such as log level (which may be increased on certain
machines to track down specific issues) and performance settings (which
may vary if some servers in your deployment are more powerful than
others). These settings are set in ``/etc/clearwater/user_settings``,
not ``/etc/clearwater/shared_config`` (in the format ``name=value``,
e.g. ``log_level=5``).

-  ``log_level`` - determines how verbose Clearwater's logging is, from
   1 (error logs only) to 5 (debug-level logs). Defaults to 2.
-  ``log_directory`` - determines which folder the logs are created in.
   This folder must exist, and be owned by the service. Defaults to
   /var/log/ (this folder is created and has the correct permissions set
   for it by the install scripts of the service).
-  ``max_log_directory_size`` - determines the maximum size of each
   Clearwater process's log\_directory in bytes. Defaults to 1GB. If you
   are co-locating multiple Clearwater processes, you'll need to reduce
   this value proportionally.
-  ``num_pjsip_threads`` - determines how many PJSIP transport-layer
   threads should run at once. Defaults to 1, and it may be dangerous to
   change this as it is not necessarily thread-safe.
-  ``num_worker_threads`` - for Sprout and Bono nodes, determines how
   many worker threads should be started to do SIP/IMS processing.
   Defaults to 50 times the number of CPU cores on the system.
-  ``upstream_connections`` - determines the maximum number of TCP
   connections which Bono will open to the I-CSCF(s). Defaults to 50.
-  ``upstream_recycle_connections`` - the average number of seconds
   before Bono will destroy and re-create a connection to Sprout. A
   higher value means slightly less work, but means that DNS changes
   will not take effect as quickly (as new Sprout nodes added to DNS
   will only start to receive messages when Bono creates a new
   connection and does a fresh DNS lookup).
-  ``authentication`` - by default, Clearwater performs authentication
   challenges (SIP Digest or IMS AKA depending on HSS configuration).
   When this is set to 'Y', it simply accepts all REGISTERs - obviously
   this is very insecure and should not be used in production.
-  ``num_http_threads`` (Homestead) - determines the number of HTTP
   worker threads that will be used to process requests. Defaults to 50
   times the number of CPU cores on the system.

Other configuration options
---------------------------

There is further documentation for Chronos configuration
`here <https://github.com/Metaswitch/chronos/blob/dev/doc/configuration.md>`__
and Homer/Homestead-prov configuration
`here <https://github.com/Metaswitch/crest/blob/master/docs/development.md#local-settings>`__.
