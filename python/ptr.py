from ctypes import *

def get_dlls():
    names = "d2client d2common d2gfx d2lang d2win d2net d2game d2launch fog\
             bnclient storm d2cmp d2multi".split()
    addrs = {}
    for name in names:
        name+=".dll"
        hmod = windll.kernel32.GetModuleHandleA(name)
        if not hmod: hmod = windll.kernel32.LoadLibraryA(name)
        if not hmod: raise RuntimeError("could not load "+name)
        addrs[name]=hmod
    return addrs
base = get_dlls()

def offset(dll_name, p):
    pass
def ordinal(dll_name, o):
    pass

class GameInfo(Structure):
    _fields_ = [
        ("_1",      c_uint*6),
        ("_2",      c_ushort),
        ("name",    c_char*0x18),
        ("ip",      c_char*0x56), # only name seems to be read correctly
        ("account", c_char*0x30), # bug?
        ("char",    c_char*0x18),
        ("realm",   c_char*0x18),
        ("_2",      c_byte*0x158), # d2bs has WAY more detailed version of this
        ("password",c_char*0x18)
    ]
def getGameInfo():
    f = WINFUNCTYPE(POINTER(GameInfo))(base["d2client.dll"]+0x108B0)
    return f().contents

#getGameInfo = stdcall(POINTER(GameInfo),offset("d2client.dll",0x108B0))
class UnitAny(Structure):
    pass
UnitAny._fields_ = [
    ("unitType",    c_uint),
    ("txtFileNo",   c_uint),
    ("_1",          c_uint),
    ("unitId",      c_uint),
    ("mode",        c_uint),
    ("unitData",    POINTER(c_uint)),
    ("act",         c_uint),
    ("actP",        POINTER(c_int)),
    ("seed",        c_uint*2),
    ("_2",          c_int),
    ("path",        POINTER(c_uint)),
    ("_3",          c_uint*5),
    ("gfxFrame",    c_int),
    ("frameRemain", c_int),
    ("frameRate",   c_ushort),
    ("_4",          c_int),
    ("pGfxUnk",     POINTER(c_byte)),
    ("pGfxInfo",    POINTER(c_uint)),
    ("_5",          c_uint),
    ("statList",    POINTER(c_int)),
    ("inventory",   POINTER(c_int)),
    ("light",       POINTER(c_int)),
    ("_6",          c_uint*9),
    ("X",           c_ushort),
    ("Y",           c_ushort),
    ("_7",          c_uint),
    ("ownerType",   c_uint),
    ("ownerId",     c_uint),
    ("_8",          c_uint*2),
    ("overheadMsg", POINTER(c_int)),
    ("info",        POINTER(c_int)),
    ("_9",          c_uint*6),
    ("flags",       c_uint),
    ("flags2",      c_uint),
    ("_10",         c_uint*5),
    ("changedNext", POINTER(UnitAny)),
    ("roomNext",    POINTER(UnitAny)),
    ("listNext",    POINTER(UnitAny))]

                  
getDifficulty = WINFUNCTYPE(c_byte)(base["d2client.dll"]+0x41930)

playerUnit = cast(get_dlls()["d2client.dll"]+0x11BBFC, POINTER(UnitAny))
mouseX = cast(base["d2client.dll"]+0x11B828, POINTER(c_uint)).contents
mouseY = cast(base["d2client.dll"]+0x11B824, POINTER(c_uint)).contents
