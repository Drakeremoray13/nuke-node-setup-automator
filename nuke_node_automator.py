"""
Nuke Node Setup Automator
Automated node tree creation for Foundry Nuke compositing workflows
"""

import nuke
import os
import json

class NukeNodeAutomator:
    def __init__(self):
        self.templates_config = {
            "standard_beauty": {
                "nodes": ["Read", "Grade", "Transform", "Write"],
                "connections": [(0,1), (1,2), (2,3)]
            },
            "multipass_comp": {
                "nodes": ["Read", "Read", "Read", "Merge", "Grade", "Write"],
                "connections": [(0,3), (1,3), (2,3), (3,4), (4,5)]
            },
            "greenscreen": {
                "nodes": ["Read", "Keyer", "Grade", "Read", "Merge", "Write"],
                "connections": [(0,1), (1,2), (2,4), (3,4), (4,5)]
            }
        }
    
    def create_standard_beauty_pass(self, input_path="", output_path=""):
        """
        Creates a standard beauty pass node tree: Read → Grade → Transform → Write
        """
        try:
            # Clear selection to avoid conflicts
            nuke.selectAll()
            nuke.delete()
            
            # Create Read node
            read_node = nuke.createNode('Read')
            read_node['name'].setValue('beauty_read')
            if input_path:
                read_node['file'].setValue(input_path)
            else:
                read_node['file'].setValue('/path/to/input/beauty_pass.####.exr')
            
            # Position node
            read_node.setXpos(0)
            read_node.setYpos(0)
            
            # Create Grade node
            grade_node = nuke.createNode('Grade')
            grade_node['name'].setValue('beauty_grade')
            grade_node.setInput(0, read_node)
            grade_node.setXpos(0)
            grade_node.setYpos(100)
            
            # Create Transform node
            transform_node = nuke.createNode('Transform')
            transform_node['name'].setValue('beauty_transform')
            transform_node.setInput(0, grade_node)
            transform_node.setXpos(0)
            transform_node.setYpos(200)
            
            # Create Write node
            write_node = nuke.createNode('Write')
            write_node['name'].setValue('beauty_write')
            write_node.setInput(0, transform_node)
            if output_path:
                write_node['file'].setValue(output_path)
            else:
                write_node['file'].setValue('/path/to/output/comp_beauty.####.exr')
            write_node.setXpos(0)
            write_node.setYpos(300)
            
            # Select the read node for user convenience
            nuke.selectAll()
            nuke.invertSelection()
            read_node['selected'].setValue(True)
            
            print("Standard beauty pass node tree created successfully!")
            return read_node, grade_node, transform_node, write_node
            
        except Exception as e:
            nuke.message(f"Error creating standard beauty pass: {str(e)}")
            print(f"Error: {str(e)}")
            return None
    
    def create_multipass_composite(self, beauty_path="", shadow_path="", spec_path="", output_path=""):
        """
        Creates a multi-pass composite setup with beauty, shadow, and specular layers
        """
        try:
            # Clear existing nodes
            nuke.selectAll()
            nuke.delete()
            
            # Create beauty Read node
            beauty_read = nuke.createNode('Read')
            beauty_read['name'].setValue('beauty_read')
            beauty_read['file'].setValue(beauty_path or '/path/to/beauty.####.exr')
            beauty_read.setXpos(-100)
            beauty_read.setYpos(0)
            
            # Create shadow Read node
            shadow_read = nuke.createNode('Read')
            shadow_read['name'].setValue('shadow_read')
            shadow_read['file'].setValue(shadow_path or '/path/to/shadow.####.exr')
            shadow_read.setXpos(0)
            shadow_read.setYpos(0)
            
            # Create specular Read node
            spec_read = nuke.createNode('Read')
            spec_read['name'].setValue('spec_read')
            spec_read['file'].setValue(spec_path or '/path/to/specular.####.exr')
            spec_read.setXpos(100)
            spec_read.setYpos(0)
            
            # Create Merge nodes for combining passes
            shadow_merge = nuke.createNode('Merge')
            shadow_merge['name'].setValue('shadow_merge')
            shadow_merge['operation'].setValue('multiply')
            shadow_merge.setInput(0, beauty_read)  # A input (background)
            shadow_merge.setInput(1, shadow_read)  # B input (foreground)
            shadow_merge.setXpos(0)
            shadow_merge.setYpos(100)
            
            spec_merge = nuke.createNode('Merge')
            spec_merge['name'].setValue('spec_merge')
            spec_merge['operation'].setValue('plus')
            spec_merge.setInput(0, shadow_merge)
            spec_merge.setInput(1, spec_read)
            spec_merge.setXpos(0)
            spec_merge.setYpos(200)
            
            # Create final Grade node
            final_grade = nuke.createNode('Grade')
            final_grade['name'].setValue('final_grade')
            final_grade.setInput(0, spec_merge)
            final_grade.setXpos(0)
            final_grade.setYpos(300)
            
            # Create Write node
            write_node = nuke.createNode('Write')
            write_node['name'].setValue('comp_write')
            write_node.setInput(0, final_grade)
            write_node['file'].setValue(output_path or '/path/to/output/final_comp.####.exr')
            write_node.setXpos(0)
            write_node.setYpos(400)
            
            print("Multi-pass composite node tree created successfully!")
            return beauty_read, shadow_read, spec_read, write_node
            
        except Exception as e:
            nuke.message(f"Error creating multi-pass composite: {str(e)}")
            print(f"Error: {str(e)}")
            return None
    
    def create_greenscreen_template(self, fg_path="", bg_path="", output_path=""):
        """
        Creates a green screen compositing template
        """
        try:
            # Clear existing nodes
            nuke.selectAll()
            nuke.delete()
            
            # Create foreground Read node
            fg_read = nuke.createNode('Read')
            fg_read['name'].setValue('fg_read')
            fg_read['file'].setValue(fg_path or '/path/to/greenscreen_footage.####.mov')
            fg_read.setXpos(-100)
            fg_read.setYpos(0)
            
            # Create Keyer node
            keyer = nuke.createNode('Keyer')
            keyer['name'].setValue('greenscreen_key')
            keyer.setInput(0, fg_read)
            keyer['operation'].setValue('red keyer')  # Default to red keyer
            keyer.setXpos(-100)
            keyer.setYpos(100)
            
            # Create Grade node for key refinement
            key_grade = nuke.createNode('Grade')
            key_grade['name'].setValue('key_grade')
            key_grade.setInput(0, keyer)
            key_grade.setXpos(-100)
            key_grade.setYpos(200)
            
            # Create background Read node
            bg_read = nuke.createNode('Read')
            bg_read['name'].setValue('bg_read')
            bg_read['file'].setValue(bg_path or '/path/to/background.####.exr')
            bg_read.setXpos(100)
            bg_read.setYpos(0)
            
            # Create Merge node
            merge_node = nuke.createNode('Merge')
            merge_node['name'].setValue('composite_merge')
            merge_node.setInput(0, bg_read)      # A input (background)
            merge_node.setInput(1, key_grade)   # B input (keyed foreground)
            merge_node.setXpos(0)
            merge_node.setYpos(300)
            
            # Create final Grade
            final_grade = nuke.createNode('Grade')
            final_grade['name'].setValue('final_grade')
            final_grade.setInput(0, merge_node)
            final_grade.setXpos(0)
            final_grade.setYpos(400)
            
            # Create Write node
            write_node = nuke.createNode('Write')
            write_node['name'].setValue('comp_write')
            write_node.setInput(0, final_grade)
            write_node['file'].setValue(output_path or '/path/to/output/greenscreen_comp.####.exr')
            write_node.setXpos(0)
            write_node.setYpos(500)
            
            print("Green screen template created successfully!")
            return fg_read, keyer, bg_read, merge_node, write_node
            
        except Exception as e:
            nuke.message(f"Error creating green screen template: {str(e)}")
            print(f"Error: {str(e)}")
            return None
    
    def batch_create_shots(self, shot_list, template_type="standard_beauty"):
        """
        Batch creates node trees for multiple shots
        """
        created_shots = []
        
        for shot_info in shot_list:
            try:
                shot_name = shot_info.get('name', 'unknown_shot')
                input_path = shot_info.get('input', '')
                output_path = shot_info.get('output', '')
                
                print(f"Creating node tree for shot: {shot_name}")
                
                # Create new script for each shot
                nuke.scriptNew()
                
                if template_type == "standard_beauty":
                    result = self.create_standard_beauty_pass(input_path, output_path)
                elif template_type == "multipass_comp":
                    beauty = shot_info.get('beauty', '')
                    shadow = shot_info.get('shadow', '')
                    spec = shot_info.get('spec', '')
                    result = self.create_multipass_composite(beauty, shadow, spec, output_path)
                elif template_type == "greenscreen":
                    fg_path = shot_info.get('foreground', '')
                    bg_path = shot_info.get('background', '')
                    result = self.create_greenscreen_template(fg_path, bg_path, output_path)
                
                if result:
                    # Save the script
                    script_path = shot_info.get('script_path', f'/path/to/scripts/{shot_name}.nk')
                    nuke.scriptSaveAs(script_path)
                    created_shots.append(shot_name)
                    print(f"Successfully created and saved: {shot_name}")
                
            except Exception as e:
                print(f"Error processing shot {shot_name}: {str(e)}")
                continue
        
        return created_shots

# Convenience functions for direct use
def create_standard_beauty_pass(input_path="", output_path=""):
    """Convenience function to create standard beauty pass"""
    automator = NukeNodeAutomator()
    return automator.create_standard_beauty_pass(input_path, output_path)

def create_multipass_composite(beauty_path="", shadow_path="", spec_path="", output_path=""):
    """Convenience function to create multi-pass composite"""
    automator = NukeNodeAutomator()
    return automator.create_multipass_composite(beauty_path, shadow_path, spec_path, output_path)

def create_greenscreen_template(fg_path="", bg_path="", output_path=""):
    """Convenience function to create green screen template"""
    automator = NukeNodeAutomator()
    return automator.create_greenscreen_template(fg_path, bg_path, output_path)

# Example usage when run directly in Nuke
if __name__ == '__main__':
    # Create an instance of the automator
    automator = NukeNodeAutomator()
    
    # Example: Create a standard beauty pass
    print("Creating standard beauty pass...")
    automator.create_standard_beauty_pass()
