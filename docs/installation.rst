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

Meet the Requirements
=====================
Now let's make all needed software and packages available on the server.
Log into a secure shell on your server. All of the package updates require
root access so I
    sudo -i
once I am logged in.

Basic Packages
--------------
    apt-get install apache2
    apt-get install libapache2-mod-wsgi
    apt-get install python-virtualenv
    
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
    db.createUser( {user: "siteUserAdmin", pwd: "password",
      roles:[{role: "userAdminAnyDatabase", db: "admin"}]
      })
      
Create Twenty47 Database
^^^^^^^^^^^^^^^^^^^^^^^^
Now we create a database for Twenty47 and add an authorized user to it.
Use any names you wish for these as the initialization script will request
your information.

    use admin
    db.auth({ user: "siteUserAdmin", pwd: "password"})
    use twenty47
    db.createUser( {user: "twenty47", pwd: "password", roles:["dbOwner"]})
    
    
* Create an Admin account
* Create an Admin account
    






Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
