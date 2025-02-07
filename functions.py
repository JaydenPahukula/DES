
def permute(input: int, table: list[int], nBits: int) -> int:
    result = 0
    for i in table:
        result = (result << 1) | ((input >> (nBits-i)) & 1)
    return result

def split(input: int, nBits: int) -> tuple[int, int]:
    mask = (1<<nBits//2)-1
    return (input>>nBits//2)&mask, input&mask

def combine(input1: int, input2: int, nBits: int) -> int:
    return (input1<<nBits//2)|(input2&((1<<nBits//2)-1))

def sBox(input: int, sBox: list[int]) -> int:
    lookupVal = (input&32)|((input&1)<<4)|((input&30)>>1)
    return sBox[lookupVal]
    
def rotate(input: int, nBits: int, numRotations = 1) -> int:
    result = input
    for _ in range(numRotations):
        result = ((result<<1)&((1<<nBits)-1))|((result>>27)&1)
    return result

def fHex(x: int, nBits: int):
    return "0x" + hex(x)[2:].upper().rjust(nBits//4,'0')

def fDec(x: int):
    return str(x).ljust(2)
