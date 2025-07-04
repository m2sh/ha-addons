# Home Assistant Add-on Repository by m2sh

[![GitHub Release][releases-shield]][releases]
![Project Stage][project-stage-shield]
![Project Maintenance][maintenance-shield]

[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]][license]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

_Home Assistant Add-on Repository for various useful add-ons_

## About

Home Assistant allows anyone to create add-on repositories to share their add-ons for Home Assistant easily. This repository is one of those repositories, providing extra Home Assistant add-ons for your installation.

This repository uses an external add-on management system that automatically syncs add-ons from their individual repositories, ensuring you always get the latest versions and updates.

## Installation

Adding this add-ons repository to your Home Assistant instance is pretty straightforward. In the Home Assistant add-on store, a possibility to add a repository is provided.

Use the following URL to add this repository:

```
https://github.com/m2sh/ha-addons
```

## Add-ons provided by this repository

### ✓ Chisel

![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports i386 Architecture][i386-shield]

Latest Version: ![Latest Version][chisel-version-shield]

A fast TCP/UDP tunnel over HTTP, secured via SSH

📚 **[Full documentation](https://github.com/m2sh/ha-addon-chisel)**


## How it works

This repository automatically syncs add-ons from their individual repositories:

1. **External Repositories**: Each add-on is maintained in its own repository (e.g., [ha-addon-chisel](https://github.com/m2sh/ha-addon-chisel))
2. **Automatic Syncing**: The repository automatically pulls the latest versions daily
3. **Centralized Distribution**: All add-ons are made available through this single repository
4. **Easy Updates**: When you update an add-on in its individual repository, it automatically appears here

## Adding New Add-ons

To add a new add-on to this repository:

1. Create a separate repository for your add-on (e.g., `ha-addon-myapp`)
2. Add the add-on configuration to `addons.json` in this repository
3. The system will automatically sync your add-on

Example `addons.json` entry:
```json
{
  "myapp": {
    "name": "My App",
    "description": "Description of my app",
    "repository": "https://github.com/m2sh/ha-addon-myapp",
    "branch": "main",
    "type": "external",
    "architectures": ["armhf", "armv7", "aarch64", "amd64", "i386"],
    "version": "1.0.0"
  }
}
```

## Manual Updates

You can manually trigger updates using the updater script:

```bash
# Update all add-ons
python scripts/update-addons.py

# Update specific add-on
python scripts/update-addons.py --addon chisel
```

## Releases

Releases are based on Semantic Versioning, and use the format of `MAJOR.MINOR.PATCH`. In a nutshell, the version will be incremented based on the following:

- `MAJOR`: Incompatible or major changes.
- `MINOR`: Backwards-compatible new features and enhancements.
- `PATCH`: Backwards-compatible bugfixes and package updates.

## Support

Got questions?

You have several options to get them answered:

- The [Home Assistant Community Add-ons Discord chat server][discord] for add-on support and feature requests.
- The [Home Assistant Discord chat server][discord-ha] for general Home Assistant discussions and questions.
- The [Home Assistant Community Forum][forum].
- Join the Reddit subreddit in [/r/homeassistant][reddit]

In case you've found a bug, please open an issue on our GitHub repository.

## Authors & contributors

The original setup of this repository is by [Mohammad Shahgolzadeh][m2sh].

For a full list of all authors and contributors, check the contributor's page.

## License

MIT License

Copyright (c) 2025 Mohammad Shahgolzadeh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
[chisel-version-shield]: https://img.shields.io/badge/dynamic/yaml?color=blue&label=chisel&query=%24.chisel&url=https%3A%2F%2Fraw.githubusercontent.com%2Fm2sh%2Fha-addons%2Fmain%2Fchisel%2Fconfig.yaml
[commits-shield]: https://img.shields.io/github/commit-activity/y/m2sh/ha-addons.svg
[commits]: https://github.com/m2sh/ha-addons/commits/main
[contributors-shield]: https://img.shields.io/github/contributors/m2sh/ha-addons.svg
[contributors]: https://github.com/m2sh/ha-addons/graphs/contributors
[discord-ha]: https://discord.gg/c5DvZ4e
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg
[discord]: https://discord.gg/hassioaddons
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg
[forum]: https://community.home-assistant.io/t/repository-m2sh-home-assistant-add-ons
[license-shield]: https://img.shields.io/github/license/m2sh/ha-addons.svg
[license]: https://github.com/m2sh/ha-addons/blob/main/LICENSE
[maintenance-shield]: https://img.shields.io/maintenance/yes/2025.svg
[m2sh]: https://github.com/m2sh
[project-stage-shield]: https://img.shields.io/badge/project%20stage-production%20ready-brightgreen.svg
[reddit]: https://reddit.com/r/homeassistant
[releases-shield]: https://img.shields.io/github/release/m2sh/ha-addons.svg
[releases]: https://github.com/m2sh/ha-addons/releases
[chisel-docs]: https://github.com/m2sh/ha-addon-chisel 