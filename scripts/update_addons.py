#!/usr/bin/env python3
"""
Script to fetch add-on repositories and copy their content directly to the repository.
This replaces the git submodule approach with direct file copying.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import yaml
from pathlib import Path
import requests
import json

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

def get_latest_commit_sha(repo_url, branch='main'):
    """Get the latest commit SHA from a GitHub repository."""
    try:
        # Convert GitHub URL to API URL
        if repo_url.startswith('https://github.com/'):
            repo_path = repo_url.replace('https://github.com/', '').replace('.git', '')
            api_url = f"https://api.github.com/repos/{repo_path}/commits/{branch}"
            
            response = requests.get(api_url)
            if response.status_code == 200:
                return response.json()['sha']
            else:
                print(f"Warning: Could not get latest commit for {repo_url}")
                return None
    except Exception as e:
        print(f"Error getting commit SHA for {repo_url}: {e}")
        return None

def clone_repository(repo_url, target_dir, branch='main'):
    """Clone a repository to a temporary directory."""
    try:
        print(f"Cloning {repo_url} (branch: {branch})...")
        cmd = f"git clone --depth 1 --branch {branch} {repo_url} {target_dir}"
        result = run_command(cmd)
        return result is not None
    except Exception as e:
        print(f"Error cloning repository {repo_url}: {e}")
        return False

def copy_addon_files(source_dir, target_dir, addon_name):
    """Copy add-on files from source to target directory."""
    try:
        # Create target directory if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)
        
        # Files and directories to copy (typical Home Assistant add-on structure)
        items_to_copy = [
            'config.yaml',
            'config.yml', 
            'Dockerfile',
            'README.md',
            'CHANGELOG.md',
            'DOCS.md',
            'icon.png',
            'logo.png',
            'build.yaml',
            'build.yml',
            'translations/',
            'rootfs/',
            'data/',
            'run.sh',
            'src/',
            'app/',
            'requirements.txt',
            'package.json',
            'apparmor.txt'
        ]
        
        copied_files = []
        
        for item in items_to_copy:
            source_path = os.path.join(source_dir, item)
            target_path = os.path.join(target_dir, item)
            
            if os.path.exists(source_path):
                if os.path.isdir(source_path):
                    if os.path.exists(target_path):
                        shutil.rmtree(target_path)
                    shutil.copytree(source_path, target_path)
                    copied_files.append(item + '/')
                else:
                    shutil.copy2(source_path, target_path)
                    copied_files.append(item)
        
        if copied_files:
            print(f"Copied files for {addon_name}: {', '.join(copied_files)}")
            return True
        else:
            print(f"No recognizable add-on files found in {source_dir}")
            return False
            
    except Exception as e:
        print(f"Error copying files for {addon_name}: {e}")
        return False

def update_addon_metadata(target_dir, addon_name, repo_url, commit_sha):
    """Update or create metadata file for the add-on."""
    try:
        metadata_file = os.path.join(target_dir, '.addon-metadata')
        metadata = {
            'name': addon_name,
            'source_repository': repo_url,
            'last_update': subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], 
                                        capture_output=True, text=True).stdout.strip(),
            'commit_sha': commit_sha
        }
        
        with open(metadata_file, 'w') as f:
            yaml.dump(metadata, f, default_flow_style=False)
        
        print(f"Updated metadata for {addon_name}")
        return True
        
    except Exception as e:
        print(f"Error updating metadata for {addon_name}: {e}")
        return False

def should_update_addon(addon_name, repo_url, branch, current_commit_sha):
    """Check if an add-on should be updated."""
    metadata_file = os.path.join(addon_name, '.addon-metadata')
    
    if not os.path.exists(metadata_file):
        print(f"No metadata found for {addon_name}, will update")
        return True
    
    try:
        with open(metadata_file, 'r') as f:
            metadata = yaml.safe_load(f)
        
        if metadata.get('commit_sha') != current_commit_sha:
            print(f"New commit available for {addon_name}")
            return True
        
        print(f"No updates needed for {addon_name}")
        return False
        
    except Exception as e:
        print(f"Error reading metadata for {addon_name}: {e}")
        return True

def main():
    """Main function to update add-ons from their repositories."""
    print("🔄 Starting add-ons update process...")
    
    # Load configuration
    addons = load_addons_config()
    if not addons:
        print("No add-ons configured in addons.yml")
        return
    
    updated_addons = []
    
    # Process each add-on
    for name, config in addons.items():
        print(f"\n📦 Processing add-on: {name}")
        
        repository = config['repository']
        target = config.get('target', name)
        branch = config.get('branch', 'main')
        
        # Get latest commit SHA
        current_commit_sha = get_latest_commit_sha(repository, branch)
        
        # Check if update is needed
        if not should_update_addon(target, repository, branch, current_commit_sha):
            continue
        
        # Create temporary directory for cloning
        with tempfile.TemporaryDirectory() as temp_dir:
            clone_dir = os.path.join(temp_dir, 'repo')
            
            # Clone repository
            if clone_repository(repository, clone_dir, branch):
                # Copy files to target directory
                if copy_addon_files(clone_dir, target, name):
                    # Update metadata
                    update_addon_metadata(target, name, repository, current_commit_sha)
                    updated_addons.append(name)
                    print(f"✅ Successfully updated {name}")
                else:
                    print(f"❌ Failed to copy files for {name}")
            else:
                print(f"❌ Failed to clone repository for {name}")
    
    if updated_addons:
        print(f"\n🎉 Successfully updated {len(updated_addons)} add-on(s): {', '.join(updated_addons)}")
    else:
        print("\n📋 No add-ons needed updating")
    
    print("✅ Add-ons update process completed!")

if __name__ == "__main__":
    main() 