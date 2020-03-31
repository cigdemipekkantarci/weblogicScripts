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
    connect("weblogic","weblogic123","t3://localhost:7001")
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
                    print 'Name\033[1;32m                                        : '  ,  dsName  , '\033[1;m'
                    print 'State\033[1;32m                                       : '  ,  dsState , '\033[1;m'
                else:
                    print 'Name\033[1;31m                                        : '  ,  dsName  , '\033[1;m'
                    print 'State\033[1;31m                                       : '  ,  dsState , '\033[1;m'
                print 'Active Connections Current Count            : '  ,  activeConn
                print 'Type                                        : '  ,  findType(dsName)
                print 'Max Connections Count                       : '  ,  findMaxConnCap(dsName)
                print 'Min Connections Count                       : '  ,  findMinConnCap(dsName)
                print 'Connection Url                              : '  ,  findUrl(dsName)
                print 'Source File                                 : '  ,  findSourceFile(dsName)
                
                print '\nTesting Datasource...                         '  
                if(dataSource.testPool() == None):
                    print '\033[1;32mConnection Successful!\n\033[1;m'
                else:
                    print dataSource.testPool() , '\n'
disconnect()
exit()