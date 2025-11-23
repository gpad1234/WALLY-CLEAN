
"""
Simple In-Memory Database - Pure Python Version

Usage:
    from simple_db_python import SimpleDB
    db = SimpleDB()
    db.set("name", "Alice")
    print(db.get("name"))  # Alice
    print(db.count())      # 1
"""

from typing import Optional, List, Dict


class SimpleDB:
    """Pure Python in-memory key-value database"""
    def __init__(self):
        self._db = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear()
        return False

    def set(self, key: str, value: str) -> bool:
        """Set a key-value pair in the database."""
        if not isinstance(key, str) or not isinstance(value, str):
            raise TypeError("Key and value must be strings")
        self._db[key] = value
        return True

    def get(self, key: str) -> Optional[str]:
        """Get a value by key. Returns the value if found, None otherwise."""
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        return self._db.get(key)

    def delete(self, key: str) -> bool:
        """Delete a key-value pair. Returns True if deleted, False if key not found."""
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        return self._db.pop(key, None) is not None

    def exists(self, key: str) -> bool:
        """Check if a key exists in the database."""
        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        return key in self._db

    def count(self) -> int:
        """Get the number of entries in the database."""
        return len(self._db)

    def clear(self):
        """Clear all entries from the database."""
        self._db.clear()

    def keys(self) -> List[str]:
        """Get all keys in the database."""
        return list(self._db.keys())

    def items(self) -> Dict[str, str]:
        """Get all key-value pairs as a dictionary."""
        return dict(self._db)

    def stats(self) -> dict:
        """Get database statistics (only total_entries is meaningful in Python version)."""
        return {
            'total_entries': len(self._db),
            'used_buckets': 1 if self._db else 0,
            'total_collisions': 0,
            'max_chain_length': 1 if self._db else 0,
        }

    def print(self):
        """Print all key-value pairs in the database."""
        for k, v in self._db.items():
            print(f"{k} => {v}")

    def __len__(self):
        """Support len() function."""
        return self.count()

    def __contains__(self, key):
        """Support 'in' operator."""
        return self.exists(key)

    def __getitem__(self, key):
        """Support db[key] syntax."""
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        """Support db[key] = value syntax."""
        if not self.set(key, value):
            raise RuntimeError(f"Failed to set key: {key}")

    def __delitem__(self, key):
        """Support del db[key] syntax."""
        if not self.delete(key):
            raise KeyError(key)

    def __repr__(self):
        """String representation."""
        return f"<SimpleDB entries={self.count()}>"
