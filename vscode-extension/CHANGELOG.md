# Changelog

All notable changes to the "Genkit for VS Code" extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.2] - 2025-10-13

### Fixed
- GitHub Actions release workflow secret name references
- Corrected conditional checks from VSCE_PAT to PAT_TOKEN
- Improved marketplace publishing error messages and logging
- Made publish step fail explicitly when PAT_TOKEN is not configured

### Changed
- Enhanced workflow summary messages for better debugging

---

## [1.1.1] - 2025-10-13

### Added
- Complete visual documentation (SCREENSHOTS.md) with UI mockups
- Comprehensive feature writeup (FEATURE_WRITEUP.md) with marketing content
- Extension icon files (PNG and SVG)

### Fixed
- GitHub Actions workflow permissions for release creation
- Extension icon file references in package.json

### Documentation
- Added detailed UI mockups for all features
- Created professional marketing content
- Updated technical specifications

---

## [1.1.0] - 2025-10-12

### 🎉 Major Feature Release

The biggest update yet with **467% more commands**, **343% more snippets**, and **167% more sidebar views**!

### Added

#### CI/CD Integration
- **New Command**: `genkit.setupCICD` - Interactive wizard to setup CI/CD pipelines
  - Support for GitHub Actions, GitLab CI, Azure Pipelines, CircleCI
  - Template generation for Firebase, Cloud Run, Vercel, AWS Lambda, Docker
- **New Command**: `genkit.configureSecrets` - Guided deployment secret configuration
- **New Command**: `genkit.testPipeline` - Local pipeline validation
- **New Command**: `genkit.viewPipelineStatus` - Monitor CI/CD pipeline status
- **New Settings**:
  - `genkit.cicd.platform` - Preferred CI/CD platform (default: "github-actions")
  - `genkit.cicd.autoSetup` - Auto-setup CI/CD on project creation (default: false)

#### Advanced RAG Patterns
- **New Command**: `genkit.createRAGFlow` - Create RAG flow with 8 advanced patterns:
  - Hybrid Search (Semantic + Keyword)
  - Hierarchical RAG (Multi-level retrieval)
  - Conversational RAG (Context-aware)
  - Multi-Query RAG (Query expansion)
  - Self-Querying RAG (Metadata filtering)
  - Parent-Child RAG (Smart document chunking)
  - Corrective RAG (Self-correction)
  - Adaptive RAG (Dynamic strategy selection)
- **New Command**: `genkit.setupVectorDB` - Configure vector databases
  - Support for Pinecone, Chroma, Weaviate, Qdrant, Milvus
  - Auto-generate integration code
  - Copy-to-clipboard install commands
- **New Command**: `genkit.testRAGQuery` - Interactive RAG testing panel with webview UI
- **New Command**: `genkit.evaluateRAG` - RAG performance evaluation dashboard
- **New Settings**:
  - `genkit.rag.defaultPattern` - Default RAG pattern (default: "hybrid-search")
  - `genkit.rag.vectorDatabase` - Preferred vector database (default: "pinecone")
  - `genkit.rag.embeddingModel` - Default embedding model (default: "text-embedding-004")
- **New Sidebar View**: `genkitRAGPatterns` - Display active RAG patterns and vector DB status

#### Multi-Region Deployment
- **New Command**: `genkit.configureMultiRegion` - Setup multi-region deployment
  - 3 deployment strategies: Active-Active, Active-Passive, Geo-Routing
  - Region selection (6 regions: US Central, Europe West, Asia East, US East, Europe North, Asia Southeast)
  - Auto-generate multi-region-config.json
  - Automatic traffic weight calculation
- **New Command**: `genkit.deployAllRegions` - Parallel deployment to all configured regions
- **New Command**: `genkit.monitorRegionalHealth` - Health monitoring dashboard with webview
  - Real-time health status indicators
  - Latency metrics per region
  - Traffic distribution visualization
- **New Command**: `genkit.triggerFailover` - Manual region failover with confirmation
- **New Settings**:
  - `genkit.deployment.defaultTarget` - Default deployment target (default: "cloud-run")
  - `genkit.deployment.multiRegion` - Enable multi-region by default (default: false)
  - `genkit.deployment.regions` - Default regions array (default: ["us-central1", "europe-west1"])
