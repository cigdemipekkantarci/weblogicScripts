# serverStateControl.py

Run the command:
```bash
$WL_HOME/oracle_common/common/bin/wlst.sh serverStateControl.py
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

# Using as Cronjob task - serverStateControl.sh
As specified in the note, if Admin server or node manager is not running the script is completely useless. This is a problem if an unexpected reboot of a host server occured. So using it as a bash script is more helpful. 
