## 1. Create Connection Files for WLST

While using wlst, using UserConfigFile and UserKeyFile is a better option rather than using clear text username and password to connect Admin Server.  Create these files as follows:
```bash
[weblogic@host01 scripts]$ $WL_HOME/oracle_common/common/bin/wlst.sh

wls:/offline> connect('weblogic','weblogic1','t3://<hostname>:7001')

storeUserConfig('/u01/scripts/serverStateControl/WLUserConfigFile.conf','/u01/scripts/serverStateControl/WLUserKeyFile.key')
Creating the key file can reduce the security of your system if it is not kept in a secured location after it is created. Creating new key...
The username and password that were used for this WebLogic Server connection are stored in /u01/scripts/serverStateControl/WLUserConfigFile.conf and /u01/scripts/serverStateControl/WLUserKeyFile.key.
```

These files are used in *serverStateControl.py* script to connect Admin Server as follows:
```bash
...
wls:/offline> connect(userConfigFile='/u01/scripts/serverStateControl/WLUserConfigFile.conf',userKeyFile='/u01/scripts/serverStateControl/WLUserKeyFile.key') 
...
```

## 2. serverStateControl.py

Run the command:
```bash
[weblogic@host01 scripts]$ $WL_HOME/oracle_common/common/bin/wlst.sh serverStateControl.py
```

This scipt is used to show the status and start time of WebLogic servers. If a server is not running and is not in the *blacklist* array, startup command is given.

**Notes:** 
- Admin server and Node Manager must be running prior to using this script. 
- *connect()* function should be adjusted according to the environment.
- Add names of the managed server that you do want to startup to the *blacklist* array. 

The script includes 3 functions:
1. *getActivationTime(serverName)*: returns the startup time of a WebLogic server. Input must be a string of Weblogic server name.

2. *startManagedSrv(serverName,blacklist)*: starts up the specified WebLogic server if the serverName is not in blacklist array. Input must be a string of Weblogic server name and an array oblacklist array.

3. *serverStatus(blacklist)*: controls the status and start time of all servers in the domain, except for the ones specified in blacklist array. If server state is RUNNING, calls *getActivationTime* function to get startup time. If server state is not RUNNING calls *startManagedSrv* function to start up the corresponding server.

## 3. serverStateControl.sh
As specified in the note, if Admin server or node manager is not running the script is completely useless. This is a problem if an unexpected reboot of a host server occured. So using it as a part of bash script is more helpful:

- *serverStateControl.sh* expects two arguments: *$WL_HOME* and *$DOMAIN_HOME*. 
- Checks if Node Manager and Admin Server processes are running or not. If not, tries to start them up at most 3 times.
- If the above are running, calls *serverStateControl.py* 
- Redirects the startup logs of Node Manager and Admin Server to the files startNodeManager-%Y%m%d-%H-%M.out and startAdminServer-%Y%m%d-%H-%M.out.

An example usage is as follows:
```bash
[weblogic@host01 scripts]$ ./serverStateControl.sh -w /u01/products/middleware/ -d /u01/config/domains/testDomain/
```

**Note**: If no arguement specified, there is a missing argument or invalid paths are given the script exits with error. 

The script includes following functions:
1. *usage()*: Prints usage of  script.

2. *exit_abnormal()*: prints usage and exits with error.

3. *_isRunning()*: checks if specified process is running or not.

4. *isAdminRunning()*: sends 'AdminServer' as process to be checked to the *_isRunning()* function. 

5. *startAdminServer()*: checks if AdminServer process is running or not. If not, starts up using $DOMAIN_HOME/bin/startWebLogic.sh

6. *isNMRunning()*: sends 'NodeManager' as process to be checked to the *_isRunning()* function. 

7. *startNM()*: Checks if NodeManager process is running or not. If not, starts up using $DOMAIN_HOME/bin/startNodeManager.sh

## 4. nmControl.sh
This is a simple script prepared for the servers that Admin Server is not running on. In order to start the managed servers running on a server, this script only checks if the Node Manager process is running or not and starts it if it does not.

- *nmControl.sh* expects one argument: *$DOMAIN_HOME*. 
- Checks if Node Manager process is running or not. If not, tries to start it up at most 3 times.
- Redirects the startup log to the file startNodeManager-%Y%m%d-%H-%M.out.

An example usage is as follows:
```bash
[weblogic@host02 scripts]$ ./nmControl.sh -d /u01/config/domains/testDomain/
```

## 5. Use Scripts as Cron Job 

Create a path for related files, send serverStateControl.sh, serverStateControl.py and README.md to the created directory:
```bash
[appltprm@eetprm01 ~]$ mkdir -p /u01/scripts/serverStateControl
[appltprm@eetprm01 serverStateControl]$ chmod u+x *
```

