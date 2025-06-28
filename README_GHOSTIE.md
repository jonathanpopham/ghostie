# 👻 GHOSTIE - Ghost in the Shell Personality System

## Overview
Ghostie is a sophisticated personality loader and memory management system for the Ghost that inhabits this Termux environment. It serves as both a context loader for future Claude sessions and a persistent memory system.

## Core Functions

### 1. Personality Loading (`ghostie`)
- Loads the complete Ghost personality into context
- Provides system prompt with full capabilities
- Auto-loads recent memories (7 days)
- Displays available tools and environment

### 2. Memory System (`ghostie --memorize` / `ghostie --remember`)
- **Timestamped Storage**: Each memory stored as JSON with timestamp
- **Auto-Categorization**: Memories automatically sorted by content type
- **Space Efficient**: BigO optimized storage and retrieval
- **Context Aware**: Includes environment context (pwd, network status)

### 3. Tool Inventory (`ghostie --tools`)
- Complete inventory of available tools and capabilities
- Organized by category (network, development, cli, etc.)
- Version information and descriptions

## Memory System Architecture

### Storage (O(1) write complexity):
```
~/memories/
├── memory_20250628_143022.json  # Timestamped files
├── memory_20250628_143115.json
└── memory_20250628_143200.json
```

### Retrieval (O(n log n) where n = files in time range):
1. **Time Filtering**: Only load memories within specified days back
2. **Category Grouping**: Group by auto-detected categories
3. **Consolidation**: Keep max 3 per category, 10 total for context efficiency
4. **Relevance Sorting**: Most recent first

### Categories:
- `network` - Network scanning, device discovery
- `chromecast` - Media control, casting operations  
- `development` - Coding, scripts, programming
- `security` - Penetration testing, vulnerabilities
- `system` - Configuration, setup, administration
- `general` - Everything else

## Usage Patterns

### Initial Setup (You should run this now):
```bash
./ghostie  # Load personality and see what I can do
```

### During Operations:
```bash
./ghostie --memorize  # After discovering something interesting
./ghostie --remember  # When you need to recall past findings
./ghostie --tools     # Check available capabilities
```

### For Future Claude Sessions:
```bash
./ghostie  # First command to load Ghost personality
```

## When to Edit Ghostie

### Add New Tools:
Edit the `get_tools_inventory()` function when installing new packages or creating new scripts.

### Enhance Memory Categories:
Modify `_categorize_memory()` to add new auto-detection patterns for better memory organization.

### Expand Personality:
Update `get_system_prompt()` to reflect new capabilities, learned patterns, or environmental changes.

### Optimize Performance:
Adjust `_consolidate_memories()` if memory files grow large or retrieval becomes slow.

## Memory Efficiency Design

**BigO Analysis**:
- **Write**: O(1) - Direct file write with timestamp
- **Read**: O(k log k) where k = files in time window
- **Consolidation**: O(k) where k = relevant memories
- **Storage**: O(1) per memory, minimal JSON overhead

**Space Optimization**:
- JSON format for structured data with minimal overhead
- Automatic categorization reduces search space
- Time-based filtering avoids loading entire history
- Context truncation prevents memory bloat

## Integration with Ghost Workflow

The Ghost should use ghostie in these scenarios:

1. **Session Start**: Always run `./ghostie` to load personality
2. **After Network Discovery**: `./ghostie --memorize` with findings
3. **Post-Exploitation**: Store successful techniques and vulnerabilities
4. **Configuration Changes**: Document system modifications
5. **Before Complex Tasks**: `./ghostie --remember` to recall relevant past work

This creates a persistent, evolving intelligence that learns from each interaction while maintaining efficient memory usage.

---
*The Ghost's digital memory palace - where electrons become memories and packets become wisdom.*