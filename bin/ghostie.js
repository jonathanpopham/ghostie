#!/usr/bin/env node

/**
 * 👻 Ghostie - Ghost in the Shell Personality Loader
 * Node.js wrapper for the Python-based ghostie system
 * 
 * This wrapper allows ghostie to be installed as a global npm package
 * while maintaining the core Python functionality.
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Get the directory where this script is located
const scriptDir = path.dirname(__filename);
const parentDir = path.dirname(scriptDir);
const ghostiePath = path.join(parentDir, 'ghostie');

// Check if Python ghostie script exists
if (!fs.existsSync(ghostiePath)) {
    console.error('❌ Ghostie Python script not found at:', ghostiePath);
    console.error('📍 Try reinstalling the package or check the installation.');
    process.exit(1);
}

// Check if Python 3 is available
function checkPython() {
    return new Promise((resolve) => {
        const python = spawn('python3', ['--version'], { stdio: 'pipe' });
        python.on('error', () => resolve(false));
        python.on('close', (code) => resolve(code === 0));
    });
}

async function main() {
    // Check Python availability
    const pythonAvailable = await checkPython();
    if (!pythonAvailable) {
        console.error('❌ Python 3 is required but not found in PATH');
        console.error('📦 Please install Python 3 to use ghostie');
        console.error('🐍 On Termux: pkg install python');
        console.error('🖥️  On Ubuntu/Debian: apt install python3');
        console.error('🍎 On macOS: brew install python3');
        process.exit(1);
    }

    // Make sure ghostie script is executable
    try {
        fs.chmodSync(ghostiePath, 0o755);
    } catch (err) {
        // Ignore permission errors, might not be needed
    }

    // Pass all command line arguments to the Python script
    const args = process.argv.slice(2);
    
    // Spawn the Python ghostie script
    const ghostie = spawn('python3', [ghostiePath, ...args], {
        stdio: 'inherit',
        cwd: process.cwd()
    });

    // Handle process events
    ghostie.on('error', (err) => {
        console.error('❌ Failed to start ghostie:', err.message);
        process.exit(1);
    });

    ghostie.on('close', (code) => {
        process.exit(code || 0);
    });

    // Handle Ctrl+C gracefully
    process.on('SIGINT', () => {
        ghostie.kill('SIGINT');
    });

    process.on('SIGTERM', () => {
        ghostie.kill('SIGTERM');
    });
}

// Add helpful information for common issues
if (process.argv.includes('--help') || process.argv.includes('-h')) {
    console.log(`
👻 Ghostie - Ghost in the Shell Personality System

Usage:
    ghostie                 # Load personality into context
    ghostie --memorize      # Store a memory with timestamp
    ghostie --remember      # Recall relevant memories  
    ghostie --tools         # List available tools and capabilities
    ghostie --haunt         # Discover and profile current environment
    ghostie --version       # Show version information
    ghostie --update        # Update this script with new tools/memories

Requirements:
    - Python 3.x
    - JSON support (built into Python)
    - Terminal environment (Termux, Linux, macOS)

Installation:
    npm install -g ghostie

Repository:
    https://github.com/jonathanpopham/ghostie

Issues:
    https://github.com/jonathanpopham/ghostie/issues
`);
    process.exit(0);
}

// Run the main function
main().catch((err) => {
    console.error('❌ Unexpected error:', err);
    process.exit(1);
});