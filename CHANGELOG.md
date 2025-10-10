# Changelog

All notable changes to the Firebase Genkit plugin for Claude Code will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-10-10

### Added
- 🎉 **Expanded to multi-plugin marketplace** with 4 new specialized plugins
- **genkit-test-writer** - Automatically generate comprehensive tests for Genkit flows
  - `/genkit-test-generate` - Generate unit, integration, and e2e tests
  - `/genkit-test-run` - Run tests with coverage reporting
  - `@test-writer` agent for test writing assistance
- **genkit-monitor** - Real-time monitoring and observability
  - `/genkit-monitor-setup` - Setup logging and telemetry
  - `/genkit-monitor-dashboard` - View real-time metrics
  - `/genkit-monitor-logs` - Stream and analyze flow logs
  - `@monitor-expert` agent for observability guidance
- **genkit-cost-tracker** - Track and optimize AI API costs
  - `/genkit-cost-report` - Generate cost analysis reports
  - `/genkit-cost-optimize` - Get cost optimization recommendations
  - `@cost-optimizer` agent for cost reduction strategies
- **genkit-security-auditor** - Security auditing and best practices
  - `/genkit-security-audit` - Run comprehensive security audit
  - `/genkit-security-fix` - Apply security fixes automatically
  - `@security-expert` agent for secure AI practices

### Changed
- Restructured repository to support multiple plugins in `plugins/` directory
- Main Genkit plugin now at root with additional plugins in subdirectories
- Marketplace now offers 5 total plugins (1 core + 4 specialized)

## [1.1.0] - 2025-10-10

### Added
- ✅ GitHub marketplace installation support via `/plugin marketplace add`
- Proper marketplace.json structure with plugins array for Claude Code plugin system
- Updated installation documentation with GitHub as recommended method

### Changed
- **Installation Method:** GitHub installation is now the primary and recommended installation method
- Restructured marketplace.json from single plugin format to proper marketplace catalog format
- Updated README.md installation instructions to prioritize GitHub marketplace installation
- Updated PUBLISH.sh script to show correct marketplace installation commands
- Local directory installation moved to alternative method

### Fixed
- Fixed marketplace.json structure to enable `/plugin marketplace add` command
- Corrected plugin discovery and installation from GitHub repositories

### Documentation
- Updated README.md with correct GitHub installation steps
- Removed "Coming Soon" label from GitHub installation
- Added marketplace.json structure documentation

## [1.0.0] - 2025-10-10

### Added
- 🎉 Initial release of Firebase Genkit plugin for Claude Code
- **Commands:**
  - `/genkit-init` - Initialize new Genkit projects with interactive setup
  - `/genkit-run` - Start development server with Genkit Developer UI
  - `/genkit-flow` - Create flows from 6 production-ready templates
  - `/genkit-deploy` - Deploy to multiple platforms (Firebase, Cloud Run, Vercel, Docker)
  - `/genkit-doctor` - Comprehensive health checks and diagnostics

- **Flow Templates:**
  - Simple Chat - Basic conversational AI
  - RAG - Retrieval Augmented Generation with document context
  - Tool Calling - Function execution and tool integration
  - Multi-step - Complex sequential workflows
  - Streaming - Real-time streaming responses
  - Empty - Blank template for custom implementations

- **AI Assistant:**
  - Genkit-specialized agent with expertise in:
    - Architecture design
    - Code generation
    - Debugging and troubleshooting
    - Performance optimization
    - Security best practices
    - Production deployment strategies

- **Language Support:**
  - TypeScript (recommended)
  - JavaScript
  - Go (Beta)
  - Python (Alpha)

- **AI Model Providers:**
  - Anthropic Claude (3.5 Sonnet, 3 Opus, etc.)
  - Google Gemini (1.5 Pro, 1.5 Flash)
  - OpenAI GPT (GPT-4, GPT-3.5)
  - Local models via Ollama

- **Deployment Platforms:**
  - Firebase Cloud Functions
  - Google Cloud Run
  - Google Cloud Functions (2nd gen)
  - Vercel
  - Docker containers
  - Custom platforms

- **Features:**
  - Automatic dependency detection and installation
  - Smart .env file management
  - TypeScript/JavaScript project detection
  - Port conflict resolution
  - Configuration file validation
  - Environment variable validation
  - Comprehensive error handling
  - Interactive wizards for all commands
  - Production-ready code templates
  - Security hardening options

- **Documentation:**
  - Complete README with examples
  - Installation instructions
  - Command reference
  - Troubleshooting guide
  - Code examples for all flow types
  - Best practices guide
  - MIT License

### Technical Details
- Supports Node.js 18+
- Compatible with Linux, macOS, and Windows
- All bash scripts with proper error handling
- Colorized terminal output for better UX
- Executable permissions pre-configured

### Known Limitations
- Go support is in Beta (refer to Genkit Go docs)
- Python support is in Alpha (refer to Genkit Python docs)
- Windows users may need WSL for full bash script support

---

## [Unreleased]

### Planned Features
- [ ] Additional flow templates (Image generation, Audio processing)
- [ ] Firebase integration helpers (Firestore, Authentication)
- [ ] Advanced monitoring and observability tools
- [ ] Testing utilities and test generation
- [ ] Migration helpers from other AI frameworks
- [ ] VS Code extension integration
- [ ] Docker Compose templates
- [ ] CI/CD pipeline templates
- [ ] Cost estimation tools
- [ ] Performance benchmarking utilities

### Potential Enhancements
- [ ] GUI interface for command wizards
- [ ] Flow visualization tools
- [ ] Interactive debugging tools
- [ ] Plugin marketplace integration
- [ ] Auto-update mechanism
- [ ] Telemetry and usage analytics (opt-in)
- [ ] Multi-language documentation
- [ ] Video tutorials and demos

---

## Release Notes

### Version 1.0.0
This is the initial stable release of the Firebase Genkit plugin for Claude Code. The plugin has been thoroughly tested and is production-ready.

**What's included:**
- 5 powerful commands for the complete Genkit development lifecycle
- 6 production-ready flow templates
- Specialized AI assistant with deep Genkit expertise
- Multi-platform deployment support
- Comprehensive health monitoring
- Full documentation and examples

**Getting Started:**
```bash
# Install the plugin
/plugin marketplace add https://github.com/amitpatole/claude-genkit-plugin.git
/plugin install genkit

# Create your first project
/genkit-init

# Start building AI applications!
```

**Feedback:**
We'd love to hear your feedback! Please report issues or suggest features at:
https://github.com/amitpatole/claude-genkit-plugin/issues

---

## Versioning Strategy

- **Major version (X.0.0)**: Breaking changes, major feature additions
- **Minor version (0.X.0)**: New features, non-breaking changes
- **Patch version (0.0.X)**: Bug fixes, minor improvements

## Links

- [Repository](https://github.com/amitpatole/claude-genkit-plugin)
- [Documentation](https://github.com/amitpatole/claude-genkit-plugin#readme)
- [Issues](https://github.com/amitpatole/claude-genkit-plugin/issues)
- [Firebase Genkit Docs](https://firebase.google.com/docs/genkit)
