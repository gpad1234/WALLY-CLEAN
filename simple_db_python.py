"""
Simple In-Memory Database - Python Wrapper

Python interface to the C database using ctypes.

Usage:
    from simple_db_python import SimpleDB
    
    db = SimpleDB()
    db.set("name", "Alice")
    print(db.get("name"))  # Alice
    print(db.count())      # 1
"""

import ctypes
import os
import sys
from typing import Optional, List, Dict

# Determine the library name based on platform
if sys.platform == 'darwin':
    LIB_NAME = 'libsimpledb.dylib'
elif sys.platform == 'win32':
    LIB_NAME = 'simpledb.dll'
else:
    LIB_NAME = 'libsimpledb.so'

# Find the library in the current directory or bin directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_PATHS = [
    os.path.join(SCRIPT_DIR, LIB_NAME),
    os.path.join(SCRIPT_DIR, 'bin', LIB_NAME),
    os.path.join(SCRIPT_DIR, '..', 'bin', LIB_NAME),
]

# Load the shared library
lib = None
for lib_path in LIB_PATHS:
    if os.path.exists(lib_path):
        lib = ctypes.CDLL(lib_path)
        break

if lib is None:
    raise RuntimeError(f"Could not find {LIB_NAME}. Please compile the library first.")

# ============================================================================
# C Structure Definitions
# ============================================================================

class DBStats(ctypes.Structure):
    """Database statistics structure"""
    _fields_ = [
        ("total_entries", ctypes.c_size_t),
        ("total_collisions", ctypes.c_size_t),
        ("max_chain_length", ctypes.c_size_t),
        ("used_buckets", ctypes.c_size_t),
    ]

# ============================================================================
# C Function Signatures
# ============================================================================

# Database* db_create(void)
lib.db_create.argtypes = []
lib.db_create.restype = ctypes.c_void_p

# void db_destroy(Database *db)
lib.db_destroy.argtypes = [ctypes.c_void_p]
lib.db_destroy.restype = None

# bool db_set(Database *db, const char *key, const char *value)
lib.db_set.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
lib.db_set.restype = ctypes.c_bool

# const char* db_get(Database *db, const char *key)
lib.db_get.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
lib.db_get.restype = ctypes.c_char_p

# bool db_delete(Database *db, const char *key)
lib.db_delete.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
lib.db_delete.restype = ctypes.c_bool

# bool db_exists(Database *db, const char *key)
lib.db_exists.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
lib.db_exists.restype = ctypes.c_bool

# size_t db_count(Database *db)
lib.db_count.argtypes = [ctypes.c_void_p]
lib.db_count.restype = ctypes.c_size_t

# void db_clear(Database *db)
lib.db_clear.argtypes = [ctypes.c_void_p]
lib.db_clear.restype = None

# char** db_keys(Database *db, size_t *count)
lib.db_keys.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t)]
lib.db_keys.restype = ctypes.POINTER(ctypes.c_char_p)

# DBStats db_stats(Database *db)
lib.db_stats.argtypes = [ctypes.c_void_p]
lib.db_stats.restype = DBStats

# void db_print(Database *db)
lib.db_print.argtypes = [ctypes.c_void_p]
lib.db_print.restype = None

# ============================================================================
# Python Wrapper Class
# ============================================================================

