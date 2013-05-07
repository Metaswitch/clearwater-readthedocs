# Making calls through Clearwater

These instructions will take you through the process of making a call on a Clearwater deployment.

## Prerequisites

* You've [installed Clearwater](Installation Instructions)
* You have access to two SIP clients.  We've tested with the following:
  - [X-Lite](http://www.counterpath.com/x-lite.html)
  - [Jitsi](https://jitsi.org/)
  - [Blink](http://icanblink.com/)
  - [Stock Android SIP client](Configuring the native Android SIP client)
  - [Zoiper Android SIP client](Configuring Zoiper Android Client)
* You have access to a web-browser.  We've tested with:
  - Google Chrome

## Work out your base domain

If you installed Clearwater manually, your base DNS name will simply by `<zone>`.  If you installed using the automated install process, your base DNS name will be `<name>.<zone>`.  For the rest of these instructions, the base DNS name will be referred to as `<domain>`.

## Create a number for your client

In your browser, navigate to your Ellis node at `http://ellis.<domain>`.

Sign up as a new user, using the signup code `vby77rb7e`.

Ellis will automatically allocate you a new number and display its password to you.  Remember this password as it will only be displayed once.  From now on, we will use `<username>` to refer to the SIP username (e.g. `6505551234`) and `<password>` to refer to the password.

## Configure your client

Client configuration methods vary by client, but the following information should be sufficient to allow your client to register with Clearwater.

* SIP Username: `<username>`
* SIP Password: `<password>`
* SIP Domain: `<domain>`
* Authorization Name: `<username>@<domain>`
* Transport: `TCP`
* STUN/TURN/ICE:
 - Enabled: `true`
 - Server: `<domain>`
 - Username: `<username>@<domain>`
 - Password: `<password>`

Once these settings have been applied, your client will register with Clearwater.

## Configure a second number and client

Create a new number in Ellis, either by creating a new Ellis user, or by clicking the `Add Number` button in the Ellis UI to add one for the existing user.

Configure a second SIP client with the new number's credentials as above.

## Make the call

From one client, dial the `<username>` of the other client to make the call.  Answer the call and check you have two-way media.

## Next steps

Now that you've got a basic call working, check that all the features of your deployment are working by running the [live tests](Running the live tests) or [explore Clearwater](Exploring Clearwater) to see what else Clearwater offers.
