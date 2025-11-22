#!/usr/bin/env python3
"""
Example: Using SimpleDB from Python
Demonstrates practical usage of the in-memory database
"""

from simple_db_python import SimpleDB

def main():
    # Create a database
    db = SimpleDB()
    
    # Store user data
    print("Storing user data...")
    db.set("user:1:name", "Alice Johnson")
    db.set("user:1:email", "alice@example.com")
    db.set("user:1:age", "30")
    
    db.set("user:2:name", "Bob Smith")
    db.set("user:2:email", "bob@example.com")
    db.set("user:2:age", "25")
    
    # Dictionary-like syntax also works
    db["user:3:name"] = "Charlie Brown"
    db["user:3:email"] = "charlie@example.com"
    db["user:3:age"] = "35"
    
    print(f"✓ Stored data for {db.count()} keys\n")
    
    # Retrieve user data
    print("User 1:")
    print(f"  Name: {db['user:1:name']}")
    print(f"  Email: {db.get('user:1:email')}")
    print(f"  Age: {db.get('user:1:age')}\n")
    
    # Check if user exists
    if "user:2:name" in db:
        print(f"User 2 exists: {db['user:2:name']}\n")
    
    # Update data
    db.set("user:1:age", "31")
    print(f"Updated user 1 age to {db['user:1:age']}\n")
    
    # List all keys
    print("All keys:")
    for key in sorted(db.keys()):
        print(f"  {key}")
    print()
    
    # Get all data
    print("All key-value pairs:")
    for key, value in sorted(db.items().items()):
        print(f"  {key} => {value}")
    print()
    
    # Statistics
    stats = db.stats()
    print("Database Statistics:")
    print(f"  Entries: {stats['total_entries']}")
    print(f"  Buckets used: {stats['used_buckets']}/1024")
    print(f"  Collisions: {stats['total_collisions']}")
    print(f"  Max chain: {stats['max_chain_length']}\n")
    
    # Delete a user
    del db["user:2:name"]
    del db["user:2:email"]
    del db["user:2:age"]
    print(f"✓ Deleted user 2. Remaining entries: {len(db)}\n")
    
    # Use as context manager (auto cleanup)
    print("Using context manager:")
    with SimpleDB() as temp_db:
        temp_db.set("temp_key", "temp_value")
        print(f"  Temp database has {len(temp_db)} entry")
    print("  ✓ Temp database auto-cleaned\n")

if __name__ == "__main__":
    main()
