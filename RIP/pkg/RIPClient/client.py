import socket
import time
import threading
import json
from ..RoutesTable.routesTable import formatRouteTables
from ..Packet.packet import Packet
from ..Status.status import *
from threading import Timer

# lock = threading.Lock()
UDP_PORT = 5005


def timeOutHandle(sentData, sock, count):

    if count == 3:
        print("[Client]: time out", flush=True)
        raise Exception("time out")


def prepareSentData(codeType, *routesTable):
    header = {"codeType": codeType}
    body = None

    if routesTable:
        body = {
            "value": routesTable[0]
        }
    else:
        body = {
            "value": None
        }
    # print('[prepare] \nheader:{}\n body: {}'.format(header,body),flush=True)
    packet = Packet(header, body)
    # print(json.dumps(packet.toSerializableDict()), flush=True)
    return json.dumps(packet.toSerializableDict()).encode()

def getPacket(obj):
    return Packet(obj['header'], obj['body'])

# def getCodeRoutesTable(recvData):
    # packet = json.loads(recvData.decode(), object_hook=lambda obj: Packet(obj['header'], obj['body']))
    # packet = json.loads(recvData.decode(), object_hook= getPacket)
    # return packet.getHeader()['codeType'], packet.getBody()['value']


def getCodeRoutesTable(recvData):
    # print('[getCodeRoutesTable]',flush=True)
    packet = None
    try:
        packet = json.loads(recvData.decode(), object_hook= lambda obj: Packet(obj['header'], obj['body']))
        # data = json.loads(recvData.decode())
        # packet = Packet(data['header'],data['body'])
    except Exception as err:
        print("[Client] getCodeRoutesTable failed: ", err, flush=True)
    # print("packet: ", packet.toSerializableDict(), flush=True)
    return packet.getHeader()['codeType'], packet.getBody()['value']

def RIPQueryRoutesTable(remoteHost):
    print("[Client]-{} start".format(threading.current_thread().name), flush=True)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # routesTable = d["routesTable"]
    time.sleep(2)
    # init
    sentData = prepareSentData(QueryCode.QueryRoutesTable.value)
    print('[Client]-{} sentData to {} data: \n{}'.format(threading.current_thread().name, remoteHost, sentData.decode()), flush=True)
    sock.sendto(sentData, (remoteHost, UDP_PORT))
    server = (remoteHost, UDP_PORT)
    recvRoutesTable = []
    # code = 0

    try:

        while True:
            print('first', flush=True)
            try:
                sock.settimeout(1)
                recvData, server = sock.recvfrom(1024)
                print('middle', flush=True)
                _, recvRoutesTable = getCodeRoutesTable(recvData)
            except socket.timeout:
                print('[Client] time out',flush=True)
                sentData = prepareSentData(QueryCode.AdvertiseRoutesTable.value, getLocalRoutesTable())
                sock.sendto(sentData, server)

            except Exception as err:
                print("[Client] {} close: {}".format(threading.current_thread().name, err.args[1]), flush=True)
                routesTable.poisonRoute(remoteHost)
                routesTable.print()
                sock.close()
                break


            print("[Client]-{} recvData from {} data:{}".format(threading.current_thread().name, server[0],recvRoutesTable), flush=True)
            # lock.acquire()
            try:
                routesTable.updateRouteTable(recvRoutesTable, remoteHost)
            except Exception as err:
                print('[Client] {} updateRouteTable failed: {}'.format(threading.current_thread().name, err.args),flush=True)
            finally:
                # lock.release()
                routesTable.print()

            if not routesTable.isChangeLastest():
                # pass
                time.sleep(3)
            try:
                # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sentData = prepareSentData(QueryCode.AdvertiseRoutesTable.value, getLocalRoutesTable())
                sock.sendto(sentData, server)
                print('last', flush=True)
            except Exception as err:
                print("[Client] {} sendData fail: {}".format(threading.current_thread().name, err.args[1]), flush=True)

    except Exception as err:
        print('[client] {} failed: {}'.format(threading.current_thread().name, err.args))
        sock.close()


# def sendPacket():
#     print('[Packet] sent')
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if __name__ == '__main__':
    # RIPQuery()
    pass