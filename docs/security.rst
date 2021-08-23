Security considerations
=======================
This is a very early version and there are things that are not secure:

* Anyone can restart and stop a job by going to the main page on IBART as long as they have authenticated themselves using Google. Anyone with a Google account can login and trigger rebuilds, cancel jobs etc. People abusing this will be banned.
* It runs Flask ``debug`` mode by default (consider using nginx for example instead of the Flask web server).
* Whatever is in the job definition file will be executed and it will do this with the same permissions as the server itself. So if one type ``cmd: rm -rf $HOME`` in the job definition file, then all files in the servers' $HOME folder **will** be deleted. So be very careful with what you or someone else puts into job definition file. 
