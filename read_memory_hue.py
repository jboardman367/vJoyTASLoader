from ReadWriteMemory import ReadWriteMemory
from time import perf_counter
import pymem as pym

pmp = pym.Pymem('Hue.exe')
base_address = int(pmp.base_address)
static_address_offset = 0x00f0799c
pointer_static_address = base_address + static_address_offset

rwm = ReadWriteMemory()
process = rwm.get_process_by_name("Hue.exe")
process.open()

PTR_GameManager = process.get_pointer(pointer_static_address, offsets=[0x8, 0x0, 0x10, 0x4, 0x4c, 0x38])

def get_currentLevelName_address():
    PTR_currentLevelName_address = process.get_pointer(PTR_GameManager,offsets=[0x44])
    pointer_value = process.read(PTR_currentLevelName_address,'unit')
    return int(pointer_value)

def get_isEnabled():
    PTR_isEnabled = process.get_pointer(PTR_GameManager, offsets=[0x18, 0x144])
    pointer_value = process.read(PTR_isEnabled,'bool')
    return bool(pointer_value)

if __name__ == "__main__":
    q = perf_counter()
    for i in range(10000):
        get_isEnabled()
    print((perf_counter()-q)**-1*10000)

   # for i in range(100):
   #    get_currentLevelName_address()
   # print(perf_counter()-q)