- **New Sidebar View**: `genkitRegions` - Display region health, traffic percentages, and status

#### Real-Time Collaboration
- **New Command**: `genkit.createRealTimeFlow` - Create real-time flows
  - WebSocket (Bidirectional) support
  - Server-Sent Events (SSE) streaming support
  - Combined WebSocket + SSE templates
  - Auto-generate integration code
- **New Command**: `genkit.testWebSocket` - WebSocket connection testing (stub)
- **New Command**: `genkit.monitorConnections` - Live connection viewer (stub)
- **New Settings**:
  - `genkit.realtime.enabled` - Enable real-time features (default: false)
  - `genkit.realtime.protocol` - Preferred protocol (default: "websocket")
- **New Sidebar View**: `genkitRealTime` - Display WebSocket and SSE connection counts

#### Plugin SDK
- **New Command**: `genkit.createPlugin` - Scaffold custom Genkit plugins
  - 4 plugin types: Model Plugin, Flow Plugin, Tool Plugin, Retriever Plugin
  - Kebab-case validation
  - Automatic directory scaffolding
  - Package.json generation
  - README generation
- **New Command**: `genkit.testPlugin` - Plugin testing environment (stub)
- **New Command**: `genkit.packagePlugin` - NPM build and pack automation
- **New Command**: `genkit.publishPlugin` - NPM publishing workflow with confirmation
- **New Setting**: `genkit.plugin.autoDiscovery` - Auto-discover plugins (default: true)
- **New Sidebar View**: `genkitPlugins` - Display installed plugins with versions

#### Enhanced Genkit Explorer
- **New Sidebar View**: `genkitDeployments` - Monitor deployments
  - Production status tracking
  - Staging status tracking
  - Deployment history
  - Refresh button
- **New Settings**:
  - `genkit.explorer.showMetrics` - Show metrics in views (default: true)
  - `genkit.explorer.autoRefresh` - Auto-refresh views (default: true)
  - `genkit.explorer.refreshInterval` - Refresh interval in ms (default: 5000)
- **New Refresh Commands** for all sidebar views:
  - `genkit.refreshFlows` - Refresh Flows view
  - `genkit.refreshDeployments` - Refresh Deployments view
  - `genkit.refreshRegions` - Refresh Regions view
  - `genkit.refreshRAGPatterns` - Refresh RAG Patterns view
  - `genkit.refreshRealTime` - Refresh Real-Time view
  - `genkit.refreshPlugins` - Refresh Plugins view

#### Code Snippets (24 New)
- **Advanced RAG Patterns**:
  - `grag-hybrid` - Hybrid Search RAG
  - `grag-hierarchical` - Hierarchical RAG
  - `grag-conversational` - Conversational RAG
  - `grag-multiquery` - Multi-Query RAG
  - `grag-selfquery` - Self-Querying RAG
  - `grag-parentchild` - Parent-Child RAG
  - `grag-corrective` - Corrective RAG
  - `grag-adaptive` - Adaptive RAG
- **Vector Databases**:
  - `gvector-pinecone` - Pinecone setup
  - `gvector-chroma` - Chroma setup
- **Real-Time**:
  - `gwebsocket` - WebSocket flow
  - `gsse` - Server-Sent Events flow
- **Plugin SDK**:
  - `gplugin-model` - Custom model plugin
  - `gplugin-retriever` - Custom retriever plugin
- **DevOps**:
  - `gregion-config` - Multi-region configuration
  - `gcicd-github` - GitHub Actions workflow
- **Advanced Features**:
  - `gevaluate` - RAG quality evaluator
  - `gprompt` - Structured prompt template
  - `gchat` - Multi-turn chat flow
  - `gmiddleware` - Logging/monitoring middleware
  - `gbatch` - Batch processing flow
- **JavaScript Snippets**: Added 10+ JavaScript equivalents for core snippets

### Changed

