# SIP OPTIONS poll support in Clearawater

Clearwater uses SIP OPTIONS polls internally for some of our health checking
functionality. These OPTIONS polls can also be used from external clients for
health checking of the Sprout process. This section gives details on how we
expect these OPTIONS messages to be formed, so that they are handled correctly
by the system. Sending OPTIONS polls through a Clearwater deployment to other
nodes or endpoints is also fully supported; these messages will be treated
similarly to any other SIP flow, subject to the same checks on subscriber
registration state etc.

## Correctly forming OPTIONS polls
The Sprout process will handle certain OPTIONS messages statelessly, without the
need to send any requests off to subscriber state stores; the decision of when
to do this is based on the URI they are sent to (detail on this below). This is
for use by health checking and monitoring tools, so that they do not need to
act as a full SIP endpoint and register with the system. Sprout will handle an
OPTIONS message in this way if:

-   the req_uri is classified as 'node local'
-   the message contains either
    -   no route headers
    -   a single route header, also classified as 'node local'

So, to poll Sprout with a SIP OPTIONS message, you simply need to make sure you
are in line with the two points above. We are already using this for our Monit
based health checking. An example of these poll messages looks like:

```
OPTIONS sip:poll-sip@10.0.10.1:5054 SIP/2.0
Via: SIP/2.0/TCP 10.0.10.1;rport;branch=z9hG4bK-1234
Max-Forwards: 2
To: <sip:poll-sip@10.0.10.1:5054>
From: poll-sip <sip:poll-sip@10.0.10.1>;tag=1234
Call-ID: poll-sip-1234
CSeq: 1234 OPTIONS
Contact: <sip:10.0.10.1>
Accept: application/sdp
Content-Length: 0
User-Agent: poll-sip
```

Which should get a 200 OK response:

```
SIP/2.0 200 OK
Via: SIP/2.0/TCP 10.0.10.1;rport=56141;received=10.0.10.1;branch=z9hG4bK-1234
Call-ID: poll-sip-1234
From: "poll-sip" <sip:poll-sip@10.0.10.1>;tag=1234
To: <sip:poll-sip@10.0.10.1>;tag=z9hG4bK-1234
CSeq: 1234 OPTIONS
Content-Length:  0
```

### Node local URIs
To determine if a URI is 'node local' Sprout compares it to the list of
identities we associate with the node when creating the stack at start of day.
To see what your Sprout process considers it's local identities to be, you can
check the beginning of your sprout logs, under the log line `Local host
aliases:`. As an example, on an EC2 based Sprout node, you will see something
like the following:

```
07-11-2017 12:25:57.539 UTC [7f5a1ed73780] Status stack.cpp:836: Local host aliases:
07-11-2017 12:25:57.539 UTC [7f5a1ed73780] Status stack.cpp:843:  10.0.10.1
07-11-2017 12:25:57.539 UTC [7f5a1ed73780] Status stack.cpp:843:  scscf.sprout.example.com
07-11-2017 12:25:57.539 UTC [7f5a1ed73780] Status stack.cpp:843:  10.0.10.1
07-11-2017 12:25:57.539 UTC [7f5a1ed73780] Status stack.cpp:843:  ec2-52-207-234-0.compute-1.amazonaws.com
07-11-2017 12:25:57.539 UTC [7f5a1ed73780] Status stack.cpp:843:  mmtel.sprout.example.com
07-11-2017 12:25:57.539 UTC [7f5a1ed73780] Status stack.cpp:843:  cdiv.sprout.example.com
07-11-2017 12:25:57.539 UTC [7f5a1ed73780] Status stack.cpp:843:  memento.sprout.example.com
07-11-2017 12:25:57.539 UTC [7f5a1ed73780] Status stack.cpp:843:  gemini.sprout.example.com
07-11-2017 12:25:57.539 UTC [7f5a1ed73780] Status stack.cpp:843:  icscf.sprout.example.com
07-11-2017 12:25:57.539 UTC [7f5a1ed73780] Status stack.cpp:843:  bgcf.sprout.example.com
07-11-2017 12:25:57.539 UTC [7f5a1ed73780] Status stack.cpp:843:  scscf.sprout.example.com
07-11-2017 12:25:57.539 UTC [7f5a1ed73780] Status stack.cpp:843:  52.207.234.0
07-11-2017 12:25:57.539 UTC [7f5a1ed73780] Status stack.cpp:843:  sprout.example.com
```

The source code for classifying URIs can be found [here.](https://github.com/Metaswitch/sprout/blob/dev/src/uri_classifier.cpp)
