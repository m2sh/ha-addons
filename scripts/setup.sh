#!/bin/bash

# Setup script for M2SH Home Assistant Add-ons repository
# This script initializes the repository and sets up git submodules

set -e

echo "🚀 Setting up M2SH Home Assistant Add-ons repository..."

# Make sure we're in the right directory
if [ ! -f "repository.yaml" ]; then
    echo "❌ Error: repository.yaml not found. Are you in the correct directory?"
    exit 1
fi

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git branch -m main
fi

# Set up git configuration
echo "⚙️  Setting up git configuration..."
git config --local user.name "Mohammad Shahgolzadeh"
git config --local user.email "m2sh@users.noreply.github.com"

# Add initial files
echo "📄 Adding initial files..."
git add -A

# Create initial commit if no commits exist
if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
    echo "💫 Creating initial commit..."
    git commit -m "🎉 Initial repository setup

- Add repository configuration
- Set up add-ons structure
- Configure GitHub Actions workflow
- Add submodule management scripts"
fi

# Initialize submodules
echo "🔗 Initializing git submodules..."
git submodule init
git submodule update --recursive --remote

echo "✅ Repository setup completed!"
echo ""
echo "Next steps:"
echo "1. Add the GitHub remote: git remote add origin https://github.com/m2sh/ha-addons.git"
echo "2. Push to GitHub: git push -u origin main"
echo "3. Enable GitHub Actions in your repository settings"
echo ""
echo "To add more add-ons, edit the addons.yml file and run:"
echo "  python scripts/update_submodules.py" 