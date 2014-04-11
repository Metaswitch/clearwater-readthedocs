These instructions detail how to enable the stock Android SIP client.
These instruction are tested in a Samaung Galay Nexus running 4.2.2. If
you get them working on another device, please add to the list below.
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
        "sip:*&lt;username\>*@*&lt;server\>*", subsituting (note: once we
        switch to storing user digest by private id, this will change)

7.  Once done, choose **Save**
8.  Go back to the main Settings menu and under **Internet Call
    Settings**, select **Use Internet Calling**. Set this to **Ask for
    each call**
9.  You should now be able to make calls.

#### Additional config

-   To enable incoming calls select **Receive Incoming Calls** under
    **Internet Call Settings -\> Accounts**. (Warning, this
    significantly reduces your battery life)

##### Making a call

-   Make a call from the standard dialler to another Clearwater line,
    e.g. 6505551234 and hit the Call button.
-   You will be prompted whether to use internet calling. Select
    internet calling and your call should connect

### Known supported devices

-   Samsung Galaxy Nexus - 4.2.2
-   Orange San Francisco II - 2.3.5