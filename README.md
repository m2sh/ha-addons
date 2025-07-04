# M2SH Home Assistant Add-ons

[![Commits][commits-shield]][commits]
[![Contributors][contributors-shield]][contributors]
[![Discord][discord-shield]][discord]
[![Forum][forum-shield]][forum]
[![GitHub Actions][github-actions-shield]][github-actions]
[![Issue][issue-shield]][issue]
[![License][license-shield]][license]
[![Maintenance][maintenance-shield]][maintenance]
[![Project Stage][project-stage-shield]][project-stage]
[![Reddit][reddit-shield]][reddit]
[![SemVer][semver-shield]][semver]

[commits-shield]: https://img.shields.io/github/commit-activity/y/m2sh/ha-addons
[commits]: https://github.com/m2sh/ha-addons/commits/main
[contributors-shield]: https://img.shields.io/github/contributors/m2sh/ha-addons
[contributors]: https://github.com/m2sh/ha-addons/graphs/contributors
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg
[discord]: https://discord.gg/c5DvZ4e
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg
[forum]: https://community.home-assistant.io?u=frenck
[github-actions-shield]: https://img.shields.io/github/workflow/status/m2sh/ha-addons/CI/main
[github-actions]: https://github.com/m2sh/ha-addons/actions
[issue-shield]: https://img.shields.io/github/issues/m2sh/ha-addons
[issue]: https://github.com/m2sh/ha-addons/issues
[license-shield]: https://img.shields.io/github/license/m2sh/ha-addons
[license]: https://github.com/m2sh/ha-addons/blob/main/LICENSE
[maintenance-shield]: https://img.shields.io/maintenance/yes/2025.svg
[maintenance]: https://github.com/m2sh/ha-addons
[project-stage-shield]: https://img.shields.io/badge/project%20stage-production%20ready-brightgreen.svg
[project-stage]: https://github.com/m2sh/ha-addons
[reddit-shield]: https://img.shields.io/badge/reddit-join-reddit.svg
[reddit]: https://reddit.com/r/homeassistant
[semver-shield]: https://img.shields.io/badge/semver-2.0.0-brightgreen.svg
[semver]: https://semver.org/spec/v2.0.0.html

_My personal Home Assistant add-ons repository._

## Add-ons

This repository contains the following add-ons:

### 🧩 Chisel

[![Chisel Release][chisel-shield]][chisel]
![Project Stage][project-stage-shield]
![Project Maintenance][maintenance-shield]

[chisel]: https://github.com/jpillora/chisel
[chisel-shield]: https://img.shields.io/github/v/release/jpillora/chisel?style=flat&color=green

**Latest Version:** 1.10.1  
**Supports:** aarch64, amd64, armhf, armv7, i386

A fast TCP/UDP tunnel over HTTP, secured via SSH. It's a single executable including both client and server. Written in Go (golang). Chisel is mainly useful for passing through firewalls, though it can also be used to provide a secure endpoint into your network.

[:books: Chisel add-on documentation][chisel-docs]

## Installation

To install any of the add-ons offered in this repository, you must first add its repository URL to your Home Assistant instance. To do so, click the following button:

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fm2sh%2Fha-addons)

or manually add the following repository URL in the Home Assistant add-on store:

```
https://github.com/m2sh/ha-addons
```

Then search for any of the add-ons in our addon store (button below) to install them.

[![Open your Home Assistant instance and show the Supervisor add-on store.](https://my.home-assistant.io/badges/supervisor_addon_store.svg)](https://my.home-assistant.io/redirect/supervisor_addon_store/)

You can also install them over the buttons in the Readmes of the addon folders.

## Support

Got questions?

You have several options to get them answered:

- The [Home Assistant Community Add-ons Discord chat server][discord] for add-on support and feature requests.
- The [Home Assistant Community Forum][forum].
- Join the [Reddit subreddit][reddit] in [/r/homeassistant][reddit]

You could also [open an issue here][issue] GitHub.

## Contributing

This is an active open-source project. We are always open to people who want to
use the code or contribute to it.

We have set up a separate document containing our
[contribution guidelines](CONTRIBUTING.md).

Thank you for being involved! :heart_eyes:

## Authors & contributors

The original setup of this repository is by [Mohammad Shahgolzadeh][m2sh].

For a full list of all authors and contributors,
check [the contributor's page][contributors].

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

[chisel-docs]: https://github.com/m2sh/ha-addons/blob/main/chisel/DOCS.md
[m2sh]: https://github.com/m2sh 