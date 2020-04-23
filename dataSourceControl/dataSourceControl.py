def findMaxConnCap(dsName):
    cd('/JDBCSystemResources/' + dsName + '/Resource/' + dsName + '/JDBCConnectionPoolParams/' + dsName)
    return cmo.getMaxCapacity()
    
def findMinConnCap(dsName):
    cd('/JDBCSystemResources/' + dsName + '/Resource/' + dsName + '/JDBCConnectionPoolParams/' + dsName)
    return cmo.getMinCapacity()
    
def findUrl(dsName):
    cd('/JDBCSystemResources/' + dsName + '/Resource/' + dsName + '/JDBCDriverParams/' + dsName)
    return cmo.getUrl()
    
def findType(dsName):
    cd('/JDBCSystemResources/' + dsName + '/Resource/' + dsName)
    return cmo.getDatasourceType()

def findSourceFile(dsName):
    cd('/JDBCSystemResources/' + dsName)
    return cmo.getSourcePath()


try:
    connect(userConfigFile='/u01/scripts/dataSourceControl/WLUserConfigFile.conf',userKeyFile='/u01/scripts/dataSourceControl/WLUserKeyFile.key')
except Exception,e:
    print "Unable to connect to Admin Server!"
    exit()
    
allServers=domainRuntimeService.getServerRuntimes();
if (len(allServers) > 0):
    for tempServer in allServers:
        jdbcServiceRT = tempServer.getJDBCServiceRuntime();
        dataSources = jdbcServiceRT.getJDBCDataSourceRuntimeMBeans();
        if (len(dataSources) > 0):
            for dataSource in dataSources:
                dsName = dataSource.getName()
                dsState = dataSource.getState()
                activeConn = dataSource.getActiveConnectionsCurrentCount()
                print 'Target Server                               : '  ,  tempServer.getName()
                if dsState == "Running":
                    print 'Name                                        : '  ,  dsName
                    print 'State                                       : '  ,  dsState
                else:
                    print 'Name                                        : '  ,  dsName
                    print 'State                                       : '  ,  dsState
                print 'Active Connections Current Count            : '  ,  activeConn
                print 'Type                                        : '  ,  findType(dsName)
                print 'Max Connections Count                       : '  ,  findMaxConnCap(dsName)
                print 'Min Connections Count                       : '  ,  findMinConnCap(dsName)
                print 'Connection Url                              : '  ,  findUrl(dsName)
                print 'Source File                                 : '  ,  findSourceFile(dsName)
                
                print '\nTesting Datasource...                         '  
                if(dataSource.testPool() == None):
                    print 'Connection Successful!\n'
                else:
                    print dataSource.testPool() , '\n'
disconnect()
exit()