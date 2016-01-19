These instructions detail how to enable the stock Android SIP client.
These instruction are tested in a Samsung Galaxy Nexus running 4.2.2. For
details on how to enable the SIP client on a Nexus 6 running 5.1.1 see below.
If you get them working on another device, please add to the list below.
Equally, if they do not work, please add your device to the unsupported
list.

### Instructions

1.  Ensure that you have a data connection (either through 3G or WiFi).
2.  Launch your standard dialer (often called Phone or Dialer).
3.  Bring up the menu. Depending on your phone, this may be via a
    physical Menu button, or via an icon (often in the bottom right,
    consisting of three square dots in a vertical line).
4.  From the menu, select **Settings** or **Call settings** to bring up
    the settings panel.
5.  Under **Internet Call Settings**, select **Accounts**
6.  Press **Add account** (at the bottom of the screen) and enter its
    configuration.
    -   Set **Username**, **Password** and **Server** to their usual
        values
    -   Open the **Optional settings** panel to see and set the
        following options.
    -   Set **Transport type** to TCP
    -   Set **Authentication username** to
        "sip:*&lt;username\>*@*&lt;server\>*", substituting (note: once we
        switch to storing user digest by private id, this will change)

7.  Once done, choose **Save**
8.  Go back to the main Settings menu and under **Internet Call
    Settings**, select **Use Internet Calling**. Set this to **Ask for each call**
9.  You should now be able to make calls.

#### Additional config

-   To enable incoming calls select **Receive Incoming Calls** under
    **Internet Call Settings -\> Accounts**. (Warning, this
    significantly reduces your battery life)

#### Adding a SIP contact to your phone book

-   Navigate to the **People** App. Select **+** in the top right to
    add a new contact to the phone book.
-   Under **Add more information** select **Add another field**.
    In this menu choose **Internet call** and type your contacts
    SIP address.
    

##### Making a call

-   Make a call from the standard dialler to another Clearwater line,
    e.g. 6505551234 and hit the Call button.
-   You will be prompted whether to use internet calling. Select
    internet calling and your call should connect

### Known supported devices

-   Samsung Galaxy Nexus - 4.2.2
-   Orange San Francisco II - 2.3.5
-   HTC One M9 - 5.1
-   Samsung Galaxy S4 - 4.3

These instructions detail how to enable the stock Android SIP client
for a Nexus 6 running 5.1.1.

### Instructions

1. Ensure that you have a data connection (either through 3G or WiFi).
2. Launch the standard dialer by pressing the phone icon.
3. Access options by pressing the three circular dots in the top right.
4. From this menu, select **Settings**.
5. From the settings menu, select **Calls**.
6. From the calls menu, select **Calling accounts**.
7. Now under **Internet Call Settings**, select **Internet calling (SIP)
   accounts**.
8. Press **Add account** (at the top right of the screen) and enter its
   configuration.
   -   Set **Username**, **Password** and **Server** to their usual
       values
   -   Open the **Optional settings** panel to see and set the
       following options.
   -   Set **Transport type** to TCP
   -   Set **Authentication username** to
       "sip:*&lt;username\>*@*&lt;server\>*", substituting (note: once we
       switch to storing user digest by private id, this will change)
   -   Some SIP clients do not have an **Authentication username** field. To
       make calls through Clearwater using these clients you will have to
       configure an external HSS to [allow one subscriber to have two private
       identities](External_HSS_Integration.md#Allowing-one-subsriber-to-have-two-private-identities).

9.  Once done, choose **Save** at the top right of the screen.
10. Go back to the Calling accounts menu and select **Use internet calling**.
    Set this to **Only for Internet Calls**.
11. You should now be able to make calls.

#### Additional config

-   To enable incoming calls select **Receive Incoming Calls** under
    **Calls -\> Calling accounts**. (Warning, this
    significantly reduces your battery life)

#### Adding a SIP contact to your phone book

-   Navigate to the **Contacts** App. Select **+** in the bottom right to
    add a new contact to the phone book.
-   Under the **Sip** field type your contacts
    SIP address.

##### Making a call

-   Make a call from the standard dialler to another Clearwater line,
    e.g. 6505551234 and hit the Call button.
-   You will be prompted whether to use internet calling. Select
    internet calling and your call should connect

### Known supported devices

-   Nexus 6 - 5.1.1

