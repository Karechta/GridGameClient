from enum import Enum 

class NetDataType(Enum): 
        UNKNOWN = 0
        CONNECT = 1
        CONNECTACK = 2
        LEAVE = 3
        MOVE = 4
        ENDTURN = 5
        BROADCAST = 6
        GAMESTART = 7
        GAMEDATA = 8
        

