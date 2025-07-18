#!/usr/bin/env python3
"""
Script to update git submodules based on addons.yml configuration.
"""

import os
import subprocess
import sys
import yaml
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            cwd=cwd
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}")
        print(f"Error: {e.stderr}")
        return None

def load_addons_config():
    """Load the addons configuration from addons.yml."""
    try:
        with open('addons.yml', 'r') as f:
            config = yaml.safe_load(f)
        return config.get('addons', {})
    except FileNotFoundError:
        print("addons.yml not found!")
        return {}
    except yaml.YAMLError as e:
        print(f"Error parsing addons.yml: {e}")
        return {}

def get_existing_submodules():
    """Get list of existing git submodules."""
    submodules = {}
    if os.path.exists('.gitmodules'):
        result = run_command('git config --file .gitmodules --get-regexp path')
        if result:
            for line in result.split('\n'):
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        path = parts[1]
                        submodules[path] = True
    return submodules

def add_submodule(name, config):
    """Add a new git submodule."""
    repository = config['repository']
    target = config['target']
    branch = config.get('branch', 'main')
    
    print(f"Adding submodule: {name} -> {target}")
    
    # Remove directory if it exists but is not a submodule
    if os.path.exists(target) and not os.path.exists(os.path.join(target, '.git')):
        run_command(f'rm -rf {target}')
    
    # Add submodule
    cmd = f'git submodule add -b {branch} {repository} {target}'
    result = run_command(cmd)
    
    if result is not None:
        print(f"Successfully added submodule: {target}")
        return True
    else:
        print(f"Failed to add submodule: {target}")
        return False

def update_submodule(target):
    """Update an existing git submodule."""
    print(f"Updating submodule: {target}")
    
    # Update submodule to latest commit
    cmd = f'git submodule update --remote {target}'
    result = run_command(cmd)
    
    if result is not None:
        print(f"Successfully updated submodule: {target}")
        return True
    else:
        print(f"Failed to update submodule: {target}")
        return False

def main():
    """Main function to update submodules based on addons.yml."""
    print("🔄 Starting add-ons update process...")
    
    # Load configuration
    addons = load_addons_config()
    if not addons:
        print("No add-ons configured in addons.yml")
        return
    
    # Get existing submodules
    existing_submodules = get_existing_submodules()
    
    # Process each add-on
    for name, config in addons.items():
        target = config.get('target', name)
        
        if target in existing_submodules:
            # Update existing submodule
            update_submodule(target)
        else:
            # Add new submodule
            add_submodule(name, config)
    
    # Initialize and update all submodules
    print("🔄 Initializing and updating all submodules...")
    run_command('git submodule init')
    run_command('git submodule update --recursive --remote')
    
    print("✅ Add-ons update process completed!")

if __name__ == "__main__":
    main() 