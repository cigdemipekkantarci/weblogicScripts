connect('weblogic','weblogic123','t3://localhost:7001')
# Admine baglanma try-catch icinde olmali
cd('AppDeployments')
deplymentsList=cmo.getAppDeployments()

for app in deplymentsList:
      domainConfig()
      cd ('/AppDeployments/'+app.getName()+'/Targets')
      mytargets = ls(returnMap='true')
      domainRuntime()
      cd('AppRuntimeStateRuntime')
      cd('AppRuntimeStateRuntime')
      for targetinst in mytargets:
            curstate4=cmo.getCurrentState(app.getName(),targetinst)
	    #srcPath=app.getAbsoluteSourcePath() bu attribute ileride kullanilabilir	
	    #active olmayan appler icin log lokasyonu verilebilir ve corrective action
      	    if(curstate4 == "STATE_ACTIVE"):
		print "\033[1;32mApplications in Active State\033[1;m"
		print "-------------------------------------------"
      		print app.getApplicationName()
       	    else:
                print "\033[1;31mApplications in Other States \033[1;m"
                print "-------------------------------------------"
                print app.getApplicationName() + ": " + curstate4 