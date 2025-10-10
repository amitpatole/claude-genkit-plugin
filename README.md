# Firebase Genkit Plugin for Claude Code

> Build production-ready AI applications with Firebase Genkit directly from Claude Code

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-blue.svg)](https://claude.com/claude-code)

A comprehensive Claude Code plugin that streamlines Firebase Genkit development with intelligent commands, templates, and an AI assistant specialized in Genkit best practices.

## Features

### 🚀 Quick Project Initialization
- **`/genkit-init`** - Create new Genkit projects with interactive setup
  - TypeScript, JavaScript, Go, or Python support
  - Multiple AI providers (Claude, Gemini, GPT)
  - Pre-configured project structure
  - Example flows to get started

### 💻 Development Tools
- **`/genkit-run`** - Start Genkit dev server with auto-configuration
  - Automatic dependency detection
  - Smart .env file management
  - Genkit Developer UI at localhost:4000
  - Hot reload support

### 📦 Flow Generation
- **`/genkit-flow`** - Create flows from templates
  - Simple Chat Flow
  - RAG (Retrieval Augmented Generation)
  - Tool Calling with function execution
  - Multi-step workflows
  - Streaming responses
  - Blank templates

### 🌐 Deployment Support
- **`/genkit-deploy`** - Deploy to multiple platforms
  - Firebase Cloud Functions
  - Google Cloud Run
  - Google Cloud Functions (2nd gen)
  - Vercel
  - Docker containers
  - Local builds

### 🏥 Health Monitoring
- **`/genkit-doctor`** - Comprehensive project health checks
  - System requirements validation
  - Package installation verification
  - Configuration file checks
  - Environment variable validation
  - Flow detection
  - Dependency health

### 🤖 AI Assistant
- **Genkit-specialized AI agent** with deep expertise in:
  - Genkit architecture and patterns
  - AI model integration
  - Production deployment strategies
  - Performance optimization
  - Security best practices

## Installation

### From Claude Code

1. **Install the plugin:**
   ```
   /plugin install /path/to/claude-genkit-plugin
   ```

2. **Enable the plugin:**
   ```
   /plugin enable genkit
   ```

3. **Verify installation:**
   ```
   /genkit-doctor
   ```

### From GitHub (Coming Soon)
```
/plugin install github:amitpatole/claude-genkit-plugin
```

## Quick Start

### Create Your First Genkit Project

```bash
# 1. Initialize a new project
/genkit-init

# Follow the interactive prompts:
# - Project name: my-ai-app
# - Language: TypeScript
# - AI Provider: Anthropic Claude

# 2. Navigate to your project
cd my-ai-app

# 3. Add your API keys to .env
# Edit .env and add:
# ANTHROPIC_API_KEY=your_key_here

# 4. Start development server
/genkit-run

# 5. Open Genkit Developer UI
# Visit http://localhost:4000
```

### Create a New Flow

```bash
# In your Genkit project
/genkit-flow

# Follow prompts:
# - Flow name: summarizeFlow
# - Template: RAG (Retrieval Augmented Generation)
```

### Deploy to Production

```bash
/genkit-deploy

# Choose deployment target:
# 1. Firebase Cloud Functions
# 2. Google Cloud Run
# 3. Vercel
# etc.
```

## Commands Reference

| Command | Description | Usage |
|---------|-------------|-------|
| `/genkit-init` | Initialize new Genkit project | Interactive setup wizard |
| `/genkit-run` | Start development server | Run from project directory |
| `/genkit-flow` | Generate new flow from template | Choose from 6 templates |
| `/genkit-deploy` | Deploy to production | Multiple platform support |
| `/genkit-doctor` | Health check and diagnostics | Validates entire setup |

## Supported Technologies

### Languages
- ✅ **TypeScript** (Recommended)
- ✅ **JavaScript**
- ✅ **Go** (Beta)
- ✅ **Python** (Alpha)

### AI Models
- 🤖 **Anthropic Claude** (3.5 Sonnet, 3 Opus, etc.)
- 🧠 **Google Gemini** (1.5 Pro, 1.5 Flash)
- 💬 **OpenAI GPT** (GPT-4, GPT-3.5)
- 🏠 **Local Models** (via Ollama)

### Deployment Platforms
- 🔥 Firebase Cloud Functions
- ☁️ Google Cloud Run
- ⚡ Google Cloud Functions (2nd gen)
- 🔺 Vercel
- 🐳 Docker
- 🌐 Custom platforms

## Flow Templates

### 1. Simple Chat
Basic conversational AI flow with single-turn responses.

### 2. RAG (Retrieval Augmented Generation)
Query documents and generate answers with context.

### 3. Tool Calling
Execute functions and tools based on AI decisions.

### 4. Multi-step
Complex workflows with sequential AI operations.

### 5. Streaming
Real-time streaming responses for better UX.

### 6. Empty
Blank template for custom implementations.

## AI Assistant

The plugin includes a specialized AI agent with expertise in:

- **Architecture Design** - Design scalable Genkit applications
- **Code Generation** - Create production-ready flows and tools
- **Debugging** - Troubleshoot configuration and runtime issues
- **Optimization** - Improve performance, reduce costs
- **Best Practices** - Security, error handling, testing

**Activate the assistant:**
```
@genkit-assistant How do I implement a RAG flow with Claude?
```

## Examples

### Example 1: Chat Application

```typescript
import { defineFlow } from '@genkit-ai/flow';
import { claude35Sonnet } from '@genkit-ai/anthropic';
import { z } from 'zod';

export const chatFlow = defineFlow(
  {
    name: 'chat',
    inputSchema: z.object({
      message: z.string(),
      history: z.array(z.object({
        role: z.enum(['user', 'assistant']),
        content: z.string(),
      })).optional(),
    }),
    outputSchema: z.string(),
  },
  async (input) => {
    const messages = [
      ...(input.history || []),
      { role: 'user', content: input.message },
    ];

    const result = await claude35Sonnet.generate({
      messages,
    });

    return result.text;
  }
);
```

### Example 2: RAG with Vector Search

```typescript
export const ragFlow = defineFlow(
  {
    name: 'rag',
    inputSchema: z.object({
      question: z.string(),
      maxResults: z.number().default(5),
    }),
    outputSchema: z.object({
      answer: z.string(),
      sources: z.array(z.string()),
    }),
  },
  async (input) => {
    // Retrieve relevant documents
    const docs = await vectorStore.search(input.question, {
      limit: input.maxResults,
    });

    // Generate answer with context
    const result = await claude35Sonnet.generate({
      prompt: `Context:\n${docs.map(d => d.content).join('\n\n')}\n\nQuestion: ${input.question}\n\nAnswer:`,
    });

    return {
      answer: result.text,
      sources: docs.map(d => d.id),
    };
  }
);
```

## Configuration

### Environment Variables

Create a `.env` file in your project:

```bash
# Anthropic (Claude)
ANTHROPIC_API_KEY=sk-ant-...

# Google AI (Gemini)
GOOGLE_AI_API_KEY=AIza...

# OpenAI (GPT)
OPENAI_API_KEY=sk-...

# Optional: Custom configuration
PORT=3000
NODE_ENV=development
```

### Genkit Configuration

Create `src/genkit.config.ts`:

```typescript
import { configureGenkit } from '@genkit-ai/core';
import { claude } from '@genkit-ai/anthropic';
import { googleAI } from '@genkit-ai/googleai';

export default configureGenkit({
  plugins: [
    claude({
      apiKey: process.env.ANTHROPIC_API_KEY,
    }),
    googleAI({
      apiKey: process.env.GOOGLE_AI_API_KEY,
    }),
  ],
  logLevel: 'debug',
  enableTracingAndMetrics: true,
});
```

## Troubleshooting

### Common Issues

**Issue: "Genkit CLI not found"**
```bash
# Install globally
npm install -g genkit-cli

# Or run without global install
npx genkit start
```

**Issue: "No API key configured"**
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your keys
nano .env
```

**Issue: "Port 4000 already in use"**
```bash
# Kill existing process
lsof -ti:4000 | xargs kill -9

# Or change port in your start script
PORT=4001 npm run dev
```

### Health Check

Run a comprehensive health check:
```
/genkit-doctor
```

## Requirements

- **Node.js** 18+ (for JavaScript/TypeScript)
- **npm** 8+
- **Go** 1.21+ (for Go projects)
- **Python** 3.10+ (for Python projects)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `/genkit-doctor`
5. Submit a pull request

## Roadmap

- [ ] Plugin marketplace submission
- [ ] Additional flow templates
- [ ] Firebase integration helpers
- [ ] Advanced monitoring tools
- [ ] Testing utilities
- [ ] Migration helpers

## Resources

- [Firebase Genkit Documentation](https://firebase.google.com/docs/genkit)
- [Claude Code Documentation](https://docs.claude.com/claude-code)
- [Anthropic API Reference](https://docs.anthropic.com/)
- [Plugin Source Code](https://github.com/amitpatole/claude-genkit-plugin)

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/amitpatole/claude-genkit-plugin/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/amitpatole/claude-genkit-plugin/discussions)
- 📧 **Email**: support@example.com

## Acknowledgments

- Firebase Genkit Team at Google
- Anthropic for Claude AI
- Claude Code Team at Anthropic

---

**Made with ❤️ for the AI developer community**

*Build amazing AI applications with Firebase Genkit and Claude Code!*
