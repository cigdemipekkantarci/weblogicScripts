"""
This scipt is used to show the status and start time of WebLogic servers. If a server is not running and is not in the 'blacklist', startup command is given.

NOTES:
- connect() function should be adjusted according to the environment
"""

def serverStatus(blacklist):
    #Get list of servers in current domain
    domainRuntime()
    servers = cmo.getServerLifeCycleRuntimes()
    print "--------------------------------------------------------------------"
    print "\t" + "Server status in " + cmo.getName() + " domain "
    print "--------------------------------------------------------------------"
    for server in servers:
        #Get Name and State of each server
        serverState = server.getState()
        serverName = server.getName()
        if serverState == "RUNNING":
                startTime = getActivationTime(serverName)
                print serverName + '\t:\033[1;32m' + serverState +  '\033[0m' + '\tStart Time\t:' + startTime
        elif serverState == "STARTING":
                print serverName + '\t:\033[1;33m' + serverState + '\033[0m'
        elif serverState == "UNKNOWN":
                print serverName + '\t:\033[1;34m' + serverState + '\033[0m'
        elif serverState == "SHUTDOWN" or "FAILED_NOT_RESTARTABLE":
                print serverName + '\t:\033[1;31m' + serverState + '\033[0m'
                startManagedSrv(serverName,blacklist)
                serverState = server.getState()
                if serverState == "RUNNING":
                    startTime = getActivationTime(serverName)
                    print serverName + '\t:\033[1;32m' + serverState +  '\033[0m' + '\tStart Time\t:' + startTime 
        else:
                print serverName + '\t:\033[1;31m' + serverState + '\033[0m'
    print "--------------------------------------------------------------------"

def startManagedSrv(serverName,blacklist):
    try:
        if serverName not in blacklist:
            print serverName + ' is not in blacklist. Starting up...'
            start(serverName,'Server')
        else:
            print serverName + ' is in blacklist. No start operation will be performed.'
    except Exception,e:
        print 'Exception while starting managed server!'       
        dumpStack()


def getActivationTime(serverName):
    import time
    cd('ServerRuntimes/'+serverName)
    tmp = cmo.getActivationTime()
    epochTime = str(tmp)[:10]
    activationTime = time.ctime(int(epochTime))    
    return activationTime          
        
try:
    connect("weblogic","weblogic123","t3://localhost:7001")
except Exception,e:
    print "Unable to connect to Admin Server!"
    exit()

blacklist = ['server_1']
serverStatus(blacklist)
