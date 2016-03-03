ENUM Guide
==========

`ENUM <http://tools.ietf.org/rfc/rfc6116.txt>`__ is a system for mapping
PSTN numbers to SIP URIs using DNS
`NAPTR <http://en.wikipedia.org/wiki/NAPTR_record>`__ records, and which
sprout supports. This article describes

-  briefly, what ENUM is
-  what we support
-  how to configure a server to respond to ENUM queries.

ENUM overview
-------------

The `NAPTR article on
Wikipedia <http://en.wikipedia.org/wiki/NAPTR_record#Example>`__ gives a
pretty good overview of how ENUM works. Essentially, you

-  convert your PSTN number into a domain name by stripping all
   punctuation, reversing the order of the digits, separating them with
   dots and suffixing with "e164.arpa" (e.g. 12012031234 becomes
   4.3.2.1.3.0.2.1.0.2.1.e164.arpa)
-  issue a DNS NAPTR query for this domain and receive the response
   (which is for the best prefix match to your number)
-  parse the response, which contains a series of regular expressions
   and replacements
-  find the best match for your number (after stripping all punctuation
   except any leading +) and apply the replacement
-  if the NAPTR response indicated this match was "terminal", then use
   the resulting SIP URI - if not, use the output of this pass as input
   for another ENUM query.

The RFCs to refer to for a definitive position are `RFC
3401 <http://www.ietf.org/rfc/rfc3401>`__ (which covers Dynamic
Delegation Discovery System (DDDS), on which ENUM is built) and `RFC
3761 <http://www.ietf.org/rfc/rfc3761>`__ (which covers ENUM itself).
Also relevant is `RFC 4769 <http://www.ietf.org/rfc/rfc4769>`__ (which
specifies ENUM service types).

Clearwater ENUM Support
-----------------------

Clearwater supports ENUM as set out in RFC 3761 and RFC 4769, with the
following points/omissions.

-  ENUM processing should only be applied to TEL URIs and SIP URIs that
   specify that this was dialed by the user. Since no SIP UAs that we're
   aware of indicate that the SIP URI was dialed by a user, we assume
   that any all-numeric (including +) URIs should have ENUM processing
   applied.
-  RFC 3761 section 2.4 says that the ENUM replacement string is
   UTF-8-encoded. We do not support this - all characters must be ASCII
   (i.e. a subset of UTF-8). It is not particularly meaningful to use
   UTF-8 replacements for SIP URIs as SIP URIs themselves must be ASCII.
-  RFC 3761 section 6.1 says that a deployed ENUM service SHOULD include
   mechanisms to ameliorate security threats and mentions using DNSSEC.
   We don't support DNSSEC, so other security approaches (such as
   private ENUM servers) must be used.
-  RFC 4769 describes ENUM rules that output TEL URIs. Since we have no
   way (apart from ENUM itself) of routing to TEL URIs, we ignore such
   rules.
-  RFC 3761 section 2.1 describes the construction of the Application
   Unique String from the E.164 number. We have no way of converting a
   user-dialed number into an E.164 number, so we assume that the number
   provided by the user is E.164.

Deciding on ENUM rules
----------------------

ENUM rules will vary with your deployment, but the (JSON-ized) rules
from an example deployment might form a reasonable basis:

::

    {
        "number_blocks" : [
            {   "name" : "Demo system number 2125550270",
                "prefix" : "2125550270",
                "regex" : "!(^.*$)!sip:\\1@10.147.226.2!"
            },
            {
                "name" : "Clearwater external numbers 2125550271-9",
                "prefix" : "212555027",
                "regex" : "!(^.*$)!sip:+1\\1@ngv.example.com!"
            },
            {
                "name" : "Clearwater external numbers +12125550271-9",
                "prefix" : "+1212555027",
                "regex" : "!(^.*$)!sip:\\1@ngv.example.com!"
            },
            {
                "name" : "Clearwater external number 2125550280",
                "prefix" : "2125550280",
                "regex" : "!(^.*$)!sip:+1\\1@ngv.example.com!"
            },
            {
                "name" : "Clearwater external number +12125550280",
                "prefix" : "+12125550280",
                "regex" : "!(^.*$)!sip:\\1@ngv.example.com!"
            },
            {   "name" : "Clearwater internal numbers",
                "prefix" : "650555",
                "regex" : "!(^.*$)!sip:\\1@ngv.example.com!"
            },
            {   "name" : "Clearwater internal numbers dialled with +1 prefix",
                "prefix" : "+1650555",
                "regex" : "!+1(^.*$)!sip:\\1@ngv.example.com!"
            },
            {   "name" : "NANP => SIP trunk",
                "prefix" : "",
                "regex" : "!(^.*$)!sip:\\1@10.147.226.2!"
            }
        ]
    }

