# Extension Icon (Optional Enhancement)

The extension currently publishes without an icon. You can add one later to improve marketplace appearance.

## Current Status

- ✅ Extension works without icon
- ✅ No errors or warnings
- ✅ Ready to publish as-is

## Adding an Icon (Optional)

If you want to add an icon later:

### Step 1: Create Icon

Create a 128x128 PNG icon:

```bash
# Requirements
- Format: PNG
- Size: 128x128 pixels
- Name: icon.png
- Location: vscode-extension/images/icon.png
- Theme: Genkit/Firebase related
```

**Icon Ideas:**
- Firebase flame logo + "G" for Genkit
- Stylized "G" with AI elements
- Firebase colors (orange/yellow) with tech theme

**Tools to create:**
- Figma: https://figma.com
- Canva: https://canva.com
- GIMP: https://gimp.org
- Adobe Illustrator

### Step 2: Add to Extension

```bash
# Create images directory
mkdir -p vscode-extension/images

# Add your icon
cp your-icon.png vscode-extension/images/icon.png
```

### Step 3: Update package.json

Add icon field:

```json
{
  "name": "genkit-vscode",
  "displayName": "Genkit for VS Code",
  "version": "1.0.0",
  "publisher": "amitpatole",
  "icon": "images/icon.png",    // ← Add this line
  "engines": {
    ...
  }
}
```

### Step 4: Publish Update

```bash
# Bump version and publish
vsce publish patch --pat YOUR_PAT

# Or use script
./publish.sh
# Select option 5 (patch version)
```

## Sidebar Icon (Optional)

For the Genkit Explorer sidebar, add SVG icon:

```bash
# Create SVG icon
# Requirements: 24x24 or 32x32 SVG
# Location: vscode-extension/images/genkit-icon.svg
```

Update package.json:

```json
{
  "viewsContainers": {
    "activitybar": [
      {
        "id": "genkit-explorer",
        "title": "Genkit",
        "icon": "images/genkit-icon.svg"    // ← Add this line
      }
    ]
  }
}
```

## Icon Design Guidelines

### VS Code Marketplace Icon (128x128 PNG)

**Requirements:**
- Must be 128x128 pixels
- PNG format with transparency
- High contrast for light/dark themes
- Clear and recognizable at small sizes
- Professional appearance

**Design Tips:**
- Use Firebase brand colors (orange #FFA000, yellow #FFCA28)
- Keep it simple - avoid too much detail
- Test on both light and dark backgrounds
- Ensure it looks good at 64x64 (thumbnail size)

### Activity Bar Icon (24x24 SVG)

**Requirements:**
- 24x24 or 32x32 pixels
- SVG format
- Single color (VS Code will theme it)
- Works in light and dark themes

**Design Tips:**
- Simple geometric shapes
- Clear at small sizes
- No text (icon only)
- Consistent with VS Code design language

## Example Icons

You can find inspiration from:

1. **Firebase Extension Icons:**
   - Firebase VS Code extension
   - Firestore extension
   - Firebase Explorer

2. **AI/ML Extension Icons:**
   - GitHub Copilot
   - Tabnine
   - AWS Toolkit

3. **Developer Tool Icons:**
   - ESLint
   - Prettier
   - Docker

## Firebase Brand Guidelines

If using Firebase branding:

- **Official Colors:**
  - Primary Orange: #FFA000
  - Secondary Yellow: #FFCA28
  - Dark: #FF6F00

- **Logo Usage:**
  - Don't modify official Firebase logo
  - Can use inspired design
  - Follow Firebase brand guidelines

- **Reference:**
  - Firebase Brand: https://firebase.google.com/brand-guidelines

## Free Icon Resources

- **Figma Community:** https://figma.com/community
- **Flaticon:** https://flaticon.com
- **Icons8:** https://icons8.com
- **Heroicons:** https://heroicons.com
- **Font Awesome:** https://fontawesome.com

## Publishing Without Icon

✅ **Current Status:** Extension is ready to publish without icon

The extension will:
- Display with default VS Code icon
- Function perfectly
- Be fully searchable
- Look professional (just no custom icon)

You can always add an icon later by:
1. Creating the icon
2. Bumping patch version
3. Publishing update

## Summary

- ✅ **No icon required** - Extension works fine without it
- 🎨 **Optional enhancement** - Add later if desired
- 📦 **Ready to publish** - No blockers
- 🔄 **Easy to update** - Just publish new version

---

**Bottom Line:** Don't let the icon hold up your launch! Publish now, add icon later if you want.

The functionality and documentation are what matters most. 🚀
