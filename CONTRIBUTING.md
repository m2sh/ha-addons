# Contributing to m2sh Home Assistant Add-ons

Thank you for your interest in contributing to this Home Assistant add-ons repository! This document provides guidelines and instructions for contributing.

## Repository Structure

This repository uses an external add-on management system where each add-on is maintained in its own repository and automatically synced here. This approach provides several benefits:

- **Separation of Concerns**: Each add-on has its own repository for focused development
- **Automatic Updates**: Add-ons are automatically synced from their individual repositories
- **Easy Maintenance**: Updates to individual add-ons automatically appear in this repository
- **Better Organization**: Each add-on can have its own issues, releases, and documentation

## Adding a New Add-on

### 1. Create Individual Add-on Repository

First, create a separate repository for your add-on (e.g., `ha-addon-myapp`):

```
ha-addon-myapp/
├── build.yaml          # Build configuration
├── config.yaml         # Add-on configuration
├── Dockerfile          # Container definition
├── README.md           # Add-on documentation
├── .README.j2          # Template for README generation
├── DOCS.md             # Detailed documentation
├── icon.png            # Add-on icon
├── logo.png            # Add-on logo
└── rootfs/             # Root filesystem overlay
    └── etc/
        ├── cont-init.d/    # Initialization scripts
        └── services.d/     # Service management scripts
```

### 2. Required Files for Individual Add-on

#### `build.yaml`
Defines the build configuration for different architectures:

```yaml
---
build_from:
  aarch64: ghcr.io/hassio-addons/base/aarch64:14.0.0
  amd64: ghcr.io/hassio-addons/base/amd64:14.0.0
  armhf: ghcr.io/hassio-addons/base/armhf:14.0.0
  armv7: ghcr.io/hassio-addons/base/armv7:14.0.0
  i386: ghcr.io/hassio-addons/base/i386:14.0.0
labels:
  io.hass.type: addon
  io.hass.version: "1.0.0"
```

#### `config.yaml`
Defines the add-on metadata and configuration:

```yaml
name: "Add-on Name"
version: "1.0.0"
slug: "addon-slug"
description: "Brief description of the add-on"
arch:
  - armhf
  - armv7
  - aarch64
  - amd64
  - i386
startup: application
init: false
ports:
  8080/tcp: 8080
map:
  - config:rw
webui: "http://[HOST]:[PORT:8080]"
ingress: true
ingress_port: 8080
panel_icon: mdi:icon-name
homeassistant_api: false
options:
  log_level: info
schema:
  log_level: list(trace|debug|info|warning|error|fatal)
```

#### `Dockerfile`
Defines how to build the container:

```dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Install dependencies
RUN apk add --no-cache package-name

# Copy root filesystem
COPY rootfs /

# Build arguments and labels
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION

LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version="${BUILD_VERSION}"
```

### 3. Service Management

#### Initialization Script (`rootfs/etc/cont-init.d/addon.sh`)
```bash
#!/usr/bin/with-contenv bashio
# ==============================================================================
# Start Add-on
# ==============================================================================

bashio::log.info "Starting Add-on..."

# Create config directory if it doesn't exist
mkdir -p /config/addon-name

# Set permissions
chmod 755 /config/addon-name

# Start the service
exec s6-setuidgid abc your-command
```

#### Service Run Script (`rootfs/etc/services.d/addon/run`)
```bash
#!/usr/bin/with-contenv bashio
# ==============================================================================
# Start Add-on
# ==============================================================================

bashio::log.info "Starting Add-on..."

# Start the service
exec s6-setuidgid abc your-command
```

#### Service Finish Script (`rootfs/etc/services.d/addon/finish`)
```bash
#!/usr/bin/with-contenv bashio
# ==============================================================================
# Stop Add-on
# ==============================================================================

bashio::log.info "Stopping Add-on..."
```

### 4. Documentation

Create comprehensive documentation for your add-on:

- `README.md`: Basic information and installation instructions
- `DOCS.md`: Detailed documentation with examples
- `.README.j2`: Template for README generation (optional)

### 5. Add to Main Repository

After creating your individual add-on repository:

1. **Add Configuration**: Add your add-on to `addons.json` in this repository:

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

2. **Sync Add-on**: Run the updater script to sync your add-on:

```bash
# Update all add-ons (including your new one)
./scripts/update.sh

# Or update specific add-on
./scripts/update.sh --addon myapp
```

3. **Test**: Verify that your add-on appears correctly in the main repository

## Updating Existing Add-ons

### Individual Repository Updates

1. Make changes to your add-on in its individual repository
2. Commit and push the changes
3. The main repository will automatically sync the changes (or you can manually trigger the sync)

### Manual Syncing

You can manually sync add-ons using the provided scripts:

```bash
# Update all add-ons
./scripts/update.sh

# Update specific add-on
./scripts/update.sh --addon chisel

# Using Python directly
python3 scripts/update-addons.py --addon chisel
```

## Development Guidelines

### Code Style

- Use consistent indentation (2 spaces for YAML)
- Follow the existing naming conventions
- Use descriptive variable and function names
- Add comments for complex logic

### Testing

- Test your add-on on multiple architectures if possible
- Verify that the add-on starts and stops correctly
- Test configuration changes
- Check that logs are properly formatted

### Security

- Run services as non-root user (use `s6-setuidgid abc`)
- Validate all user inputs
- Use secure defaults
- Follow the principle of least privilege

## Submitting Changes

### For Individual Add-ons

1. Fork your add-on's individual repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes
4. Test thoroughly
5. Commit with a descriptive message
6. Push to your fork
7. Create a pull request

### For Main Repository

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/add-new-addon`
3. Add your add-on configuration to `addons.json`
4. Run the updater script to sync your add-on
5. Commit the changes
6. Push to your fork
7. Create a pull request

## Questions?

If you have questions about contributing, please:

- Open an issue on the relevant repository (individual add-on or main repository)
- Join the [Home Assistant Community Discord][discord]
- Check the [Home Assistant Community Forum][forum]

[discord]: https://discord.gg/hassioaddons
[forum]: https://community.home-assistant.io/ 