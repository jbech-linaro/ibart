Running IBART
=============

Exports
-------

.. note:: Before starting IBART there are few **mandatory** exports that you need to do in the shell:

* ``$ export IBART_URL=http://URL-to-the-server:5000``
* ``$ export GITHUB_SECRET="The string you provided in the webhooks"``
* ``$ export GITHUB_TOKEN="my-long-hex-string"`` which you generated at the `Peronal access token`_ page.

.. _Peronal access token: https://github.com/settings/tokens

Besides that there are the following optional exports that will override what
you have specified in `configs/settings.yaml`_.

* ``$ export IBART_CORE_LOG="/my/path/to/ibart/core.log"``
* ``$ export IBART_DB_FILE="/my/location/to/ibart.db"``
* ``$ export IBART_JOBDEFS="/my/folder/with/jobdefs"``
* ``$ export IBART_LOG_DIR="/my/path/to/ibart/build-job/logs"``

Server Settings
---------------
Set up global settings in `configs/settings.yaml`_. Note that quite a few of them are not in use in this current version.

.. _configs/settings.yaml: ../configs/settings.yaml

Default job definitions
-----------------------
Write a job definition and store it in ``jobdefs/my-job.yaml``. Any name will do as long as it ends with ``.yaml``. There are a few example jobs in the subfolder `jobdefs/examples`_. That can be used either directly or as a template when writing your own. The script will ignore jobs in the examples folder, so either you have to copy the up one level or you have to symlink to them.

.. _jobdefs/examples: ../jobdefs/examples

Since IBART runs all job definition it finds in the ``jobdefs`` folder in alphabetic order it is a good practice to prefix them with a number. I.e using symlinks one could do like this:

.. code-block:: bash

    $ cd jobdefs
    $ ln -s examples/optee_qemu.yaml 01-optee-qemu.yaml
    $ ln -s examples/linux_kernel.yaml 02-linux-kernel.yaml

By doing so, IBART will first run the jobs ``01-optee-qemu.yaml`` and when that has completed it will continue with ``02-linux-kernel.yaml``. You don't have to number like this, but the running order might not be what you expect if you don't do it.

At this moment it is only possible to use job definitions at the server. In the future we will add support for reading a ``ibart.yaml`` from the Git / pull request itself.

Starting IBART
--------------
Starting IBART is as simple as:

.. code-block:: bash

    $ ./ibart.py

If everything done correctly, IBART should now be listening for build requests as well as serve HTML queries at ``http://${IBART_URL}``

How jobs are processed
----------------------
There are two ways to get jobs running. Either it comes as a webhook request from directly from GitHub or it is user request by a user to rebuild a certain job. For GitHub jobs the following happens:

* If it is a new pull request, then a new job will always be added to the queue.
* If it is an update to an existing pull request, then it will first cancel ongoing and remove pending jobs and then add the updated pull request to the queue. I.e., there can only be a single job in the queue for a given pull request when it is a build request coming from GitHub.

If it is an user initiated request (typically pressed ``restart`` or ``stop``), then following applies:

* If a request affects a job already in the queue, then it will stop and remove it, then it will (re-)add the job to the queue.
