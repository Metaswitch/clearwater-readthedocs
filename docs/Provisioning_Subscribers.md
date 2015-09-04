# Provisioning Subscribers

Clearwater provides the Ellis web UI for easy provisioning of subscribers.  However, sometimes a more programmatic interface is desirable.

Homestead provides a [provisioning API](https://github.com/Metaswitch/crest/blob/dev/docs/homestead_api.md) but, for convenience, Clearwater also provides some command-line provisioning tools.

By default, the tools are installed on the Homestead servers only (as part of the clearwater-prov-tools package), in the `/usr/share/clearwater/bin` directory.

There are 4 tools.

*   `create_user` - for creating users
*   `update_user` - for updating users' passwords
*   `delete_user` - for deleting users
*   `display_user` - for displaying users' details

## Creating users

New users can be created with the `create_user` tool.  As well as creating single users, it's also possible to create multiple users with a single command.  Note that this is not recommended for provisioning large numbers of users - for that, [bulk provisioning](https://github.com/Metaswitch/crest/blob/dev/docs/Bulk-Provisioning%20Numbers.md) is much quicker.

```
usage: create_user.py [-h] [-k] [-q] [--hsprov IP:PORT] [--plaintext]
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
  -q, --quiet           don't display the user
  --hsprov IP:PORT      IP address and port of homestead-prov
  --plaintext           store password in plaintext
  --ifc iFC-FILE        XML file containing the iFC
  --prefix TWIN_PREFIX  twin-prefix (default: 123)
```

## Update users

Existing users' passwords can be updated with the `update_user` tool.

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

Users can be deleted with the `delete_user` tool.

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

Users' details can be displayed with the `display_user` tool.

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
