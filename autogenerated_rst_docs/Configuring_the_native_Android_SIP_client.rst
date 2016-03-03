Using the Android SIP Client with Clearwater
============================================

These instructions detail how to enable the stock Android SIP client.
The instructions vary depending on your handset and Android model, in
particular the Nexus 6 running 5.1.1 has different menus to the other
known `supported
devices <Configuring_the_native_Android_SIP_client.md#known-supported-devices>`__
listed. If you get them working on another device, please add to the
list. Equally, if they do not work, please add your device to the
unsupported list.

Instructions
~~~~~~~~~~~~

1. Ensure that you have a data connection (either through 3G or WiFi).
2. Launch your standard dialer (often called Phone or Dialer).
3. Bring up the menu. Depending on your phone, this may be via a
   physical Menu button, or via an icon (consisting of three dots in a
   vertical line in either the top right or bottom right).
4. From the menu, navigate to the internet calling accounts menu.

   -  On many devices this is located in **Settings** (or **Call
      Settings**) > **Internet Call Settings** > **Accounts**.
   -  On the Nexus 6 running 5.1.1 this is located in **Settings** >
      **Calls** > **Calling accounts** > **Internet Call Settings** >
      **Internet calling (SIP) accounts**.

5. Press **Add account** and enter its configuration.

   -  Set **Username**, **Password** and **Server** to their usual
      values.
   -  Open the **Optional settings** panel to see and set the following
      options.
   -  Set **Transport type** to TCP.
   -  Set **Authentication username** to
      "sip:*<username>*\ @\ *<server>*", substituting (note: once we
      switch to storing user digest by private id, this will change)
   -  Some SIP clients do not have an **Authentication username** field.
      To make calls through Clearwater using these clients you will have
      to configure an external HSS to `allow one subscriber to have two
      private
      identities <External_HSS_Integration.md#allowing-one-subscriber-to-have-two-private-identities>`__.
      This will allow the subscriber to have one private identity of the
      form **``1234@example.com``** (the IMS standard form), and one
      private identity **``1234``** (which the phone will default to in
      the absence of a Authentication username).

6. Once done, choose **Save**.
7. Enable making internet calls.

   -  On many devices this is located in the **Call** menu (which can be
      accessed from the dialler by selecting **Settings** as above).
      Once here under **Internet Call Settings** select **Use Internet
      Calling** and set this to **Ask for each call**.
   -  On a Nexus 6 running 5.1.1 this is located in the **Calling
      accounts** menu. From here select **Use internet calling** and set
      this to **Only for Internet Calls**.

8. Enable receiving internet calls (note this significantly reduces your
   battery life).

   -  On many devices this is located in **Settings** > **Internet Call
      Settings** > **Accounts** once here select **Receive Incoming
      Calls**.
   -  On the Nexus 6 running 5.1.1 this is located in **Settings** >
      **Calls** > **Calling accounts** once here select **Receive
      Incoming Calls**.

Adding a SIP contact to your phone book
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  For many devices:

   -  navigate to the **People** App. Select **+** in the top right to
      add a new contact to the phone book.
   -  Under **Add more information** select **Add another field**. In
      this menu choose **Internet call** and enter your contact's SIP
      address.

-  For the Nexus 6 running 5.1.1:

   -  navigate to the **Contacts** App. Select **+** in the bottom right
      to add a new contact to the phone book.
   -  Under the **Sip** field enter your contact's SIP address.

Making a call
'''''''''''''

-  Make a call from the standard dialler to another Clearwater line,
   e.g. 6505551234 and hit the Call button.
-  You will be prompted whether to use internet calling. Select internet
   calling and your call should connect.

Known supported devices
~~~~~~~~~~~~~~~~~~~~~~~

-  Samsung Galaxy Nexus - 4.2.2
-  Orange San Francisco II - 2.3.5
-  HTC One M9 - 5.1
-  Samsung Galaxy S4 - 4.3
-  Nexus 6 - 5.1.1

