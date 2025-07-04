#!/usr/bin/env python3
"""
Home Assistant Add-ons Repository Updater

This script updates add-ons from their source repositories based on the .addons.yml configuration.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


def load_config(config_file: str = ".addons.yml") -> Dict[str, Any]:
    """Load the repository configuration from .addons.yml."""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in '{config_file}': {e}")
        sys.exit(1)


def run_command(cmd: list, cwd: Optional[str] = None) -> bool:
    """Run a command and return True if successful."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        return False


def clone_repository(repo_url: str, branch: str, temp_dir: str) -> bool:
    """Clone a repository to a temporary directory."""
    print(f"Cloning {repo_url} (branch: {branch})...")
    
    # Clone the repository
    if not run_command(['git', 'clone', '--depth', '1', '--branch', branch, repo_url, temp_dir]):
        return False
    
    return True


def update_addon(addon_name: str, addon_config: Dict[str, Any], repo_root: Path) -> bool:
    """Update a single add-on from its source repository."""
    print(f"\n{'='*50}")
    print(f"Updating add-on: {addon_name}")
    print(f"{'='*50}")
    
    repo_url = addon_config.get('repo')
    branch = addon_config.get('branch', 'main')
    
    if not repo_url:
        print(f"Error: No repository URL specified for {addon_name}")
        return False
    
    with tempfile.TemporaryDirectory() as temp_dir:
        if not clone_repository(repo_url, branch, temp_dir):
            return False
        source_addon_dir = Path(temp_dir) / addon_name
        if not source_addon_dir.exists():
            print(f"Error: Add-on directory '{addon_name}' not found in {repo_url}")
            return False
        target_addon_dir = repo_root / addon_name
        if target_addon_dir.exists():
            print(f"Removing existing {addon_name} directory...")
            shutil.rmtree(target_addon_dir)
        print(f"Copying {addon_name} from source repository...")
        shutil.copytree(source_addon_dir, target_addon_dir)
        print(f"✅ Successfully updated {addon_name}")
        return True


def update_addons_config(config: Dict[str, Any], repo_root: Path) -> bool:
    """Update the .addons.yml file with latest versions from source repositories."""
    print(f"\n{'='*50}")
    print("Updating .addons.yml with latest versions...")
    print(f"{'='*50}")
    
    addons = config.get('addons', {})
    updated = False
    
    for addon_name, addon_config in addons.items():
        addon_dir = repo_root / addon_name
        config_file = addon_dir / "config.yaml"
        
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    addon_yaml = yaml.safe_load(f)
                    new_version = addon_yaml.get('version')
                    current_version = addon_config.get('version')
                    
                    if new_version and new_version != current_version:
                        print(f"Updating {addon_name} version: {current_version} -> {new_version}")
                        addon_config['version'] = new_version
                        updated = True
                    else:
                        print(f"Version unchanged for {addon_name}: {current_version}")
            except yaml.YAMLError:
                print(f"Warning: Could not parse config.yaml for {addon_name}")
    
    if updated:
        # Write updated configuration back to .addons.yml
        with open(repo_root / ".addons.yml", 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        print("✅ Updated .addons.yml with latest versions")
    else:
        print("No version updates found")
    
    return True


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Update Home Assistant add-ons from source repositories")
    parser.add_argument(
        "--addon",
        help="Update only a specific add-on (by name)"
    )
    parser.add_argument(
        "--config",
        default=".addons.yml",
        help="Path to configuration file (default: .addons.yml)"
    )
    parser.add_argument(
        "--skip-version-update",
        action="store_true",
        help="Skip updating versions in .addons.yml"
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    addons = config.get('addons', {})
    
    if not addons:
        print("No add-ons found in configuration")
        sys.exit(1)
    
    # Get repository root
    repo_root = Path.cwd()
    
    # Determine which add-ons to update
    if args.addon:
        if args.addon not in addons:
            print(f"Error: Add-on '{args.addon}' not found in configuration")
            sys.exit(1)
        addons_to_update = {args.addon: addons[args.addon]}
    else:
        addons_to_update = addons
    
    print(f"Repository: {config.get('repository', {}).get('name', 'Unknown')}")
    print(f"Add-ons to update: {', '.join(addons_to_update.keys())}")
    
    # Update each add-on
    success_count = 0
    for addon_name, addon_config in addons_to_update.items():
        if update_addon(addon_name, addon_config, repo_root):
            success_count += 1
    
    # Update .addons.yml with latest versions
    if not args.skip_version_update:
        update_addons_config(config, repo_root)
    
    print(f"\n{'='*50}")
    print(f"Update complete: {success_count}/{len(addons_to_update)} add-ons updated successfully")
    print(f"{'='*50}")
    
    if success_count < len(addons_to_update):
        sys.exit(1)


if __name__ == "__main__":
    main() 