"""
Nuke Menu Integration for Node Automator
Add this to your Nuke menu.py or init.py file
"""

import nuke
from nuke_node_automator import create_standard_beauty_pass, create_multipass_composite, create_greenscreen_template

# Add menu items to Nuke
toolbar = nuke.toolbar("Nodes")
automator_menu = toolbar.addMenu("Node Automator", "automator_icon.png")

automator_menu.addCommand("Standard Beauty Pass", create_standard_beauty_pass)
automator_menu.addCommand("Multi-pass Composite", create_multipass_composite)
automator_menu.addCommand("Green Screen Template", create_greenscreen_template)

print("Node Automator menu loaded successfully!")
