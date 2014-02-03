# All-in-one IPv6

All-in-one nodes will automatically configure themselves correctly if their local IP address is IPv6.  However

* an All-in-one nodes will use an IPv4 address in preference to an IPv6 address if one is present.
* the cassandra configuration needs to be set up manually.

## Add an IPv6 address to the node

If the node does not automatically pick up an IPv6 address when it booted, assign an address.

## Use IPv6 in preference to IPv4

If the node has an IPv4 and an IPv6 address create a file /etc/clearwater/force_ipv6.  The contents of the file are unimportant.

## Fix up cassandra configuration

Edit /etc/cassandra/cassandra-env.sh.

* Comment out the line that prefers IPv4.
    `# JVM_OPTS="-Djava.net.preferIPv4Stack=true"`

Edit /etc/cassandra/cassandra.yaml

* alter the seeds line

    `- seeds: "::1"`

* alter the listen_address line to contain the IP address of the node
 
    `listen_address: <IPv6 address>`

## Restart Clearwater

In order to pick up the configuration changes restart clearwater

    `sudo service clearwater-infrastructure restart`

