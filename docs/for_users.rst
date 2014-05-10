################################
User Documentation for Twenty47
################################

Contents:

.. toctree::
   :maxdepth: 2

Purpose
=======
Twenty47 allows simple input of basic dispatch information. This data
is then pushed to email or SMS subscribers. For most users, there are
2 forms available.


The Dispatch Create form
========================
The use this should be self-explanatory. Upon submission,
Dispatch Create sends a notification to all subscribers.

.. image:: _static/dispatch_create.png
   :alt: Create a new dispatch form

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
**Dispatch using Email** <no-reply@sns.amazonaws.com>. Click the included
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

