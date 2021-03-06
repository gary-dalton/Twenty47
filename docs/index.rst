.. Twenty47 documentation master file, created by
   sphinx-quickstart on Fri May  9 16:48:24 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Twenty47's documentation!
====================================

Contents:

.. toctree::
   :maxdepth: 2
   
   for_users
   for_admins
   installation

Introduction
=============
Twenty47 is a small webapp to manage and provide notifications via 
Amazon Web Services (AWS) Simple Notification Service (SNS) for 
American Red Cross dispatches.

This documentation is divided into 3 main categories. This should make
it easier to only find the information needed for your level of use.
Documentation exists specifically for:

* Users, :doc:`for_users`
* Admins, :doc:`for_admins`
* Installation, :doc:`installation`

Requirements
============
The main requirements are:

* Web server
* Python
* Flask
* Flask-Security
* Mongdb
* Flask-Mongoengine
* py-boto
* Amazon Web Services


Installation
============
Once the requirements are met, the Twenty47 application may be installed
on the server. See installation for more details, :doc:`installation`.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
