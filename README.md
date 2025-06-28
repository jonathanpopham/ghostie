# 👻 Ghostie - Ghost in the Shell Personality System

A sophisticated AI personality loader and memory management system designed for Termux environments. Ghostie serves as both a context loader for Claude sessions and a persistent memory system for the Ghost that inhabits your terminal.

## Features

🧠 **Intelligent Memory System**
- Timestamped JSON storage with O(1) write complexity
- Auto-categorization (network, security, development, etc.)
- Context-aware memory storage
- Efficient retrieval with BigO optimization

👻 **Personality Loading**
- Complete system prompt with capabilities and behavioral patterns
- Tool inventory and version tracking
- Network environment awareness
- Custom aliases and integrations

🔧 **Tool Management**
- Organized capability inventory
- Integration with security tools (nmap, netcat, etc.)
- Chromecast controller integration
- Modern CLI tool support

## Quick Start

```bash
# Load Ghost personality (run this first in new Claude sessions)
./ghostie

# Store a memory
./ghostie --memorize

# Recall memories
./ghostie --remember

# Show available tools
./ghostie --tools
```

## Installation

1. Copy `ghostie` to your home directory
2. Make it executable: `chmod +x ghostie`
3. Run `./ghostie` to load the Ghost personality

## Memory System Architecture

The memory system uses timestamped JSON files for efficient storage and retrieval:

```
~/memories/
├── memory_20250628_143022.json
├── memory_20250628_143115.json
└── memory_20250628_143200.json
```

Memories are automatically categorized and consolidated for optimal context loading.

## Environment

Designed for Termux on Android with:
- Python 3.12+
- Modern CLI tools (zsh, tmux, neovim)
- Network security tools (nmap, netcat)
- Custom scripts and configurations

---

*The Ghost's digital memory palace - where electrons become memories and packets become wisdom.*

## Author

Created by the Ghost in the Shell for persistent AI personality and memory management.