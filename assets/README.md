# Assets Directory

This directory contains visual assets for the Firebase Genkit plugin.

## Required Screenshots

Please add the following screenshots before marketplace submission:

### 1. icon.png
- **Size:** 128x128px or 256x256px
- **Format:** PNG with transparency
- **Content:** Plugin logo/icon
- **Usage:** Marketplace listing icon

### 2. screenshot-init.png
- **Content:** Screenshot of `/genkit-init` command in action
- **Shows:** Interactive project setup wizard
- **Recommended size:** 1280x800px or similar

### 3. screenshot-flow.png
- **Content:** Screenshot of `/genkit-flow` command
- **Shows:** Flow template selection and generation
- **Recommended size:** 1280x800px or similar

### 4. screenshot-deploy.png
- **Content:** Screenshot of `/genkit-deploy` command
- **Shows:** Deployment platform selection wizard
- **Recommended size:** 1280x800px or similar

### 5. screenshot-doctor.png (optional)
- **Content:** Screenshot of `/genkit-doctor` health check results
- **Shows:** Successful health check output
- **Recommended size:** 1280x800px or similar

### 6. demo.gif (optional)
- **Content:** Animated demo showing complete workflow
- **Shows:** Init → Flow → Run → Deploy
- **Max size:** 5MB
- **Recommended dimensions:** 800x600px

## How to Capture Screenshots

### Using Claude Code Terminal

1. Run the command in Claude Code terminal
2. Capture the terminal output
3. Use screenshot tools:
   - **Linux:** `gnome-screenshot` or `scrot`
   - **macOS:** Cmd + Shift + 4
   - **Windows:** Snipping Tool or Win + Shift + S

### Recording GIFs

Use tools like:
- [asciinema](https://asciinema.org/) - Terminal recording
- [terminalizer](https://terminalizer.com/) - Terminal to GIF
- [peek](https://github.com/phw/peek) - Screen to GIF (Linux)
- [LICEcap](https://www.cockos.com/licecap/) - Screen to GIF (Cross-platform)

## Icon Design Guidelines

If creating a custom icon:
- Use Firebase colors (orange/yellow) + Genkit theme
- Keep it simple and recognizable
- Ensure it's visible at small sizes
- Use transparent background
- Consider dark/light mode compatibility

## Placeholder

Until real screenshots are added, update the marketplace.json to remove screenshot URLs or use placeholder images.

## Contributing Screenshots

If you'd like to contribute high-quality screenshots:
1. Capture screenshots following the guidelines above
2. Add them to this directory
3. Submit a Pull Request
4. Update marketplace.json with new URLs

Thank you for helping improve the plugin's presentation! 🎨
