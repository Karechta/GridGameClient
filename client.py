from pwnlib.tubes import remote
from netdatatype import NetDataType
from serializer import Serializer

class Client:
    m_connected = False
    m_server = "localhost"
    m_socket  = None

    def __init__(self):
        ""

    def TryConnect(self, adress: str):
        self.m_socket = remote.remote(adress, 8888)
        packet = Serializer.buildPacket(NetDataType.CONNECT, "Karechta")
        self.m_socket.send(packet)


    def Connect():
        ""

    def HandleReceive():
        ""
