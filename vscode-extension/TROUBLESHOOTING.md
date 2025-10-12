# Troubleshooting VS Code Extension Publishing

## Error: "Cannot create an item in a locked collection"

This error occurs when `vsce` tries to save credentials to your system keychain, but the keychain is locked or unavailable.

### Solution 1: Use PAT Directly (Recommended for Linux/CI)

Instead of using `vsce login`, pass the PAT directly with the `--pat` flag:

```bash
# Don't use vsce login, use this instead:
vsce publish --pat YOUR_PERSONAL_ACCESS_TOKEN

# Or with version bump:
vsce publish patch --pat YOUR_PERSONAL_ACCESS_TOKEN
vsce publish minor --pat YOUR_PERSONAL_ACCESS_TOKEN
vsce publish major --pat YOUR_PERSONAL_ACCESS_TOKEN
```

**Example:**
```bash
cd vscode-extension

# Package
vsce package --pat xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Publish
vsce publish --pat xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Solution 2: Use Environment Variable

Set your PAT as an environment variable:

```bash
# Set the PAT
export VSCE_PAT="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Now publish without --pat flag
vsce publish

# Or use it directly in the command
VSCE_PAT=xxxx vsce publish
```

**Add to ~/.bashrc or ~/.zshrc for permanent use:**
```bash
echo 'export VSCE_PAT="your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

### Solution 3: Unlock Keychain (Linux with GNOME)

If you're using Linux with GNOME keyring:

```bash
# Install gnome-keyring if not installed
sudo apt-get install gnome-keyring

# Unlock the keyring
gnome-keyring-daemon --unlock

# Or set password
echo -n "your_password" | gnome-keyring-daemon --unlock
```

### Solution 4: Use libsecret (Linux)

Configure git/vsce to use libsecret:

```bash
# Install libsecret
sudo apt-get install libsecret-1-0 libsecret-1-dev

# Configure
git config --global credential.helper /usr/share/doc/git/contrib/credential/libsecret/git-credential-libsecret
```

### Solution 5: Store PAT in Config File (Not Recommended for Security)

Create a `.vsce` file in your home directory:

```bash
# Create config file
cat > ~/.vsce << EOF
{
  "publishers": [
    {
      "name": "amitpatole",
      "pat": "your_personal_access_token_here"
    }
  ]
}
EOF

# Secure the file
chmod 600 ~/.vsce

# Now vsce will use this
vsce publish
```

**⚠️ Security Warning:** This stores your PAT in plain text. Only use for testing or in secure environments.

## Updated publish.sh Script

The script has been updated to handle this error. It now uses the `--pat` flag method.

### Using the Updated Script:

```bash
cd vscode-extension

# Run the script
./publish.sh

# When prompted for PAT, it will use --pat flag instead of login
```

## Quick Fix Command Reference

```bash
# Package with PAT
vsce package --pat YOUR_PAT

# Publish with PAT (no version bump)
vsce publish --pat YOUR_PAT

# Publish patch version
vsce publish patch --pat YOUR_PAT

# Publish minor version
vsce publish minor --pat YOUR_PAT

# Publish major version
vsce publish major --pat YOUR_PAT

# Show extension info (no auth needed)
vsce show amitpatole.genkit-vscode

# List all extensions (no auth needed)
vsce ls-publishers
```

## Environment-Specific Solutions

### Linux (Headless/SSH)
```bash
# Use --pat flag or environment variable
export VSCE_PAT="your_token"
vsce publish
```

### Linux (Desktop with GNOME)
```bash
# Unlock keyring
gnome-keyring-daemon --unlock
# Then use normal commands
vsce login amitpatole
```

### macOS
```bash
# Keychain should work normally
vsce login amitpatole
# If issues, use --pat flag
vsce publish --pat YOUR_PAT
```

### Windows
```bash
# Use Credential Manager
vsce login amitpatole
# Or use --pat flag
vsce publish --pat YOUR_PAT
```

### Docker/CI/CD
```bash
# Always use --pat flag or environment variable
vsce publish --pat $VSCE_PAT
```

## GitHub Actions Workflow (Automated Publishing)

Create `.github/workflows/publish-extension.yml`:

```yaml
name: Publish Extension

on:
  push:
    tags:
      - 'vscode-v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: |
          cd vscode-extension
          npm install

      - name: Compile
        run: |
          cd vscode-extension
          npm run compile

      - name: Publish to Marketplace
        run: |
          cd vscode-extension
          npx vsce publish --pat ${{ secrets.VSCE_PAT }}
        env:
          VSCE_PAT: ${{ secrets.VSCE_PAT }}
```

**Setup GitHub Secret:**
1. Go to: https://github.com/amitpatole/claude-genkit-plugin/settings/secrets/actions
2. Click "New repository secret"
3. Name: `VSCE_PAT`
4. Value: Your Personal Access Token
5. Click "Add secret"

**Publish with tag:**
```bash
git tag vscode-v1.0.1
git push origin vscode-v1.0.1
```

## Testing Without Publishing

```bash
# Package the extension
vsce package --pat YOUR_PAT

# Install locally
code --install-extension genkit-vscode-1.0.0.vsix --force

# Test in VS Code
# Then uninstall
code --uninstall-extension amitpatole.genkit-vscode
```

## Common Errors & Fixes

### Error: "401 Unauthorized"
```bash
# PAT is invalid or expired
# Solution: Regenerate PAT and use --pat flag
vsce publish --pat NEW_PAT
```

### Error: "404 Not Found - Publisher 'amitpatole' not found"
```bash
# Publisher doesn't exist
# Solution: Create at https://marketplace.visualstudio.com/manage/createpublisher
```

### Error: "Extension 'genkit-vscode' already exists"
```bash
# Extension already published
# Solution: Bump version first
npm version patch  # or minor/major
vsce publish --pat YOUR_PAT
```

### Error: "Missing README.md"
```bash
# README is required
# Solution: Ensure README.md exists in extension directory
ls -la README.md
```

## Best Practices

1. **Always use `--pat` flag in scripts and CI/CD**
   ```bash
   vsce publish --pat $VSCE_PAT
   ```

2. **Use environment variables for security**
   ```bash
   export VSCE_PAT="token"
   # Add to ~/.bashrc for persistence
   ```

3. **Never commit PAT to git**
   ```bash
   # Add to .gitignore
   echo ".vsce" >> .gitignore
   echo "*.pat" >> .gitignore
   ```

4. **Rotate PAT regularly**
   - Every 90 days minimum
   - Immediately if compromised

5. **Test locally before publishing**
   ```bash
   vsce package --pat $PAT
   code --install-extension *.vsix
   ```

## Quick Reference

```bash
# The fix: Use --pat flag
vsce publish --pat YOUR_PERSONAL_ACCESS_TOKEN

# Or use environment variable
export VSCE_PAT="YOUR_TOKEN"
vsce publish

# Package only
vsce package --pat YOUR_PAT

# Check what will be published
vsce ls --pat YOUR_PAT
```

---

**Problem solved!** Use `--pat` flag to bypass keychain issues. ✅

For more help, see [PUBLISHING.md](PUBLISHING.md) or [QUICKSTART.md](QUICKSTART.md).
