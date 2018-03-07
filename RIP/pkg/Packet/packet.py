# from ..RoutesTable.routesTable import RoutesTable
from ..Status.status import QueryCode

class Packet(object):
    # header format: {codeType: xxx, }
    # body format: {value: xxx}
    def __init__(self, *args):
        if len(args) >= 1 and isinstance(args[0], dict) and  'codeType' in args[0]:
            self.__header = args[0]
        else:
            self.__header = {'codeType': QueryCode.Unknown.value}

        if len(args) >= 2 and isinstance(args[1], dict) and  'value' in args[1]:
            self.__body = args[1]
        else:
            self.__body = {"value": None}
        # print("[packet]: \nheader {} \n body:{}".format(self.__header, self.__body), flush=True)

    def setBody(self, data):
        self.__body = data

    def setHeader(self, codeType):
        self.__header['codeType'] = codeType

    def toSerializableDict(self):
        return {
            "header": self.__header,
            "body"  : self.__body

        }

    def getHeader(self):
        return self.__header.copy()


    def getBody(self):
        return self.__body.copy()

    # def jsonParse(self, obj):
    #     return Packet(obj.header, obj.body)

    if __name__ == '__main__':
        pass

