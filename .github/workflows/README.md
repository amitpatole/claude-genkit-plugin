# GitHub Actions Workflows

This directory contains automated CI/CD workflows for the Genkit VS Code Extension.

## Workflows

### 1. VS Code Extension CI/CD (`vscode-extension-ci.yml`)

**Triggers:**
- Push to `main` branch (only when `vscode-extension/` files change)
- Pull requests to `main` branch (only when `vscode-extension/` files change)
- Manual workflow dispatch

**What it does:**
1. **Build & Test** (runs on Node.js 18.x and 20.x)
   - Installs dependencies
   - Compiles TypeScript code
   - Runs linter (if configured)
   - Runs tests (if configured)
   - Packages extension as VSIX
   - Uploads VSIX as artifact (retained for 30 days)

2. **Publish to Marketplace** (only on push to main with "Release v" in commit message)
   - Automatically publishes to VS Code Marketplace
   - Creates GitHub Release
   - Requires `VSCE_PAT` secret to be configured

3. **Notify on Failure**
   - Sends notification if build fails

### 2. VS Code Extension Release (`vscode-extension-release.yml`)

**Triggers:**
- Push of version tags (e.g., `v1.1.0`, `v1.2.0`)
- Manual workflow dispatch with version input

**What it does:**
1. Compiles TypeScript and verifies compilation
2. Packages extension as VSIX with version in filename
3. Extracts changelog for the version from CHANGELOG.md
4. Publishes to VS Code Marketplace (if `VSCE_PAT` is configured)
5. Creates comprehensive GitHub Release with:
   - Changelog excerpt
   - Installation instructions
   - Documentation links
   - VSIX file as release asset
6. Generates workflow summary with release details

---

## Setup Instructions

### 1. Configure Secrets

To enable automatic publishing to VS Code Marketplace, you need to add a secret to your GitHub repository:

#### Get Your VS Code Marketplace Personal Access Token (PAT)