- **Updated** `package.json` from 150 to 506 lines with comprehensive configuration
- **Enhanced** Flows sidebar view with type indicators (Chat, RAG, Streaming, Real-time)
- **Improved** error handling throughout all commands
- **Expanded** extension description to reflect new capabilities
- **Upgraded** version from 1.0.1 to 1.1.0

### Technical Details

- **Code Growth**: Extension code expanded from ~350 lines to 1,070 lines
- **Architecture**: Modular design with separate functions for each command
- **Error Handling**: Try-catch blocks for all file operations
- **User Experience**: Progress notifications, input validation, confirmation dialogs
- **Performance**: Lazy loading of tree views, efficient refresh mechanisms
- **TypeScript**: Strong typing throughout, interfaces for tree items
- **VS Code API**: Following best practices for extension development

### Statistics

- **Total Commands**: 34 (up from 6) - **+467%**
- **Total Snippets**: 31 TypeScript, 12 JavaScript (up from 7) - **+343%**
- **Sidebar Views**: 8 (up from 3) - **+167%**
- **Settings**: 17 (up from 3) - **+467%**
- **Lines of Code**: 1,900+ (up from ~300) - **+533%**

### Known Limitations

- WebSocket connection testing is a stub (to be implemented in v1.2.0)
- RAG performance evaluation is a stub (to be implemented in v1.2.0)
- Plugin testing environment is a stub (to be implemented in v1.2.0)

---

## [1.0.1] - 2025-10-01

### Added
- Initial VS Code Marketplace release
- 6 core Genkit commands:
  - Initialize New Project
  - Create New Flow
  - Start Dev Server
  - Open Developer UI
  - Deploy to Production
  - Run Health Check
- 7 code snippets for TypeScript and JavaScript
- 3 sidebar views:
  - Flows view
  - AI Models view
  - Tools view
- 3 configuration settings:
  - Auto-start dev server
  - Dev server port
  - Enable IntelliSense

### Technical Details
- Extension size: ~300 lines of TypeScript
- VS Code API version: 1.80.0
- Node.js requirement: 18+

---

## [1.0.0] - 2025-09-28

### Added
- Initial development release
- Basic Genkit project scaffolding
- Flow creation templates
- Dev server integration
- Basic code snippets

### Technical Details
- Proof of concept implementation
- Core functionality established
- Testing framework setup

---

## Roadmap

### v1.2.0 (Planned - Q1 2026)
- Implement WebSocket connection testing
- Complete RAG performance evaluation dashboard
- Add plugin testing environment
- RAG visual debugger with query → retrieval → generation visualization
- Pipeline visualization dashboard
- Enhanced IntelliSense with context-aware completions
- Integration tests

### v2.0.0 (Future - Q2 2026)
- Live real-time preview for WebSocket/SSE flows
- Multi-user collaboration features
- Enterprise deployment templates
- Advanced monitoring and observability
- Plugin marketplace integration
- Custom workflow automation

---

## Upgrade Guide

### From v1.0.1 to v1.1.0

**No breaking changes** - all v1.0.1 features remain fully functional.

**New features to explore:**
1. Try the CI/CD setup: `Ctrl+Shift+P` → "Genkit: Setup CI/CD Pipeline"
2. Create an advanced RAG flow: `Ctrl+Shift+P` → "Genkit: Create RAG Flow"
3. Configure multi-region deployment: `Ctrl+Shift+P` → "Genkit: Configure Multi-Region Deployment"
4. Check out the new sidebar views in the Genkit Explorer
5. Use new snippets like `grag-hybrid`, `gwebsocket`, `gplugin-model`

**Settings you might want to configure:**
```json
{
  "genkit.rag.defaultPattern": "hybrid-search",
  "genkit.rag.vectorDatabase": "pinecone",
  "genkit.deployment.multiRegion": true,
  "genkit.deployment.regions": ["us-central1", "europe-west1", "asia-east1"]
}
```

---

## Support

- 🐛 Report bugs: [GitHub Issues](https://github.com/amitpatole/claude-genkit-plugin/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/amitpatole/claude-genkit-plugin/discussions)
- 📧 Email: amit.patole@gmail.com

---

**[View Full Documentation](https://github.com/amitpatole/claude-genkit-plugin/tree/main/vscode-extension#readme)**
