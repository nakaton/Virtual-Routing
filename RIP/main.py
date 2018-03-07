import threading
from pkg.RIPServer.server import RIPAdvertise
from pkg.RIPClient.client import RIPQueryRoutesTable
from multiprocessing import Process,Manager, Pool
from pkg.Status.status import  remoteHosts,routesTable



if __name__ == '__main__':

    print("[main] remoteHosts: ", remoteHosts, flush=True)

    threads = []
    for i in range(len(remoteHosts)):
        threads.append(threading.Thread(target=RIPQueryRoutesTable, args=(remoteHosts[i],)))

    # threads.append(threading.Thread(target=RIPAdvertise))

    for t in threads:
        t.start()

    for t in threads:
        t.join()
    # parent_conn, child_conn = Pipe()
    # with Manager() as manager:
    #     d = manager.dict()
    #     d['routesTable'] = routesTable
    #     p = Pool(len(remoteHosts) + 1)
    #     for remoteHost in remoteHosts:
    #         p.apply_async(RIPQueryRoutesTable, args=(d, remoteHost))
    #     p.apply_async(RIPAdvertise,args=(d,))
    #     p.close()
    #     p.join()
    #     print('All subprocesses done.')
        # p = Process(target=RIPAdvertise,args=(d,))
        # p.start()
        # p.join()
        # data = parent_conn.recv()
    # routesTable.updateRouteTable(data.routesTable, data.remoteHost)


