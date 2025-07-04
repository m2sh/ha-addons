# Setup Guide for m2sh Home Assistant Add-ons Repository

This guide explains how to set up and use the external add-on management system.

## Overview

This repository uses an external add-on management system that automatically syncs add-ons from their individual repositories. This approach provides several benefits:

- **Automatic Updates**: Add-ons are automatically synced from their individual repositories
- **Separation of Concerns**: Each add-on has its own repository for focused development
- **Easy Maintenance**: Updates to individual add-ons automatically appear here
- **Better Organization**: Each add-on can have its own issues, releases, and documentation

## How It Works

1. **Individual Repositories**: Each add-on is maintained in its own repository (e.g., `ha-addon-chisel`)
2. **Configuration**: Add-ons are defined in `addons.json` with their repository URLs
3. **Automatic Syncing**: The system automatically pulls the latest versions
4. **Centralized Distribution**: All add-ons are made available through this single repository

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/m2sh/ha-addons.git
cd ha-addons
```

### 2. Sync Add-ons

```bash
# Sync all add-ons
./scripts/update.sh

# Or sync specific add-on
./scripts/update.sh --addon chisel
```

### 3. Add to Home Assistant

In Home Assistant:
1. Go to Settings → Add-ons → Add-on Store
2. Click the three dots menu and select "Repositories"
3. Add: `https://github.com/m2sh/ha-addons`

## Adding a New Add-on

### 1. Create Individual Repository

Create a new repository for your add-on (e.g., `ha-addon-myapp`) with the standard Home Assistant add-on structure.

### 2. Add to Configuration

Add your add-on to `addons.json`:

```json
{
  "myapp": {
    "name": "My App",
    "description": "Description of my app",
    "repository": "https://github.com/m2sh/ha-addon-myapp",
    "branch": "main",
    "type": "external",
    "architectures": ["armhf", "armv7", "aarch64", "amd64", "i386"],
    "version": "1.0.0",
    "panel_icon": "mdi:app",
    "ports": {
      "8080/tcp": 8080
    }
  }
}
```

### 3. Sync the Add-on

```bash
./scripts/update.sh --addon myapp
```

## Available Scripts

### Update Scripts

- `./scripts/update.sh`: Shell wrapper for the Python updater
- `python3 scripts/update-addons.py`: Direct Python updater
- `./scripts/build.sh`: Local build script for testing

### Usage Examples

```bash
# Update all add-ons
./scripts/update.sh

# Update specific add-on
./scripts/update.sh --addon chisel

# Build add-on locally for testing
./scripts/build.sh chisel

# Update with custom config file
python3 scripts/update-addons.py --config custom-addons.json
```

## Configuration File Format

The `addons.json` file defines all add-ons and their properties:

```json
{
  "addons": {
    "addon-slug": {
      "name": "Add-on Name",
      "description": "Add-on description",
      "repository": "https://github.com/username/repo-name",
      "branch": "main",
      "type": "external",
      "architectures": ["armhf", "armv7", "aarch64", "amd64", "i386"],
      "version": "1.0.0",
      "panel_icon": "mdi:icon-name",
      "ports": {
        "8080/tcp": 8080
      }
    }
  }
}
```

### Configuration Options

- `name`: Display name of the add-on
- `description`: Brief description
- `repository`: Git repository URL
- `branch`: Git branch to sync from (default: "main")
- `type`: Always "external" for external repositories
- `architectures`: List of supported architectures
- `version`: Current version
- `panel_icon`: Material Design icon name
- `ports`: Port mappings (optional)

## GitHub Actions

The repository includes GitHub Actions workflows that:

1. **Daily Updates**: Automatically sync add-ons daily at 2 AM UTC
2. **Manual Updates**: Allow manual triggering of updates
3. **Linting**: Check YAML files for errors
4. **Building**: Build Docker images for all add-ons

### Manual Workflow Trigger

You can manually trigger the update workflow:
1. Go to Actions tab in GitHub
2. Select "CI" workflow
3. Click "Run workflow"
4. Optionally specify a specific add-on

## Troubleshooting

### Common Issues

1. **Add-on not syncing**: Check that the repository URL is correct and accessible
2. **Build failures**: Verify that the add-on has the correct structure
3. **Permission errors**: Ensure the repository is public or you have access

### Debug Mode

Run the updater with verbose output:

```bash
python3 scripts/update-addons.py --addon chisel --verbose
```

### Manual Sync

If automatic syncing fails, you can manually sync:

```bash
# Clone the add-on repository
git clone https://github.com/m2sh/ha-addon-chisel temp-chisel

# Copy to main repository
cp -r temp-chisel/chisel ./

# Clean up
rm -rf temp-chisel

# Update repository files
python3 scripts/update-addons.py
```

## Support

For issues and questions:

- **Add-on specific**: Open an issue on the individual add-on repository
- **Repository specific**: Open an issue on this repository
- **General**: Join the [Home Assistant Community Discord](https://discord.gg/hassioaddons)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines. 