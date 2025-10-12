#!/bin/bash

# VS Code Extension Publishing Script
# This script helps publish the Genkit extension to VS Code Marketplace

set -e

echo "🚀 Genkit VS Code Extension Publisher"
echo "======================================"
echo ""

# Check if vsce is installed
if ! command -v vsce &> /dev/null; then
    echo "❌ vsce is not installed. Installing..."
    npm install -g @vscode/vsce
    echo "✅ vsce installed successfully"
    echo ""
fi

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Are you in the vscode-extension directory?"
    exit 1
fi

# Display current version
CURRENT_VERSION=$(node -p "require('./package.json').version")
PUBLISHER=$(node -p "require('./package.json').publisher")
NAME=$(node -p "require('./package.json').name")

echo "📦 Current Extension Info:"
echo "   Name: $NAME"
echo "   Publisher: $PUBLISHER"
echo "   Version: $CURRENT_VERSION"
echo ""

# Menu
echo "What would you like to do?"
echo ""
echo "1. Install dependencies and compile"
echo "2. Package extension (.vsix)"
echo "3. Test extension locally"
echo "4. Login to publisher account"
echo "5. Publish to marketplace (patch version)"
echo "6. Publish to marketplace (minor version)"
echo "7. Publish to marketplace (major version)"
echo "8. Show extension info"
echo "9. Exit"
echo ""

read -p "Enter your choice (1-9): " choice

case $choice in
    1)
        echo ""
        echo "📥 Installing dependencies..."
        npm install
        echo ""
        echo "🔨 Compiling TypeScript..."
        npm run compile
        echo ""
        echo "✅ Dependencies installed and compiled successfully!"
        ;;

    2)
        echo ""
        echo "📦 Packaging extension..."
        npm install
        npm run compile
        vsce package
        echo ""
        echo "✅ Extension packaged successfully!"
        echo "📁 File created: $NAME-$CURRENT_VERSION.vsix"
        ;;

    3)
        echo ""
        echo "🧪 Testing extension locally..."
        npm install
        npm run compile
        vsce package
        echo ""
        echo "Installing extension in VS Code..."
        code --install-extension "$NAME-$CURRENT_VERSION.vsix" --force
        echo ""
        echo "✅ Extension installed! Restart VS Code to test."
        ;;

    4)
        echo ""
        echo "🔐 Setup Personal Access Token (PAT)..."
        echo ""
        echo "You'll need your Personal Access Token (PAT) from Azure DevOps."
        echo "Create one at: https://dev.azure.com/[YOUR_ORG]/_usersSettings/tokens"
        echo "Scope: Marketplace (Manage)"
        echo ""
        echo "NOTE: We'll use the --pat flag to avoid keychain issues."
        echo ""
        read -s -p "Enter your PAT (input hidden): " PAT
        echo ""
        echo ""
        echo "Saving PAT to environment variable..."
        export VSCE_PAT="$PAT"
        echo ""
        echo "✅ PAT configured! You can now publish using options 5-7."
        echo "💡 To persist this, add to ~/.bashrc: export VSCE_PAT=\"your_token\""
        ;;

    5)
        echo ""
        echo "🚀 Publishing PATCH version ($CURRENT_VERSION → patch)..."
        echo ""

        if [ -z "$VSCE_PAT" ]; then
            echo "⚠️  VSCE_PAT not set. Please run option 4 first or:"
            read -s -p "Enter your PAT: " PAT
            echo ""
            export VSCE_PAT="$PAT"
        fi

        npm install
        npm run compile
        vsce publish patch --pat "$VSCE_PAT"
        echo ""
        echo "✅ Published successfully!"
        ;;

    6)
        echo ""
        echo "🚀 Publishing MINOR version ($CURRENT_VERSION → minor)..."
        echo ""

        if [ -z "$VSCE_PAT" ]; then
            echo "⚠️  VSCE_PAT not set. Please run option 4 first or:"
            read -s -p "Enter your PAT: " PAT
            echo ""
            export VSCE_PAT="$PAT"
        fi

        npm install
        npm run compile
        vsce publish minor --pat "$VSCE_PAT"
        echo ""
        echo "✅ Published successfully!"
        ;;

    7)
        echo ""
        echo "🚀 Publishing MAJOR version ($CURRENT_VERSION → major)..."
        echo ""
        read -p "⚠️  This is a breaking change. Are you sure? (y/N): " confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            if [ -z "$VSCE_PAT" ]; then
                echo "⚠️  VSCE_PAT not set. Please run option 4 first or:"
                read -s -p "Enter your PAT: " PAT
                echo ""
                export VSCE_PAT="$PAT"
            fi

            npm install
            npm run compile
            vsce publish major --pat "$VSCE_PAT"
            echo ""
            echo "✅ Published successfully!"
        else
            echo "❌ Cancelled"
        fi
        ;;

    8)
        echo ""
        echo "ℹ️  Extension Information:"
        vsce show "$PUBLISHER.$NAME" || echo "Extension not yet published"
        ;;

    9)
        echo ""
        echo "👋 Goodbye!"
        exit 0
        ;;

    *)
        echo ""
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "✨ Done!"
echo ""
echo "📚 For detailed instructions, see PUBLISHING.md"
echo "🔗 Marketplace: https://marketplace.visualstudio.com/manage/publishers/$PUBLISHER"
echo ""
