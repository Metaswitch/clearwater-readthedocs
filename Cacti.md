Using Cacti with Clearwater
===========================

[Cacti](http://www.cacti.net/) is an open-source statistics and graphing
solution. It supports gathering statistics via native SNMP and also via
external scripts. It then exposes graphs over a web interface.

We use Cacti for monitoring Clearwater deployment, in particular large
ones running stress.

This document describes how to

-   create and configure a Cacti node
-   point it at your Clearwater nodes
-   view graphs of statistics from your Clearwater nodes.

### Setting up a Cacti node

Assuming you've followed the [Automated Chef install](Automated Install),
here are the steps to create and configure a Cacti node:

1.  use knife box create to create a Cacti node - "knife box create -E
    ENVIRONMENT cacti"
2.  set up a DNS entry for it - "knife dns record create -E ENVIRONMENT
    cacti -z DOMAIN -T A --public cacti -p ENVIRONMENT"
3.  point your web browser at cacti.ENVIRONMENT.DOMAIN
4.  accept all the configuration defaults
5.  login (admin/admin) and set a new password
6.  modify configuration by
    1.  going to Devices and deleting "localhost"
    2.  going to Settings-\>Poller and set "Poller Type" to "spin" and
        "Poller Interval" to "Every Minute"
    3.  going to Data Templates and, for each of "ucd/net - CPU Usage -
        \*" set "Associated RRA's" to "Hourly (1 Minute Average)" and
        "Step" to 60
    4.  going to Graph Templates and change "ucd/net - CPU Usage" to
        disable "Auto Scale"
    5.  going to Import Templates and import the attached XML files
        [cacti\_sip\_stress\_status.xml](cacti_sip_stress_status.xml)
        and
        [cacti\_client\_count.xml](cacti_client_count.xml) -
        these define new data input methods and graph templates for
        retrieving statistics from our components via
        [0MQ](http://www.zeromq.org/)

7.  set up the 0MQ-querying script by
    1.  ssh-ing into the cacti node
    2.  running the following

            sudo apt-get install -y --force-yes git ruby1.9.3 build-essential libzmq3-dev
            sudo gem install bundler --no-ri --no-rdoc
            git clone git@bitbucket.org:metaswitch/sprout.git
            cd sprout/scripts/stats
            sudo bundle install

### Pointing Cacti at a Node

Before you point Cacti at a node, make sure the node has the required
packages installed. All nodes need clearwater-snmpd installed ("sudo
apt-get install clearwater-snmpd"). Additionally, sipp nodes need
clearwater-sip-stress-stats ("sudo apt-get install
clearwater-sip-stress-stats").

To manually point Cacti at a new node,

1.  go to Devices and Add a new node, giving a Description and Hostname,
    setting a Host Template of "ucd/net host" and setting Downed Device
    Detection to "SNMP"
2.  click "Create Graphs for this Host" and select the graphs that you
    want - "ucd/net - CPU Usage" is a safe bet, but you might also want
    "Client Counts" (if a bono node) or "SIP Stress Status" (if a sipp
    node)
3.  click "Edit this Host" to go back to the device, choose "List
    Graphs", select the new graphs and choose "Add to Default Tree" -
    this exposes them on the "graphs" tab you can see at the top of the
    page (although it may take a couple of minutes for them to
    accumulate enough state to render properly).

Alternatively, you can add nodes to Cacti based on chef configuration
using the following chunk of bash, run from the `~/chef` directory.

    knife box list -E ENVIROMENT | grep "Found node" | cut -d\  -f 3,8 | sort | while read description ip ; do
      knife ssh -E ENVIRONMENT -x ubuntu "role:cacti" '
        description='$description'
        ip='$ip'
        echo Configuring $description $ip...
        host_id=$(sudo php -q /usr/share/cacti/cli/add_device.php --template=3 --avail=snmp --description=$description --ip=$ip | tee -a /tmp/knife-ssh.cacti | grep Success | sed -e "s/\(^.*(\|).*$\)//g")
        graph_id=$(sudo php -q /usr/share/cacti/cli/add_graphs.php --graph-type=cg --graph-template-id=4 --host-id=$host_id | tee -a /tmp/knife-ssh.cacti | grep "Graph Added" | sed -e "s/\(^[^)]*(\|).*$\)//g")
        sudo php -q /usr/share/cacti/cli/add_tree.php --type=node --node-type=graph --tree-id=1 --graph-id=$graph_id >> /tmp/knife-ssh.cacti
        if echo $description | grep -q bono ; then
          graph_id=$(sudo php -q /usr/share/cacti/cli/add_graphs.php --graph-type=cg --graph-template-id=35 --host-id=$host_id | tee -a /tmp/knife-ssh.cacti | grep "Graph Added" | sed -e "s/\(^[^)]*(\|).*$\)//g")
          sudo php -q /usr/share/cacti/cli/add_tree.php --type=node --node-type=graph --tree-id=1 --graph-id=$graph_id >> /tmp/knife-ssh.cacti
        fi
        if echo $description | grep -q sipp ; then
          graph_id=$(sudo php -q /usr/share/cacti/cli/add_graphs.php --graph-type=cg --graph-template-id=36 --host-id=$host_id | tee -a /tmp/knife-ssh.cacti | grep "Graph Added" | sed -e "s/\(^[^)]*(\|).*$\)//g")
          sudo php -q /usr/share/cacti/cli/add_tree.php --type=node --node-type=graph --tree-id=1 --graph-id=$graph_id >> /tmp/knife-ssh.cacti
        fi
        cat /tmp/knife-ssh.cacti
        rm /tmp/knife-ssh.cacti'
    done

### Viewing Graphs

Graphs can be viewed on the top "graphs" tab. Useful features include

-   the "Half hour" preset, which shows only the last half-hour rather
    than the last day
-   the search box, which matches on graph name
-   the thumbnail view checkbox, which gets you many more graphs on
    screen
-   the auto-refresh interval, configured on the settings panel
-   CSV export, achievable via the icon on the right of the graph.
