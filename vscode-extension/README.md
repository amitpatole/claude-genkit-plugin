# Genkit for VS Code

> Complete Firebase Genkit development toolkit - Build, deploy, and scale AI applications from your IDE

[![Version](https://img.shields.io/visual-studio-marketplace/v/amitpatole.genkit-vscode)](https://marketplace.visualstudio.com/items?itemName=amitpatole.genkit-vscode)
[![Installs](https://img.shields.io/visual-studio-marketplace/i/amitpatole.genkit-vscode)](https://marketplace.visualstudio.com/items?itemName=amitpatole.genkit-vscode)
[![Rating](https://img.shields.io/visual-studio-marketplace/r/amitpatole.genkit-vscode)](https://marketplace.visualstudio.com/items?itemName=amitpatole.genkit-vscode)

The most comprehensive VS Code extension for Firebase Genkit development. Build sophisticated AI applications with advanced RAG patterns, deploy globally with multi-region support, and automate your workflows with integrated CI/CD.

## Latest Updates

### v1.1.0 - Major Feature Release 🚀

**The biggest update yet with 28 new commands, 24 new snippets, and 5 new sidebar views!**

**New in v1.1.0:**
- ✅ **CI/CD Integration** - Setup GitHub Actions, GitLab CI, Azure Pipelines, CircleCI
- ✅ **8 Advanced RAG Patterns** - Hybrid Search, Hierarchical, Conversational, Multi-Query, and more
- ✅ **Multi-Region Deployment** - Active-Active, Active-Passive, Geo-Routing strategies
- ✅ **Real-Time Collaboration** - WebSocket and Server-Sent Events templates
- ✅ **Plugin SDK** - Create and publish custom Genkit plugins
- ✅ **Enhanced Explorer** - 5 new sidebar views for deployments, regions, RAG, real-time, and plugins
- ✅ **31 TypeScript Snippets** - Comprehensive code templates for all features
- ✅ **34 Total Commands** - Complete development workflow automation

**Comparison:**
| Feature | v1.0.1 | v1.1.0 | Improvement |
|---------|--------|--------|-------------|
| Commands | 6 | 34 | +467% |
| Sidebar Views | 3 | 8 | +167% |
| Settings | 3 | 17 | +467% |
| Snippets | 7 | 31 | +343% |

---

## Features

### 🚀 Quick Commands (34 Total)

Access all Genkit functionality from the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`):

#### Core Commands
- **Genkit: Initialize New Project** - Set up a new Genkit project
- **Genkit: Create New Flow** - Generate flows from templates
- **Genkit: Start Dev Server** - Launch development server
- **Genkit: Open Developer UI** - Open Genkit UI in browser
- **Genkit: Deploy to Production** - Deploy to cloud platforms
- **Genkit: Run Health Check** - Verify project health

#### CI/CD Integration (New in v1.1.0)
- **Genkit: Setup CI/CD Pipeline** - Interactive setup wizard for GitHub Actions, GitLab CI, Azure Pipelines, CircleCI
- **Genkit: Configure Deployment Secrets** - Guided secret configuration
- **Genkit: Test Pipeline Locally** - Validate pipeline before push
- **Genkit: View Pipeline Status** - Monitor build and deployment status

#### Advanced RAG Patterns (New in v1.1.0)
- **Genkit: Create RAG Flow** - Choose from 8 production-ready RAG patterns:
  - Hybrid Search (Semantic + Keyword)
  - Hierarchical RAG (Multi-level retrieval)
  - Conversational RAG (Context-aware)
  - Multi-Query RAG (Query expansion)
  - Self-Querying RAG (Metadata filtering)
  - Parent-Child RAG (Smart chunking)
  - Corrective RAG (Self-correction)
  - Adaptive RAG (Dynamic strategy)
- **Genkit: Setup Vector Database** - Configure Pinecone, Chroma, Weaviate, Qdrant, or Milvus
- **Genkit: Test RAG Query** - Interactive testing panel
- **Genkit: Evaluate RAG Performance** - Quality metrics dashboard

#### Multi-Region Deployment (New in v1.1.0)
- **Genkit: Configure Multi-Region Deployment** - Setup global deployment:
  - Active-Active (all regions serve traffic)
  - Active-Passive (primary + failover)
  - Geo-Routing (route by location)
- **Genkit: Deploy to All Regions** - Parallel deployment
- **Genkit: Monitor Regional Health** - Health dashboard
- **Genkit: Trigger Region Failover** - Manual failover controls

#### Real-Time Collaboration (New in v1.1.0)
- **Genkit: Create Real-Time Flow** - WebSocket and SSE templates
- **Genkit: Test WebSocket Connection** - Connection testing
- **Genkit: Monitor Active Connections** - Live connection viewer

#### Plugin Development (New in v1.1.0)
- **Genkit: Create Genkit Plugin** - Scaffold new plugin (Model, Flow, Tool, Retriever)
- **Genkit: Test Plugin** - Testing environment
- **Genkit: Package Plugin for NPM** - Build and pack
- **Genkit: Publish Plugin to NPM** - Publishing workflow

---

### 📝 Code Snippets (31 Total)

#### Core Snippets
| Prefix | Description |
|--------|-------------|
| `gflow` | Basic flow template |
| `gtool` | Tool definition |
| `gconfig` | Genkit configuration |
| `gstream` | Streaming flow |
| `genclaude` | Generate with Claude |
| `gengemini` | Generate with Gemini |
| `grag` | Basic RAG flow |

#### Advanced RAG Patterns (New in v1.1.0)
| Prefix | Description |
|--------|-------------|
| `grag-hybrid` | Hybrid Search RAG (semantic + keyword) |
| `grag-hierarchical` | Hierarchical RAG (multi-level) |
| `grag-conversational` | Conversational RAG (context-aware) |
| `grag-multiquery` | Multi-Query RAG (query expansion) |
| `grag-selfquery` | Self-Querying RAG (metadata filtering) |
| `grag-parentchild` | Parent-Child RAG (document chunking) |
| `grag-corrective` | Corrective RAG (self-correction) |
| `grag-adaptive` | Adaptive RAG (dynamic strategy) |

#### Vector Databases (New in v1.1.0)
| Prefix | Description |
|--------|-------------|
| `gvector-pinecone` | Setup Pinecone vector database |
| `gvector-chroma` | Setup Chroma vector database |

#### Real-Time (New in v1.1.0)
| Prefix | Description |
|--------|-------------|
| `gwebsocket` | WebSocket real-time flow |
| `gsse` | Server-Sent Events streaming flow |

#### Plugin SDK (New in v1.1.0)
| Prefix | Description |
|--------|-------------|
| `gplugin-model` | Custom model plugin |
| `gplugin-retriever` | Custom retriever plugin |

#### DevOps (New in v1.1.0)
| Prefix | Description |
|--------|-------------|
| `gregion-config` | Multi-region deployment configuration |
| `gcicd-github` | GitHub Actions CI/CD workflow |

#### Advanced Features (New in v1.1.0)
| Prefix | Description |
|--------|-------------|
| `gevaluate` | RAG quality evaluator |
| `gprompt` | Structured prompt template |
| `gchat` | Multi-turn chat flow |
| `gmiddleware` | Logging/monitoring middleware |
| `gbatch` | Batch processing with rate limiting |

---

### 🔍 Enhanced Genkit Explorer

#### Existing Views
- **Flows** - View all defined flows
- **AI Models** - See configured models
- **Tools** - Browse available tools

#### New Views in v1.1.0
- **Deployments** - Monitor production/staging status, view history, rollback actions
- **Regions** - Multi-region health monitoring, traffic distribution, latency metrics
- **RAG Patterns** - Active patterns, vector DB status, document counts
- **Real-Time** - Active WebSocket/SSE connections, throughput stats
- **Plugins** - Installed plugins, versions, update indicators

All views include refresh buttons and auto-refresh capabilities.

---

### ⚙️ Configuration

Extensive configuration options in VS Code settings:

#### Core Settings
```json
{
  "genkit.autoStartDevServer": false,
  "genkit.devServerPort": 4000,
  "genkit.enableIntelliSense": true
}
```

#### CI/CD Settings (New in v1.1.0)
```json
{
  "genkit.cicd.platform": "github-actions",
  "genkit.cicd.autoSetup": false
}
```

#### Deployment Settings (New in v1.1.0)
```json
{
  "genkit.deployment.defaultTarget": "cloud-run",
  "genkit.deployment.multiRegion": false,
  "genkit.deployment.regions": ["us-central1", "europe-west1"]
}
```

#### RAG Settings (New in v1.1.0)
```json
{
  "genkit.rag.defaultPattern": "hybrid-search",
  "genkit.rag.vectorDatabase": "pinecone",
  "genkit.rag.embeddingModel": "text-embedding-004"
}
```

#### Real-Time Settings (New in v1.1.0)
```json
{
  "genkit.realtime.enabled": false,
  "genkit.realtime.protocol": "websocket"
}
```

#### Plugin Settings (New in v1.1.0)
```json
{
  "genkit.plugin.autoDiscovery": true
}
```

#### Explorer Settings (New in v1.1.0)
```json
{
  "genkit.explorer.showMetrics": true,
  "genkit.explorer.autoRefresh": true,
  "genkit.explorer.refreshInterval": 5000
}
```

---

## Quick Start

### 1. Setup CI/CD Pipeline

```
Ctrl+Shift+P → "Genkit: Setup CI/CD Pipeline"
```

Choose your platform and deployment target. The extension will:
- Generate workflow configuration files
- Guide you through secret setup
- Provide testing commands

### 2. Create Advanced RAG Flow

```
Ctrl+Shift+P → "Genkit: Create RAG Flow"
```

Select "Hybrid Search" for best results:
- Combines semantic and keyword search
- Auto-generates optimal configuration
- Includes evaluation metrics

Then setup your vector database:
```
Ctrl+Shift+P → "Genkit: Setup Vector Database"
```

### 3. Deploy Multi-Region

```
Ctrl+Shift+P → "Genkit: Configure Multi-Region Deployment"
```

Choose strategy and regions:
- Active-Active for best performance
- Active-Passive for cost efficiency
- Geo-Routing for optimal latency

Then deploy:
```
Ctrl+Shift+P → "Genkit: Deploy to All Regions"
```

---

## Usage Examples

### Example 1: Build Hybrid Search RAG Application

1. Type `grag-hybrid` in a TypeScript file
2. Configure vector store (Pinecone, Chroma, etc.)
3. Set semantic/keyword weights
4. Test with `Ctrl+Shift+P → "Genkit: Test RAG Query"`
5. Deploy with CI/CD pipeline

### Example 2: Setup Multi-Region Deployment

1. `Ctrl+Shift+P → "Genkit: Configure Multi-Region Deployment"`
2. Select "Active-Active" strategy
3. Choose regions: US Central, Europe West, Asia East
4. Configure traffic weights (33% each)
5. Monitor in "Regions" sidebar view
6. Failover with one click if needed

### Example 3: Create Real-Time Chat Application

1. Type `gwebsocket` in a TypeScript file
2. Configure WebSocket server
3. Implement message broadcasting
4. Test connections with `Ctrl+Shift+P → "Genkit: Test WebSocket"`
5. Monitor active connections in "Real-Time" sidebar view

### Example 4: Build Custom Plugin

1. `Ctrl+Shift+P → "Genkit: Create Genkit Plugin"`
2. Choose "Model Plugin"
3. Implement your model integration
4. Test with `Ctrl+Shift+P → "Genkit: Test Plugin"`
5. Package and publish to NPM

---

## Installation

### From VS Code Marketplace (Recommended)

1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X` / `Cmd+Shift+X`)
3. Search for "Genkit"
4. Click "Install"

### From VSIX

1. Download the `.vsix` file from [Releases](https://github.com/amitpatole/claude-genkit-plugin/releases)
2. Run: `code --install-extension genkit-vscode-1.1.0.vsix`

---

## Requirements

- **VS Code** 1.80.0 or higher
- **Node.js** 18+ (for Genkit projects)
- **npm** or **yarn**

---

## Extension Settings Reference

### All 17 Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `genkit.autoStartDevServer` | boolean | `false` | Auto-start dev server on project open |
| `genkit.devServerPort` | number | `4000` | Port for development server |
| `genkit.enableIntelliSense` | boolean | `true` | Enable IntelliSense features |
| `genkit.cicd.platform` | string | `"github-actions"` | Preferred CI/CD platform |
| `genkit.cicd.autoSetup` | boolean | `false` | Auto-setup CI/CD on project creation |
| `genkit.deployment.defaultTarget` | string | `"cloud-run"` | Default deployment target |
| `genkit.deployment.multiRegion` | boolean | `false` | Enable multi-region by default |
| `genkit.deployment.regions` | array | `["us-central1", "europe-west1"]` | Default regions |
| `genkit.rag.defaultPattern` | string | `"hybrid-search"` | Default RAG pattern |
| `genkit.rag.vectorDatabase` | string | `"pinecone"` | Preferred vector database |
| `genkit.rag.embeddingModel` | string | `"text-embedding-004"` | Default embedding model |
| `genkit.realtime.enabled` | boolean | `false` | Enable real-time features |
| `genkit.realtime.protocol` | string | `"websocket"` | Preferred real-time protocol |
| `genkit.plugin.autoDiscovery` | boolean | `true` | Auto-discover installed plugins |
| `genkit.explorer.showMetrics` | boolean | `true` | Show metrics in Explorer |
| `genkit.explorer.autoRefresh` | boolean | `true` | Auto-refresh Explorer views |
| `genkit.explorer.refreshInterval` | number | `5000` | Refresh interval (ms) |

---

## Troubleshooting

### CI/CD Pipeline Not Working

1. Ensure secrets are configured in your CI/CD platform
2. Check workflow file syntax
3. Verify deployment target configuration
4. Review pipeline logs in platform UI

### RAG Flow Not Retrieving Documents

1. Verify vector database credentials
2. Check documents are indexed
3. Test embedding model configuration
4. Use "Test RAG Query" command for debugging

### Multi-Region Deployment Failing

1. Ensure all regions are properly configured
2. Verify cloud provider credentials
3. Check regional quotas and limits
4. Review regional health in sidebar view

### WebSocket Connection Issues

1. Check WebSocket server port availability
2. Verify firewall rules
3. Test with "Test WebSocket Connection" command
4. Review connection logs

### Dev Server Not Starting

1. Ensure Genkit is installed: `npm install -g genkit`
2. Check port availability: `lsof -i :4000`
3. Try a different port in settings
4. Check Node.js version (18+ required)

### Snippets Not Working

1. Verify file language mode is TypeScript or JavaScript
2. Restart VS Code
3. Check extension is enabled
4. Try typing the full prefix

---

## What's New in Each Version

### v1.1.0 (Current)
- 28 new commands for CI/CD, RAG, Multi-Region, Real-Time, Plugins
- 24 new code snippets
- 5 new sidebar views
- 14 new configuration settings
- Complete multi-region deployment support
- Advanced RAG pattern library
- Plugin development toolkit

### v1.0.1 (Previous)
- Initial marketplace release
- 6 core commands
- 7 basic snippets
- 3 sidebar views
- Basic Genkit workflow support

---

## Contributing

Contributions are welcome! Here's how:

1. Fork the [repository](https://github.com/amitpatole/claude-genkit-plugin)
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Setup

```bash
cd vscode-extension
npm install
npm run compile
code .
```

Press F5 to launch extension development host.

---

## Telemetry and Privacy

This extension collects anonymous usage data to help improve the product. **We respect your privacy!**

### What We Collect (Anonymized)
- Command usage and performance
- Extension activation/deactivation
- Error reports (sanitized)
- VS Code and OS versions

### What We DON'T Collect
- ❌ No file names, paths, or content
- ❌ No personal information
- ❌ No API keys or credentials
- ❌ No user-generated code

### How to Disable

Telemetry respects VS Code's settings. To disable:

**Option 1**: VS Code Settings UI
1. Go to `File` → `Preferences` → `Settings`
2. Search for "telemetry"
3. Set `telemetry.telemetryLevel` to `"off"`

**Option 2**: settings.json
```json
{
  "telemetry.telemetryLevel": "off"
}
```

**Option 3**: Command Line
```bash
code --telemetry-level off
```

📖 **Full details**: [TELEMETRY.md](TELEMETRY.md)

✅ **GDPR & CCPA compliant** | ✅ **Open source** | ✅ **No PII collected**

---

## Resources

- [Firebase Genkit Documentation](https://firebase.google.com/docs/genkit)
- [Extension GitHub Repository](https://github.com/amitpatole/claude-genkit-plugin)
- [Report Issues](https://github.com/amitpatole/claude-genkit-plugin/issues)
- [Feature Requests](https://github.com/amitpatole/claude-genkit-plugin/discussions)
- [VS Code Extension API](https://code.visualstudio.com/api)
- [Privacy Policy](TELEMETRY.md)

---

## Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/amitpatole/claude-genkit-plugin/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/amitpatole/claude-genkit-plugin/discussions)
- 📧 **Email**: amit.patole@gmail.com
- 🌟 **Star on GitHub**: Show your support!

---

## License

MIT License - see [LICENSE](../LICENSE) file for details

---

## Acknowledgments

- Firebase Genkit Team at Google
- Anthropic for Claude AI
- Visual Studio Code Team
- Open source contributors

---

## Roadmap

### v1.2.0 (Planned)
- RAG visual debugger
- Pipeline visualization dashboard
- Live real-time preview
- Enhanced IntelliSense
- Integration tests

### v2.0.0 (Future)
- Multi-user collaboration features
- Enterprise deployment templates
- Advanced monitoring and observability
- Plugin marketplace integration

---

**Made with ❤️ for the Genkit developer community**

*The most comprehensive VS Code extension for Firebase Genkit - from local development to global production deployment.*

**[Install Now](https://marketplace.visualstudio.com/items?itemName=amitpatole.genkit-vscode) | [View on GitHub](https://github.com/amitpatole/claude-genkit-plugin) | [Give Feedback](https://github.com/amitpatole/claude-genkit-plugin/discussions)**