Configuring ENUM rules
----------------------

Normally, the ENUM server would be an existing part of the customer's
network (not part of Clearwater itself) but, for testing and
demonstration, it is useful to be able to configure our own.

Unfortunately, AWS Route 53 does not support the required NAPTR records,
so we can't use this. Fortunately, BIND (easy to install) does, and
dnsmasq (our standard DNS forwarder on Clearwater nodes) does to a
limited extent. This section describes how to configure BIND or dnsmasq
to respond to ENUM queries.

You can set up ENUM rules on either BIND or dnsmasq. BIND is the better
choice, but requires installing an additional package and a few
additional file tweaks. dnsmasq is the weaker choice - it does not
support wildcard domains properly, so rules for each directory number
must be added separately.

BIND
~~~~

Create a new node to run BIND, and open port 53 on it to the world
(``0.0.0.0/0``).

If you are using chef, you can do this by adding a new 'enum' node.

On the new node,

1. install bind by typing "sudo apt-get install bind9"
2. modify /etc/bind/named.conf to add a line 'include
   "/etc/bind/named.conf.e164.arpa";' - we'll create that file next
3. create /etc/bind/named.conf.e164.arpa, with the following contents -
   we'll create the /etc/bind/e164.arpa.db file next

   ::

       zone "e164.arpa" {
               type master;
               file "/etc/bind/e164.arpa.db";
       };

4. create /etc/bind/e164.arpa.db, with the following header

   ::

       $TTL 1h
       @ IN SOA e164.arpa ngv-admin@example.com (
                                                               2009010910 ;serial
                                                               3600 ;refresh
                                                               3600 ;retry
                                                               3600 ;expire
                                                               3600 ;minimum TTL
       )
       @ IN NS e164.arpa.
       @ IN A <this server's IP address>

5. add additional rules of the form '<enum domain name> <order>
   <preference> "<flags>" "<service>" "<regexp>" .' to this file (being
   careful to maintain double-quotes and full-stops)

   -  enum domain name is the domain name for which you want to return
      this regular expression - for example, if you want to use a
      regular expression for number "1201", this would be
      "1.0.2.1.e164.arpa" - if you want to specify a wildcard domain
      (i.e. a prefix match), use \*.1.0.2.1.e164.arpa - note, however,
      that non-wildcard children of a wildcard domain are not themselves
      wildcarded, e.g. if you have a domain \*.1.e164.arpa and a domain
      2.1.e164.arpa, a query for 3.2.1.e164.arpa would not resolve (even
      though it matches \*.1.e164.arpa)
   -  order specifies the order in which this rule is applied compared
      to others - rules of order 1 and processed before those of order 2
      (and rules of order 2 are not processed if one of the matching
      rules of of order 1 are non-terminal)
   -  preference specifies how preferable one rule is compared to
      another - if both rules match, the one with the higher preference
      is used
   -  flags specifies how a match should be processed - it can either be
      blank (meaning apply the regular expression and then continue) or
      "U" (meaning the rule is terminal and, after applying the regular
      expression, no further rules should be processed)
   -  service must be "E2U+SIP", indicating ENUM rather than other
      services
   -  regexp must be a regular expression to apply and is of the form
      !<pattern>!<replacement>! - note that the "!" delimiter is only by
      convention and can be replaced with other symbols (such as "/") if
      "!" occurs within the pattern or replacement.

6. restart bind by typing "sudo service bind9 restart"
7. check /var/log/syslog for errors reported by bind on start-up
8. test your configuration by typing "dig -t NAPTR <enum domain name>"
   and checking you get back the responses you just added.

As an example, the JSON-ized ENUM rules for an example system (above),
translate to the following entries in /etc/bind/e164.arpa.db.

