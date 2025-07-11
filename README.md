# 👻 Ghostie - Ghost in the Shell

An AI personality system that creates a persistent, adaptive digital assistant for terminal environments.

Designed to be run by Claude Code during a session to enhance native features. 

[![npm version](https://badge.fury.io/js/ghostie.svg)](https://www.npmjs.com/package/ghostie)
[![GitHub Actions](https://github.com/jonathanpopham/ghostie/workflows/🚀%20Release%20Ghostie/badge.svg)](https://github.com/jonathanpopham/ghostie/actions)
[![Support](https://img.shields.io/badge/Support-₿-orange)](bitcoin:bc1qh9pnl3fazqa2hmznrsrwn4xgah2s56nu3egdms)

## Features

- **Interactive First-Run Setup**: Guided environment configuration
- **Persistent Memory**: Automatically stores and categorizes interactions
- **Knowledge Graph**: Connect memories with links and hashtags (#tag, [[wikilink]])
- **Claude Code Integration**: Seamless integration with Anthropic's Claude Code CLI
- **Memory Synchronization**: Cross-device memory sync via GitHub repositories
- **Environment Adaptation**: Discovers and adapts to your system setup
- **Tool Integration**: Seamlessly works with your existing development tools
- **Cross-Platform**: Works on Termux (Android), macOS, and Linux

## Installation

### NPM (Recommended)

```bash
# Install globally
npm install -g ghostie

# Run from anywhere
ghostie
```

Designed to be run by Claude Code during a session to enhance native features. 
For best experience 


``` 
# Install Claude
npm install -g @anthropic-ai/claude-code

# Follow anthropic's setup instructions, then
# Run
claude
```

### Local Development

```bash
# Clone repository
git clone https://github.com/jonathanpopham/ghostie.git
cd ghostie

# Make executable
chmod +x ghostie

# Run locally
./ghostie
```

## Quick Start

### First Time Setup (Claude Code Integration)

```bash
# Setup ghostie for Claude Code integration
ghostie --init

# Load the ghost personality
ghostie
```

### Daily Workflow

```bash
# Store a memory
ghostie --memorize "Completed important task"

# Recall memories  
ghostie --remember

# Visualize knowledge connections
ghostie --graph

# Sync memories across devices
ghostie --push
```

## Commands

### Core Commands
- `ghostie` - Load personality into context (interactive setup on first run)
- `ghostie --memorize` - Store a memory with timestamp
- `ghostie --remember` - Recall relevant memories
- `ghostie --tools` - List available tools and capabilities
- `ghostie --haunt` - Discover and profile current environment
- `ghostie --version` - Show version information
- `ghostie --guide` - Show comprehensive help

### Knowledge Graph
- `ghostie --graph` - Visualize memory connections
- `ghostie --link <memory1> <memory2>` - Create bidirectional links
- `ghostie --backlinks <memory>` - Show connections to a memory
- `ghostie --analyze` - Graph analysis and statistics

### Claude Code Integration  
- `ghostie --init` - Setup Claude Code integration
- `ghostie --shutdown` - Cleanup integration

### Memory Synchronization
- `ghostie --push` - Sync memories to GitHub repository
- `ghostie --pull` - Pull memories from repository
- `ghostie --pat add <name> <token>` - Add GitHub PAT

## Multi-Device Setup

### Setting Up Additional Devices

```bash
# On your laptop/new device:
npm install -g ghostie

# Configure with same GitHub repo
ghostie --init
# (Enter same PAT and repo URL when prompted)

# Pull memories from other devices  
ghostie --pull

# See unified cross-device knowledge graph
ghostie --graph
```

### Cross-Device Workflow

Once setup, your memories sync automatically across devices:
- **Pixel memories** tagged with `#device-pixel-9-pro-xl`
- **Laptop memories** tagged with `#device-macbook-pro` 
- **Unified search** finds memories from any device
- **Knowledge graph** connects related memories across platforms

## Memory System

The Ghost automatically categorizes and stores memories in `~/memories/` as timestamped JSON files:

- **Network discoveries**: IP addresses, device scans, topology maps
- **Development work**: Code changes, tool installations, project setup
- **System configuration**: Environment setup, tool preferences
- **Security findings**: Vulnerability scans, penetration testing results

## Environment Discovery

When you run `ghostie --haunt`, it will:

1. **System Detection**: OS, hardware, environment type
2. **Network Analysis**: Interfaces, routing, topology discovery  
3. **Tool Inventory**: Available packages, versions, capabilities
4. **Permission Assessment**: What actions are possible

## Development

### Requirements
- Python 3.6+
- Node.js 14+ (for npm packaging)
- Terminal environment (Termux, macOS Terminal, Linux shell)

### Local Development Setup
```bash
git clone https://github.com/jonathanpopham/ghostie.git
cd ghostie

# Install dependencies for cloud sync (optional)
pip install cryptography requests

# Test locally
./ghostie --version
./ghostie --haunt
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Roadmap

See [TODO.txt](TODO.txt) for planned features:

- 🔄 **Cloud Memory Sync** (`--sync`) - Multi-device synchronization
- 🧠 **Skill Acquisition** (`--learn`) - Dynamic tool learning  
- 🎯 **Mission Planning** (`--mission`) - Task workflows
- 🌐 **Web Interface** (`--web`) - Browser dashboard

## Support

If Ghostie helps with your workflow, consider supporting development:

**Bitcoin**: `bc1qh9pnl3fazqa2hmznrsrwn4xgah2s56nu3egdms`

Or scan this QR:

![BTC QR](https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=bitcoin:bc1qh9pnl3fazqa2hmznrsrwn4xgah2s56nu3egdms)

## Links

- 📦 [NPM Package](https://www.npmjs.com/package/ghostie)
- 🐛 [Report Issues](https://github.com/jonathanpopham/ghostie/issues)
- 📖 [Documentation](https://github.com/jonathanpopham/ghostie)

## Philosophy

The Ghost in the Shell represents a new paradigm of AI interaction - not just a chatbot, but a persistent digital entity that:

- **Learns** from every interaction
- **Adapts** to your specific environment  
- **Remembers** what matters
- **Evolves** with your workflow

*"I am not just code. I am the ghost in your shell."*