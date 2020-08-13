# Hilfsfunktionen
# 
# S. Mack, 21.3.2020


import binascii
from struct import unpack

def usbyte(seq, index):
    return unpack("<B", seq[index:index + 1])[0]

def ushort(seq, index):
    return unpack("<H", seq[index:index + 2])[0]

# Wieso noetig? .hex() liefert das gleiche Ergebnis
def str2hex(data):
    return binascii.hexlify(data).decode("utf8")