::

    ; Demo system number 2125550270
    0.7.2.0.5.5.5.2.1.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .

    ; Demo system number +12125550270
    0.7.2.0.5.5.5.2.1.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .

    ; Clearwater external numbers 2125550271-9
    *.7.2.0.5.5.5.2.1.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:+1\\1@ngv.example.com!" .

    ; Clearwater external numbers +12125550271-9
    ; Note that we can't define a domain name containing + so we must define a
    ; domain without it and then match a telephone number starting with a + (if
    ; present) or (if not) use the default route via the SIP trunk.
    *.7.2.0.5.5.5.2.1.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(\+^.*$)!sip:\\1@ngv.example.com!" .
    *.7.2.0.5.5.5.2.1.2.1 IN NAPTR 2 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .

    ; Clearwater external number 2125550280
    0.8.2.0.5.5.5.2.1.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:+1\\1@ngv.example.com!" .

    ; Clearwater external number +12125550280
    ; Note that we can't define a domain name containing + so we must define a
    ; domain without it and then match a telephone number starting with a + (if
    ; present) or (if not) use the default route via the SIP trunk.
    0.8.2.0.5.5.5.2.1.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(\+^.*$)!sip:\\1@ngv.example.com!" .
    0.8.2.0.5.5.5.2.1.2.1 IN NAPTR 2 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .

    ; Clearwater internal numbers
    *.5.5.5.0.5.6 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@ngv.example.com!" .

    ; Clearwater internal numbers dialled with +1 prefix
    ; Note that we can't define a domain name containing + so we must define a
    ; domain without it and then match a telephone number starting with a + (if
    ; present) or (if not) use the default route via the SIP trunk.
    *.5.5.5.0.5.6.1 IN NAPTR 1 1 "u" "E2U+sip" "!\+1(^.*$)!sip:\\1@ngv.example.com!" .
    *.5.5.5.0.5.6.1 IN NAPTR 2 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .

    ; NANP => SIP trunk.
    * IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    1.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.1.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    2.1.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.2.1.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    5.2.1.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.5.2.1.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    5.5.2.1.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.5.5.2.1.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    5.5.5.2.1.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.5.5.5.2.1.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    0.5.5.5.2.1.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.0.5.5.5.2.1.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    2.0.5.5.5.2.1.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.2.0.5.5.5.2.1.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    7.2.0.5.5.5.2.1.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    1.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.1.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    2.1.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.2.1.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    5.2.1.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.5.2.1.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    5.5.2.1.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.5.5.2.1.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    5.5.5.2.1.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.5.5.5.2.1.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    0.5.5.5.2.1.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.0.5.5.5.2.1.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    2.0.5.5.5.2.1.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.2.0.5.5.5.2.1.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    7.2.0.5.5.5.2.1.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    8.2.0.5.5.5.2.1.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.8.2.0.5.5.5.2.1.2 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    8.2.0.5.5.5.2.1.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.8.2.0.5.5.5.2.1.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.0.8.2.0.5.5.5.2.1.2.1 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    6 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.6 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    5.6 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.5.6 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    5.0.5.6 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.5.0.5.6 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    5.5.0.5.6 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    *.5.5.0.5.6 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .
    5.5.5.0.5.6 IN NAPTR 1 1 "u" "E2U+sip" "!(^.*$)!sip:\\1@10.147.226.2!" .

dnsmasq
~~~~~~~

Before configuring dnsmasq, you need to find a suitable host.

-  For a deployment with only one sprout node you should just be able to
   use the sprout node itself.
-  For deployments with more than one sprout node, you'll need to either
   create a new node or pick one of your sprout nodes (bearing in mind
   that it will become a single point-of-failure) and then configure
   dnsmasq on all sprouts to query this server for enum lookups by
   creating an "/etc/dnsmasq.d/enum-forwarding" file containing a single
   line of the form "server=/e164.arpa/<DNS IP address/" and then
   restarting dnsmasq with "sudo service dnsmasq restart". Note that
   you'll also need to open UDP port 53 (DNS) to this server in the
   security group.

On the host you've chosen,

1. ensure dnsmasq is installed (it is standard on all Clearwater nodes)
   by typing "sudo apt-get install dnsmasq"
2. create an "/etc/dnsmasq.d/enum" file containing lines of the form
   "naptr-record=<enum domain
   name>,<order>,<preference>,<flags>,<service>,<regexp>" where

   -  enum domain name is the domain name for which you want to return
      this regular expression - for example, if you want to use a
      regular expression for number "1201", this would be
      "1.0.2.1.e164.arpa"
   -  order specifies the order in which this rule is applied compared
      to others - rules of order 1 and processed before those of order 2
      (and rules of order 2 are not processed if one of the matching
      rules of of order 1 are non-terminal)
   -  preference specifies how preferable one rule is compared to
      another - if both rules match, the one with the higher preference
      is used
   -  flags specifies how a match should be processed - it can either be
      blank (meaning apply the regular expression and then continue) or
      "U" (meaning the rule is terminal and, after applying the regular
      expression, no further rules should be processed)
   -  service must be "E2U+SIP", indicating ENUM rather than other
      services
   -  regexp must be a regular expression to apply and is of the form
      !<pattern>!<replacement>! - note that the "!" delimeter is only by
      convention and can be replaced with other symbols (such as "/") if
      "!" occurs within the pattern or replacement.

3. restart dnsmasq by typing "sudo service dnsmasq restart"
4. test your configuration by typing "dig -t NAPTR <enum domain name>"
   and checking you get back the responses you just added.

As an example, the JSON-ized ENUM rules for an example system (above),
translate to the following entries in /etc/dnsmasq.d/enum.

