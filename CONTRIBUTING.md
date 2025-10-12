# Contributing to Firebase Genkit Plugin for Claude Code

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Requesting Features](#requesting-features)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to:
- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other contributors

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/claude-genkit-plugin.git
   cd claude-genkit-plugin
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Prerequisites
- Node.js 18+ (for testing JavaScript/TypeScript flows)
- Bash shell (Linux/macOS/WSL)
- Git
- Text editor or IDE

### Local Testing
```bash
# Make scripts executable
chmod +x commands/*.sh

# Test the plugin locally in Claude Code
/plugin install /path/to/claude-genkit-plugin

# Test individual commands
cd test-project
/genkit-doctor
```

## How to Contribute

### Types of Contributions

1. **Bug Fixes**
   - Fix issues in existing commands
   - Improve error handling
   - Fix documentation errors

2. **New Features**
   - New flow templates
   - Additional deployment platforms
   - Enhanced AI assistant capabilities
   - New commands

3. **Documentation**
   - Improve README
   - Add examples
   - Fix typos
   - Translate documentation

4. **Testing**
   - Add test scenarios
   - Improve test coverage
   - Report bugs

## Coding Standards

### Bash Scripts

```bash
#!/bin/bash
set -e  # Exit on error

# Use descriptive variable names
PROJECT_NAME="my-project"

# Add comments for complex logic
# Calculate the hash of the file
HASH=$(sha256sum file.txt)

# Use color codes for output
GREEN='\033[0;32m'
NC='\033[0m'
echo -e "${GREEN}Success!${NC}"

# Always handle errors
if [ ! -f "package.json" ]; then
    echo "Error: package.json not found"
    exit 1
fi
```

### JSON Files

- Use 2-space indentation
- Keep property order consistent
- Validate JSON syntax before committing

### Documentation

- Use clear, concise language
- Include code examples
- Add screenshots where helpful
- Keep formatting consistent

## Testing

### Manual Testing Checklist

Before submitting a PR, test:

- [ ] `/genkit-init` - Creates valid project structure
- [ ] `/genkit-run` - Starts dev server successfully
- [ ] `/genkit-flow` - All templates generate valid code
- [ ] `/genkit-deploy` - Deployment wizards work correctly
- [ ] `/genkit-doctor` - Health checks are accurate
- [ ] AI assistant responds appropriately

### Test on Multiple Platforms

If possible, test on:
- [ ] Linux
- [ ] macOS
- [ ] Windows (WSL)

### Test with Multiple Languages

- [ ] TypeScript projects
- [ ] JavaScript projects
- [ ] Go projects (if applicable)
- [ ] Python projects (if applicable)

## Submitting Changes

### Pull Request Process

1. **Update your fork** with the latest changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Make your changes** following coding standards

3. **Test thoroughly** using the checklist above

4. **Commit your changes** with descriptive messages:
   ```bash
   git add .
   git commit -m "feat: add support for Cloud Functions 2nd gen deployment"
   ```

   **Commit Message Format:**
   ```
   <type>: <description>

   [optional body]

   [optional footer]
   ```

   **Types:**
   - `feat`: New feature
   - `fix`: Bug fix
   - `docs`: Documentation changes
   - `style`: Code style changes (formatting)
   - `refactor`: Code refactoring
   - `test`: Adding tests
   - `chore`: Maintenance tasks

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** on GitHub:
   - Provide a clear title and description
   - Reference related issues
   - Include screenshots if applicable
   - List what you tested

### PR Review Process

- Maintainers will review your PR
- Address any requested changes
- Once approved, your PR will be merged
- Your contribution will be credited in CHANGELOG.md

## Reporting Bugs

### Before Reporting

1. Check [existing issues](https://github.com/amitpatole/claude-genkit-plugin/issues)
2. Test with the latest version
3. Reproduce the bug in a clean environment

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Run `/genkit-init`
2. Select TypeScript
3. See error...

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Node.js version: [e.g., 18.16.0]
- Plugin version: [e.g., 1.0.0]

**Screenshots**
If applicable, add screenshots.

**Additional context**
Any other relevant information.
```

## Requesting Features

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
Describe the problem.

**Proposed solution**
Describe your solution.

**Alternatives considered**
What alternatives did you consider?

**Additional context**
Any other context or mockups.
```

## Development Tips

### Adding a New Command

1. Create script in `commands/`:
   ```bash
   commands/genkit-newcommand.sh
   ```

2. Add to `plugin.json`:
   ```json
   {
     "name": "genkit-newcommand",
     "description": "Description",
     "script": "commands/genkit-newcommand.sh"
   }
   ```

3. Make executable:
   ```bash
   chmod +x commands/genkit-newcommand.sh
   ```

4. Test locally
5. Update README.md
6. Update CHANGELOG.md

### Adding a Flow Template

In `commands/genkit-flow.sh`, add a new case:

```bash
case $TEMPLATE_CHOICE in
    7)
        # Your new template
        cat > "$FLOW_FILE" << EOF
// Template code here
EOF
        echo -e "${GREEN}✅ Created custom flow${NC}"
        ;;
esac
```

### Updating the AI Assistant

Edit `agents/genkit-assistant.json`:
- Add new expertise areas
- Update code examples
- Enhance prompts

## Style Guide

### Bash Scripts
- Use `set -e` to exit on errors
- Add descriptive comments
- Use colored output for clarity
- Validate inputs
- Provide helpful error messages

### Documentation
- Use Markdown formatting
- Include code examples
- Add headers for navigation
- Keep line length reasonable

### Git Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Capitalize first letter
- Keep first line under 72 characters
- Add detailed description in body if needed

## Questions?

- Open a [GitHub Discussion](https://github.com/amitpatole/claude-genkit-plugin/discussions)
- Create an [Issue](https://github.com/amitpatole/claude-genkit-plugin/issues)
- Email: amit.patole@gmail.com

## Recognition

Contributors will be:
- Listed in CHANGELOG.md
- Credited in release notes
- Acknowledged in README.md (for significant contributions)

Thank you for contributing to make this plugin better! 🎉
