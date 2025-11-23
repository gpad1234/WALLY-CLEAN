import ctypes
import os

# Path to the DLL
DLL_PATH = os.path.join('bin', 'simpledb.dll')
print('[TEST] Loading DLL from:', DLL_PATH)

try:
    lib = ctypes.CDLL(DLL_PATH)
    print('[TEST] DLL loaded successfully.')

    # Try calling db_create (adjust if your DLL exports a different function)
    try:
        lib.db_create.restype = ctypes.c_void_p
        db = lib.db_create()
        print('[TEST] db_create() returned:', db)
    except Exception as e:
        print('[TEST] Error calling db_create:', e)
except Exception as e:
    print('[TEST] Failed to load DLL:', e)
