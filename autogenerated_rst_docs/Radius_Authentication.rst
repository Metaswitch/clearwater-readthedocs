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
expected to use a key, or provide a password to verify their identity.
This process requires a locally provisioned set of authentication
details for each user that the sshd process compares to the provided
credentials for verification. For password based authentication,
enabling RADIUS means that all user accounts can be configured centrally
on a RADIUS server (or in a database the RADIUS server can access). Each
node can then pass on the user credentials provided to this server to
complete the authentication process.

Sshd requires that the user attempting to access a node must exist
locally. To allow the authentication process to complete correctly, any
locally unknown user is mapped to a single configurable user (usually
the system default user). As such, all RADIUS authenticated users will
be acting as this user on the local node. For auditing purposes however,
the username provided at login is recorded (e.g. in
``/var/log/auth.log``, and the output of commands like ``who``).

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

libnss-ato configuration
^^^^^^^^^^^^^^^^^^^^^^^^

You need to create configuration for the all-to-one module,
`libnss-ato <https://github.com/Metaswitch/libnss-ato>`__, which is used
to map your RADIUS authenticated users onto a locally provisioned user.
A template of this configuration is provided in
``/etc/libnss-ato.conf.TEMPLATE``. You will need to create the file
``/etc/libnss-ato.conf``, and provide an entry in the same format as in
the template file. For most users, the template can be copied directly,
simply running
``sudo cp /etc/libnss-ato.conf.TEMPLATE /etc/libnss-ato.conf``; this
will map locally unknown users to the default linux user (UID 1000). If
you wish to configure the module to use a different user, the entry
should match how the user appears in ``/etc/passwd``. Only a single user
mapping is configurable, and so only the first line of the configuration
file is parsed.

RADIUS server configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The details of your RADIUS server will need to be entered into
``/etc/pam_radius_auth.conf``. This file provides an example of how
entries should be structured: \* Multiple entries are allowed, but each
must be on a new line. \* Each line consists of three fields:

::

        server[:port] (The default is port 1812. All traffic will be UDP)
        secret
        [timeout] (Default timeout is 3 seconds)

-  The secret is shared between each client and the server to allow
   simple encryption of passwords. The secret must match the entry for
   the client in the RADIUS server configuration.
-  Both the port and timeout entries are optional. We recommend a
   relatively small timeout value (e.g. 3 seconds), as in the case that
   your RADIUS server becomes uncontactable users will have to wait the
   full duration of all configured timeouts before falling back to local
   password based authentication. Authentication by SSH-key does not
   enter this authentication path, and so timeout values will not impact
   SSH-key based access.

Sshd configuration
^^^^^^^^^^^^^^^^^^

Your sshd configuration must allow password authentication, and use of
PAM. If you are unsure, check that the ``PasswordAuthentication`` and
``UsePAM`` entries in ``/etc/ssh/sshd_config`` are set to ``yes``. Any
changes to ssh configuration will require the ssh process to be
restarted before coming into effect.

You must ensure that your firewall/security groups allow UDP traffic to
the RADIUS server on port 1812.

Usage
-----

Once the above is installed and configured, you will need to enable the
RADIUS authentication process. To do this, simply run
``sudo /usr/share/clearwater-radius-auth/bin/enable-radius-authentication``.
Once enabled, any user provisioned in the RADIUS server can attempt SSH
or SFTP access to the configured node, and on providing their password
they will be authenticated against the details held on the RADIUS
server, and logged in, acting as the node default user. Commands such as
``who`` or ``last`` will output the username supplied at login, and this
will also be recorded in the auth log ``/var/log/auth.log``.

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

If you simply want to disable RADIUS authentication on a node, run
``sudo /usr/share/clearwater-radius-auth/bin/disable-radius-authentication``.

To properly remove clearwater-radius-auth, and the components it brings
with it, run the following:

::

    sudo apt-get purge clearwater-radius-auth
    sudo apt-get purge libpam-radius-auth
    sudo apt-get purge libnss-ato
    sudo rm -f /etc/libnss-ato.conf

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

The libnss-ato configuration file is found at ``/etc/libnss-ato.conf``.
Users will need to manually create the file on their first installation.
The file contains an entry specifying the user identity to which unknown
users are mapped. A template of the configuration is provided at
``/etc/libnss-ato.conf.TEMPLATE``. It will look like the following:

::

    radius_authenticated_user:x:1000:1000:radius_authenticated_user:/tmp:/bin/bash

For most installations, copying the template across to create the
configuration file will be sufficient. This will map unknown users to
the default user, UID 1000.

Only the first line of this file is parsed. The user entry is the same
format as is found in ``/etc/passwd``. Replacing this file with a
different user entry will map unknown users to the entry provided.

pam.d/sshd and pam.d/login
~~~~~~~~~~~~~~~~~~~~~~~~~~

The PAM configuration file for the sshd and login processes are found at
``/etc/pam.d/sshd`` and ``/etc/pam.d/login`` respectively. As part of
the installation, the 3 lines around
``auth sufficient pam_radius_auth.so`` are added at the top of these
files, configuring PAM to attempt RADIUS authentication before other
methods. It will look like the following:

::

    # PAM configuration for the Secure Shell service
    # +clearwater-radius-auth
    auth sufficient pam_radius_auth.so
    # -clearwater-radius-auth
    # Standard Un*x authentication.

It is strongly recommended that users do not modify these entries.
Further information on this configuration can be found at
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
