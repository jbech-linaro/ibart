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

    $ pip install --user pexpect pyyaml flask requests

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
First one needs to setup webhooks_ at GitHub. Important things to configure here is the ``Payload URL``, which should point to the server running IBART. The listening port is by default ``5000``. For ``Content type`` one should select ``application/json``. The secret on the GitHub webhooks page is a string that you need to export in your shell before starting IBART (see "Running IBART/Exports"). At the section ``Which events would you like to trigger this webhook?`` it is sufficient to select ``Pull requests``.

.. _webhooks: https://developer.github.com/webhooks/creating

Personal access token
~~~~~~~~~~~~~~~~~~~~~
You need to generate a personal access token for your GitHub account. Note that this is not something unique for an individual git. You can generate the token at the `Peronal access token`_ page.

.. _Peronal access token: https://github.com/settings/tokens

Clone IBART
-----------
Obviously one need to clone IBART also, it doesn't matter where it is placed.

.. code-block:: bash

    $ git clone https://github.com/jbech-linaro/ibart.git
