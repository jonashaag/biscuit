**b**\iscuit **i**\s a **s**\tupid **c**\ontin\ **u**\ous **i**\n\ **t**\egration server for GitHub

Requirements
------------
* Nano_, my WSGI nano framework

Setup
-----
Create config file that contain the following attributes:

``PROJECT_NAME``
   Name of the project to continuously integrate
``EMAIL_SENDER_HOST``
   SMTP host to send reports from
``EMAIL_SENDER_EMAIL``
   SMTP user name (email address)
``EMAIL_RECEIVER``
   Report mail receiver address
``run``
   A function, called without arguments, that does the buildout/testing stuff.
   Returns nothing on build/test success and a string containing an error
   description on failure.
``HTTP_HOST`` and ``HTTP_PORT`` (optional, defaults to "0.0.0.0" and 8080)
   Where should the server listen?


Repo Setup
----------
Add a post-commit hook for ``HTTP_HOST:HTTP_PORT/postcommithook/``

.. _Nano: https://github.com/jonashaag/Nano
