from tabulate import tabulate
class RoutesTable(object):
    def __init__(self,initRoutes, localHost):
        self.__host = localHost
        self.__table = initRoutes
        self.__table.append([localHost,localHost,0])
        # mockHost = '224.0.0.1'
        self.__table.append(["192.168.199.101", "192.168.199.134", 2])
        self.__change = False
        # print('routeTable host: ', self.__host, flush=True)

    def isTableEmpty(self):
        return self.__table == []

    def print(self):
        print("The router({}) routeTable: ".format(self.__host), flush=True)

        if self.isTableEmpty():
            print('No routes', flush=True)
        else:
            # print('__table: ', self.__table, flush=True)
            print(tabulate(self.__table, headers=['target', 'next hop', 'metric'], tablefmt='orgbl'), end='\n\n', flush=True)

    def updateRoute(self, route, remoteHost):
        if self.isTableEmpty():
            route[1] = remoteHost
            self.__table.append(route)
            self.change = True
        else:
            change = False
            isFound = False
            for localRouteItem in self.__table:

                # 避免路由环路
                if  route[0] == self.__host:
                    print("[updateRouteFunc]same host: ", route[0] ,flush=True)
                    return
                elif  localRouteItem[0] == route[0]:
                    isFound = True
                    if  localRouteItem[2] > route[2] + 1:
                        localRouteItem[2] = route[2] + 1
                        localRouteItem[1] = remoteHost
                        change = True
                        print("[updateRouteFunc]found condition: ",localRouteItem,flush=True)
                    break

            if not isFound:
                self.__table.append([route[0], remoteHost, route[2] + 1])
                print('[updateRouteFunc]not found condition: ',self.__table[-1],flush=True)
                change = True
            self.__change = change
            print("[updateRouteFunc] finish", flush=True)

    def updateRouteTable(self, routesTable, remoteHost):
        for route in routesTable:
            self.updateRoute(route, remoteHost)

        print("updateRouteTable", flush=True)
        self.print()

    def poisonRoute(self, remoteHost):
        for route in self.__table:
            if route[1] == remoteHost:
                # As rip protocol show , it means that it is unreachable when a remotehost metric is set to 16
                route[2] = 16

    def getTable(self):
        return self.__table[:]


    def getHost(self):
        return self.__host

    def setHost(self, host):
        self.__host = host

    def isChangeLastest(self):
        return self.__change

def formatRouteTables(routesTable):
    print(tabulate(routesTable, headers=['target', 'next hop', 'metric'], tablefmt='orgbl'), end='\n\n', flush=True)
# a = routeTable("127.0.0.1")
# b = routeTable("127.0.0.2")
# a.updateRoute(["127.0.0.3", "127.0.0.2", 2])
# a.print()
# b.updateRoute(["127.0.0.3","127.0.0.3",1])
# b.updateRouteTable(a.getTable())
# b.print()
# def RIPadvertise(ip):



