"""
Batch Shot Processor for Nuke Node Automator
Processes multiple shots using JSON configuration files
"""

import json
import os
from nuke_node_automator import NukeNodeAutomator

def load_shot_config(config_file):
    """Load shot configuration from JSON file"""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config file {config_file}: {str(e)}")
        return None

def process_shots_from_config(config_file):
    """Process shots based on JSON configuration"""
    config = load_shot_config(config_file)
    if not config:
        return []
    
    automator = NukeNodeAutomator()
    shot_list = config.get('shots', [])
    template_type = config.get('template_type', 'standard_beauty')
    
    print(f"Processing {len(shot_list)} shots with template: {template_type}")
    
    return automator.batch_create_shots(shot_list, template_type)

# Example usage
if __name__ == '__main__':
    # Example config file path
    config_file = '/path/to/shot_config.json'
    
    if os.path.exists(config_file):
        created_shots = process_shots_from_config(config_file)
        print(f"Successfully created {len(created_shots)} shots:")
        for shot in created_shots:
            print(f"  - {shot}")
    else:
        print("Config file not found. Please create a shot configuration file.")
        print("Example format:")
        example_config = {
            "template_type": "standard_beauty",
            "shots": [
                {
                    "name": "shot_001",
                    "input": "/path/to/shot_001/beauty.####.exr",
                    "output": "/path/to/output/shot_001_comp.####.exr",
                    "script_path": "/path/to/scripts/shot_001.nk"
                }
            ]
        }
        print(json.dumps(example_config, indent=2))
