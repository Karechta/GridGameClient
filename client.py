from pwnlib.tubes.remote import remote
from netdatatype import NetDataType
from struct import pack, unpack 
import traceback

from time import sleep
class Client:
    m_server    = "localhost"
    m_port      = 8000
    m_socket    = None

    m_connected = False
    m_my_name   = None
    m_my_id     = None

    def __init__(self, adress: str, port: int, name: str):
        self.m_server   = adress
        self.m_port     = port
        self.m_my_name  = name

    def Run(self):
        while True:
            if not self.m_connected: 
                self.TryConnect()
            self.HandleReceive()
            sleep(5)


    #Try Connecting until connected
    def TryConnect(self): 
        success = False
        while not success:
            try:
                self.m_socket = remote(self.m_server, self.m_port)
                packet = self.buildPacket(NetDataType.CONNECT, "Karechta") 
                self.m_socket.send(packet)
                success = True
            except:
                sleep(5)
                print("Couldnt Connect, retrying...")

    #Handle Serverpackets
    def HandleReceive(self):
        try:
            magic, = unpack("!I", self.m_socket.recvn(4))

            match NetDataType(magic):
                case NetDataType.CONNECTACK: #Server sends ID to us
                    self.m_my_id = deserializeByte(self.m_socket)
                    self.m_connected = True
                    print("Id erhalten")
                
                case NetDataType.BROADCAST: #Server sends a String to us, lets print it
                    print(deserializeString(self.m_socket))
                
                case NetDataType.GAMESTART:
                    return "TODO"
                
                case NetDataType.GAMEDATA:
                    return "TODO"
        except:
            traceback.print_exc()
            self.m_connected = False
            self.m_socket.close()

    def buildPacket(self, typ: NetDataType, *args):
        packet = pack("!I", typ.value)
        match typ:
            case NetDataType.CONNECT:
                 return packet + serializeString(args[0])
            
            case NetDataType.LEAVE:
                return "TODO"
            
            case NetDataType.MOVE:
                return "TODO"
            
            case NetDataType.ENDTURN:
                return "TODO"
            
            case NetDataType.BROADCAST:
                return "TODO"    


def serializeString(s: str):
    b = s.encode("utf-8")
    return pack("!I", len(b)) + b

def deserializeString(socket: remote):
    l, = unpack("!I", socket.recvn(4))
    return socket.recvn(l).decode("utf-8")

def deserializeByte(socket: remote):
    b, = unpack("!B", socket.recvn(1))
    return b
