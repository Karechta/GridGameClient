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

    m_grid_width = 0
    m_grid_height = 0
    m_playercount = 0
    m_players = []

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
            magic = deserializeInt(self.m_socket, 32)

            match NetDataType(magic):
                case NetDataType.CONNECTACK: #Server sends ID to us
                    self.m_my_id = deserializeInt(self.m_socket,8)
                    self.m_connected = True
                
                case NetDataType.BROADCAST: #Server sends a String to us, lets print it
                    print(deserializeString(self.m_socket))
                
                case NetDataType.GAMESTART:
                    self.m_grid_width, self.m_grid_height = deserializeGrid(self.m_socket)
                    self.m_playercount = deserializeInt(self.m_socket, 32)
                    self.m_players.clear()
                    for _ in range(self.m_playercount):
                        player = {
                            "id": deserializeInt(self.m_socket, 8),
                            "name": deserializeString(self.m_socket)    
                        }
                        self.m_players.append(player)
                
                case NetDataType.GAMEDATA:
                    playerturn = deserializeInt(self.m_socket, 8)
                    epoch = deserializeInt(self.m_socket, 64)  
                    fields = deserializeInt(self.m_socket, 32)
                    for _ in range(fields):
                        pos_x, pos_y = deserializeGrid(self.m_socket)
                        type = deserializeInt(self.m_socket, 8)
                        owner = deserializeInt(self.m_socket, 8)
                        power = deserializeInt(self.m_socket, 16, False)
                        #TODO Feld updaten 
                    next_food = deserializeInt(self.m_socket, 32)
                    for _ in range(next_food):
                        pos_x, pos_y = deserializeGrid(self.m_socket)
                        
                           

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
                return packet
            
            case NetDataType.MOVE:
                return serializeMove(args[0], args[1], args[2], args[3], args[4])
            
            case NetDataType.ENDTURN:
                return packet
            
            case NetDataType.BROADCAST:
                return packet + serializeString(args[0])    


def serializeString(s: str):
    b = s.encode("utf-8")
    return pack("!I", len(b)) + b

def serializeMove(b:bool, from_x: int, from_y: int, to_x:int, to_y:int):
    return pack("!bHHHH", b, from_x, from_y, to_x, to_y)

def deserializeString(socket: remote):
    l, = unpack("!I", socket.recvn(4))
    return socket.recvn(l).decode("utf-8")

def deserializeGrid(socket: remote):
    w,h = unpack("!HH", socket.recvn(4))
    return w,h

def deserializeInt(socket:remote, size: int, signed:bool = False):
    f = unpack_formats[size]
    if signed: f.lower()
    i, = unpack ("!" + f, socket.recvn(size/8))

unpack_formats = {
    8: "B",
    16: "H",
    32: "I",
    64: "Q"
}