Create connection files for WLST (see Tilte #1). Change serverStateControl.py connect() function and blacklist array:
```python
try:
    connect(userConfigFile='/u01/scripts/serverStateControl/WLUserConfigFile.conf',userKeyFile='/u01/scripts/serverStateControl/WLUserKeyFile.key')
except Exception,e:
    print "Unable to connect to Admin Server!"
    exit()
...
blacklist = ['AdminServer','p6tmserver_1','p6tmserver_2']
...
```

Check if serverStatusControl.py runs as expected:
```bash
[appltprm@eetprm01 serverStateControl]$ $WL_HOME/oracle_common/common/bin/wlst.sh serverStateControl.py

Initializing WebLogic Scripting Tool (WLST) ...

Welcome to WebLogic Server Administration Scripting Shell

Type help() for help on available commands

Connecting to t3://localhost:7001 with userid weblogic ...
Successfully connected to Admin Server "AdminServer" that belongs to domain "primaveraDomain".

Warning: An insecure protocol was used to connect to the server. 
To ensure on-the-wire security, the SSL port or Admin port should be used instead.

Location changed to domainRuntime tree. This is a read-only tree 
with DomainMBean as the root MBean. 
For more help, use help('domainRuntime')

--------------------------------------------------------------------
        Server status in primaveraDomain domain 
--------------------------------------------------------------------
p6tmserver_1    :SHUTDOWN
p6tmserver_1 is in blacklist. No start operation will be performed.
p6tmserver_2    :SHUTDOWN
p6tmserver_2 is in blacklist. No start operation will be performed.
AdminServer     :RUNNING        Start Time      :Wed Apr  8 11:32:53 2020
p6cloudserver_2 :RUNNING        Start Time      :Tue Dec 31 08:49:25 2019
p6cloudserver_1 :RUNNING        Start Time      :Wed Apr  8 11:37:21 2020
gatewayserver_1 :RUNNING        Start Time      :Wed Apr  8 11:38:45 2020
gatewayserver_2 :RUNNING        Start Time      :Tue Dec 31 08:50:08 2019
p6apiserver_1   :RUNNING        Start Time      :Wed Apr  8 11:37:48 2020
p6wsserver_2    :RUNNING        Start Time      :Tue Dec 31 08:50:02 2019
p6apiserver_2   :RUNNING        Start Time      :Tue Dec 31 08:49:08 2019
p6server_2      :RUNNING        Start Time      :Tue Feb 11 14:51:57 2020
unifierserver_1 :RUNNING        Start Time      :Wed Apr  8 11:39:10 2020
unifierserver_2 :RUNNING        Start Time      :Tue Dec 31 08:50:09 2019
p6wsserver_1    :RUNNING        Start Time      :Wed Apr  8 11:38:44 2020
p6server_1      :RUNNING        Start Time      :Wed Apr  8 11:39:55 2020
--------------------------------------------------------------------
```

Check if serverStatusControl.py runs as expected:
```bash
[appltprm@eetprm01 serverStateControl]$ ./serverStateControl.sh -w /u01/products/middleware/ -d /u01/config/domains/primaveraDomain/

--------------------------------------------------------------------
                     Start Time: 16.04.2020 - 15:21:01
--------------------------------------------------------------------
WL_HOME is set to /u01/products/middleware/
DOMAIN_HOME is set to /u01/config/domains/primaveraDomain/
--------------------------------------------------------------------
                Admin Server and Node Manager Control
--------------------------------------------------------------------
Both Admin Server and Node Manager is Running. No need to startup.
--------------------------------------------------------------------
                    Managed Servers Control
--------------------------------------------------------------------

Initializing WebLogic Scripting Tool (WLST) ...

Welcome to WebLogic Server Administration Scripting Shell

Type help() for help on available commands

Connecting to t3://localhost:7001 with userid weblogic ...
Successfully connected to Admin Server "AdminServer" that belongs to domain "primaveraDomain".

Warning: An insecure protocol was used to connect to the server. 
To ensure on-the-wire security, the SSL port or Admin port should be used instead.

Location changed to domainRuntime tree. This is a read-only tree 
with DomainMBean as the root MBean. 
For more help, use help('domainRuntime')

--------------------------------------------------------------------
        Server status in primaveraDomain domain 
--------------------------------------------------------------------
p6tmserver_1    :SHUTDOWN
p6tmserver_1 is in blacklist. No start operation will be performed.
p6tmserver_2    :SHUTDOWN
p6tmserver_2 is in blacklist. No start operation will be performed.
AdminServer     :RUNNING        Start Time      :Wed Apr  8 11:32:53 2020
p6cloudserver_2 :RUNNING        Start Time      :Tue Dec 31 08:49:25 2019
p6cloudserver_1 :RUNNING        Start Time      :Wed Apr  8 11:37:21 2020
gatewayserver_1 :RUNNING        Start Time      :Wed Apr  8 11:38:45 2020
gatewayserver_2 :RUNNING        Start Time      :Tue Dec 31 08:50:08 2019
p6apiserver_1   :RUNNING        Start Time      :Wed Apr  8 11:37:48 2020
p6wsserver_2    :RUNNING        Start Time      :Tue Dec 31 08:50:02 2019
p6apiserver_2   :RUNNING        Start Time      :Tue Dec 31 08:49:08 2019
p6server_2      :RUNNING        Start Time      :Tue Feb 11 14:51:57 2020
unifierserver_1 :RUNNING        Start Time      :Wed Apr  8 11:39:10 2020
unifierserver_2 :RUNNING        Start Time      :Tue Dec 31 08:50:09 2019
p6wsserver_1    :RUNNING        Start Time      :Wed Apr  8 11:38:44 2020
p6server_1      :RUNNING        Start Time      :Wed Apr  8 11:39:55 2020
--------------------------------------------------------------------
--------------------------------------------------------------------
                    End Time: 16.04.2020 - 15:21:01
--------------------------------------------------------------------

                  ~~~ FIN ~~~
```

**Note**: If you get */bin/bash^M: bad interpreter: No such file or directory* error. Open file with vi and use ```:set ff=unix``` and save the file.

Add the script to the cron as follows:
```bash
[appltprm@eetprm01 serverStateControl]$ crontab -e
no crontab for appltprm - using an empty one
0 */4 * * * /u01/scripts/serverStateControl/serverStateControl.sh -w /u01/products/middleware/ -d /u01/config/domains/primaveraDomain/ >> serverStateControl.out
```