# Nuke Node Setup Automator

Python automation tool for Foundry Nuke that streamlines compositing workflows by automatically generating standardized node trees. Reduces manual setup time and ensures consistency across VFX shots and projects.

## Features
- Automated creation of standard compositing node trees
- Configurable templates for different shot types
- Batch processing capabilities for multiple shots
- Customizable node parameters and connections
- Error handling and validation
- Team workflow standardization

## Technologies Used
- Python 3.x
- Foundry Nuke Python API
- JSON for configuration management
- File path automation

## Node Templates Included
- **Standard Beauty Pass**: Read → Grade → Transform → Write
- **Multi-pass Composite**: Beauty, Shadow, Reflection, Specular layers
- **Green Screen Template**: Read → Keyer → Grade → Merge → Write
- **Cleanup Template**: Read → RotoPaint → Grade → Write

## Installation
1. Copy scripts to your Nuke scripts directory
2. Add to Nuke menu or run directly in script editor
3. Configure file paths for your project structure

## Usage

