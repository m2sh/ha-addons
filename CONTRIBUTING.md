# Contributing to M2SH Home Assistant Add-ons

Thank you for considering contributing to this Home Assistant add-ons repository! 

## 🤝 Ways to Contribute

There are many ways you can contribute to this project:

- **Bug Reports**: Found a bug? Please create an issue with detailed information
- **Feature Requests**: Have an idea for a new feature? Open an issue to discuss it
- **Code Contributions**: Submit pull requests to fix bugs or add features
- **Documentation**: Help improve documentation and guides
- **Testing**: Help test add-ons and report issues

## 📋 Before You Start

1. **Check existing issues**: Before creating a new issue, please search existing ones
2. **Read the code**: Familiarize yourself with the codebase structure
3. **Test your changes**: Ensure your modifications work correctly

## 🚀 Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/ha-addons.git
   cd ha-addons
   ```
3. **Run the setup script**:
   ```bash
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

## 📝 Adding a New Add-on

To add a new add-on to this repository:

1. **Create the add-on repository** first (separate repository)
2. **Update `addons.yml`** with your add-on configuration:
   ```yaml
   addons:
     your-addon:
       repository: https://github.com/m2sh/ha-addon-your-addon
       target: your-addon
       branch: main
       description: Brief description of your add-on
   ```
3. **Run the update script**:
   ```bash
   python3 scripts/update_addons.py
   ```
4. **Update the README.md** to include your add-on in the list

## 🔧 Making Changes

1. **Create a new branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes** following the coding standards
3. **Test thoroughly** - ensure everything works as expected
4. **Commit your changes** with clear commit messages:
   ```bash
   git commit -m "✨ Add new feature: brief description"
   ```

## 📤 Submitting Changes

1. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
2. **Create a Pull Request** on GitHub with:
   - Clear title and description
   - Reference to any related issues
   - Screenshots if applicable
   - Test results

## 🎯 Pull Request Guidelines

- **Keep it focused**: One feature/fix per pull request
- **Write clear descriptions**: Explain what changes you made and why
- **Include tests**: Add or update tests for your changes
- **Follow coding style**: Match the existing code style
- **Update documentation**: Include relevant documentation updates

## 🐛 Bug Reports

When reporting bugs, please include:

- **Add-on name and version**
- **Home Assistant version**
- **Steps to reproduce** the issue
- **Expected behavior** vs **actual behavior**
- **Logs** if applicable
- **System information** (OS, architecture, etc.)

## 💡 Feature Requests

For feature requests, please provide:

- **Clear description** of the feature
- **Use case** - why would this be useful?
- **Proposed implementation** (if you have ideas)
- **Alternative solutions** you've considered

## 📚 Code Style

- Follow Python PEP 8 guidelines
- Use meaningful variable and function names
- Include docstrings for functions and classes
- Keep functions small and focused
- Use type hints where appropriate

## 🏷️ Commit Message Format

Use clear, descriptive commit messages:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- ✨ `feat`: New feature
- 🐛 `fix`: Bug fix
- 📚 `docs`: Documentation changes
- 🎨 `style`: Code style changes
- ♻️ `refactor`: Code refactoring
- 🧪 `test`: Adding tests
- 🔧 `chore`: Maintenance tasks

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

All contributors will be recognized in the project documentation and releases.

Thank you for contributing to making Home Assistant add-ons better! 🎉 