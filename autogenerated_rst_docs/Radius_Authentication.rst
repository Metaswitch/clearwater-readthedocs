Radius Authentication
=====================

It is possible to authenticate users for SSH/SFTP access by using the
RADIUS authentication protocol to contact a third party RADIUS
authentication server. The following will explain how to install and
configure this capability on a Clearwater node, and how to go about
using it.

The authentication process
--------------------------

On attempting to access a node via SSH or SFTP, a user is either
expected to use a key, or to provide a password to verify their
identity, and thus pass through authentication successfully. This
process requires a locally provisioned set of authentication details for
each user that the sshd process can compare to the provided credentials
for verification. In the case of password authentication, by enabling
RADIUS all user accounts can be configured centrally on a RADIUS server,
or in a database said server can access, and each node can pass user
credentials provided at log in across to this server to complete the
authentication process.

As the user attempting access may not exist locally on the node, which
sshd requires, any unknown user is mapped to the default Ubuntu user to
allow authentication to proceed correctly. As such, once authenticated,
they will be acting as if they were the default user, but for auditing
purposes it is the username provided at login that is recorded.

Prerequisites
-------------

The following conditions are assumed by this process:

-  Your nodes are running on Ubuntu 14.04.
-  Your nodes have access to both Clearwater and Ubuntu repositories.
-  Your SSH configuration allows password authentication and PAM (the
   correct configuration will be detailed below).
-  You have access to a third-party RADIUS server (such as freeRADIUS).
-  Your firewall allows UDP traffic to the above server on port 1812.

Installation
------------

Package installation
~~~~~~~~~~~~~~~~~~~~

Install the Clearwater RADIUS authentication package:

::

    sudo apt-get install clearwater-radius-auth

Configuration
~~~~~~~~~~~~~

The details of your RADIUS server will need to be entered into
``/etc/pam_radius_auth.conf``. This file provides an example of how
entries should be structured: \* Multiple entries are allowed, but each
must be on a new line. \* Each line consists of three fields: \*
``server[:port]`` (The default is port 1812. All traffic will be UDP) \*
``secret`` \* ``[timeout]`` (Default timeout is 3 seconds) \* The secret
is shared between each client and the server to allow simple encryption
of passwords. The secret must match the entry for the client in the
RADIUS server configuration. \* Both the port and timeout entries are
optional.

Your sshd configuration must allow password authentication, and use of
PAM. If you are unsure, check that the ``PasswordAuthentication`` and
``UsePAM`` entries in ``/etc/ssh/sshd_config`` are set to ``yes``. Any
changes to ssh configuration will require the ssh process to be
restarted before coming into effect.

You must ensure that your firewall/security groups allow UDP traffic to
the RADIUS server on port 1812.

Usage
-----

Once the above is installed and configured, any user provisioned in the
RADIUS server can attempt SSH or SFTP access to the configured node, and
on providing their password they will be authenticated against the
details held on the RADIUS server, and logged in, acting as the default
Ubuntu user. Commands such as ``who`` or ``last`` will output the
username supplied at login, and this will also be recorded in the auth
log ``/var/log/auth.log``.

Any users provisioned locally on the node will see no change to their
authentication experience. By default, RADIUS authentication is set to
be a sufficient, but not required condition. As such, failing to
authenticate against the server credentials will cause the
authentication attempt to fall back to checking locally provisioned
details. See below for further details on configuration options.

Troubleshooting
---------------

-  If you are not seeing any traffic reaching your RADIUS server, and
   entries in ``/var/log/auth.log`` state that no RADIUS server was
   reachable, re-check the RADIUS server entry in
   ``/etc/pam_radius_auth.conf``, and ensure that your firewall is
   configured to allow UDP traffic to the RADIUS server on port 1812.
-  If your RADIUS server is rejecting authentication requests, ensure
   that the server is configured correctly.

Removal
-------

To properly remove clearwater-radius-auth, and the components it brings
with it, run the following:

::

    sudo apt-get purge clearwater-radius-auth
    sudo apt-get purge libpam-radius-auth
    sudo apt-get purge libnss-ato

This will remove all configuration put in place by the installation.
Should your configuration become corrupt, purging and re-installing the
associated module will re-instate the correct configuration.

Further configuration
---------------------

This section details the configuration put in place by the installation.
It is highly recommended that these be left as their defaults. The
following is for information purposes only.

libnss-ato.conf
~~~~~~~~~~~~~~~

The libnss-ato configuration file is found at ``/etc/libnss-ato.conf``,
and will look like the following:

::

    ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash

It holds the information of the default user to which unknown users are
mapped. By default this maps to the Ubuntu user.

Only the first line of this file is parsed. The user entry is the same
format as is found in ``/etc/passwd``. Replacing this file with a
different user entry will map unknown users to the entry provided.

pam.d/sshd
~~~~~~~~~~

The PAM configuration file for the sshd process is found at
``/etc/pam.d/sshd``. As part of the installation, the 3 lines around
``auth sufficient pam_radius_auth.so`` are added at the top of the file,
configuring PAM to attempt RADIUS authentication before other methods.
It will look like the following:

::

    # PAM configuration for the Secure Shell service
    # +clearwater-radius-auth
    auth sufficient pam_radius_auth.so
    # -clearwater-radius-auth
    # Standard Un*x authentication.

It is strongly recommended that users do not modify this entry. Further
information on this configuration can be found at
`FreeRADIUS <http://freeradius.org/pam_radius_auth/>`__.

nsswitch.conf
~~~~~~~~~~~~~

The NSS configuration file is found at ``/etc/nsswitch.conf``. After
installation, the top three entries in this file will look as follows:

::

    passwd:   compat ato
    group:    compat
    shadow:   compat ato

Modifications to the NSS configuration make it check the libnss-ato
component for a user mapping if no local user is found. The addition of
``ato`` at the end of both the ``passwd`` and ``shadow`` entries
provides this function. Removal of these addition will disable the user
mapping, and break RADIUS authentication.
