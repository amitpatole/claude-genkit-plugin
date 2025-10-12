# Publishing Genkit Extension to VS Code Marketplace

Complete guide to publish the Genkit VS Code extension to the Visual Studio Marketplace.

## Prerequisites

- Microsoft/GitHub account
- Azure DevOps account (free)
- Node.js 18+ installed
- Extension package ready

## Step 1: Create Azure DevOps Organization

1. **Go to Azure DevOps:**
   - Visit: https://dev.azure.com
   - Sign in with your Microsoft account (or create one)

2. **Create a new organization:**
   - Click "Create new organization"
   - Name it (e.g., `amitpatole-vscode`)
   - Choose region: United States
   - Complete CAPTCHA

3. **Create a project (optional but recommended):**
   - Name: `vscode-extensions`
   - Visibility: Private
   - Click "Create project"

## Step 2: Create Personal Access Token (PAT)

1. **Navigate to Personal Access Tokens:**
   - Click on your profile icon (top right)
   - Select "Personal access tokens"
   - Or visit: https://dev.azure.com/[YOUR_ORG]/_usersSettings/tokens

2. **Create new token:**
   - Click "+ New Token"
   - Name: `vscode-marketplace-publish`
   - Organization: Select your organization
   - Expiration: Custom defined (1 year recommended)
   - Scopes: **IMPORTANT - Select "Custom defined"**
   - Check: **"Marketplace" → "Manage"** (this is critical!)
   - Click "Create"

3. **Save your token:**
   - **COPY THE TOKEN IMMEDIATELY** - You won't see it again!
   - Save it securely (e.g., password manager)
   - Format: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## Step 3: Create Publisher on VS Code Marketplace

1. **Go to Visual Studio Marketplace:**
   - Visit: https://marketplace.visualstudio.com/manage
   - Sign in with the same Microsoft account

2. **Create a publisher:**
   - Click "Create publisher"
   - **Publisher ID:** `amitpatole` (must be unique, lowercase, no spaces)
   - **Display Name:** `Amit Patole`
   - **Description:** `Firebase Genkit tools and extensions`
   - Click "Create"

