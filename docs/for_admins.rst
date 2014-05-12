################################
Admin Documentation for Twenty47
################################

Contents:

.. toctree::
   :maxdepth: 2

Purpose
=======
Twenty47 allows simple input of basic dispatch information. This data
is then pushed to email or SMS subscribers. The protected Admin section
provides access to user and subscriber administrative forms.

The Admin Section
=================
Click the Admin menu item to be taken directly to the Users List. Click
the lower Admin button to access Dropdown Box Content List.

**The Users List**

+-------------------------------------------+
| .. image:: _static/admin_users_list.png   |
|   :alt: The Users List                    |
+-------------------------------------------+

**The Dropdown Box Content List**

+-------------------------------------------+
| .. image:: _static/admin_others_list.png  |
|   :alt: The Dropdown Box Content List     |
+-------------------------------------------+

   
Users
==============
Most of your administrative tasks may be completed directly on Users List.
From here:

* Users may be activated and deactivated.
* User subscriptions may be approved or denied
* Users may be deleted
* Users may be selected for editing

Roles
-----
Users must be assigned roles, mostly, this is done via the emailed links.
If you wish to change roles for a user, click edit for that user. On the
Edit User form, you may select multiple roles for that user.

* **Admin** - the only role with access to the Admin UI
* **Manager** - role which receives emailed notifications of new users
* **SubMan** - role which receives emailed notification of pending subscriptions
* **User** - the only role with access to the Dispatch form
* **Registered** - role which can log in and manage their own subscriptions

The roles of User and Registered may be automatically applied using emailed
links. The roles of Admin, Manager, and SubMan must be applied by an
Admin via the Admin UI.

The Dropdown Box Content List
=============================
The items on this list are used to fill the dropdown boxes on the
Dispatch Form. The dropdown boxes may be edited and added to as needed
and the forms will automatically be updated to your new values.

Triggers
========
A trigger is an action taken by a user that triggers a separate action
by Twenty47. There are many triggers, two of which are important for
administration.

======================  ============================    ====================
 Trigger                 Twenty47 Action                 Response via link
======================  ============================    ====================
User confirmed          Send email to Managers          * Set as User
                                                        * Set as Registered
                                                        * Deactivate
Subscription requested  Send email to SubMans           * Approve
                                                        * Deny
======================  ============================    ====================

The administrative triggers will send emails which include action links.
The action links may be clicked on to complete that action. No login or
additional thought is needed.

Users
=====
Administrative tasks on Users are intened to be minimal. Most Users should
be self-sufficient once receiving their initial roles. User are able to
complete the following without Admin assistance:

* Register for an account
* Confirm their registration
* Change their password
* Reset a lost password
* Manage their subscriptions

Admins are needed to:

* Assign roles
* Activate or deactivate User accounts
* Approve or deny subscription requests
* Change a User's email address

User Accounts
--------------
Once an account is confirmed, it is automatically activated. This permits
the User to immediately make a subscription request. An activated user
does not have permissions to create a Dispatch. The account confirmation
triggers an email to Managers for further action. The Manager may click
a link to give the account the role of User. Those with the role of User,
may create a Dispatch.

All accounts which are active may login to the system. In order to prevent
an account from logging in, Deactivate that account. Deactivation may
also be performed via emailed link.

Subscription Requests
---------------------
Administrative control over subscriptions is done entirely from the
Users List. There are four buttons which indicate the current subscription
status and allow you to select a different status. The status levels are:

None
 The User has not requested nor submitted a subscription request
 
Denied
 The User has requested a subscription and it has been denied. No futher
 subscription requests may be made by the User.
 
Pending
 The User has requested a subsciption and that request is awaiting
 administrative action. That action my be completed via emailed link of
 via the Users List.
 
Approve
 The User's request for a subscription has been approved. Additional
 requests from the User or changes submitted by that User are considered
 approved.
   





Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

