# Birinin çalıştığı case yanlış geliyor
#!/bin/bash

WL_HOME=""
DOMAIN_HOME="" 

usage() {                                      # Print a help message.
  echo "Usage: $0 -w WL_HOME -d DOMAIN_HOME" 1>&2 
}

exit_abnormal() {                              # Exit with error.
  usage
  exit 1
}


_isRunning() {									# Check if a process is running
    ps aux | grep -v grep | grep "$1" > /dev/null
}

# Returns true if an AdminServer process is running, otherwise returns false
isAdminRunning(){
	if _isRunning AdminServer; then
		return #return true
	else 
		false
	fi
}

# Starts up Admin Server, writes log to the startAdminServer.out file
startAdminServer(){
	if isAdminRunning;
		then echo "No need to startup Admin Server, already running."
	else
		echo "Starting up Admin Server..."
		nohup $DOMAIN_HOME/bin/startWebLogic.sh >> ./startAdminServer.out &
	fi
}

# Returns true if a NodeManager process is running, otherwise returns false
isNMRunning(){
	if _isRunning NodeManager; then
		return #return true
	else 
		false
	fi
}

# Starts up Node Manager, writes log to the startNodeManager.out file
startNM(){
	if isNMRunning
		then echo "No need to startup Node Manager, already running."
	else
		echo "Starting up Node Manager..."
		nohup $DOMAIN_HOME/bin/startNodeManager.sh >> ./startNodeManager.out &
	fi
}




# Get WL_HOME (-w) and DOMAIN_HOME (-d) from user, if no argument specified exit with error.
no_args="true"
while getopts ":w:d:" options; do
	case "${options}" in
		w)
			WL_HOME=${OPTARG} 
			if [ -f $WL_HOME/oracle_common/common/bin/wlst.sh ]
			then
				echo "WL_HOME is set to $WL_HOME."
			else
				echo "Specified path for WL_HOME does not exist or wrong!"
				exit_abnormal
				exit 1
			fi
			;;
		d)
			DOMAIN_HOME=${OPTARG}
			if [ -f $DOMAIN_HOME/bin/startWebLogic.sh ]
			then
				echo "DOMAIN_HOME is set to $DOMAIN_HOME." 
			else
				echo "Specified path for DOMAIN_HOME does not exist or wrong!"
				exit_abnormal
				exit 1
			fi
			;;
		:) 						# If expected argument omitted:
			echo "Error: -${OPTARG} requires an argument."
			exit_abnormal
			;;
		*) 						# If unknown (any other) option:
			echo "Error: Unknown argument specified."
			exit_abnormal
			;;
	esac
	no_args="false"
done
[[ "$no_args" == "true" ]] && { echo "Error: No argument specified."; exit_abnormal; }


# Check if Admin Server and Node Manager is running. If not, try to start up 3 times. Give 1 min of sleep time in between.
COUNT=1                                
while [ $COUNT -le 3 ]; do  
           
	if isNMRunning & isAdminRunning 				# Both running
		then echo "Both Admin Server and Node Manager is Running. No need to startup."
		break
	elif isNMRunning 								# Only Node Manager running.
		then startAdminServer
	elif isAdminRunning 							# Only Admin Server running.
		then startNM
	else											# Both not running.
		echo "Both Admin Server and Node Manager is NOT Running. Startup needed."
		startNM
		startAdminServer
	fi
	sleep 1m	
	let COUNT+=1                         
done
echo "~~~ FIN ~~~"
exit 0