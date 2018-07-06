Job definitions - Yaml-files
============================
This is the main thing a user will work with. This is where all commands to clone, build, flash etc takes place. There are ``15`` pre-defined sections and at this moment they are the only ones that can be there. You don't have to add nor use all of them. But you cannot add more or invent your own. A full file contains the following:

.. code-block:: yaml

    pre_clone:
    clone:
    post_clone:

    pre_build:
    build:
    post_build:

    pre_flash:
    flash:
    post_flash:

    pre_boot:
    boot:
    post_boot:

    pre_test:
    test:
    post_test:

Commands
--------
Within each section one states commands, expected output and the timeout. Timeout (``timeout``) is by default ``3`` seconds if that is not stated. The expected output (``exp``) can be omitted if not needed. Most often one either writes a single command (``cmd``) or a combination with all three of them. Here is an example of how a job definition file could look like:

.. code-block:: yaml

    pre_clone:
        - cmd: mkdir -p /opt/myworking-dir
        - cmd: cd /opt/myworking-dir
        
    clone:
        - cmd: git clone https://github.com/torvalds/linux.git
          timeout: 600
    
    build:
        - cmd: make ARCH=arm defconfig
        - cmd: make -j8
          timeout: 600
          
This simple test would create a working directory, clone Linux kernel with a 600 second timeout, build it for Arm (again 600 seconds timeout). Note that one can use both this 

.. code-block:: yaml

    :emphasize-lines: 3
    build:
        - cmd: echo $?
          exp: '0'

as well as this syntax (pay attention to the added ``-`` at ``exp``. 

.. code-block:: yaml

    build:
        - cmd: echo $?
        - exp: '0'

From user point of view there is no difference. But under the hood, the later is done in two loops within the script and the first one is done in a single loop.

Exported variables
------------------
Under the hood IBART uses `pexpect`_ and for each section the job-definition file (yaml) it will spawn a new shell. This means that things are not normally carried over between sections in the job-definition file. But since it is both cumbersome and easy to forget export the same things over and over again, IBART saves every export it sees and when entering a new section it will export the same environment variables again. So, from a user perspective exports will work as expected.

.. _pexpect: http://pexpect.readthedocs.io/en/stable/index.html

Pull request variables
~~~~~~~~~~~~~~~~~~~~~~
There are a few of the pull request variables automatically exported to the
"environment" which can be used directly in the script, they are:

.. code-block:: bash

+------------------+------------------------------------------------------+---------------------------------------+
| Variable         | Meaning                                              | Example                               |
+------------------+------------------------------------------------------+---------------------------------------+
| ``PR_NUMBER``    | The current pull request number                      | 123                                   |
+------------------+------------------------------------------------------+---------------------------------------+
| ``PR_NAME``      | The name git corresponding to the current pr number  | ibart                                 |
+------------------+------------------------------------------------------+---------------------------------------+
| ``PR_FULL_NAME`` | Both the GitHub project name and the name of the git | jbech-linaro/ibart                    |
+------------------+------------------------------------------------------+---------------------------------------+
| ``PR_CLONE_URL`` | URL to the submitters git/tree                       | https://github.com/jbech-linaro/ibart |
+------------------+------------------------------------------------------+---------------------------------------+
| ``PR_BRANCH``    | URL to the submitters branch                         | my_super_branch_with_fixes            |
+------------------+------------------------------------------------------+---------------------------------------+


Directory changes
-----------------
Just as for the exported variables the last seen ``cd`` command is saved and then executed when spawning a new shell on for a new section in the job definition file. I.e., from user perspective a ``cd`` will carry over to the section in the job definition file.

