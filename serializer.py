from struct import * 
from netdatatype import NetDataType

class Serializer:

    def buildPacket(typ: NetDataType, *args):
        packet = pack("!I", typ.value)
        match typ:
            case NetDataType.UNKNOWN:
                return "???"
            
            case NetDataType.CONNECT:
                 return packet + Serializer.serializeString(args[0])
            
            case NetDataType.CONNECTACK:
                return ""
            
            case NetDataType.LEAVE:
                return ""
            
            case NetDataType.MOVE:
                return ""
            
            case NetDataType.ENDTURN:
                return ""
            
            case NetDataType.BROADCAST:
                return ""
            
            case NetDataType.GAMESTART:
                return ""
            
            case NetDataType.GAMEDATA:
                return ""

    def serializeString(s: str):
        b = s.encode("utf-8")
        return pack("!I", len(b)) + b


