Installation Process
====================

Prerequisites
--------------------------

Ubuntu / Debian
~~~~~~~~~~~~~~~
Install the necessary packages using apt-get.

.. code-block:: bash

    $ sudo apt update
    $ sudo apt install git python3 python3-flask python3-pexpect python3-yaml python3-requests

Arch Linux
~~~~~~~~~~
Install the necessary packages using pacman.

.. code-block:: bash

    $ sudo pacman -Syy
    $ sudo pacman -S git python3 python-flask python-pexpect python-yaml python-requests

pip based
~~~~~~~~~
If you prefer working with pip based install instead of the above, then you should install

.. code-block:: bash

    $ pip install --user pexpect pyyaml flask requests google-oauth2 \
                         google-api-python-client google-auth \
                         google-auth-oauthlib google-auth-httplib2

For Ubuntu and Debian based system you also need the pip package

.. code-block:: bash

    $ sudo apt install git python3 python3-pip

Likewise for Arch Linux

.. code-block:: bash

    $ sudo pacman -S git python3 python-pip

GitHub
------

Webhooks
~~~~~~~~
First one needs to setup webhooks_ at GitHub. Important things to configure here
is the ``Payload URL``, which should point to the server running IBART. The
listening port is by default ``5000``. For ``Content type`` one should select
``application/json``. The secret on the GitHub webhooks page is a string that
you need to export in your shell before starting IBART (see "Running
IBART/Exports"). At the section ``Which events would you like to trigger this
webhook?`` it is sufficient to select ``Pull requests``.

.. _webhooks: https://developer.github.com/webhooks/creating

Personal access token
~~~~~~~~~~~~~~~~~~~~~
You need to generate a personal access token for your GitHub account. Note that
this is not something unique for an individual git. You can generate the token
at the `Peronal access token`_ page.

.. _Peronal access token: https://github.com/settings/tokens


Google cloud console
--------------------
This is a necessary step to be able to support authentication via Google login.

Create the app
~~~~~~~~~~~~~~
First you need to create a web-application at the `Google cloud console`_. 

.. _Google cloud console: https://console.cloud.google.com/

OAuth consent screen
~~~~~~~~~~~~~~~~~~~~
Next step is fill in the `OAuth consent screen`_. There you have to fill in the
authorized domains and some support emails etc.

.. _OAuth consent screen: https://console.cloud.google.com/apis/credentials/consent

Create OAuth credentials
~~~~~~~~~~~~~~~~~~~~~~~~
Last step is to create the OAuth credentials. Go to
https://console.cloud.google.com/apis/credentials and press + `CREATE
CREDENTIALS`, select `OAuth client ID`. For `Application type`, select `Web
application` and give it a (any) name. 

You need to add `Authorised JavaScript origins`, which typically is this for
development https://localhost:5000 and for real domain it is something like
https://mydomain.com:5000.

You also need to add `Authorised redirect URIs`, which is a list of URL that
Google are willing to redirect you to after your Google identity has been
authenticated. IBART needs the `callback` page to be enabled, i.e. for local
development, this: https://localhost:5000/callback and for real use, something
like this: https://mydomain.com:5000/callback.

Once completed, press save and you should find your new Oauth2 credential under
OAuth 2.0 Client IDs. On the right side, press the arrow to download this
credential. Save the file for now (there are "download" links/buttons to get the
`json` file), we will use it later on (rename the file to `client_secret.json`).

Clone IBART
-----------
Obviously one need to clone IBART also, it doesn't matter where it is placed.

.. code-block:: bash

    $ git clone https://github.com/jbech-linaro/ibart.git