3. **Verify publisher:**
   - You should see your publisher page
   - Note your publisher ID (you'll need this)

## Step 4: Install VSCE (Visual Studio Code Extensions CLI)

```bash
# Install vsce globally
npm install -g @vscode/vsce

# Verify installation
vsce --version
```

## Step 5: Update package.json

Make sure your `package.json` has the correct publisher:

```json
{
  "name": "genkit-vscode",
  "publisher": "amitpatole",  // ← Your publisher ID
  "version": "1.0.0",
  // ... rest of config
}
```

## Step 6: Add Publisher Icon (Optional but Recommended)

1. **Create icon:**
   - Size: 128x128 pixels (PNG format)
   - Name: `icon.png`
   - Place in: `vscode-extension/images/icon.png`

2. **Update package.json:**
   ```json
   {
     "icon": "images/icon.png",
     // ...
   }
   ```

## Step 7: Login to Publisher Account

```bash
# Navigate to extension directory
cd vscode-extension

# Login with your PAT
vsce login amitpatole

# When prompted, paste your Personal Access Token
# PAT: [paste your token here]
```

You should see: `Successfully logged in as amitpatole`

## Step 8: Package the Extension

```bash
# Install dependencies first
npm install

# Compile TypeScript
npm run compile

# Package the extension
vsce package

# This creates: genkit-vscode-1.0.0.vsix
```

## Step 9: Publish to Marketplace

### Option A: Publish Directly

```bash
# Publish the extension
vsce publish

# Or publish with version bump
vsce publish patch  # 1.0.0 → 1.0.1
vsce publish minor  # 1.0.0 → 1.1.0
vsce publish major  # 1.0.0 → 2.0.0
```

### Option B: Upload Manually

1. Go to: https://marketplace.visualstudio.com/manage/publishers/amitpatole
2. Click "New extension" → "Visual Studio Code"
3. Drag and drop the `.vsix` file
4. Click "Upload"

## Step 10: Verify Publication

1. **Check your publisher page:**
   - Visit: https://marketplace.visualstudio.com/publishers/amitpatole

2. **Search for your extension:**
   - Go to VS Code
   - Press `Ctrl+Shift+X` (Extensions)
   - Search: "Genkit"
   - You should see your extension!

3. **Install and test:**
   ```bash
   code --install-extension amitpatole.genkit-vscode
   ```

## Automated Publishing with GitHub Actions (Optional)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish VS Code Extension

on:
  push:
    tags:
      - 'v*'

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

      - name: Publish to VS Code Marketplace
        run: |
          cd vscode-extension
          npx vsce publish -p ${{ secrets.VSCE_PAT }}
        env:
          VSCE_PAT: ${{ secrets.VSCE_PAT }}
```

**Set up GitHub Secret:**
1. Go to: https://github.com/amitpatole/claude-genkit-plugin/settings/secrets/actions
2. Click "New repository secret"
3. Name: `VSCE_PAT`
4. Value: Your Personal Access Token
5. Click "Add secret"

## Publishing Updates

```bash
# Make changes to your extension

# Bump version and publish
vsce publish patch  # For bug fixes (1.0.0 → 1.0.1)
vsce publish minor  # For new features (1.0.0 → 1.1.0)
vsce publish major  # For breaking changes (1.0.0 → 2.0.0)
```

## Troubleshooting

### Error: "Failed to create publisher"
- **Solution:** Publisher ID must be unique. Try a different ID.

### Error: "401 Unauthorized"
- **Solution:**
  - PAT expired or invalid
  - Regenerate PAT with "Marketplace (Manage)" scope
  - Run `vsce login` again

### Error: "Cannot find module"
- **Solution:**
  ```bash
  cd vscode-extension
  npm install
  npm run compile
  ```

### Error: "Missing README.md"
- **Solution:** Ensure `README.md` exists in extension directory

### Error: "Publisher 'amitpatole' not found"
- **Solution:**
  - Create publisher at marketplace.visualstudio.com/manage
  - Use exact publisher ID in package.json

### Extension not showing in search
- **Solution:**
  - Wait 5-10 minutes for indexing
  - Refresh VS Code extensions view
  - Clear VS Code cache: Delete `~/.vscode/extensions`

## Best Practices

1. **Version your releases:**
   - Use semantic versioning (MAJOR.MINOR.PATCH)
   - Update CHANGELOG.md with each release

2. **Test before publishing:**
   ```bash
   vsce package
   code --install-extension genkit-vscode-1.0.0.vsix
   ```

3. **Add marketplace badges to README:**
   ```markdown
   [![Version](https://img.shields.io/visual-studio-marketplace/v/amitpatole.genkit-vscode)](https://marketplace.visualstudio.com/items?itemName=amitpatole.genkit-vscode)
   [![Installs](https://img.shields.io/visual-studio-marketplace/i/amitpatole.genkit-vscode)](https://marketplace.visualstudio.com/items?itemName=amitpatole.genkit-vscode)
   ```

4. **Unpublish if needed:**
   ```bash
   vsce unpublish amitpatole.genkit-vscode
   ```

## Quick Reference

### Essential Commands

```bash
# Login
vsce login amitpatole

# Package
vsce package

# Publish
vsce publish

# Publish with version bump
vsce publish patch|minor|major

# Show extension info
vsce show amitpatole.genkit-vscode

# Unpublish
vsce unpublish amitpatole.genkit-vscode
```

### Important URLs

- **Azure DevOps:** https://dev.azure.com
- **Create PAT:** https://dev.azure.com/[ORG]/_usersSettings/tokens
- **Marketplace Management:** https://marketplace.visualstudio.com/manage
- **Create Publisher:** https://marketplace.visualstudio.com/manage/createpublisher
- **Your Extensions:** https://marketplace.visualstudio.com/manage/publishers/amitpatole

## Security Notes

⚠️ **IMPORTANT:**
- Never commit your PAT to git
- Add PAT to `.gitignore` or use environment variables
- Rotate PAT every 90-365 days
- Use GitHub Secrets for CI/CD

## Support

If you encounter issues:
1. Check: https://code.visualstudio.com/api/working-with-extensions/publishing-extension
2. VS Code Extension API: https://code.visualstudio.com/api
3. VSCE Issues: https://github.com/microsoft/vscode-vsce/issues

---

**You're ready to publish! 🚀**

Follow these steps and your Genkit extension will be live on the VS Code Marketplace.
