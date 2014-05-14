.. Twenty47 documentation master file, created by
   sphinx-quickstart on Fri May  9 16:48:24 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Installation of Twenty47
====================================

Contents:

.. toctree::
   :maxdepth: 2
   

Introduction
=============
There are many possible ways to perform an effective installation, so please
consider this as just a working example. I will guide you through the
full provisioning of a server to creation of subscription lists and end on
initial setup and configuration of the application.

Prepare Your EC2 Server
=======================
Since Twenty47 relies on Amazon Web Services, those services will be
prominent throughout this installation guide.

Create an IAM Role
------------------
From AWS, select IAM and then Roles. Create a new role for Amazon EC2
and give it Power User access.
See `Granting Applications that Run on Amazon EC2 Instances Access to AWS Resources <http://docs.aws.amazon.com/IAM/latest/UserGuide/role-usecase-ec2app.html>`_
and `IAM Roles for Amazon EC2 <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html>`_

Launch EC2 Instance with IAM Role
---------------------------------
The IAM role you just created now needs to be associated with an EC2 instance.
This is done by launching a new AMI instance. For this guide, I am using the
Ubuntu 14.01 AMI with the ID of ami-358c955c.

Follow whatever settings you want with this. Just make certain that on the
"Configure Instance Details" tab, you select the IAM Role you just created.

Email Settings
==============
You do want to send out email. Since you already have an AWS account,
you can easily add Simple Email Services (SES). To set up SES, follow
`What Is Amazon SES? <http://docs.aws.amazon.com/ses/latest/DeveloperGuide/Welcome.html/>`_

Of course using SES is optional, what is needed is an SMTP server and the
proper credentials to send email through that server.


Meet the Requirements
=====================
Now let's make all needed software and packages available on the server.
Log into a secure shell on your server. All of the package updates require
root access so once I am logged in.

    sudo -i

Basic Packages
--------------
These are just to get us started. Later, we'll do a more complete setup
of these packages.
    
    apt-get update
    
    apt-get install apache2 libapache2-mod-wsgi python-virtualenv
    
    apt-get install git python-dev
    
MongoDB
--------
MongoDB fits the schematic of Twenty47 quite well. It does require some
intial setup. Since this was my first project using MongoDB, I have
included additional details here.

Install MongoDB
^^^^^^^^^^^^^^^
Follow the installation instructions given at
`Install MongoDB on Ubuntu <http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu//>`_
This is typically a new version of Mongodb and the commands used should
work properly.

Enable Authentication
^^^^^^^^^^^^^^^^^^^^^
Refer to `Enable Client Access Control <http://docs.mongodb.org/manual/tutorial/enable-authentication/>`_
for details or other options

Edit the /etc/mongodb.conf file to enable auth. (set auth = true)
    
    service mongodb restart
    
Next, create a userAdminAnyDatabase role

    use admin   # use the admin db
    
    db.createUser({user:"siteUserAdmin", pwd:"password", roles:[{role: "userAdminAnyDatabase", db: "admin"}]})
      
Create Twenty47 Database
^^^^^^^^^^^^^^^^^^^^^^^^
Now we create a database for Twenty47 and add an authorized user to it.
Use any names you wish for these and they will be used to configure
Twenty47.

    use admin
    
    db.auth({ user: "siteUserAdmin", pwd: "password"})
    
    use twenty47
    
    db.createUser( {user: "twenty47", pwd: "password", roles:["dbOwner"]})
    
Virtualenv
----------
I prefer to use Python virtualenv to reduce problems with versions and
dependencies. See `vitualenv <https://virtualenv.pypa.io/en/latest/virtualenv.html/>`_.

Change to the directory you wish to install Twenty47.

    mkdir -p /srv/www/twenty47

    cd /srv/www/twenty47
    
Make the virtualenv and start using it.

    vitualenv venv
    
    . venv/bin/activate
    
Now let's start installing packages into our virtualenv.

    pip install Flask flask-bcrypt flask-mongoengine flask-security
    
    pip install boto
    
Amazon SNS
-------------
Assuming you have properly started your EC2 instance with an IAM role, the
following comands will allow you to create your subscription topics.

    python
    
    from boto import sns
    
    conn = sns.SNSConnection()
    
    conn.get_all_topics()
    
If you receive any errors here, it means one or more of the following:

* The EC2 instance is not associated with an IAM role
* boto is not able to find your credentials

See `Troubleshooting Connections <http://docs.pythonboto.org/en/latest/getting_started.html#troubleshooting-connections/>`_
for more help.

Now, let's create your topics. Choose relatively short names for these,
especially for your SMS topic.

    conn.create_topic('dispatch_email')     #for email
    
    conn.create_topic('dispatch_sms)        #for SMS
    
Each of these commands should return a CreateTopicResult which looks
similar to *arn:aws:sns:us-zone-1:700000000000:del_test*. Make a note
of these strings as you will need them when we configure Twenty47.

Since SMS uses either the topic name or the topic attribute *DisplayName*
as part of the SMS message, I recommend setting a very short DisplayName.

    topic = *arn:aws:sns:us-zone-1:700000000000:del_test* (your topic string)
    
    conn.set_topic_attributes(topic, 'DisplayName', 'DSPH')
    

Git Twenty47
------------
Now lets get the Twenty47 code onto your server. Make certain you are
in the directory you wish to install to, then

    git clone 'https://github.com/gary-dalton/Twenty47.git'
    
Configuration and Initialization
================================
Only a few more steps to complete before Twenty47 is ready to handle
your dispatches.

The Config File
---------------
Open the config file, located at Twenty47/twenty47/config.py, for editing.
Here you will be able to all of the included Flask extensions that are
installed. Please see the documentation of each extension for a full list
of possible configuration settings.

Flask-Mail
    http://pythonhosted.org/flask-mail/
    
Flask-Security
    https://pythonhosted.org/Flask-Security/configuration.html
    
In the config file, a number of settings are marked *Change these*. Please
do review those and change them to match your circumstances.



Preparing Apache2
-----------------
    
    

`Flask-Mail <http://pythonhosted.org/flask-mail/>`_




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
