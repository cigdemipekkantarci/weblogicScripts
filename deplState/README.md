## 1. Create Connection Files for WLST

While using wlst, using UserConfigFile and UserKeyFile is a better option rather than using clear text username and password to connect Admin Server.  Create these files as follows:
```bash
[weblogic@host01 scripts]$ $WL_HOME/oracle_common/common/bin/wlst.sh

wls:/offline> connect('weblogic','weblogic1','t3://<hostname>:7001')

storeUserConfig('/u01/scripts/deplState/WLUserConfigFile.conf','/u01/scripts/deplState/WLUserKeyFile.key')
Creating the key file can reduce the security of your system if it is not kept in a secured location after it is created. Creating new key...
The username and password that were used for this WebLogic Server connection are stored in /u01/scripts/deplState/WLUserConfigFile.conf and /u01/scripts/deplState/WLUserKeyFile.key.
```

These files are used in *deplState.py* script to connect Admin Server as follows:
```bash
...
wls:/offline> connect(userConfigFile='/u01/scripts/deplState/WLUserConfigFile.conf',userKeyFile='/u01/scripts/deplState/WLUserKeyFile.key') 
...
```

## 2. deplState.py

Run the command:
```bash
[weblogic@host01 deplState]$ $WL_HOME/oracle_common/common/bin/wlst.sh deplState.py
```

This scipt is used to show the status of Application. No start/stop operation is performed afterwards.

**Notes:** 
- Admin server and Node Manager must be running prior to using this script. 
- *connect()* function should be adjusted according to the environment.

## 3. Using with deplState.sh and as a Cron Task

Similar to *serverStateControl.sh*, I would like to use this script as a Crontask as follows:

- *deplState.sh* expects two arguments: *$WL_HOME* and *$DOMAIN_HOME*
- Checks if Node Manager and Admin Server processes are running or not. If not, tries to start them up at most 3 times.
- If the above are running, calls *deplState.py* and checks the status of applications.
- Redirects the startup logs of Node Manager and Admin Server to the files startNodeManager-%Y%m%d-%H-%M.out and startAdminServer-%Y%m%d-%H-%M.out.

An example usage is as follows:
```bash
[weblogic@host01 deplState]$ ./deplState.sh -w /u01/products/middleware/ -d /u01/config/domains/testDomain/
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

Create a path for related files, send deplState.sh, deplState.py and README.md to the created directory:
```bash
[weblogic@host01 ~]$ mkdir -p /u01/scripts/deplState
[weblogic@host01 deplState]$ chmod u+x *
```

Create connection files for WLST (see Tilte #1). Change deplState.py connect() function
```python
try:
    connect(userConfigFile='/u01/scripts/deplState/WLUserConfigFile.conf',userKeyFile='/u01/scripts/deplState/WLUserKeyFile.key')
except Exception,e:
    print "Unable to connect to Admin Server!"
    exit()
```

Check if deplState.py runs as expected:
```bash
[weblogic@host01 deplState]$ $WL_HOME/oracle_common/common/bin/wlst.sh deplState.py

Initializing WebLogic Scripting Tool (WLST) ...

Welcome to WebLogic Server Administration Scripting Shell

Type help() for help on available commands

Connecting to t3://localhost:7001 with userid weblogic ...
Successfully connected to Admin Server "AdminServer" that belongs to domain "starter_domain".

Warning: An insecure protocol was used to connect to the server. 
To ensure on-the-wire security, the SSL port or Admin port should be used instead.

Location changed to domainConfig tree. This is a read-only tree 
with DomainMBean as the root MBean. 
For more help, use help('domainConfig')

dr--   cluster_1

Location changed to domainRuntime tree. This is a read-only tree 
with DomainMBean as the root MBean. 
For more help, use help('domainRuntime')

Applications in Active State
-------------------------------------------
starter

```

Check if *deplState.sh* runs as expected:

```bash
[weblogic@host01 deplState]$ ./deplState.sh -w /u01/app/fmw/weblogic/ -d /u01/app/fmw/admin/domains/starter_domain/
--------------------------------------------------------------------
                     Start Time: 23.04.2020 - 14:24:32
--------------------------------------------------------------------
WL_HOME is set to /u01/app/fmw/weblogic/
DOMAIN_HOME is set to /u01/app/fmw/admin/domains/starter_domain/
--------------------------------------------------------------------
                Admin Server and Node Manager Control
--------------------------------------------------------------------
Both Admin Server and Node Manager is Running. No need to startup.
--------------------------------------------------------------------
                    Applications Control
--------------------------------------------------------------------

Initializing WebLogic Scripting Tool (WLST) ...

Welcome to WebLogic Server Administration Scripting Shell

Type help() for help on available commands

Connecting to t3://localhost:7001 with userid weblogic ...
Successfully connected to Admin Server "AdminServer" that belongs to domain "starter_domain".

Warning: An insecure protocol was used to connect to the server. 
To ensure on-the-wire security, the SSL port or Admin port should be used instead.

Location changed to domainConfig tree. This is a read-only tree 
with DomainMBean as the root MBean. 
For more help, use help('domainConfig')

dr--   cluster_1

Location changed to domainRuntime tree. This is a read-only tree 
with DomainMBean as the root MBean. 
For more help, use help('domainRuntime')

Applications in Active State
--------------------------------------------------------------------
starter
Disconnected from weblogic server: AdminServer


Exiting WebLogic Scripting Tool.

--------------------------------------------------------------------
                    End Time: 23.04.2020 - 14:24:32
--------------------------------------------------------------------

                  ~~~ FIN ~~~

```

**Note**: If you get */bin/bash^M: bad interpreter: No such file or directory* error. Open file with vi and use ```:set ff=unix``` and save the file.

Add the script to the cron as follows:
```bash
[weblogic@host01 deplState]$ crontab -e
no crontab for weblogic - using an empty one
0 */4 * * * /u01/scripts/deplState/deplState.sh -w /u01/products/middleware/ -d /u01/config/domains/primaveraDomain/ >> deplState.out
```