class SimpleDB:
    """Python wrapper for the simple in-memory database"""
    
    def __init__(self):
        """Create a new database instance"""
        self._db = lib.db_create()
        if not self._db:
            raise MemoryError("Failed to create database")
    
    def __del__(self):
        """Destroy the database when the object is garbage collected"""
        if hasattr(self, '_db') and self._db:
            lib.db_destroy(self._db)
            self._db = None
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.__del__()
        return False
    
    def set(self, key: str, value: str) -> bool:
        """
        Set a key-value pair in the database
        
        Args:
            key: The key (max 256 characters)
            value: The value (max 4096 characters)
            
        Returns:
            True if successful, False otherwise
        """
        if not isinstance(key, str) or not isinstance(value, str):
            raise TypeError("Key and value must be strings")
        
        return lib.db_set(
            self._db,
            key.encode('utf-8'),
            value.encode('utf-8')
        )
    
    def get(self, key: str) -> Optional[str]:
        """
        Get a value by key
        
        Args:
            key: The key to look up
            
        Returns:
            The value if found, None otherwise
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        
        result = lib.db_get(self._db, key.encode('utf-8'))
        return result.decode('utf-8') if result else None
    
    def delete(self, key: str) -> bool:
        """
        Delete a key-value pair
        
        Args:
            key: The key to delete
            
        Returns:
            True if deleted, False if key not found
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        
        return lib.db_delete(self._db, key.encode('utf-8'))
    
    def exists(self, key: str) -> bool:
        """
        Check if a key exists
        
        Args:
            key: The key to check
            
        Returns:
            True if key exists, False otherwise
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        
        return lib.db_exists(self._db, key.encode('utf-8'))
    
    def count(self) -> int:
        """
        Get the number of entries in the database
        
        Returns:
            The number of key-value pairs
        """
        return lib.db_count(self._db)
    
    def clear(self):
        """Clear all entries from the database"""
        lib.db_clear(self._db)
    
    def keys(self) -> List[str]:
        """
        Get all keys in the database
        
        Returns:
            List of all keys
        """
        count = ctypes.c_size_t()
        keys_ptr = lib.db_keys(self._db, ctypes.byref(count))
        
        if not keys_ptr or count.value == 0:
            return []
        
        # Extract keys from C array
        keys = []
        for i in range(count.value):
            key = keys_ptr[i]
            if key:
                keys.append(key.decode('utf-8'))
        
        # Free the array (but not the strings, they belong to the database)
        ctypes.pythonapi.PyMem_Free(keys_ptr)
        
        return keys
    
    def items(self) -> Dict[str, str]:
        """
        Get all key-value pairs
        
        Returns:
            Dictionary of all key-value pairs
        """
        result = {}
        for key in self.keys():
            value = self.get(key)
            if value is not None:
                result[key] = value
        return result
    
    def stats(self) -> dict:
        """
        Get database statistics
        
        Returns:
            Dictionary with statistics:
            - total_entries: Number of entries
            - used_buckets: Number of hash buckets in use
            - total_collisions: Number of hash collisions
            - max_chain_length: Longest collision chain
        """
        stats = lib.db_stats(self._db)
        return {
            'total_entries': stats.total_entries,
            'used_buckets': stats.used_buckets,
            'total_collisions': stats.total_collisions,
            'max_chain_length': stats.max_chain_length,
        }
    
    def print(self):
        """Print database contents (for debugging)"""
        lib.db_print(self._db)
    
    def __len__(self):
        """Support len() function"""
        return self.count()
    
    def __contains__(self, key):
        """Support 'in' operator"""
        return self.exists(key)
    
    def __getitem__(self, key):
        """Support db[key] syntax"""
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value
    
    def __setitem__(self, key, value):
        """Support db[key] = value syntax"""
        if not self.set(key, value):
            raise RuntimeError(f"Failed to set key: {key}")
    
    def __delitem__(self, key):
        """Support del db[key] syntax"""
        if not self.delete(key):
            raise KeyError(key)
    
    def __repr__(self):
        """String representation"""
        return f"<SimpleDB entries={self.count()}>"


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    print("Simple In-Memory Database - Python Interface")
    print("=" * 50)
    print()
    
    # Create database
    db = SimpleDB()
    print(f"✓ Created database: {db}")
    print()
    
    # Test SET operations
    print("Testing SET operations...")
    db.set("name", "Alice")
    db.set("age", "30")
    db.set("city", "New York")
    db["country"] = "USA"  # Using dict-like syntax
    print(f"✓ Added {db.count()} entries")
    print()
    
    # Test GET operations
    print("Testing GET operations...")
    print(f"name => {db.get('name')}")
    print(f"age => {db['age']}")  # Using dict-like syntax
    print(f"city => {db.get('city')}")
    print(f"missing => {db.get('missing')}")
    print()
    
    # Test UPDATE operation
    print("Testing UPDATE operation...")
    db.set("age", "31")
    print(f"age => {db.get('age')} (updated)")
    print()
    
    # Test EXISTS operation
    print("Testing EXISTS operation...")
    print(f"exists('name') => {db.exists('name')}")
    print(f"'name' in db => {'name' in db}")
    print(f"'missing' in db => {'missing' in db}")
    print()
    
    # Test KEYS operation
    print("Testing KEYS operation...")
    keys = db.keys()
    print(f"Keys: {keys}")
    print()
    
    # Test ITEMS operation
    print("Testing ITEMS operation...")
    items = db.items()
    for key, value in items.items():
        print(f"  {key} => {value}")
    print()
    
    # Test DELETE operation
    print("Testing DELETE operation...")
    db.delete("city")
    print(f"✓ Deleted 'city'")
    print(f"Count after delete: {db.count()}")
    print()
    
    # Statistics
    print("Database Statistics:")
    stats = db.stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()
    
    # Performance test
    print("Performance test: Adding 1000 entries...")
    for i in range(1000):
        db.set(f"key_{i}", f"value_{i}")
    print(f"✓ Added 1000 entries")
    print(f"Total count: {len(db)}")
    print()
    
    # Final statistics
    print("Final Statistics:")
    stats = db.stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    if stats['used_buckets'] > 0:
        avg_chain = stats['total_entries'] / stats['used_buckets']
        print(f"  avg_chain_length: {avg_chain:.2f}")
    print()
    
    # Test CLEAR operation
    print("Testing CLEAR operation...")
    db.clear()
    print("✓ Database cleared")
    print(f"Count after clear: {db.count()}")
    print()
    
    # Context manager test
    print("Testing context manager...")
    with SimpleDB() as temp_db:
        temp_db.set("temp", "value")
        print(f"Temp DB count: {temp_db.count()}")
    print("✓ Context manager cleanup complete")
