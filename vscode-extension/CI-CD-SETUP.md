# CI/CD Setup for VS Code Extension

Automated publishing to VS Code Marketplace using GitHub Actions.

## Overview

The CI/CD pipeline automatically publishes the VS Code extension to the marketplace when changes are merged to the `main` branch and the version number in `package.json` has been updated.

## Features

- ✅ **Automatic Publishing** - Publishes on merge to main (if version changed)
- ✅ **Version Check** - Skips publish if version already exists on marketplace
- ✅ **Dependency Caching** - Faster builds with npm cache
- ✅ **Compilation** - TypeScript compilation and validation
- ✅ **Testing** - Runs tests before publishing (if configured)
- ✅ **Package Verification** - Validates package structure with `vsce ls`
- ✅ **Git Tags** - Creates version tags automatically
- ✅ **GitHub Releases** - Creates releases with VSIX artifacts
- ✅ **Manual Trigger** - Can be triggered manually for hotfixes
- ✅ **Build Summaries** - Clear success/skip messages in GitHub UI

## Workflow Triggers

### Automatic (Push to Main)

The workflow triggers automatically when:
1. Code is pushed or PR is merged to `main` branch
2. Changes are in the `vscode-extension/` directory
3. Version in `package.json` is different from published version

### Manual (Workflow Dispatch)

You can manually trigger the workflow from GitHub:
1. Go to **Actions** tab
2. Select **"Publish VS Code Extension"** workflow
3. Click **"Run workflow"**
4. Choose version bump type: `patch`, `minor`, or `major`

## Setup Instructions

### 1. Create Personal Access Token (PAT)

1. **Go to Azure DevOps:**
   - URL: https://dev.azure.com/_usersSettings/tokens

2. **Create New Token:**
   - Name: `GitHub Actions VS Code Publisher`
   - Organization: `All accessible organizations`
   - Expiration: 1 year (or your preference)
   - Scopes: **Marketplace (Manage)** ✅

