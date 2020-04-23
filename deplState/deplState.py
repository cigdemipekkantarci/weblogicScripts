try:
    connect(userConfigFile='/u01/scripts/serverStateControl/WLUserConfigFile.conf',userKeyFile='/u01/scripts/serverStateControl/WLUserKeyFile.key')
except Exception,e:
    print "Unable to connect to Admin Server!"
    exit()
    
cd('AppDeployments')
deplymentsList=cmo.getAppDeployments()

for app in deplymentsList:
      domainConfig()
      cd ('/AppDeployments/'+app.getName()+'/Targets')
      mytargets = ls(returnMap='true')
      domainRuntime()
      cd('AppRuntimeStateRuntime/AppRuntimeStateRuntime')
      for targetinst in mytargets:
            curstate4=cmo.getCurrentState(app.getName(),targetinst)
      	    if(curstate4 == "STATE_ACTIVE"):
		print "Applications in Active State"
		print "--------------------------------------------------------------------"
      		print app.getApplicationName()
       	    else:
                print "Applications in Other States"
                print "--------------------------------------------------------------------"
                print app.getApplicationName() + ": " + curstate4 
                
disconnect()
exit()