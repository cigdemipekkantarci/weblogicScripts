# line 28deyim

#!/bin/bash
WL_HOME 			= ""
DOMAIN_HOME 		= "" 
startIfNotRunning 	= false
nmRunning 			= false

usage() {                                      # Function: Print a help message.
  echo "Usage: $0 [ -w WL_HOME ] [ -d DOMAIN_HOME ]" 1>&2 
}
exit_abnormal() {                              # Function: Exit with error.
  usage
  exit 1
}

# Admin processi calismiyorsa false, calisiyorsa true doner
isAdminRunning(){
	if ps aux | grep -v grep | grep "AdminServer"
		then echo "Admin Server is already RUNNING."
		return #return true
	else 
		echo "Admin Server is not running."
		false
	fi
}

startAdminServer(){
	if adminServerRunning
		then echo "No need to startup Admin Server"
	else
		while [! isAdminRunning]
			echo "Starting up Admin Server..."
			nohup $DOMAIN_HOME/bin/startWebLogic.sh >> ./startAdminServer.out &
	fi
}

# Node manager processi calismiyorsa false, calisiyorsa true doner
isNMRunning(){
	if ps aux | grep -v grep | grep "NodeManager"
		then echo "Node Manager is already RUNNING."
		return #return true
	else 
		echo "Node Manager is not running."
		false
	fi
}

startNM(){
	if isNMRunning
		then echo "No need to startup Node Manager"
	else
		echo "Starting up Node Manager..."
		nohup $DOMAIN_HOME/bin/startNodeManager.sh >> ./startNodeManager.out &
	fi
}

while getopts ":w:d:" options; do
	case "${options}" in
		w)
			WL_HOME=${OPTARG} 
			if [ -d $WL_HOME ] 
			then
				echo "WL_HOME set to $WL_HOME." 
			else
				echo "Specified path for WL_HOME does not exist!"
				exit_abnormal
				exit 1
			fi
			;;
		d)
			DOMAIN_HOME=${OPTARG}
			if [ -d $DOMAIN_HOME ] 
			then
				echo "DOMAIN_HOME set to $DOMAIN_HOME." 
			else
				echo "Specified path for DOMAIN_HOME does not exist!"
				exit_abnormal
				exit 1
			fi
			;;
		:) 										# If expected argument omitted:
			echo "Error: -${OPTARG} requires an argument."
			exit_abnormal
			;;
		*) 										# If unknown (any other) option:
			exit_abnormal
			;;
	esac
done

