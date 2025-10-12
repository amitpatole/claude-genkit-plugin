# Quick Start: Publishing to VS Code Marketplace

The fastest way to get your Genkit extension published!

## TL;DR - Fast Track (5 minutes)

### 1. Create Azure DevOps Account & PAT
```
1. Go to: https://dev.azure.com
2. Sign in / Create account
3. Create organization (any name)
4. User Settings → Personal Access Tokens → New Token
5. Name: "vscode-marketplace"
6. Scope: Marketplace (Manage) ← IMPORTANT!
7. Copy token (you won't see it again!)
```

### 2. Create Publisher
```
1. Go to: https://marketplace.visualstudio.com/manage
2. Sign in (same Microsoft account)
3. Create Publisher
   - ID: amitpatole (or your choice)
   - Name: Amit Patole
```

### 3. Install vsce
```bash
# Install vsce
npm install -g @vscode/vsce

# DON'T use vsce login (causes keychain errors on Linux)
# Instead, use --pat flag (see step 4)
```

### 4. Publish!
```bash
# Use the automated script (handles PAT automatically)
./publish.sh

# Or manually with --pat flag:
npm install
npm run compile
vsce publish --pat YOUR_PERSONAL_ACCESS_TOKEN

# Or use environment variable:
export VSCE_PAT="YOUR_TOKEN"
vsce publish
```

### 🔴 Fix for "Cannot create an item in a locked collection" Error

**The Fix:** Use `--pat` flag instead of `vsce login`

```bash
# ❌ DON'T DO THIS (causes keychain error):
vsce login amitpatole

# ✅ DO THIS INSTEAD:
vsce publish --pat YOUR_PERSONAL_ACCESS_TOKEN

# Or set environment variable:
export VSCE_PAT="YOUR_TOKEN"
vsce publish
```

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

## Using the Automated Script

```bash
cd vscode-extension
./publish.sh
```

**Menu Options:**
1. ✅ Install dependencies and compile
2. 📦 Package extension (.vsix)
3. 🧪 Test extension locally
4. 🔐 Login to publisher account
5. 🚀 Publish (patch: 1.0.0 → 1.0.1)
6. 🚀 Publish (minor: 1.0.0 → 1.1.0)
7. 🚀 Publish (major: 1.0.0 → 2.0.0)
8. ℹ️  Show extension info
9. 🚪 Exit

## Manual Commands

```bash
# Package only (for testing)
vsce package

# Test locally
code --install-extension genkit-vscode-1.0.0.vsix

# Publish with version bump
vsce publish patch   # Bug fixes
vsce publish minor   # New features
vsce publish major   # Breaking changes

# Unpublish
vsce unpublish amitpatole.genkit-vscode
```

## First Time Setup Checklist

- [ ] Create Azure DevOps account
- [ ] Create Personal Access Token with "Marketplace (Manage)" scope
- [ ] Save PAT securely (password manager)
- [ ] Create publisher at marketplace.visualstudio.com/manage
- [ ] Install vsce: `npm install -g @vscode/vsce`
- [ ] Update package.json with your publisher ID
- [ ] Login: `vsce login your-publisher-id`
- [ ] Test locally: `./publish.sh` → Option 3
- [ ] Publish: `./publish.sh` → Option 5

## Troubleshooting

### "401 Unauthorized"
- Regenerate PAT with correct scope: **Marketplace (Manage)**
- Login again: `vsce login amitpatole`

### "Publisher not found"
- Create publisher at: https://marketplace.visualstudio.com/manage/createpublisher
- Update `package.json`: `"publisher": "your-id"`

### "Extension not found in search"
- Wait 5-10 minutes for indexing
- Check: https://marketplace.visualstudio.com/items?itemName=amitpatole.genkit-vscode

## Important Links

- **Azure DevOps:** https://dev.azure.com
- **Create PAT:** https://dev.azure.com/_usersSettings/tokens
- **Publisher Portal:** https://marketplace.visualstudio.com/manage
- **Extension Page:** https://marketplace.visualstudio.com/items?itemName=amitpatole.genkit-vscode

## Next Steps After Publishing

1. ✅ Verify on marketplace
2. 🎉 Share on social media
3. 📢 Add to README badges:
   ```markdown
   [![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/amitpatole.genkit-vscode)](https://marketplace.visualstudio.com/items?itemName=amitpatole.genkit-vscode)
   ```
4. 🔄 Set up GitHub Actions for auto-publish (see PUBLISHING.md)

---

**Need detailed help?** See [PUBLISHING.md](PUBLISHING.md) for the complete guide.

**Ready to publish?** Run `./publish.sh` and follow the prompts! 🚀
