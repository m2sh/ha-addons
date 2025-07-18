#!/bin/bash

# Setup script for M2SH Home Assistant Add-ons repository
# This script initializes the repository and fetches add-ons from their repositories

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

# Install Python dependencies if needed
if command -v python3 &> /dev/null; then
    echo "🐍 Installing Python dependencies..."
    python3 -m pip install --user pyyaml requests
fi

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
- Add add-on management scripts"
fi

# Fetch add-ons from their repositories
echo "📦 Fetching add-ons from repositories..."
if [ -f "scripts/update_addons.py" ]; then
    python3 scripts/update_addons.py
else
    echo "⚠️  Warning: update_addons.py script not found. Add-ons will be fetched by GitHub Actions."
fi

echo "✅ Repository setup completed!"
echo ""
echo "Next steps:"
echo "1. Add the GitHub remote: git remote add origin https://github.com/m2sh/ha-addons.git"
echo "2. Push to GitHub: git push -u origin main"
echo "3. Enable GitHub Actions in your repository settings"
echo ""
echo "To add more add-ons, edit the addons.yml file and run:"
echo "  python3 scripts/update_addons.py"
echo ""
echo "Or trigger the GitHub Action manually for automatic updates." 