################################
For Administrators
################################

Twenty47 allows simple input of basic dispatch information. This data
is then pushed to email or SMS subscribers. The protected Admin section
provides access to user and subscriber administrative forms.

The Admin Section
=================
Click the Admin menu item to be taken directly to the Users List.

**The Users List**

+-------------------------------------------+
| .. image:: _static/admin_users_list.png   |
|   :alt: The Users List                    |
+-------------------------------------------+
 
Users
==============
Administrative tasks on users are intended to be minimal. Most users should
be self-sufficient once receiving their initial roles. Users are able to
complete the following without Admin assistance:

* Register for an account
* Confirm their registration
* Change their password
* Reset a lost password
* Manage their subscriptions

Admins are needed to:

* Assign roles
* Activate or deactivate user accounts
* Approve or deny subscription requests
* Change a user's email address

From the Users List, an Admin may:

* Activate and deactivate users
* Act upon user subscription requests
* Delete a user
* Select a user for editing

Roles
-----
Users must be assigned roles, mostly, this is done via the emailed links.
If you wish to change roles for a user, click Edit for that user. On the
Edit User form, you may select multiple roles for that user.

Admin
 The only role with access to the Admin UI
 
Manager
 Role which receives emailed notifications of new users
 
SubMan
 Role which receives emailed notifications of pending subscriptions

Dispatch
 The only role with access to the Dispatch form

Registered
 Role which can log in and manage their own subscriptions

The roles of Dispatch and Registered may be automatically applied using
emailed links. The roles of Admin, Manager, and SubMan must be applied by
an Admin via the Admin UI.

User Accounts
--------------
Once an account is confirmed, it is automatically activated. This permits
the user to immediately make a subscription request. An activated user
does not have permissions to create a Dispatch. The account confirmation
triggers an email to Managers for further action. The Manager may click
a link to give the account the role of Dispatch. Those with the role of
Dispatch, may create a Dispatch.

All accounts which are active may login to the system. In order to prevent
an account from logging in, deactivate that account. Deactivation may
also be performed via emailed link.

Subscription Requests
---------------------
Administrative control over subscriptions is done from the Users List or
via emailed links. There are four buttons which indicate the current
subscription status and allow you to select a different status. The
status levels are:

None
 The User has not requested nor submitted a subscription request.
 
Denied
 The User has requested a subscription and it has been denied. No futher
 subscription requests may be made by the User.
 
Pending
 The user has requested a subsciption and that request is awaiting
 administrative action. That action may be completed via emailed link or
 via the Users List.
 
Approved
 The user's request for a subscription has been approved. Additional
 requests from the user or changes submitted by that user are considered
 approved.

The Dropdown Box Content List
=============================
Click the lower Admin button to access Dropdown Box Content List.

The items on this list are used to fill the dropdown boxes on the
Dispatch Form. The dropdown boxes may be edited and added to as needed
and the forms will automatically be updated to your new values.

**The Dropdown Box Content List**

+-------------------------------------------+
| .. image:: _static/admin_others_list.png  |
|   :alt: The Dropdown Box Content List     |
+-------------------------------------------+

Triggers
========
A trigger is an action taken by a user that triggers a separate action
by Twenty47. There are many triggers, two of which are important for
administration.

======================  =========================   ====================
 Trigger                 Twenty47 Action              Response via link
======================  =========================   ====================
User confirmed          Send email to Managers      Set as Dispatch

                                                    Set as Registered
                                                    
                                                    Deactivate
                                                    
Subscription requested  Send email to SubMans       Approve

                                                    Deny
======================  =========================   ====================

The administrative triggers will send emails which include action links.
The action links may be clicked on to complete that action without
requiring a login.

   





Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

