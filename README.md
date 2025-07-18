# M2SH Home Assistant Add-ons

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

This repository contains Home Assistant add-ons developed and maintained by Mohammad Shahgolzadeh.

## Add-ons

This repository contains the following add-ons:

### [🛡️ Gluetun VPN Client](./gluetun/)

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]

A VPN client add-on that provides a secure tunnel for your Home Assistant instance with support for multiple VPN providers.

## Installation

To install these add-ons, follow these steps:

1. Navigate to the **Supervisor** page in your Home Assistant instance
2. Open the **Add-on Store** tab
3. Click on the **⋮** (three dots) button in the top right corner
4. Select **Repositories**
5. Add the following repository URL:
   ```
   https://github.com/m2sh/ha-addons
   ```
6. Click **Add**
7. The add-ons from this repository should now be available in your **Add-on Store**

## Add-on Documentation

Each add-on has its own documentation with installation instructions, configuration options, and usage guidelines. Click on the add-on name above to access its documentation.

## Support

If you encounter any issues with these add-ons, please check the following:

1. Read the add-on documentation thoroughly
2. Check the [Issues](https://github.com/m2sh/ha-addons/issues) page for known problems
3. Create a new issue if your problem isn't already reported

### 🔧 Adding More Add-ons

To add new add-ons, simply:

1. Update `addons.yml` with the new add-on configuration
2. Run `python3 scripts/update_addons.py` or trigger the GitHub Action
3. Update the README.md to include the new add-on

### 📋 How It Works

- **`addons.yml`**: Defines which add-ons are included and their source repositories
- **Direct File Copying**: Each add-on is fetched and copied directly from its repository
- **GitHub Actions**: Automatically updates add-ons when changes are detected in source repositories
- **Smart Updates**: Only updates add-ons when new commits are available
- **Home Assistant Integration**: The repository structure is compatible with Home Assistant's add-on system

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Home Assistant team for the excellent platform
- The community for inspiration and support

---

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
[commits-shield]: https://img.shields.io/github/commit-activity/y/m2sh/ha-addons.svg
[commits]: https://github.com/m2sh/ha-addons/commits/main
[license-shield]: https://img.shields.io/github/license/m2sh/ha-addons.svg
[releases-shield]: https://img.shields.io/github/release/m2sh/ha-addons.svg
[releases]: https://github.com/m2sh/ha-addons/releases 