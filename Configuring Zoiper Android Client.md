These instructions detail how to configure the Zoiper Android SIP client to work against a Clearwater system.

Instructions
============

1. Download the application from the [Play Store](https://play.google.com/store/apps/details?id=com.zoiper.android.app)
2. Once installed, go to Config -> Accounts -> Add account -> SIP
3. Fill in the following details:
  - Account name: Clearwater
  - Host: the root domain of your Clearwater deployment
  - Username: your username, e.g. 6505551234
  - Password: password for this account
  - Authentication user: &lt;username\>@&lt;server\> e.g. 6505551234@my-clearwater.com
4. Hit Save
5. If your account was successfully enabled you should see a green tick notification
6. Go back to the main Config menu and select Codecs
7. Unselect everything except uLaw and aLaw.
8. Hit Save
9. You are now ready to make calls.

Known supported devices
=======================

- Galaxy S3
- Galaxy S2
- Nexus One

Known unsupported devices
=========================

- Galaxy Nexus (no media)
