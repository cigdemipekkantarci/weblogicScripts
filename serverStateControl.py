# This script shows the state of weblogic servers in a domain. Don't forget to write your environment credentials in connect() function.
# How to run?   $WL_HOME/oracle_common/common/wlst.sh /home/oracle/serverStateControl.py

def serverStatus():
    #Get list of servers in current domain
    domainRuntime()
    servers = cmo.getServerLifeCycleRuntimes()
    print "----------------------------------------------------------"
    print "\t" + "Server status in " + cmo.getName() + " domain "
    print "----------------------------------------------------------"
    for server in servers:
    	#Get Name and State of each server
        serverState = server.getState()
        if serverState == "RUNNING":
        	print server.getName() + '\t:\033[1;32m' + serverState + '\033[0m'
        elif serverState == "STARTING":
       		print server.getName() + '\t:\033[1;33m' + serverState + '\033[0m'
        elif serverState == "UNKNOWN":
        	print server.getName() + '\t:\033[1;34m' + serverState + '\033[0m'
        else:
        	print server.getName() + '\t:\033[1;31m' + serverState + '\033[0m'
    print "----------------------------------------------------------"
    quit()

def quit():
    print '\033[1;35mTo re-run the script HIT any key..\033[0m'
    Ans = raw_input("Are you sure quit from WLST? (y/n)")
    if (Ans == 'y'):
        disconnect()
        stopRedirect()
        exit()
    else:
        serverStatus()

try:
    connect("weblogic","weblogic123","t3://localhost:7001")
except Exception,e:
    print "Unable to connect Admin Server!"
    exit()

serverStatus()