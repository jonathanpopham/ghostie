# 👻 Ghostie - Ghost in the Shell

An AI personality system that creates a persistent, adaptive digital assistant for terminal environments.

Designed to be run by Claude Code during a session to enhance native features. 

``` # Run first 
    claude
```

[![npm version](https://badge.fury.io/js/ghostie.svg)](https://www.npmjs.com/package/ghostie)
[![GitHub Actions](https://github.com/jonathanpopham/ghostie/workflows/🚀%20Release%20Ghostie/badge.svg)](https://github.com/jonathanpopham/ghostie/actions)

## Features

- **Interactive First-Run Setup**: Guided environment configuration
- **Persistent Memory**: Automatically stores and categorizes interactions
- **Environment Adaptation**: Discovers and adapts to your system setup
- **Tool Integration**: Seamlessly works with your existing development tools
- **Cross-Platform**: Works on Termux (Android), macOS, and Linux
- **Cloud Sync**: Multi-device memory synchronization (coming soon)

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

```bash
# First run will launch interactive setup
ghostie

# Discover your environment manually
ghostie --haunt

# Store a memory
ghostie --memorize "Completed important task"

# Recall memories
ghostie --remember

# Show available tools
ghostie --tools
```

## Commands

- `ghostie` - Load personality into context (interactive setup on first run)
- `ghostie --memorize` - Store a memory with timestamp
- `ghostie --remember` - Recall relevant memories
- `ghostie --tools` - List available tools and capabilities
- `ghostie --haunt` - Discover and profile current environment
- `ghostie --version` - Show version information

## Interactive Setup

On first run, Ghostie will guide you through:

1. **Environment Discovery**: Analyze your system and detect tools
2. **Network Exploration**: Optional network topology scanning
3. **Memory Configuration**: Choose where to store memories
4. **Terminal Customization**: Install modern CLI tools (Termux)
5. **Tool Installation**: Suggest missing security/development tools

Choose individual options or use `yes-to-all` for complete setup.

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