::

    # Demo system number 2125550270
    naptr-record=0.7.2.0.5.5.5.2.1.2.e164.arpa,1,1,U,E2U+SIP,!(^.*$)!sip:\\1@10.147.226.2!

    # Clearwater external numbers 2125550271-9
    naptr-record=7.2.0.5.5.5.2.1.2.e164.arpa,1,1,U,E2U+SIP,!(^.*$)!sip:+1\\1@ngv.example.com!

    # Clearwater external numbers +12125550271-9
    # Note that we can't define a domain name containing + so we must define a # domain without it and then match a telephone number starting with a + (if
    # present) or (if not) use the default route via the SIP trunk.
    naptr-record=7.2.0.5.5.5.2.1.2.1.e164.arpa,1,1,U,E2U+SIP,!(\+^.*$)!sip:\\1@ngv.example.com!
    naptr-record=7.2.0.5.5.5.2.1.2.1.e164.arpa,2,1,U,E2U+SIP,!(^.*$)!sip:\\1@10.147.226.2!

    # Clearwater external number 2125550280
    naptr-record=0.8.2.0.5.5.5.2.1.2.e164.arpa,1,1,U,E2U+SIP,!(^.*$)!sip:+1\\1@ngv.example.com!

    # Clearwater external number +12125550280
    # Note that we can't define a domain name containing + so we must define a
    # domain without it and then match a telephone number starting with a + (if
    # present) or (if not) use the default route via the SIP trunk.
    naptr-record=0.8.2.0.5.5.5.2.1.2.1.e164.arpa,1,1,U,E2U+SIP,!(\+^.*$)!sip:\\1@ngv.example.com!
    naptr-record=0.8.2.0.5.5.5.2.1.2.1.e164.arpa,2,1,U,E2U+SIP,!(^.*$)!sip:\\1@10.147.226.2!

    # Clearwater internal numbers
    naptr-record=5.5.5.0.5.6.e164.arpa,1,1,U,E2U+SIP,!(^.*$)!sip:\\1@ngv.example.com!

    # Clearwater internal numbers dialled with +1 prefix
    # Note that we can't define a domain name containing + so we must define a
    # domain without it and then match a telephone number starting with a + (if
    # present) or (if not) use the default route via the SIP trunk.
    naptr-record=5.5.5.0.5.6.1.e164.arpa,1,1,U,E2U+SIP,!\+1(^.*$)!sip:\\1@ngv.example.com!
    naptr-record=5.5.5.0.5.6.1.e164.arpa,2,1,U,E2U+SIP,!(^.*$)!sip:\\1@10.147.226.2!

    # NANP => SIP trunk
    naptr-record=e164.arpa,1,1,U,E2U+SIP,!(^.*$)!sip:\\1@10.147.226.2!

ENUM Domain Suffix
------------------

`RFC 3761 <http://www.ietf.org/rfc/rfc3761.txt>`__ mandates that domain
names used during ENUM processing are suffixed with .e164.arpa.
Obviously, this means that there can only be one such public domain. If
you need your domain to be public (rather than private as set up above),
you can instead change the suffix, e.g. to .e164.arpa.ngv.example.com,
by

-  configuring sprout to use this suffix via the --enum-suffix parameter
-  configuring your DNS server to respond to this domain rather than
   .e164.arpa (by search-replacing in the config files described above)
-  configuring Route 53 to forward DNS requests for
   e164.arpa.ngv.example.com to your DNS server by creating an NS (Name
   Server) record with name "e164.arpa.ngv.example.com" and value set to
   the name/IP address of your DNS server.

ENUM and Sprout
---------------

To enable ENUM lookups on Sprout, edit ``/etc/clearwater/shared_config``
and add the following configuration to use either an ENUM server
(recommended) or an ENUM file:

::

    enum_server=<IP addresses of enum servers>
    enum_file=<location of enum file>

If you use the ENUM file, enter the ENUM rules in the JSON format (shown
above). If you are using the enhanced node management framework provided
by ``clearwater-etcd``, and you use ``/etc/clearwater/enum.json`` as
your ENUM filename, you can automatically synchronize changes across
your deployment by running
``sudo /usr/share/clearwater/clearwater-config-manager/scripts/upload_enum_json``
after creating or updating the file. In this case, other Sprout nodes
will automatically download and use the uploaded ENUM rules.

It's possible to configure Sprout with secondary and tertiary ENUM
servers, by providing a comma-separated list (e.g.
``enum_server=1.2.3.4,10.0.0.1,192.168.1.1``). If this is done:

-  Sprout will always query the first server in the list first
-  If this returns SERVFAIL or times out (which happens after a
   randomised 500ms-1000ms period), Sprout will resend the query to the
   second server
-  If this returns SERVFAIL or times out, Sprout will resend the query
   to the third server
-  If all servers return SERVFAIL or time out, the ENUM query will fail

