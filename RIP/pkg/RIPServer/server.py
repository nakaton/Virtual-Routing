import socket
from ..Status.status import QueryCode, routesTable
import json
import threading
from ..Packet.packet import Packet
import logging

UDP_IP = "0.0.0.0"
UDP_PORT = 5005
MAX = 1024

lock = threading.Lock()
logger = logging.getLogger('udp_server')

def prepareSentData(codeType, *routesTable):
    body = None
    header = {"codeType": codeType}
    if routesTable:
        body = {
            "value": routesTable[0]
        }
    else:
        body = {
            "value": None
        }

    packet = Packet(header, body)

    return json.dumps(packet.toSerializableDict()).encode()


def getCodeRoutesTable(recvData):
    packet = None
    try:
        # packet = json.loads(recvData.decode(), object_hook= lambda obj: Packet(obj['header'], obj['body']))
        data = json.loads(recvData.decode())
        packet = Packet(data['header'],data['body'])
    except Exception as err:
        print("[Server] getCodeRoutesTable failed: ", err, flush=True)

    return packet.getHeader()['codeType'], packet.getBody()['value']


# def RIPAdvertise(d):
def RIPAdvertise():
    print("[Server]: start", flush=True)
    # routesTable = d['routesTable']
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    try:

        while True:
            print('\n[Server]: waiting to receive message', flush=True)
            recvData, addr = sock.recvfrom(MAX)
            code, recvRoutesTable= getCodeRoutesTable(recvData)
            print("[Server] queryCode: ",code, flush=True)
            if code == QueryCode.QueryRoutesTable.value:
                # sentData = prepareSentData(QueryCode.AdvertiseRoutesTable.value, d['routesTable'].getTable())
                sentData = prepareSentData(QueryCode.AdvertiseRoutesTable.value, routesTable.getTable())
                print("[Server] senddata to {} data: {} ".format(addr[0],sentData.decode()),flush=True)
                sock.sendto(sentData, addr)
            elif code == QueryCode.MockSendPacket.value:
                pass

            elif code == QueryCode.AdvertiseRoutesTable.value:
                print("[Server] get routeTable from client {} data: {}".format(addr[0],recvRoutesTable), flush=True)
                lock.acquire()
                try:
                    # d['routesTable'].updateRouteTable(recvRoutesTable, addr[0])
                    routesTable.updateRouteTable(recvRoutesTable, addr[0])

                finally:
                    lock.release()

                print('[Server]', flush=True)
                # d['routesTable'].print()
                routesTable.print()
            else:

                print("[Server] get a unknown packet and dismiss it", flush=True)
    except Exception as err:
        print("[Server] close: ", err.args,  flush=True)
    finally:
        sock.close()


if __name__ == '__main__':
    print("start",flush=True)

    RIPAdvertise()
