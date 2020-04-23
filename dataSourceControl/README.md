## 1. Create Connection Files for WLST

While using wlst, using UserConfigFile and UserKeyFile is a better option rather than using clear text username and password to connect Admin Server.  Create these files as follows:
```bash
[weblogic@host01 scripts]$ $WL_HOME/oracle_common/common/bin/wlst.sh

wls:/offline> connect('weblogic','weblogic1','t3://<hostname>:7001')

storeUserConfig('/u01/scripts/dataSourceControl/WLUserConfigFile.conf','/u01/scripts/dataSourceControl/WLUserKeyFile.key')
Creating the key file can reduce the security of your system if it is not kept in a secured location after it is created. Creating new key...
The username and password that were used for this WebLogic Server connection are stored in /u01/scripts/dataSourceControl/WLUserConfigFile.conf and /u01/scripts/dataSourceControl/WLUserKeyFile.key.
```

These files are used in *dataSourceControl.py* script to connect Admin Server as follows:
```bash
...
wls:/offline> connect(userConfigFile='/u01/scripts/dataSourceControl/WLUserConfigFile.conf',userKeyFile='/u01/scripts/dataSourceControl/WLUserKeyFile.key') 
...
```

## 2. dataSourceControl.py

Run the command:
```bash
[weblogic@host01 dataSourceControl]$ $WL_HOME/oracle_common/common/bin/wlst.sh dataSourceControl.py
```

This scipt is used to show the status and current configuration of data sources. Remind that if data source is not in Running state because the target cluster/managed server is down, then you do not see any info saying data source is down.

**Notes:** 
- Admin server must be running prior to using this script. 
- *connect()* function should be adjusted according to the environment.

The script connects to server runtime gets the information about the data source: Name, State, Active Connections Current Count, Type, Max Connections Count, Min Connections Count, Connection Url, Source File. Also tests the connection because automatically testing take place each 2 mins, unless being configured differently.

**Note:** For security related reasons you may want to remove the function that returns the Connection Url.
                                                                                                              
## 3. Using with dataSourceControl.sh and as a Cron Task                                         
                                                                                             
Similar to *serverStateControl.sh*, I would like to use this script as a Crontask as follows:
                           
- *dataSourceControl.sh* expects two arguments: *$WL_HOME* and *$DOMAIN_HOME*
- Checks Admin Server process is running or not. If not, tries to start up at most 3 times.
- If the above is running, calls *dataSourceControl.py* and gathers the information about data sources.
- Redirects the startup log of Admin Server to the file startAdminServer-%Y%m%d-%H-%M.out.

An example usage is as follows:
```bash
[weblogic@host01 dataSourceControl]$ ./dataSourceControl.sh -w /u01/products/middleware/ -d /u01/config/domains/testDomain/
```

**Note**: If no arguement specified, there is a missing argument or invalid paths are given the script exits with error. 

The script includes following functions:
1. *usage()*: Prints usage of  script.

2. *exit_abnormal()*: prints usage and exits with error.

3. *_isRunning()*: checks if specified process is running or not.

4. *isAdminRunning()*: sends 'AdminServer' as process to be checked to the *_isRunning()* function. 

5. *startAdminServer()*: checks if AdminServer process is running or not. If not, starts up using $DOMAIN_HOME/bin/startWebLogic.sh

Create a path for related files, send dataSourceControl.sh, dataSourceControl.py and README.md to the created directory:
```bash
[weblogic@host01 ~]$ mkdir -p /u01/scripts/dataSourceControl
[weblogic@host01 dataSourceControl]$ chmod u+x *
```

Create connection files for WLST (see Tilte #1). Change dataSourceControl.py connect() function
```python
try:
    connect(userConfigFile='/u01/scripts/dataSourceControl/WLUserConfigFile.conf',userKeyFile='/u01/scripts/dataSourceControl/WLUserKeyFile.key')
except Exception,e:
    print "Unable to connect to Admin Server!"
    exit()
```

Check if dataSourceControl.py runs as expected:
```bash
[weblogic@host01 dataSourceControl]$ $WL_HOME/oracle_common/common/bin/wlst.sh dataSourceControl.py

Initializing WebLogic Scripting Tool (WLST) ...

Welcome to WebLogic Server Administration Scripting Shell

Type help() for help on available commands

Connecting to t3://localhost:7001 with userid weblogic ...
Successfully connected to Admin Server "AdminServer" that belongs to domain "starter_domain".

Warning: An insecure protocol was used to connect to the server. 
To ensure on-the-wire security, the SSL port or Admin port should be used instead.

Target Server                               :  server_2
Name                                        :  TESTDB
State                                       :  Running
Active Connections Current Count            :  0
Type                                        :  GENERIC
Max Connections Count                       :  15
Min Connections Count                       :  1
Connection Url                              :  jdbc:oracle:thin:@//192.168.56.101:1521/TEST
Source File                                 :  ./config/jdbc/TESTDB-0112-jdbc.xml

Testing Datasource...                         
Connection Successful!

Disconnected from weblogic server: AdminServer


Exiting WebLogic Scripting Tool.

```

Check if *dataSourceControl.sh* runs as expected:

```bash
[weblogic@host01 dataSourceControl]$ ./dataSourceControl.sh -w /u01/app/fmw/weblogic/ -d /u01/app/fmw/admin/domains/starter_domain/
--------------------------------------------------------------------
                     Start Time: 23.04.2020 - 19:04:59
--------------------------------------------------------------------
WL_HOME is set to /u01/app/fmw/weblogic/
DOMAIN_HOME is set to /u01/app/fmw/admin/domains/starter_domain/
--------------------------------------------------------------------
                Admin Server Control
--------------------------------------------------------------------
Admin Server is Running. No need to startup.
--------------------------------------------------------------------
                    Data Source Control
--------------------------------------------------------------------

Initializing WebLogic Scripting Tool (WLST) ...

Welcome to WebLogic Server Administration Scripting Shell

Type help() for help on available commands

Connecting to t3://localhost:7001 with userid weblogic ...
Successfully connected to Admin Server "AdminServer" that belongs to domain "starter_domain".

Warning: An insecure protocol was used to connect to the server. 
To ensure on-the-wire security, the SSL port or Admin port should be used instead.

Target Server                               :  server_2
Name                                        :  TESTDB
State                                       :  Running
Active Connections Current Count            :  0
Type                                        :  GENERIC
Max Connections Count                       :  15
Min Connections Count                       :  1
Connection Url                              :  jdbc:oracle:thin:@//192.168.56.101:1521/TEST
Source File                                 :  ./config/jdbc/TESTDB-0112-jdbc.xml

Testing Datasource...                         
Connection Successful!

Disconnected from weblogic server: AdminServer


Exiting WebLogic Scripting Tool.

--------------------------------------------------------------------
                    End Time: 23.04.2020 - 19:04:59
--------------------------------------------------------------------

                  ~~~ FIN ~~~

```

**Note**: If you get */bin/bash^M: bad interpreter: No such file or directory* error. Open file with vi and use ```:set ff=unix``` and save the file.

Add the script to the cron as follows:
```bash
[weblogic@host01 dataSourceControl]$ crontab -e
no crontab for weblogic - using an empty one
0 */4 * * * /u01/scripts/dataSourceControl/dataSourceControl.sh -w /u01/products/middleware/ -d /u01/config/domains/primaveraDomain/ >> dataSourceControl.out
```