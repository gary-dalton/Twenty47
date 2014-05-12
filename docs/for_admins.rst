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

The roles of User and Registered my be automatically applied using emailed
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
by Twenty47. There are three triggers, two of which are important for
administration.

======================  ============================    ====================
 Trigger                 Twenty47 Action                 Response via link
======================  ============================    ====================
Dispatch created        Send dispatch notifications     None
User confirmed          Send email to Managers          * Set as User
                                                        * Set as Registered
                                                        * Deactivate
Subscription requested  Send email to SubMans           * Approve
                                                        * Deny
======================  ============================    ====================





The Subscriber form
===================
This form is also self-explanatory. What happens after pressing "Save" 
does, however; require more explanation. Also before selecting "SMS
Phone", make certain you have a phone capable of receiving SMS text
messages and you are aware of any fees your service provider might charge.

.. image:: _static/subscriber.png
   :alt: Manage your subscription form
   

Effects of Subscriber form
--------------------------
All subscribers must be approved before they are allowed to receive
notifications. Once you submit your subscription request, a Subscription
Manager receives an email notification of your request. The Subscription
Manager must then approve your request. Once you request is approved, 
you will receive confirmation notices for your email or your SMS phone.

Email Confirmation
^^^^^^^^^^^^^^^^^^
Once a Subscription Manager approves your request, you will received an
email requiring you to confirm your request. This will come from 
**Dispatch using Email** <no-reply\@sns.amazonaws.com>. Click the included
link to complete your subscription.

.. image:: _static/email_sub_pending.png
   :alt: Emailed confirmation request

Once you have confirmed, you will be directed to a page similar to this:
   
.. image:: _static/email_sub_confirm.png
   :alt: Your email is confirmed




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

