from ..RoutesTable.routesTable import RoutesTable
from enum import Enum, unique
import sys

# ------------------------ util Func-----------------------------------
def getHost():
    localHostIndex = sys.argv.index('-h') + 1
    remoteHostsStartIndex = sys.argv.index('-r') + 1
    localHost = sys.argv[localHostIndex]
    remoteHosts = None

    if localHostIndex < remoteHostsStartIndex:
        remoteHosts = sys.argv[remoteHostsStartIndex:]
    else:
        remoteHosts = sys.argv[remoteHostsStartIndex : localHostIndex - 1]

    for index, remoteHost in enumerate(remoteHosts):
        if remoteHost == localHost:
            remoteHosts.pop(index)

    return (localHost, remoteHosts)


def getInitRoute(localHost, remoteHosts):
    routes = []
    for  remoteHost in remoteHosts:
        routes.append([remoteHost, remoteHost, 1])


    return routes

def getLocalRoutesTable():
    return routesTable.getTable()

# ------------------------ init data-----------------------------------
@unique
class QueryCode(Enum):
    QueryRoutesTable     = 0
    AdvertiseRoutesTable = 1
    MockSendPacket       = 2
    Unknown              = 3



localHost, remoteHosts = getHost()
routes = getInitRoute(localHost,remoteHosts)
print("[Status] routes: \n", routes, flush=True)

routesTable = RoutesTable(routes, localHost)
routesTable.print()







