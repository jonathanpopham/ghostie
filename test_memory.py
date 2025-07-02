#!/usr/bin/env python3
import json
import datetime
from pathlib import Path

# Test the memory creation directly
memory_dir = Path.home() / ".ghostie" / "memories"
memory_dir.mkdir(parents=True, exist_ok=True)

timestamp = datetime.datetime.now()
memory_file = memory_dir / f"memory_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"

print(f"Creating memory file: {memory_file}")

# Import the GhostInShell class
exec(open('ghostie').read())

# Create instance and test
ghost = GhostInShell()
ghost.memorize("Test memory with #tags and [[links]]")