1. Go to [Azure DevOps](https://dev.azure.com/)
2. Sign in with your Microsoft account
3. Click on your profile icon → "Security" → "Personal Access Tokens"
4. Click "New Token"
5. Configure the token:
   - **Name**: "VS Code Marketplace - Genkit Extension"
   - **Organization**: "All accessible organizations"
   - **Expiration**: Set to 1 year (recommended)
   - **Scopes**:
     - Select "Custom defined"
     - Check "Marketplace" → "Acquire" and "Manage"
6. Click "Create"
7. **Copy the token immediately** (you won't be able to see it again)

#### Add Secret to GitHub Repository

1. Go to your GitHub repository
2. Click "Settings" → "Secrets and variables" → "Actions"
3. Click "New repository secret"
4. **Name**: `PAT_TOKEN`
5. **Value**: Paste your Personal Access Token
6. Click "Add secret"

**Note:** ✅ If you already have a `PAT_TOKEN` secret configured, the workflows will use it automatically!

### 2. Verify GitHub Token

The `GITHUB_TOKEN` is automatically provided by GitHub Actions and doesn't need configuration. It's used for creating releases.

---

## Usage

### Automatic CI on Every Push

The CI workflow runs automatically on every push to `main` or pull request that modifies `vscode-extension/` files:

```bash
git add vscode-extension/
git commit -m "feat: add new feature"
git push origin main
```

GitHub Actions will:
- ✅ Compile TypeScript
- ✅ Run tests
- ✅ Package extension
- ✅ Upload VSIX artifact

### Publish to Marketplace (Method 1: Commit Message)

Trigger marketplace publishing by including "Release v" in your commit message:

```bash
git add vscode-extension/
git commit -m "Release v1.1.0 - Major feature update"
git push origin main
```

This will:
- ✅ Run full CI/CD pipeline
- ✅ Publish to VS Code Marketplace
- ✅ Create GitHub Release

### Publish to Marketplace (Method 2: Git Tag)

Create and push a version tag to trigger the release workflow:

```bash
# Create annotated tag
git tag -a v1.1.0 -m "Release v1.1.0 - Major feature update"

# Push tag to GitHub
git push origin v1.1.0
```

This will:
- ✅ Compile and package extension
- ✅ Extract changelog for this version
- ✅ Publish to VS Code Marketplace
- ✅ Create comprehensive GitHub Release with VSIX file

### Manual Release

You can also trigger a release manually from GitHub:

1. Go to "Actions" tab in your repository
2. Click "VS Code Extension Release"
3. Click "Run workflow"
4. Enter the version (e.g., `v1.1.0`)
5. Click "Run workflow"

---

## Workflow Outputs

### CI/CD Workflow

**Artifacts:**
- `vscode-extension-18.x` - VSIX built with Node.js 18.x
- `vscode-extension-20.x` - VSIX built with Node.js 20.x

**Duration:** ~2-3 minutes

### Release Workflow

**Artifacts:**
- GitHub Release with VSIX file: `genkit-vscode-v1.1.0.vsix`
- Published on VS Code Marketplace (if VSCE_PAT is configured)

**Duration:** ~2-3 minutes

---

## Troubleshooting

### Workflow Not Triggering

**Problem:** Workflow doesn't run after pushing changes

**Solutions:**
1. Verify changes are in `vscode-extension/` directory
2. Check that you pushed to `main` branch
3. Check GitHub Actions is enabled: Settings → Actions → General → "Allow all actions"

### Compilation Failing

**Problem:** TypeScript compilation fails

**Solutions:**
1. Run locally first: `cd vscode-extension && npm run compile`
2. Fix any TypeScript errors
3. Commit and push again

### Marketplace Publishing Failing

**Problem:** Extension doesn't publish to marketplace

**Solutions:**
1. Verify `PAT_TOKEN` secret is set correctly in repository settings
2. Check token hasn't expired (renew if needed)
3. Verify token has "Marketplace" → "Manage" scope
4. Check extension publisher name matches your account
5. Ensure you have "Marketplace Publisher" permissions in VS Code

### Release Creation Failing

**Problem:** GitHub Release not created

**Solutions:**
1. Verify tag follows format `v*.*.*` (e.g., `v1.1.0`)
2. Check `GITHUB_TOKEN` has required permissions (should be automatic)
3. Ensure tag is pushed: `git push origin v1.1.0`

---

## Workflow Status Badges

Add these badges to your README to show workflow status:

### CI/CD Status
```markdown
[![CI/CD](https://github.com/amitpatole/claude-genkit-plugin/actions/workflows/vscode-extension-ci.yml/badge.svg)](https://github.com/amitpatole/claude-genkit-plugin/actions/workflows/vscode-extension-ci.yml)
```

### Release Status
```markdown
[![Release](https://github.com/amitpatole/claude-genkit-plugin/actions/workflows/vscode-extension-release.yml/badge.svg)](https://github.com/amitpatole/claude-genkit-plugin/actions/workflows/vscode-extension-release.yml)
```

---

## Best Practices

### 1. Version Bumping

Before creating a release:
1. Update version in `vscode-extension/package.json`
2. Update `CHANGELOG.md` with new version section
3. Commit changes: `git commit -m "chore: bump version to v1.1.0"`
4. Create and push tag: `git tag -a v1.1.0 -m "Release v1.1.0" && git push origin v1.1.0`

### 2. Testing Before Release

Always test locally before releasing:
```bash
cd vscode-extension
npm install
npm run compile
npx vsce package
code --install-extension genkit-vscode-1.1.0.vsix
```

### 3. Changelog Maintenance

Keep `CHANGELOG.md` updated with format:
```markdown
## [1.1.0] - 2025-10-12

### Added
- New feature description

### Changed
- Changed feature description

### Fixed
- Bug fix description
```

The release workflow extracts this section automatically.

---

## Advanced Configuration

### Modify Workflow Triggers

Edit the `on:` section in workflow files:

```yaml
on:
  push:
    branches: [main, develop]  # Add more branches
    paths:
      - 'vscode-extension/**'
  pull_request:
    branches: [main]
```

### Add More Test Steps

Add test steps in the `build-and-test` job:

```yaml
- name: Run unit tests
  working-directory: ./vscode-extension
  run: npm test

- name: Run integration tests
  working-directory: ./vscode-extension
  run: npm run test:integration
```

### Enable Code Coverage

Add coverage reporting:

```yaml
- name: Generate coverage report
  working-directory: ./vscode-extension
  run: npm run coverage

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    files: ./vscode-extension/coverage/lcov.info
```

---

## Support

If you encounter issues with the workflows:
1. Check workflow logs in GitHub Actions tab
2. Review this documentation
3. Open an issue in the repository

---

**Last Updated:** 2025-10-12
**Workflows Version:** 1.0.0
