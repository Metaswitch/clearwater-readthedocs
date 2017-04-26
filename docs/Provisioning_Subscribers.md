# Provisioning Subscribers

Clearwater provides the Ellis web UI for easy provisioning of subscribers.  However, sometimes a more programmatic interface is desirable.

Homestead-Prov provides a [provisioning API](https://github.com/Metaswitch/crest/blob/dev/docs/homestead_prov_api.md) but, for convenience, Clearwater also provides some command-line provisioning tools.

By default, the tools are installed on the Dime nodes only (as part of the clearwater-prov-tools package), in the `/usr/share/clearwater/bin` directory.

There are 5 tools.

*   `cw-create_user` - for creating users
*   `cw-update_user` - for updating users' passwords
*   `cw-delete_user` - for deleting users
*   `cw-display_user` - for displaying users' details
*   `cw-list_users` - for listing users

## Creating users

New users can be created with the `cw-create_user` tool.  As well as creating single users, it's also possible to create multiple users with a single command.  Note that this is not recommended for provisioning large numbers of users - for that, [bulk provisioning](https://github.com/Metaswitch/crest/blob/dev/docs/Bulk-Provisioning%20Numbers.md) is much quicker.

```
usage: create_user.py [-h] [-k] [--hsprov IP:PORT] [--plaintext]
                      [--ifc iFC-FILE] [--prefix TWIN_PREFIX]
                      <directory-number>[..<directory-number>] <domain>
                      <password>

Create user

positional arguments:
  <directory-number>[..<directory-number>]
  <domain>
  <password>

optional arguments:
  -h, --help            show this help message and exit
  -k, --keep-going      keep going on errors
  --hsprov IP:PORT      IP address and port of homestead-prov
  --plaintext           store password in plaintext
  --ifc iFC-FILE        XML file containing the iFC
  --prefix TWIN_PREFIX  twin-prefix (default: 123)
```

## Update users

Existing users' passwords can be updated with the `cw-update_user` tool.

```
usage: update_user.py [-h] [-k] [-q] [--hsprov IP:PORT] [--plaintext]
                      <directory-number>[..<directory-number>] <domain>
                      <password>

Update user

positional arguments:
  <directory-number>[..<directory-number>]
  <domain>
  <password>

optional arguments:
  -h, --help            show this help message and exit
  -k, --keep-going      keep going on errors
  -q, --quiet           don't display the user
  --hsprov IP:PORT      IP address and port of homestead-prov
  --plaintext           store password in plaintext
```

## Delete users

Users can be deleted with the `cw-delete_user` tool.

```
usage: delete_user.py [-h] [-f] [-q] [--hsprov IP:PORT]
                      <directory-number>[..<directory-number>] <domain>

Delete user

positional arguments:
  <directory-number>[..<directory-number>]
  <domain>

optional arguments:
  -h, --help            show this help message and exit
  -f, --force           proceed with delete in the face of errors
  -q, --quiet           silence 'forced' error messages
  --hsprov IP:PORT      IP address and port of homestead-prov
```

## Display users

Users' details can be displayed with the `cw-display_user` tool.

```
usage: display_user.py [-h] [-k] [-q] [-s] [--hsprov IP:PORT]
                       <directory-number>[..<directory-number>] <domain>

Display user

positional arguments:
  <directory-number>[..<directory-number>]
  <domain>

optional arguments:
  -h, --help            show this help message and exit
  -k, --keep-going      keep going on errors
  -q, --quiet           suppress errors when ignoring them
  -s, --short           less verbose display
  --hsprov IP:PORT      IP address and port of homestead-prov
```

## List users

All the users provisioned on the system can be listed with the `cw-list_users` tool.

Note that the `--full` parameter defaults to off because it greatly decreases the performance of the tool (by more than an order of magnitude).

The `--pace` parameter's default values should ensure that this does not use more than 10% of the Dime cluster's CPU - that is 5 users per second if `--force` is set and 500 if not.  If you set the "--pace" parameter to more than the default, you'll be prompted to confirm (or specify the `--force` parameter).

```
usage: list_users.py [-h] [-k] [--hsprov IP:PORT] [--full] [--pace PACE] [-f]

List users

optional arguments:
  -h, --help        show this help message and exit
  -k, --keep-going  keep going on errors
  --hsprov IP:PORT  IP address and port of homestead-prov
  --full            displays full information for each user
  --pace PACE       sets the target number of users to list per second
  -f, --force       forces specified pace
```
