#!/bin/bash
set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Firebase Genkit Plugin - Marketplace Publisher${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════${NC}"
echo ""

# Check if we're in the right directory
if [ ! -f ".claude-plugin/plugin.json" ]; then
    echo -e "${RED}❌ Error: Not in plugin directory${NC}"
    echo "Please run this script from the claude-genkit-plugin directory"
    exit 1
fi

# Get version from plugin.json
VERSION=$(grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' .claude-plugin/plugin.json | cut -d'"' -f4)

echo -e "${BLUE}Current Version:${NC} v${VERSION}"
echo ""

# Check git status
echo -e "${BLUE}Checking git status...${NC}"
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}⚠️  Uncommitted changes detected${NC}"
    git status --short
    echo ""
    read -p "Commit all changes? (y/n): " commit_changes

    if [[ $commit_changes == "y" || $commit_changes == "Y" ]]; then
        git add .
        read -p "Commit message (default: 'chore: prepare for v${VERSION} release'): " commit_msg
        commit_msg=${commit_msg:-"chore: prepare for v${VERSION} release"}
        git commit -m "$commit_msg"
        echo -e "${GREEN}✓ Changes committed${NC}"
    else
        echo -e "${RED}Aborting. Please commit changes first.${NC}"
        exit 1
    fi
fi

# Push to GitHub
echo ""
echo -e "${BLUE}Pushing to GitHub...${NC}"
if git push origin main; then
    echo -e "${GREEN}✓ Pushed to origin/main${NC}"
else
    echo -e "${RED}❌ Failed to push. Please check your authentication.${NC}"
    echo "You may need to:"
    echo "  1. Use SSH: git remote set-url origin git@github.com:amitpatole/claude-genkit-plugin.git"
    echo "  2. Or configure your personal access token"
    exit 1
fi

# Create and push tag
echo ""
echo -e "${BLUE}Creating release tag v${VERSION}...${NC}"

if git rev-parse "v${VERSION}" >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Tag v${VERSION} already exists${NC}"
    read -p "Delete and recreate? (y/n): " recreate_tag

    if [[ $recreate_tag == "y" || $recreate_tag == "Y" ]]; then
        git tag -d "v${VERSION}"
        git push origin --delete "v${VERSION}" 2>/dev/null || true
        echo -e "${GREEN}✓ Deleted old tag${NC}"
    else
        echo -e "${YELLOW}Skipping tag creation${NC}"
        exit 0
    fi
fi

git tag -a "v${VERSION}" -m "Release v${VERSION}: Firebase Genkit plugin for Claude Code

Features:
- Project initialization with multi-language support
- 6 production-ready flow templates
- Multi-platform deployment support
- Comprehensive health monitoring
- Genkit-specialized AI assistant

See CHANGELOG.md for full release notes."

git push origin "v${VERSION}"
echo -e "${GREEN}✓ Created and pushed tag v${VERSION}${NC}"

# Summary
echo ""
echo -e "${GREEN}════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   ✓ Publication Complete!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Repository:${NC} https://github.com/amitpatole/claude-genkit-plugin"
echo -e "${BLUE}Version:${NC} v${VERSION}"
echo -e "${BLUE}Tag:${NC} v${VERSION}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo ""
echo "1. Verify on GitHub:"
echo "   https://github.com/amitpatole/claude-genkit-plugin/releases"
echo ""
echo "2. Create GitHub Release (optional):"
echo "   - Go to: https://github.com/amitpatole/claude-genkit-plugin/releases/new"
echo "   - Select tag: v${VERSION}"
echo "   - Copy release notes from CHANGELOG.md"
echo "   - Publish release"
echo ""
echo "3. Submit to Claude Code Marketplace:"
echo "   - Visit Claude Code marketplace submission portal"
echo "   - Or contact: claude-code-plugins@anthropic.com"
echo "   - Include: Repository URL and version tag"
echo ""
echo "4. Test Installation:"
echo "   /plugin marketplace add https://github.com/amitpatole/claude-genkit-plugin.git"
echo "   /plugin install genkit"
echo ""
echo -e "${GREEN}Plugin is now published and ready for use! 🎉${NC}"
