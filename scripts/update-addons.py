#!/usr/bin/env python3
"""
Home Assistant Add-ons Repository Updater

This script syncs external add-ons from their individual repositories
into this main repository for centralized distribution.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
import argparse


class AddonUpdater:
    def __init__(self, config_file: str = "addons.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.repo_root = Path(__file__).parent.parent

    def load_config(self) -> Dict[str, Any]:
        """Load the addons configuration file."""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file '{self.config_file}' not found.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in '{self.config_file}': {e}")
            sys.exit(1)

    def clone_repository(self, repo_url: str, branch: str = "main") -> Optional[Path]:
        """Clone a repository to a temporary directory."""
        temp_dir = tempfile.mkdtemp()
        try:
            print(f"Cloning {repo_url} (branch: {branch})...")
            result = subprocess.run([
                "git", "clone", "--depth", "1", "--branch", branch, repo_url, temp_dir
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Error cloning repository: {result.stderr}")
                return None
                
            return Path(temp_dir)
        except Exception as e:
            print(f"Error cloning repository: {e}")
            return None

    def sync_addon(self, addon_name: str, addon_config: Dict[str, Any]) -> bool:
        """Sync a single add-on from its repository."""
        print(f"\nSyncing add-on: {addon_name}")
        
        # Clone the repository
        repo_path = self.clone_repository(
            addon_config["repository"], 
            addon_config.get("branch", "main")
        )
        
        if not repo_path:
            return False

        try:
            # Check if the add-on directory exists in the cloned repo
            addon_source_path = repo_path / addon_name
            if not addon_source_path.exists():
                print(f"Error: Add-on directory '{addon_name}' not found in repository")
                return False

            # Create target directory
            addon_target_path = self.repo_root / addon_name
            if addon_target_path.exists():
                shutil.rmtree(addon_target_path)
            
            # Copy the add-on
            shutil.copytree(addon_source_path, addon_target_path)
            
            # Update config.yaml with repository-specific information
            self.update_addon_config(addon_target_path, addon_name, addon_config)
            
            print(f"✓ Successfully synced {addon_name}")
            return True
            
        except Exception as e:
            print(f"Error syncing add-on {addon_name}: {e}")
            return False
        finally:
            # Clean up temporary directory
            shutil.rmtree(repo_path, ignore_errors=True)

    def update_addon_config(self, addon_path: Path, addon_name: str, addon_config: Dict[str, Any]):
        """Update the add-on's config.yaml with repository-specific information."""
        config_file = addon_path / "config.yaml"
        if not config_file.exists():
            return

        # Read existing config
        with open(config_file, 'r') as f:
            lines = f.readlines()

        # Update or add repository information
        updated_lines = []
        repo_info_added = False
        
        for line in lines:
            if line.startswith("repository:"):
                updated_lines.append(f"repository: {addon_config['repository']}\n")
                repo_info_added = True
            else:
                updated_lines.append(line)

        # Add repository info if not found
        if not repo_info_added:
            # Find a good place to insert (after name/version/slug)
            insert_index = 0
            for i, line in enumerate(lines):
                if line.startswith("description:"):
                    insert_index = i + 1
                    break
            
            updated_lines.insert(insert_index, f"repository: {addon_config['repository']}\n")

        # Write updated config
        with open(config_file, 'w') as f:
            f.writelines(updated_lines)

    def update_main_readme(self):
        """Update the main README.md with current add-on information."""
        readme_file = self.repo_root / "README.md"
        if not readme_file.exists():
            return

        # Read existing README
        with open(readme_file, 'r') as f:
            content = f.read()

        # Generate add-ons section
        addons_section = self.generate_addons_section()
        
        # Replace the add-ons section in README
        import re
        pattern = r'(## Add-ons provided by this repository\n\n)(.*?)(\n## )'
        replacement = r'\1' + addons_section + r'\3'
        
        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # Write updated README
        with open(readme_file, 'w') as f:
            f.write(updated_content)

    def generate_addons_section(self) -> str:
        """Generate the add-ons section for the README."""
        section = ""
        
        for addon_name, addon_config in self.config["addons"].items():
            section += f"### ✓ {addon_config['name']}\n\n"
            
            # Architecture badges
            for arch in addon_config.get("architectures", []):
                section += f"![Supports {arch} Architecture][{arch}-shield]\n"
            section += "\n"
            
            # Version badge
            section += f"Latest Version: ![Latest Version][{addon_name}-version-shield]\n\n"
            
            # Description
            section += f"{addon_config['description']}\n\n"
            
            # Documentation link
            section += f"📚 **[Full documentation]({addon_config['repository']})**\n\n"
        
        return section

    def update_github_workflow(self):
        """Update the GitHub Actions workflow with current add-ons."""
        workflow_file = self.repo_root / ".github" / "workflows" / "ci.yaml"
        if not workflow_file.exists():
            return

        # Read existing workflow
        with open(workflow_file, 'r') as f:
            content = f.read()

        # Generate add-ons list for matrix
        addons_list = list(self.config["addons"].keys())
        addons_yaml = f"[{', '.join(addons_list)}]"
        
        # Replace the addon matrix
        import re
        pattern = r'(addon: \[).*?(\])'
        replacement = rf'\1{addons_yaml}\2'
        
        updated_content = re.sub(pattern, replacement, content)
        
        # Write updated workflow
        with open(workflow_file, 'w') as f:
            f.write(updated_content)

    def run(self, addon_name: Optional[str] = None):
        """Run the updater for all add-ons or a specific add-on."""
        if addon_name:
            if addon_name not in self.config["addons"]:
                print(f"Error: Add-on '{addon_name}' not found in configuration")
                return False
            
            success = self.sync_addon(addon_name, self.config["addons"][addon_name])
        else:
            # Sync all add-ons
            success = True
            for addon_name, addon_config in self.config["addons"].items():
                if not self.sync_addon(addon_name, addon_config):
                    success = False

        if success:
            # Update main repository files
            self.update_main_readme()
            self.update_github_workflow()
            print("\n✓ Repository updated successfully!")
        
        return success


def main():
    parser = argparse.ArgumentParser(description="Update Home Assistant add-ons from external repositories")
    parser.add_argument("--addon", help="Update specific add-on only")
    parser.add_argument("--config", default="addons.json", help="Configuration file path")
    
    args = parser.parse_args()
    
    updater = AddonUpdater(args.config)
    success = updater.run(args.addon)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 