3. **Copy the token** (you won't see it again!)

### 2. Add GitHub Secret

1. **Go to your GitHub repository:**
   - URL: https://github.com/amitpatole/claude-genkit-plugin/settings/secrets/actions

2. **Add new secret:**
   - Name: `PAT_TOKEN`
   - Value: Paste your Azure DevOps PAT from step 1

3. **Save the secret**

### 3. Verify Workflow File

The workflow file should be at:
```
.github/workflows/publish-vscode-extension.yml
```

It's already configured and ready to use!

### 4. Test the Workflow

**Option A: Test with version bump**
```bash
cd vscode-extension

# Update version in package.json
npm version patch  # or minor, or major

# Commit and push
git add package.json package-lock.json
git commit -m "chore: bump version to $(node -p 'require(\"./package.json\").version')"
git push origin main
```

**Option B: Manual trigger**
1. Go to Actions tab
2. Select workflow
3. Click "Run workflow"
4. Select version bump type

## Workflow Steps

The workflow performs these steps sequentially (matching `publish.sh`):

### 1. Environment Setup
- ✅ Checkout code
- ✅ Setup Node.js 20
- ✅ Cache npm dependencies

### 2. Build & Test
- ✅ Install dependencies (`npm ci`)
- ✅ Compile TypeScript (`npm run compile`)
- ✅ Run tests (`npm test` - optional)
- ✅ Install vsce globally

### 3. Validation
- ✅ Verify package structure (`vsce ls`)
- ✅ Check current vs published version
- ✅ Skip if version unchanged

### 4. Publishing (if version changed)
- ✅ Package extension (`vsce package`)
- ✅ Publish to marketplace (`vsce publish`)
- ✅ Create Git tag (`vscode-v1.0.1`)
- ✅ Upload VSIX artifact (90-day retention)
- ✅ Create GitHub Release with notes

### 5. Reporting
- ✅ Generate build summary
- ✅ Show marketplace link
- ✅ Provide install command

## Version Management

### Semantic Versioning

Follow semantic versioning (semver):
- **Patch** (1.0.0 → 1.0.1) - Bug fixes, minor changes
- **Minor** (1.0.0 → 1.1.0) - New features, backwards compatible
- **Major** (1.0.0 → 2.0.0) - Breaking changes

### Updating Version

**Method 1: npm version command (recommended)**
```bash
cd vscode-extension

# For bug fixes
npm version patch

# For new features
npm version minor

# For breaking changes
npm version major
```

**Method 2: Manual edit**
Edit `vscode-extension/package.json`:
```json
{
  "version": "1.0.2"
}
```

Then run:
```bash
npm install  # Updates package-lock.json
```

### Version Check Logic

The workflow checks if the version should be published:

```bash
# Gets current version from package.json
CURRENT_VERSION=$(node -p "require('./package.json').version")

# Gets published version from marketplace
PUBLISHED_VERSION=$(npx vsce show amitpatole.genkit-vscode --json | jq -r '.versions[0].version')

# Publishes only if different
if [ "$CURRENT_VERSION" != "$PUBLISHED_VERSION" ]; then
  # Publish to marketplace
fi
```

## Artifacts & Releases

### VSIX Artifacts

Every successful publish creates a VSIX artifact:
- **Location:** Actions → Workflow run → Artifacts section
- **Retention:** 90 days
- **Filename:** `genkit-vscode-{version}.vsix`
- **Use case:** Manual installation, testing, backup

### GitHub Releases

Automatic GitHub releases include:
- **Tag:** `vscode-v{version}` (e.g., `vscode-v1.0.1`)
- **Name:** `VS Code Extension v{version}`
- **Assets:** VSIX file
- **Description:** Installation instructions and links

## Monitoring & Debugging

### View Workflow Runs

1. Go to **Actions** tab in GitHub
2. Select **"Publish VS Code Extension"** workflow
3. View recent runs and their status

### Workflow Status Badges

Add to your README:
```markdown
[![Publish VS Code Extension](https://github.com/amitpatole/claude-genkit-plugin/actions/workflows/publish-vscode-extension.yml/badge.svg)](https://github.com/amitpatole/claude-genkit-plugin/actions/workflows/publish-vscode-extension.yml)
```

### Check Logs

Each step has detailed logs:
- Click on workflow run
- Click on "publish" job
- Expand any step to see logs

### Common Issues

#### Issue: "Version already published"

**Symptom:** Workflow runs but skips publishing
**Cause:** Version in `package.json` matches marketplace version
**Fix:** Bump version number

```bash
npm version patch
git add package.json package-lock.json
git commit -m "chore: bump version"
git push
```

#### Issue: "401 Unauthorized"

**Symptom:** Publishing fails with 401 error
**Cause:** Invalid or expired PAT token
**Fix:** Regenerate PAT and update GitHub secret

1. Create new PAT at https://dev.azure.com/_usersSettings/tokens
2. Update `PAT_TOKEN` secret in GitHub repository settings

#### Issue: "Could not find publisher"

**Symptom:** Publishing fails with publisher not found
**Cause:** Publisher ID mismatch
**Fix:** Verify publisher ID in `package.json` matches your Azure DevOps publisher

```json
{
  "publisher": "amitpatole"
}
```

#### Issue: "Compilation failed"

**Symptom:** Workflow fails at compile step
**Cause:** TypeScript compilation errors
**Fix:** Test compilation locally

```bash
cd vscode-extension
npm run compile
```

#### Issue: "Package verification failed"

**Symptom:** `vsce ls` step fails
**Cause:** Missing required files or invalid structure
**Fix:** Test packaging locally

```bash
cd vscode-extension
vsce package
vsce ls
```

## Security Best Practices

### PAT Token Security

✅ **DO:**
- Store PAT in GitHub Secrets (encrypted at rest)
- Set minimal required scopes (Marketplace: Manage only)
- Set reasonable expiration (90-365 days)
- Rotate tokens regularly
- Use different PATs for different purposes

❌ **DON'T:**
- Commit PAT to git
- Share PAT in plain text
- Use PAT with excessive permissions
- Use same PAT across multiple projects
- Store PAT in environment variables locally

### Workflow Permissions

The workflow uses:
- `GITHUB_TOKEN` - Automatic, scoped to repository, creates releases
- `PAT_TOKEN` - Your secret, only for VS Code Marketplace publishing

### Audit Trail

Every publish creates:
- Git commit (if version bump via npm)
- Git tag (`vscode-v{version}`)
- GitHub Release
- GitHub Actions log
- VS Code Marketplace entry

## Manual Publishing (Fallback)

If CI/CD is unavailable, use manual publishing:

```bash
cd vscode-extension

# Install and compile
npm install
npm run compile

# Publish with PAT
vsce publish --pat YOUR_PAT_TOKEN

# Or use environment variable
export VSCE_PAT="YOUR_PAT_TOKEN"
vsce publish
```

See [QUICKSTART.md](QUICKSTART.md) for detailed manual publishing instructions.

## Workflow Customization

### Trigger on Different Branch

Edit `.github/workflows/publish-vscode-extension.yml`:
```yaml
on:
  push:
    branches:
      - main        # Change to your branch
      - release/*   # Add pattern matching
```

### Add Pre-publish Checks

Add steps before publishing:
```yaml
- name: Lint code
  run: npm run lint

- name: Run integration tests
  run: npm run test:integration

- name: Security audit
  run: npm audit --audit-level=moderate
```

### Notifications

Add Slack/Discord/Email notifications:
```yaml
- name: Notify success
  if: success()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "VS Code extension v${{ steps.version_check.outputs.current_version }} published!"
      }
```

### Staging Environment

Add a staging marketplace:
```yaml
- name: Publish to staging
  if: github.ref == 'refs/heads/develop'
  run: vsce publish --pre-release --pat $VSCE_PAT
```

## Comparing with publish.sh

The GitHub Actions workflow replicates all `publish.sh` functionality:

| Feature | publish.sh | GitHub Actions | Notes |
|---------|------------|----------------|-------|
| Install dependencies | ✅ npm install | ✅ npm ci | CI uses ci for reproducibility |
| Compile TypeScript | ✅ npm run compile | ✅ npm run compile | Identical |
| Run tests | ✅ npm test | ✅ npm test | Optional in both |
| Install vsce | ✅ npm install -g @vscode/vsce | ✅ Same | Identical |
| Verify package | ✅ vsce ls | ✅ vsce ls | Identical |
| Publish | ✅ vsce publish --pat | ✅ vsce publish --pat | Identical |
| Version check | ❌ Manual | ✅ Automatic | CI checks marketplace |
| Git tags | ❌ Manual | ✅ Automatic | CI creates tags |
| Releases | ❌ Manual | ✅ Automatic | CI creates releases |
| Artifacts | ❌ Local only | ✅ Uploaded | 90-day retention |

**Advantage:** CI/CD is automated, consistent, and creates audit trail.

## Rollback Procedure

If you need to rollback a published version:

### Option 1: Unpublish (Not Recommended)
```bash
vsce unpublish amitpatole.genkit-vscode
```
⚠️ **Warning:** This removes the extension entirely from marketplace.

### Option 2: Publish Previous Version
```bash
# Revert to previous version
git checkout vscode-v1.0.0  # Previous tag
cd vscode-extension
npm version 1.0.2  # Higher than current bad version
vsce publish --pat $PAT_TOKEN
```

### Option 3: Quick Hotfix
```bash
# Fix the bug
# Bump patch version
npm version patch
git commit -am "fix: critical bug fix"
git push origin main  # Triggers CI/CD
```

## Support & Resources

- **Workflow Status:** https://github.com/amitpatole/claude-genkit-plugin/actions
- **Marketplace:** https://marketplace.visualstudio.com/manage/publishers/amitpatole
- **VSCE Documentation:** https://code.visualstudio.com/api/working-with-extensions/publishing-extension
- **GitHub Actions Docs:** https://docs.github.com/en/actions

## Troubleshooting Commands

```bash
# Check current published version
npx vsce show amitpatole.genkit-vscode

# Validate package locally
cd vscode-extension
vsce package
vsce ls

# Test installation locally
code --install-extension genkit-vscode-*.vsix

# Check workflow syntax
cd .github/workflows
yamllint publish-vscode-extension.yml  # If yamllint installed
```

---

**Ready to publish automatically?** Just merge to main with a version bump! 🚀

**Questions?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or open an issue.
