Security considerations
=======================
This is a very early version and there are things that are not secure:

* There has so far been no real attempt yet to protect against SQL injection. This is of course something that should be dealt with sooner or later.
* Anyone can restart and stop a job by going to the main page on IBART, i.e., there are current no access control, so anyone could abuse this as of now.
* It runs Flask ``debug`` mode by default.
* Whatever is in the job definition file will be executed and it will do this with the same permissions as the server itself. So if one type ``cmd: rm -rf $HOME`` in the job definition file, then all files in the servers' $HOME folder **will** be deleted. So be very careful with what you or someone else puts into job definition file. 
