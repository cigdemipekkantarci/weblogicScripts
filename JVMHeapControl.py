# This script shows the heap size of running weblogic servers in a domain. Don't forget to write your environment credentials in connect() function.
# How to run?   $WL_HOME/oracle_common/common/wlst.sh /home/oracle/JVMHeapControl.py

def monitorHeapSize():
    #Get list of servers in current domain
    print pwd()
    domainRuntime()
    servers = cmo.getServerLifeCycleRuntimes()
    print "--------------------------------------------------------------------------------"
    print "Server Name         Total Heap (MB)     Free Heap (MB)      Used Heap (MB)      "
    print "--------------------------------------------------------------------------------"
    for server in servers:
    	#Get Name and State of each server
        serverState = server.getState()
        if serverState == "RUNNING":
		try:
    			cd("/ServerRuntimes/"+server.getName()+"/JVMRuntime/"+server.getName())
    			free = int(get('HeapFreeCurrent'))/(1024*1024)
    			total = int(get('HeapSizeCurrent'))/(1024*1024)
    			used = (total - free)
			print '%-20s%-20d%-20d%-20d' %(server.getName(),total, free, used)
   		except Exception,e:
     			print e
    print "--------------------------------------------------------------------------------"
    quit()

def quit():
    print '\033[1;35mTo re-run the script HIT any key..\033[0m'
    Ans = raw_input("Are you sure quit from WLST? (y/n)")
    if (Ans == 'y'):
        disconnect()
        stopRedirect()
        exit()
    
    # Yeniden fonksiyona girdiginde hata aliyor????????
    else:
    	serverConfig()
	monitorHeapSize()

try:
    connect("weblogic","weblogic123","t3://localhost:7001")
except Exception,e:
    print "Unable to connect Admin Server!"

monitorHeapSize()
