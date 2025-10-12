# Genkit for VS Code

> Official Visual Studio Code extension for Firebase Genkit development

[![Version](https://img.shields.io/visual-studio-marketplace/v/amitpatole.genkit-vscode)](https://marketplace.visualstudio.com/items?itemName=amitpatole.genkit-vscode)
[![Installs](https://img.shields.io/visual-studio-marketplace/i/amitpatole.genkit-vscode)](https://marketplace.visualstudio.com/items?itemName=amitpatole.genkit-vscode)
[![Rating](https://img.shields.io/visual-studio-marketplace/r/amitpatole.genkit-vscode)](https://marketplace.visualstudio.com/items?itemName=amitpatole.genkit-vscode)

Streamline your Firebase Genkit development with intelligent code completion, snippets, commands, and integrated tooling.

## Features

### 🚀 Quick Commands

Access powerful Genkit commands directly from the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`):

- **Genkit: Initialize New Project** - Set up a new Genkit project with interactive wizard
- **Genkit: Create New Flow** - Generate flows from templates (Chat, RAG, Streaming, etc.)
- **Genkit: Start Dev Server** - Launch Genkit development server with one click
- **Genkit: Open Developer UI** - Open Genkit Developer UI in browser
- **Genkit: Deploy to Production** - Deploy to Firebase, Cloud Run, Vercel, or Docker
- **Genkit: Run Health Check** - Verify project health and dependencies

### 📝 Code Snippets

Type these prefixes to insert Genkit code:

**TypeScript/JavaScript:**
- `gflow` - Create a new Genkit flow
- `gtool` - Create a new Genkit tool
- `grag` - Create a RAG flow with vector search
- `gconfig` - Create Genkit configuration
- `gstream` - Create a streaming flow
- `genclaude` - Generate with Claude
- `gengemini` - Generate with Gemini

### 🔍 Genkit Explorer

Sidebar panel showing your project structure:
- **Flows** - View all defined flows
- **AI Models** - See configured models
- **Tools** - Browse available tools

### ⚙️ Configuration

Customize extension behavior in VS Code settings:

```json
{
  "genkit.autoStartDevServer": false,
  "genkit.devServerPort": 4000,
  "genkit.enableIntelliSense": true
}
```

## Installation

### From VS Code Marketplace

1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X` / `Cmd+Shift+X`)
3. Search for "Genkit"
4. Click "Install"

### From VSIX

1. Download the `.vsix` file from [Releases](https://github.com/amitpatole/claude-genkit-plugin/releases)
2. Run: `code --install-extension genkit-vscode-1.0.0.vsix`

## Quick Start

### 1. Create a New Genkit Project

```
Ctrl+Shift+P → "Genkit: Initialize New Project"
```

Follow the prompts to:
- Enter project name
- Choose language (TypeScript/JavaScript)
- Select AI provider (Claude, Gemini, GPT)

### 2. Create Your First Flow

Open a `.ts` or `.js` file and type:

```typescript
gflow
```

This expands to a complete flow template:

```typescript
import { defineFlow } from '@genkit-ai/flow';
import { z } from 'zod';

export const myFlow = defineFlow(
  {
    name: 'myFlow',
    inputSchema: z.object({
      input: z.string(),
    }),
    outputSchema: z.string(),
  },
  async (input) => {
    // Implement flow logic
    return input.input;
  }
);
```

### 3. Start Development Server

```
Ctrl+Shift+P → "Genkit: Start Dev Server"
```

Then open the Developer UI:

```
Ctrl+Shift+P → "Genkit: Open Developer UI"
```

## Snippets Reference

### Flow Templates

| Snippet | Description |
|---------|-------------|
| `gflow` | Basic flow template |
| `grag` | RAG flow with vector search |
| `gstream` | Streaming flow template |
| `gtool` | Tool definition |
| `gconfig` | Genkit configuration |

### AI Model Integration

| Snippet | Description |
|---------|-------------|
| `genclaude` | Claude generation |
| `gengemini` | Gemini generation |

## Commands

| Command | Description | Keyboard Shortcut |
|---------|-------------|-------------------|
| `genkit.init` | Initialize new project | - |
| `genkit.createFlow` | Create new flow | - |
| `genkit.startDevServer` | Start dev server | - |
| `genkit.openDevUI` | Open Developer UI | - |
| `genkit.deploy` | Deploy to production | - |
| `genkit.runDoctor` | Run health check | - |

## Requirements

- **VS Code** 1.80.0 or higher
- **Node.js** 18+ (for Genkit projects)
- **npm** or **yarn**

## Extension Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `genkit.autoStartDevServer` | boolean | `false` | Auto-start dev server on project open |
| `genkit.devServerPort` | number | `4000` | Port for development server |
| `genkit.enableIntelliSense` | boolean | `true` | Enable IntelliSense features |

## Troubleshooting

### Dev Server Not Starting

1. Ensure Genkit is installed: `npm install -g genkit`
2. Check port availability: `lsof -i :4000`
3. Try a different port in settings

### Snippets Not Working

1. Verify file language mode is TypeScript or JavaScript
2. Restart VS Code
3. Check extension is enabled

### Extension Not Activating

1. Check VS Code version (must be 1.80.0+)
2. Look for errors in Output panel: `View → Output → Genkit`
3. Reload window: `Ctrl+Shift+P → "Developer: Reload Window"`

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Resources

- [Firebase Genkit Documentation](https://genkit.dev/docs/get-started/)
- [Extension GitHub Repository](https://github.com/amitpatole/claude-genkit-plugin)
- [Report Issues](https://github.com/amitpatole/claude-genkit-plugin/issues)
- [VS Code Extension API](https://code.visualstudio.com/api)

## Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/amitpatole/claude-genkit-plugin/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/amitpatole/claude-genkit-plugin/discussions)
- 📧 **Email**: amit.patole@gmail.com

## License

MIT License - see [LICENSE](../LICENSE) file for details

## Acknowledgments

- Firebase Genkit Team at Google
- Anthropic for Claude AI
- Visual Studio Code Team

---

**Made with ❤️ for the Genkit developer community**

*Build amazing AI applications faster with Genkit and VS Code!*
