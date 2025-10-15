# Complete Developer Guide to Genkit Development Suite
## Master AI Application Development with Firebase Genkit, Claude Plugin & VSCode Extension

---

## Table of Contents

1. [Introduction](#introduction)
2. [What is the Genkit Development Suite?](#what-is-the-genkit-development-suite)
3. [Why Use Genkit?](#why-use-genkit)
4. [Installation & Setup](#installation--setup)
5. [Core Concepts](#core-concepts)
6. [Firebase Genkit Framework](#firebase-genkit-framework)
7. [Claude-Genkit Plugin](#claude-genkit-plugin)
8. [Genkit VSCode Extension](#genkit-vscode-extension)
9. [Building Your First AI Application](#building-your-first-ai-application)
10. [Advanced Patterns](#advanced-patterns)
11. [Testing & Debugging](#testing--debugging)
12. [Deployment](#deployment)
13. [Best Practices](#best-practices)
14. [Real-World Examples](#real-world-examples)
15. [Troubleshooting](#troubleshooting)
16. [Resources & Community](#resources--community)

---

## Introduction

Welcome to the complete developer guide for the Genkit Development Suite. This guide will take you from zero to building production-ready AI applications in days, not weeks.

### Who This Guide Is For

- **Backend Developers** wanting to add AI capabilities to their applications
- **Frontend Developers** building AI-powered user experiences
- **Full-Stack Engineers** creating end-to-end AI solutions
- **DevOps Engineers** deploying and maintaining AI services
- **Technical Leads** evaluating AI development frameworks

### What You'll Learn

By the end of this guide, you'll be able to:
- Set up the complete Genkit development environment
- Build AI flows for chat, RAG, tool calling, and more
- Test and debug AI applications effectively
- Deploy AI services to production
- Implement best practices for security and performance
- Choose the right AI model for each use case

### Prerequisites

- **Node.js 18+** (or Go 1.20+ / Python 3.10+ depending on your language choice)
- **Basic TypeScript/JavaScript knowledge** (recommended)
- **VS Code** (for VSCode extension features)
- **Git** (for version control)
- **API keys** for at least one AI provider (Claude, OpenAI, or Google AI)

### Time Investment

- **Quick Start**: 30 minutes
- **Core Concepts**: 2-3 hours
- **First Application**: 1-2 days
- **Advanced Features**: 1 week
- **Production Mastery**: 2-3 weeks

---

## What is the Genkit Development Suite?

The Genkit Development Suite is a comprehensive toolkit for building AI-powered applications. It consists of three integrated components:

### 1. Firebase Genkit Framework

**What it is:**
An open-source framework created by Google (Firebase team) for building full-stack AI applications.

**Key Features:**
- Unified API for multiple AI providers
- Built-in support for flows, prompts, RAG, and agents
- Type-safe development with TypeScript
- Comprehensive testing and evaluation tools
- Production-ready deployment options

**Language Support:**
- TypeScript/JavaScript (Production-ready)
- Go (Production-ready)
- Python (Alpha stage)

### 2. Claude-Genkit Plugin

**What it is:**
A plugin for Claude Code that brings AI-assisted development directly into your workflow.

**Key Features:**
- One-command project initialization
- AI-powered code generation
- 6 pre-built flow templates
- Deployment automation
- Built-in health checking

**Commands:**
- `/genkit-init` - Initialize new projects
- `/genkit-run` - Start development server
- `/genkit-deploy` - Deploy to cloud platforms
- `/genkit-doctor` - Health check and diagnostics

### 3. Genkit VSCode Extension

**What it is:**
A complete development toolkit integrated into Visual Studio Code.

**Key Features:**
- 34 commands for project management
- 31 code snippets for rapid development
- Visual flow explorer
- Integrated deployment tools
- Real-time monitoring dashboard

**Components:**
- Enhanced Explorer Views
- Command Palette integration
- Inline code snippets
- Debug configuration
- CI/CD templates

### How They Work Together

```
┌─────────────────────────────────────────────────────┐
│         YOU (The Developer)                         │
└─────────────────────────────────────────────────────┘
                          ↓
        ┌─────────────────┴─────────────────┐
        ↓                                   ↓
┌──────────────────┐            ┌──────────────────┐
│  Claude Code     │            │  VS Code         │
│  + Plugin        │            │  + Extension     │
│                  │            │                  │
│  AI Assistant    │            │  Visual Tools    │
│  Code Generation │            │  Snippets        │
│  Auto-deploy     │            │  Commands        │
└──────────────────┘            └──────────────────┘
        ↓                                   ↓
        └─────────────────┬─────────────────┘
                          ↓
        ┌─────────────────────────────────┐
        │  FIREBASE GENKIT FRAMEWORK      │
        │                                 │
        │  Flows • RAG • Agents • Tools   │
        └─────────────────────────────────┘
                          ↓
        ┌─────────────────────────────────┐
        │     AI MODEL PROVIDERS          │
        │  Claude • Gemini • GPT • More   │
        └─────────────────────────────────┘
```

---

## Why Use Genkit?

### The Problem with Traditional AI Development

Building AI applications from scratch involves:

1. **Complex Integration**: Each AI provider has different APIs
2. **No Standard Patterns**: Teams reinvent the wheel
3. **Limited Testing Tools**: Hard to debug AI behavior
4. **Manual Deployment**: Complex production setup
5. **Vendor Lock-in**: Difficult to switch providers

### How Genkit Solves These Problems

| Problem | Genkit Solution | Benefit |
|---------|----------------|---------|
| Different APIs | Unified interface | Write once, switch providers easily |
| No patterns | Built-in flows & templates | 60-70% faster development |
| Hard to test | Developer UI + tracing | Visual debugging, clear insights |
| Manual deployment | One-command deploy | Minutes, not hours |
| Vendor lock-in | Multi-provider support | Choose best model per task |

### Key Benefits

#### 1. **Rapid Development**
```
Traditional:  [====== 2-3 weeks ======]
With Genkit:  [== 2-3 days ==]
```

#### 2. **Cost Efficiency**
- Use cheaper models for simple tasks
- Easy A/B testing between providers
- Local development reduces API costs

#### 3. **Production Ready**
- Error handling built-in
- Monitoring and tracing
- Scalable architecture
- Security best practices

#### 4. **Developer Experience**
- Type-safe development
- IntelliSense support
- Hot reload
- Visual debugging tools

#### 5. **Flexibility**
- Deploy anywhere (cloud, on-premises, edge)
- Use any AI model (commercial or open-source)
- Integrate with existing codebases

### When to Use Genkit

**Perfect For:**
- ✅ Building AI chatbots and assistants
- ✅ RAG (Retrieval Augmented Generation) applications
- ✅ AI agents with tool calling
- ✅ Multi-step AI workflows
- ✅ Streaming AI responses
- ✅ Production AI services

**Not Ideal For:**
- ❌ Pure machine learning model training
- ❌ Computer vision pipelines (use TensorFlow/PyTorch)
- ❌ Real-time audio/video AI (specialized tools better)
- ❌ Embedded AI on edge devices (too heavy)

### Comparison with Alternatives

| Feature | Genkit | LangChain | OpenAI SDK | Custom |
|---------|--------|-----------|------------|--------|
| Learning Curve | Low | Medium | Low | High |
| Multi-provider | ✅ | ✅ | ❌ | ⚠️ |
| TypeScript Support | Excellent | Good | Good | Varies |
| Developer UI | ✅ | ❌ | ❌ | ❌ |
| Production Ready | ✅ | ⚠️ | ⚠️ | ⚠️ |
| Deployment Tools | ✅ | ❌ | ❌ | ❌ |
| Testing Tools | ✅ | Limited | Limited | Custom |
| Community Size | Growing | Large | Large | N/A |

---

## Installation & Setup

### System Requirements

**Minimum:**
- Node.js 18.0.0 or higher
- npm 8.0.0 or higher
- 4GB RAM
- 2GB disk space

**Recommended:**
- Node.js 20.x LTS
- npm 10.x
- 8GB RAM
- VS Code 1.80+
- Git 2.30+

### Step 1: Install Node.js (if needed)

**Check current version:**
```bash
node --version
npm --version
```

**Install Node.js:**
- **macOS**: `brew install node@20`
- **Windows**: Download from [nodejs.org](https://nodejs.org)
- **Linux**:
  ```bash
  curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
  sudo apt-get install -y nodejs
  ```

### Step 2: Install Genkit CLI

**Option A: NPM (Recommended)**
```bash
npm install -g genkit-cli
```

**Option B: macOS/Linux Script**
```bash
curl -sL cli.genkit.dev | bash
```

**Option C: Windows**
1. Download binary from [https://genkit.dev/downloads](https://genkit.dev/downloads)
2. Add to PATH

**Verify Installation:**
```bash
genkit --version
# Expected output: genkit/1.x.x
```

### Step 3: Install Claude-Genkit Plugin

**Requirements:**
- Claude Code CLI installed
- Active Claude account

**Installation Steps:**

1. **Add Plugin Marketplace:**
```bash
# In Claude Code
/plugin marketplace add https://github.com/amitpatole/claude-genkit-plugin.git
```

2. **Install Plugin:**
```bash
/plugin install genkit
```

3. **Verify Installation:**
```bash
/genkit-doctor
```

**Expected Output:**
```
✓ Genkit CLI found (v1.x.x)
✓ Node.js version compatible (v20.x.x)
✓ npm version compatible (v10.x.x)
✓ Claude Code integration working
✓ All dependencies satisfied
```

### Step 4: Install VSCode Extension

**Method 1: VS Code Marketplace (Recommended)**

1. Open VS Code
2. Click Extensions icon (Ctrl+Shift+X)
3. Search for "Genkit for VS Code"
4. Click **Install**

**Method 2: Command Line**
```bash
code --install-extension AmitPatole.genkit-vscode
```

**Method 3: VSIX File**
```bash
# Download .vsix file from marketplace
code --install-extension genkit-vscode-1.x.x.vsix
```

**Verify Installation:**
1. Open Command Palette (Ctrl+Shift+P)
2. Type "Genkit"
3. You should see multiple Genkit commands

### Step 5: Configure API Keys

**Create Environment File:**
```bash
# In your project directory
touch .env
```

**Add API Keys:**
```bash
# .env file
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_AI_API_KEY=AIzaxxxxxxxxxxxxxxxxxxxxx

# Optional: Custom model endpoints
CUSTOM_MODEL_ENDPOINT=https://your-endpoint.com
```

**Important Security Notes:**
- ⚠️ Never commit `.env` files to version control
- ⚠️ Add `.env` to your `.gitignore`
- ⚠️ Use environment-specific keys (dev, staging, prod)
- ⚠️ Rotate keys regularly

### Step 6: Verify Complete Setup

**Run Health Check:**
```bash
genkit config list
```

**Expected Output:**
```
Genkit Configuration:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLI Version:        1.x.x
Node Version:       20.x.x
Default Port:       4000
Analytics:          opt-in
Telemetry:          enabled
Plugins:            claude, vscode
Status:             ✓ Ready
```

**Test Simple Command:**
```bash
genkit --help
```

You should see a list of available commands.

### Troubleshooting Installation

**Issue: `genkit: command not found`**

**Solution:**
```bash
# Add to PATH (macOS/Linux)
echo 'export PATH="$PATH:$HOME/.genkit/bin"' >> ~/.bashrc
source ~/.bashrc

# Windows: Add installation directory to System PATH
```

**Issue: Permission denied**

**Solution:**
```bash
# macOS/Linux
sudo chown -R $USER:$GROUP ~/.npm
sudo chown -R $USER:$GROUP ~/.genkit

# Or use npx instead of global install
npx genkit-cli@latest --version
```

**Issue: Version conflicts**

**Solution:**
```bash
# Remove old installation
npm uninstall -g genkit-cli
rm -rf ~/.genkit

# Reinstall
npm install -g genkit-cli@latest
```

---

## Core Concepts

Before diving into code, let's understand the fundamental concepts that power Genkit.

### 1. Flows

**What is a Flow?**
A flow is a reusable, type-safe AI workflow with defined inputs and outputs.

**Think of it as:**
- A function, but for AI operations
- A pipeline that processes data through AI models
- A blueprint for an AI feature

**Anatomy of a Flow:**
```typescript
export const myFlow = defineFlow(
  {
    // 1. Metadata
    name: 'myFlow',

    // 2. Input Schema (validation)
    inputSchema: z.object({
      query: z.string(),
    }),

    // 3. Output Schema (validation)
    outputSchema: z.object({
      response: z.string(),
    }),
  },
  // 4. Implementation
  async (input) => {
    // Your AI logic here
    return { response: 'result' };
  }
);
```

**Why Flows?**
- ✅ **Type Safety**: Catch errors at compile time
- ✅ **Testability**: Easy to unit test
- ✅ **Reusability**: Use across different parts of your app
- ✅ **Traceability**: Built-in logging and monitoring
- ✅ **Composability**: Flows can call other flows

### 2. Prompts

**What is a Prompt?**
A prompt is a templated instruction to an AI model, with variables and formatting.

**Types of Prompts:**

1. **Simple String Prompt:**
```typescript
const prompt = "Translate this to French: Hello";
```

2. **Template Prompt:**
```typescript
const prompt = `Translate this to ${language}: ${text}`;
```

3. **Structured Prompt:**
```typescript
const prompt = definePrompt(
  {
    name: 'translator',
    inputSchema: z.object({
      text: z.string(),
      targetLanguage: z.string(),
    }),
  },
  async (input) => {
    return `You are a professional translator.

    Translate the following text to ${input.targetLanguage}:
    ${input.text}

    Provide only the translation, no explanations.`;
  }
);
```

**Best Practices:**
- Be specific and clear
- Provide examples when needed
- Set the right tone and context
- Use consistent formatting

### 3. Models

**What is a Model?**
A model is an AI service (like Claude, GPT, Gemini) that generates text, images, or other outputs.

**Supported Models:**

| Provider | Models | Best For |
|----------|--------|----------|
| **Anthropic** | Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku | Code, analysis, long context |
| **OpenAI** | GPT-4, GPT-4 Turbo, GPT-3.5 Turbo | General purpose, speed |
| **Google** | Gemini 1.5 Pro, Gemini 1.5 Flash | Multimodal, speed |
| **Ollama** | Llama 3, Mistral, CodeLlama | Local, private, free |

**Using Models:**
```typescript
import { claude35Sonnet } from '@genkit-ai/anthropic';
import { gemini15Pro } from '@genkit-ai/googleai';
import { gpt4 } from '@genkit-ai/openai';

// Generate with Claude
const result = await claude35Sonnet.generate({
  prompt: 'Explain quantum computing',
  config: {
    temperature: 0.7,
    maxOutputTokens: 1024,
  },
});
```

**Choosing the Right Model:**

**For Code & Technical Analysis:**
- 🥇 Claude 3.5 Sonnet (best)
- 🥈 GPT-4 Turbo
- 🥉 Gemini 1.5 Pro

**For Speed & Cost:**
- 🥇 Claude 3 Haiku
- 🥈 GPT-3.5 Turbo
- 🥉 Gemini 1.5 Flash

**For Privacy:**
- 🥇 Ollama (local)
- 🥈 Self-hosted models

### 4. Tools

**What is a Tool?**
A tool is a function that AI can call to interact with external systems or perform actions.

**Example:**
```typescript
const weatherTool = defineTool(
  {
    name: 'getWeather',
    description: 'Get current weather for a location',
    inputSchema: z.object({
      location: z.string(),
      units: z.enum(['celsius', 'fahrenheit']).default('celsius'),
    }),
    outputSchema: z.object({
      temperature: z.number(),
      conditions: z.string(),
      humidity: z.number(),
    }),
  },
  async (input) => {
    // Call weather API
    const data = await fetch(`https://api.weather.com/${input.location}`);
    return {
      temperature: 22,
      conditions: 'Sunny',
      humidity: 60,
    };
  }
);
```

**Using Tools in Flows:**
```typescript
const result = await claude35Sonnet.generate({
  prompt: 'What should I wear in San Francisco today?',
  tools: [weatherTool],
});
```

**The AI will:**
1. Analyze the question
2. Decide to use the `getWeather` tool
3. Call it with `location: "San Francisco"`
4. Use the result to answer the question

### 5. Retrievers (RAG)

**What is a Retriever?**
A retriever fetches relevant documents from a knowledge base to provide context to AI.

**RAG Pattern:**
```
User Question
     ↓
Generate Embeddings
     ↓
Search Vector Database
     ↓
Retrieve Relevant Docs
     ↓
Build Context
     ↓
Send to AI Model
     ↓
Contextualized Answer
```

**Example:**
```typescript
// Define retriever
const docRetriever = defineRetriever(
  {
    name: 'documentRetriever',
    configSchema: z.object({
      k: z.number().default(5),
    }),
  },
  async (query, options) => {
    // Search vector database
    const results = await vectorDB.search(query, options.k);
    return results;
  }
);

// Use in flow
const docs = await retrieve({
  retriever: docRetriever,
  query: 'How do I deploy to production?',
  options: { k: 5 },
});
```

### 6. Embedders

**What is an Embedder?**
An embedder converts text into numerical vectors for semantic search.

**Common Embedders:**
- `textembedding-gecko` (Google)
- `text-embedding-3-large` (OpenAI)
- `all-MiniLM-L6-v2` (Ollama, free)

**Usage:**
```typescript
import { embed } from '@genkit-ai/ai/embedder';

const embedding = await embed({
  embedder: 'textembedding-gecko',
  content: 'This is the text to embed',
});

// Result: [0.123, -0.456, 0.789, ...]
```

### 7. Schemas & Validation

**What is Zod?**
Zod is a TypeScript-first schema validation library used by Genkit.

**Common Patterns:**

```typescript
import { z } from 'zod';

// String validation
z.string()                          // Any string
z.string().min(1)                   // Non-empty
z.string().max(100)                 // Max 100 chars
z.string().email()                  // Valid email
z.string().url()                    // Valid URL
z.string().regex(/^[A-Z]+$/)        // Pattern match

// Number validation
z.number()                          // Any number
z.number().int()                    // Integer only
z.number().positive()               // > 0
z.number().min(0).max(100)          // Range

// Enums
z.enum(['option1', 'option2'])      // One of

// Objects
z.object({
  name: z.string(),
  age: z.number().int().positive(),
  email: z.string().email().optional(),
})

// Arrays
z.array(z.string())                 // Array of strings
z.array(z.number()).min(1)          // Non-empty array

// Optional & Default
z.string().optional()               // Can be undefined
z.number().default(0)               // Default value
```

---

## Firebase Genkit Framework

This section covers the core Genkit framework in depth.

### Project Structure

**Recommended Layout:**
```
my-genkit-project/
├── src/
│   ├── flows/           # Flow definitions
│   │   ├── chat.ts
│   │   ├── rag.ts
│   │   └── tools.ts
│   ├── prompts/         # Prompt templates
│   │   ├── system.ts
│   │   └── templates.ts
│   ├── tools/           # Tool definitions
│   │   ├── weather.ts
│   │   └── search.ts
│   ├── retrievers/      # Custom retrievers
│   │   └── docs.ts
│   ├── config/          # Configuration
│   │   └── models.ts
│   └── index.ts         # Entry point
├── tests/               # Test files
├── data/                # Training data, etc.
├── .env                 # Environment variables
├── .env.example         # Template
├── .gitignore
├── genkit.config.ts     # Genkit configuration
├── package.json
└── tsconfig.json
```

### Configuration File

**genkit.config.ts:**
```typescript
import { config } from 'dotenv';
import { defineConfig } from '@genkit-ai/core';
import { anthropic } from '@genkit-ai/anthropic';
import { googleAI } from '@genkit-ai/googleai';
import { openai } from '@genkit-ai/openai';

// Load environment variables
config();

export default defineConfig({
  // Plugins for AI providers
  plugins: [
    anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    }),
    googleAI({
      apiKey: process.env.GOOGLE_AI_API_KEY,
    }),
    openai({
      apiKey: process.env.OPENAI_API_KEY,
    }),
  ],

  // Telemetry settings
  telemetry: {
    enabled: true,
    logLevel: 'info',
  },

  // Development server settings
  server: {
    port: 4000,
    host: 'localhost',
  },

  // Production settings
  production: {
    telemetry: {
      instrumentation: 'opentelemetry',
    },
  },
});
```

### Building Flows - Deep Dive

#### Simple Chat Flow

```typescript
import { defineFlow } from '@genkit-ai/flow';
import { claude35Sonnet } from '@genkit-ai/anthropic';
import { z } from 'zod';

export const simpleChatFlow = defineFlow(
  {
    name: 'simpleChat',
    inputSchema: z.object({
      message: z.string().min(1, 'Message cannot be empty'),
      systemPrompt: z.string().optional(),
    }),
    outputSchema: z.object({
      response: z.string(),
      model: z.string(),
      tokens: z.number(),
    }),
  },
  async (input) => {
    const prompt = input.systemPrompt
      ? `${input.systemPrompt}\n\nUser: ${input.message}`
      : input.message;

    const result = await claude35Sonnet.generate({
      prompt,
      config: {
        temperature: 0.7,
        maxOutputTokens: 1024,
      },
    });

    return {
      response: result.text,
      model: 'claude-3-5-sonnet',
      tokens: result.usage?.totalTokens || 0,
    };
  }
);
```

#### RAG Flow (Complete Implementation)

```typescript
import { defineFlow } from '@genkit-ai/flow';
import { claude35Sonnet } from '@genkit-ai/anthropic';
import { embed } from '@genkit-ai/ai/embedder';
import { retrieve } from '@genkit-ai/ai/retriever';
import { z } from 'zod';

// Define vector store interface
interface VectorStore {
  search(embedding: number[], limit: number): Promise<Document[]>;
}

interface Document {
  content: string;
  metadata: {
    title: string;
    url: string;
    date: string;
  };
  score: number;
}

export const ragFlow = defineFlow(
  {
    name: 'rag',
    inputSchema: z.object({
      question: z.string(),
      maxResults: z.number().int().positive().default(5),
      minRelevanceScore: z.number().min(0).max(1).default(0.7),
    }),
    outputSchema: z.object({
      answer: z.string(),
      sources: z.array(z.object({
        title: z.string(),
        url: z.string(),
        relevance: z.number(),
        excerpt: z.string(),
      })),
      confidence: z.number(),
    }),
  },
  async (input) => {
    // Step 1: Generate query embedding
    const questionEmbedding = await embed({
      embedder: 'textembedding-gecko',
      content: input.question,
    });

    // Step 2: Retrieve relevant documents
    const docs = await retrieve({
      retriever: 'myVectorStore',
      query: questionEmbedding,
      options: {
        limit: input.maxResults,
      },
    });

    // Step 3: Filter by relevance score
    const relevantDocs = docs.filter(
      doc => doc.score >= input.minRelevanceScore
    );

    // Step 4: Build context from documents
    const context = relevantDocs
      .map((doc, idx) => {
        return `[${idx + 1}] ${doc.metadata.title}
Source: ${doc.metadata.url}
Content: ${doc.content}`;
      })
      .join('\n\n---\n\n');

    // Step 5: Generate answer with Claude
    const result = await claude35Sonnet.generate({
      prompt: `You are a helpful assistant that answers questions based on provided context.

Context from knowledge base:
${context}

User Question: ${input.question}

Instructions:
- Answer the question using ONLY the information in the context above
- Cite sources using [number] notation
- If the answer is not in the context, say "I don't have enough information to answer this question"
- Be concise but thorough
- If you're uncertain, express that uncertainty

Answer:`,
      config: {
        temperature: 0.3, // Lower temperature for factual accuracy
        maxOutputTokens: 2048,
      },
    });

    // Step 6: Calculate confidence score
    const avgRelevance = relevantDocs.reduce((sum, doc) => sum + doc.score, 0)
      / relevantDocs.length;
    const confidence = Math.min(avgRelevance, 1);

    // Step 7: Format sources
    const sources = relevantDocs.map(doc => ({
      title: doc.metadata.title,
      url: doc.metadata.url,
      relevance: doc.score,
      excerpt: doc.content.substring(0, 200) + '...',
    }));

    return {
      answer: result.text,
      sources,
      confidence,
    };
  }
);
```

#### Tool Calling Flow (Multi-Tool Agent)

```typescript
import { defineFlow, defineTool } from '@genkit-ai/flow';
import { claude35Sonnet } from '@genkit-ai/anthropic';
import { z } from 'zod';
import axios from 'axios';

// Define tools
const searchTool = defineTool(
  {
    name: 'search',
    description: 'Search the web for current information',
    inputSchema: z.object({
      query: z.string(),
      maxResults: z.number().default(5),
    }),
    outputSchema: z.object({
      results: z.array(z.object({
        title: z.string(),
        url: z.string(),
        snippet: z.string(),
      })),
    }),
  },
  async (input) => {
    // Implement actual search (e.g., using Google Custom Search API)
    const response = await axios.get('https://api.search.com/search', {
      params: { q: input.query, limit: input.maxResults },
    });

    return {
      results: response.data.results,
    };
  }
);

const calculatorTool = defineTool(
  {
    name: 'calculator',
    description: 'Perform mathematical calculations',
    inputSchema: z.object({
      expression: z.string(),
    }),
    outputSchema: z.object({
      result: z.number(),
    }),
  },
  async (input) => {
    // Safe eval using a math library
    const result = eval(input.expression); // In production, use a safe math parser!
    return { result };
  }
);

const weatherTool = defineTool(
  {
    name: 'getWeather',
    description: 'Get current weather for a location',
    inputSchema: z.object({
      location: z.string(),
    }),
    outputSchema: z.object({
      temperature: z.number(),
      conditions: z.string(),
      humidity: z.number(),
    }),
  },
  async (input) => {
    // Implement actual weather API call
    const response = await axios.get('https://api.weather.com/current', {
      params: { location: input.location },
    });

    return response.data;
  }
);

// Agent flow that can use multiple tools
export const agentFlow = defineFlow(
  {
    name: 'agent',
    inputSchema: z.object({
      task: z.string(),
      context: z.string().optional(),
    }),
    outputSchema: z.object({
      result: z.string(),
      toolsUsed: z.array(z.object({
        name: z.string(),
        input: z.any(),
        output: z.any(),
      })),
      reasoning: z.string(),
    }),
  },
  async (input) => {
    const systemPrompt = `You are a helpful AI assistant with access to tools.

Available tools:
- search: Search the web for current information
- calculator: Perform mathematical calculations
- getWeather: Get weather information

${input.context ? `Context: ${input.context}` : ''}

Task: ${input.task}

Think step by step:
1. Analyze what information you need
2. Use tools to gather that information
3. Synthesize the information to complete the task`;

    const result = await claude35Sonnet.generate({
      prompt: systemPrompt,
      tools: [searchTool, calculatorTool, weatherTool],
      config: {
        temperature: 0.2,
        maxOutputTokens: 2048,
      },
    });

    // Extract tool usage
    const toolsUsed = result.toolCalls?.map(call => ({
      name: call.name,
      input: call.input,
      output: call.output,
    })) || [];

    return {
      result: result.text,
      toolsUsed,
      reasoning: 'The agent analyzed the task and used the appropriate tools.',
    };
  }
);
```

#### Streaming Flow

```typescript
import { defineFlow } from '@genkit-ai/flow';
import { claude35Sonnet } from '@genkit-ai/anthropic';
import { z } from 'zod';

export const streamingFlow = defineFlow(
  {
    name: 'streaming',
    inputSchema: z.object({
      prompt: z.string(),
    }),
    outputSchema: z.object({
      fullResponse: z.string(),
    }),
    streamSchema: z.string(), // Type of each chunk
  },
  async (input, { stream }) => {
    // Generate streaming response
    const result = await claude35Sonnet.generateStream({
      prompt: input.prompt,
      config: {
        temperature: 0.7,
        maxOutputTokens: 2048,
      },
    });

    let fullResponse = '';

    // Stream chunks to client
    for await (const chunk of result.stream) {
      if (chunk.text) {
        stream.push(chunk.text);
        fullResponse += chunk.text;
      }
    }

    return { fullResponse };
  }
);
```

### Advanced Patterns

#### Chaining Flows

```typescript
// Flow 1: Extract entities
const extractEntitiesFlow = defineFlow(
  {
    name: 'extractEntities',
    inputSchema: z.object({ text: z.string() }),
    outputSchema: z.object({
      entities: z.array(z.object({
        name: z.string(),
        type: z.string(),
      })),
    }),
  },
  async (input) => {
    // Implementation...
    return { entities: [] };
  }
);

// Flow 2: Enrich entities
const enrichEntitiesFlow = defineFlow(
  {
    name: 'enrichEntities',
    inputSchema: z.object({
      entities: z.array(z.object({
        name: z.string(),
        type: z.string(),
      })),
    }),
    outputSchema: z.object({
      enrichedEntities: z.array(z.any()),
    }),
  },
  async (input) => {
    // Implementation...
    return { enrichedEntities: [] };
  }
);

// Combined flow
export const entityPipelineFlow = defineFlow(
  {
    name: 'entityPipeline',
    inputSchema: z.object({ text: z.string() }),
  },
  async (input) => {
    // Step 1: Extract
    const extracted = await extractEntitiesFlow(input);

    // Step 2: Enrich
    const enriched = await enrichEntitiesFlow(extracted);

    return enriched;
  }
);
```

#### Error Handling & Retries

```typescript
import { defineFlow } from '@genkit-ai/flow';
import { claude35Sonnet } from '@genkit-ai/anthropic';
import { gemini15Pro } from '@genkit-ai/googleai';
import { z } from 'zod';

export const resilientFlow = defineFlow(
  {
    name: 'resilient',
    inputSchema: z.object({ prompt: z.string() }),
    outputSchema: z.object({
      response: z.string(),
      provider: z.string(),
      attempts: z.number(),
    }),
  },
  async (input) => {
    let attempts = 0;
    let lastError: Error | null = null;

    // Try primary provider (Claude)
    try {
      attempts++;
      const result = await claude35Sonnet.generate({
        prompt: input.prompt,
      });

      return {
        response: result.text,
        provider: 'claude',
        attempts,
      };
    } catch (error) {
      console.error('Claude failed:', error);
      lastError = error as Error;
    }

    // Try fallback provider (Gemini)
    try {
      attempts++;
      const result = await gemini15Pro.generate({
        prompt: input.prompt,
      });

      return {
        response: result.text,
        provider: 'gemini',
        attempts,
      };
    } catch (error) {
      console.error('Gemini failed:', error);
      lastError = error as Error;
    }

    // All providers failed
    throw new Error(
      `All AI providers failed after ${attempts} attempts. ` +
      `Last error: ${lastError?.message}`
    );
  }
);
```

#### Caching Results

```typescript
import { defineFlow } from '@genkit-ai/flow';
import { z } from 'zod';
import { createHash } from 'crypto';

// Simple in-memory cache
const cache = new Map<string, { value: any; timestamp: number }>();
const CACHE_TTL = 3600000; // 1 hour

function getCacheKey(input: any): string {
  return createHash('md5').update(JSON.stringify(input)).digest('hex');
}

export const cachedFlow = defineFlow(
  {
    name: 'cached',
    inputSchema: z.object({ query: z.string() }),
    outputSchema: z.object({
      result: z.string(),
      fromCache: z.boolean(),
    }),
  },
  async (input) => {
    const cacheKey = getCacheKey(input);
    const now = Date.now();

    // Check cache
    const cached = cache.get(cacheKey);
    if (cached && (now - cached.timestamp) < CACHE_TTL) {
      return {
        result: cached.value,
        fromCache: true,
      };
    }

    // Generate new result
    const result = await claude35Sonnet.generate({
      prompt: input.query,
    });

    // Store in cache
    cache.set(cacheKey, {
      value: result.text,
      timestamp: now,
    });

    return {
      result: result.text,
      fromCache: false,
    };
  }
);
```

---

## Claude-Genkit Plugin

Comprehensive guide to using the Claude Code plugin.

### Available Commands

#### 1. `/genkit-init` - Initialize Project

**Purpose:** Create a new Genkit project with all dependencies.

**Interactive Prompts:**
```
? Select language:
  > TypeScript (recommended)
    JavaScript
    Go
    Python

? Select AI provider:
  > Claude (Anthropic)
    Gemini (Google AI)
    GPT (OpenAI)
    Multiple providers

? Select template:
  > Simple Chat
    RAG (Retrieval Augmented Generation)
    Tool Calling
    Multi-step Workflow
    Streaming
    Blank
```

**Generated Structure:**
```
my-project/
├── src/
│   ├── index.ts
│   └── flows/
│       └── chat.ts (or selected template)
├── tests/
├── .env.example
├── .gitignore
├── genkit.config.ts
├── package.json
└── tsconfig.json
```

**Example Usage:**
```bash
# In Claude Code
/genkit-init my-ai-app

# Follow the prompts...
```

#### 2. `/genkit-run` - Start Development Server

**Purpose:** Launch development server with hot reload and Developer UI.

**What it does:**
- Starts your application server
- Launches Genkit Developer UI (localhost:4000)
- Watches for file changes
- Auto-reloads on save

**Usage:**
```bash
/genkit-run

# Or with custom port
/genkit-run --port 5000

# With watch mode
/genkit-run --watch
```

**Output:**
```
✓ Genkit development server started
✓ Application running on http://localhost:3000
✓ Developer UI available at http://localhost:4000

Watching for changes...
```

#### 3. `/genkit-deploy` - Deploy to Cloud

**Purpose:** Deploy your Genkit application to production.

**Supported Platforms:**
- Firebase Cloud Functions
- Google Cloud Run
- Vercel
- Docker

**Usage:**

**Firebase:**
```bash
/genkit-deploy firebase

# Prompts:
# - Project ID
# - Region
# - Function name
```

**Cloud Run:**
```bash
/genkit-deploy cloud-run

# Prompts:
# - Project ID
# - Region
# - Service name
# - Allow unauthenticated? (y/n)
```

**Vercel:**
```bash
/genkit-deploy vercel

# Prompts:
# - Project name
# - Production? (y/n)
```

**Docker:**
```bash
/genkit-deploy docker

# Generates:
# - Dockerfile
# - .dockerignore
# - docker-compose.yml
```

#### 4. `/genkit-doctor` - Health Check

**Purpose:** Verify installation and dependencies.

**Checks:**
- ✓ Genkit CLI version
- ✓ Node.js version compatibility
- ✓ npm version
- ✓ API keys configured
- ✓ Dependencies installed
- ✓ Configuration valid

**Usage:**
```bash
/genkit-doctor

# Detailed output
/genkit-doctor --verbose
```

**Sample Output:**
```
Genkit Health Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ CLI Version: 1.5.0 (latest)
✓ Node.js: v20.10.0 (compatible)
✓ npm: v10.2.0 (compatible)
✓ TypeScript: v5.3.3 (compatible)
✓ API Keys: 2/3 configured
  ✓ ANTHROPIC_API_KEY
  ✓ GOOGLE_AI_API_KEY
  ✗ OPENAI_API_KEY (missing)
✓ Dependencies: All installed
✓ Configuration: Valid

Status: HEALTHY (1 warning)
Warnings: OpenAI API key not configured
```

#### 5. AI Assistant Commands

**Ask for Architecture Advice:**
```bash
# In Claude Code
"Help me design a RAG system for customer support"
```

Claude will:
- Suggest appropriate flows
- Recommend models
- Provide code examples
- Explain best practices

**Generate Code:**
```bash
"Create a tool calling flow that can check stock prices"
```

Claude generates:
```typescript
// Complete, working code
import { defineFlow, defineTool } from '@genkit-ai/flow';
// ... full implementation
```

**Debug Issues:**
```bash
"My flow is returning undefined, here's my code: [paste code]"
```

Claude will:
- Analyze the code
- Identify the issue
- Suggest fixes
- Explain why

### Working with Templates

#### Simple Chat Template

**Generated Code:**
```typescript
import { defineFlow } from '@genkit-ai/flow';
import { claude35Sonnet } from '@genkit-ai/anthropic';
import { z } from 'zod';

export const chatFlow = defineFlow(
  {
    name: 'chat',
    inputSchema: z.object({
      message: z.string(),
    }),
    outputSchema: z.object({
      response: z.string(),
    }),
  },
  async (input) => {
    const result = await claude35Sonnet.generate({
      prompt: input.message,
      config: {
        temperature: 0.7,
        maxOutputTokens: 1024,
      },
    });

    return {
      response: result.text,
    };
  }
);
```

**Customization Ideas:**
- Add conversation history
- Implement user personas
- Add content filtering
- Include rate limiting

#### RAG Template

**Generated Code:**
```typescript
import { defineFlow } from '@genkit-ai/flow';
import { claude35Sonnet } from '@genkit-ai/anthropic';
import { embed, retrieve } from '@genkit-ai/ai';
import { z } from 'zod';

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
    // 1. Generate embeddings
    const embedding = await embed({
      embedder: 'textembedding-gecko',
      content: input.question,
    });

    // 2. Retrieve documents
    const docs = await retrieve({
      retriever: 'myVectorStore',
      query: embedding,
      options: { limit: input.maxResults },
    });

    // 3. Build context
    const context = docs.map(d => d.content).join('\n\n');

    // 4. Generate answer
    const result = await claude35Sonnet.generate({
      prompt: `Context: ${context}\n\nQuestion: ${input.question}`,
    });

    return {
      answer: result.text,
      sources: docs.map(d => d.metadata.url),
    };
  }
);
```

**Customization Ideas:**
- Implement custom vector store
- Add reranking
- Filter by metadata
- Implement semantic caching

---

## Genkit VSCode Extension

Complete guide to the VSCode extension features.

### Commands (34 Total)

**Access:** `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) → Type "Genkit"

#### Project Management (8 commands)

1. **Genkit: Initialize Project**
   - Creates new Genkit project
   - Same as `/genkit-init`

2. **Genkit: Open in Developer UI**
   - Opens http://localhost:4000 in browser

3. **Genkit: Start Development Server**
   - Starts dev server with hot reload

4. **Genkit: Stop Development Server**
   - Gracefully stops server

5. **Genkit: Restart Development Server**
   - Restart without manual stop/start

6. **Genkit: Show Project Info**
   - Display project details, version, config

7. **Genkit: Validate Configuration**
   - Check genkit.config.ts for errors

8. **Genkit: Update Dependencies**
   - Update @genkit-ai packages

#### Flow Management (10 commands)

9. **Genkit: Create New Flow**
   - Interactive flow creation wizard

10. **Genkit: Run Flow**
    - Select and run any flow

11. **Genkit: Run Flow with Input**
    - Provide custom JSON input

12. **Genkit: Debug Flow**
    - Run flow in debug mode with breakpoints

13. **Genkit: View Flow Traces**
    - Show execution traces for debugging

14. **Genkit: Test Flow**
    - Run associated test file

15. **Genkit: Duplicate Flow**
    - Copy flow with new name

16. **Genkit: Delete Flow**
    - Remove flow and associated files

17. **Genkit: Export Flow**
    - Export as standalone function

18. **Genkit: View Flow Documentation**
    - Generate docs from code

#### Deployment (6 commands)

19. **Genkit: Deploy to Firebase**
    - Deploy to Cloud Functions

20. **Genkit: Deploy to Cloud Run**
    - Deploy to Google Cloud Run

21. **Genkit: Deploy to Vercel**
    - Deploy to Vercel platform

22. **Genkit: Generate Dockerfile**
    - Create optimized Docker image

23. **Genkit: Setup CI/CD Pipeline**
    - Generate GitHub Actions / GitLab CI config

24. **Genkit: View Deployment Status**
    - Check deployed services

#### Tools & Utilities (10 commands)

25. **Genkit: Create Tool**
    - Generate tool definition

26. **Genkit: Create Retriever**
    - Generate retriever for RAG

27. **Genkit: Create Prompt Template**
    - Create reusable prompt

28. **Genkit: Generate Tests**
    - Auto-generate test file

29. **Genkit: Run All Tests**
    - Execute test suite

30. **Genkit: View Test Coverage**
    - Show coverage report

31. **Genkit: Evaluate Flow**
    - Run evaluation metrics

32. **Genkit: View Logs**
    - Show application logs

33. **Genkit: Clear Cache**
    - Clear Genkit cache

34. **Genkit: Generate TypeScript Types**
    - Generate types from schemas

### Code Snippets (31 Total)

**Usage:** Type the prefix in a TypeScript file and press `Tab`

#### Flow Snippets (8)

**Prefix:** `genkit-flow-simple`
```typescript
import { defineFlow } from '@genkit-ai/flow';
import { z } from 'zod';

export const ${1:flowName}Flow = defineFlow(
  {
    name: '${1:flowName}',
    inputSchema: z.object({
      ${2:input}: z.string(),
    }),
    outputSchema: z.object({
      ${3:output}: z.string(),
    }),
  },
  async (input) => {
    ${4:// Implementation}
    return { ${3:output}: '' };
  }
);
```

**More Flow Snippets:**
- `genkit-flow-rag` - RAG flow template
- `genkit-flow-streaming` - Streaming flow
- `genkit-flow-tool-calling` - Tool calling flow
- `genkit-flow-multi-step` - Multi-step workflow
- `genkit-flow-async` - Async flow
- `genkit-flow-error-handling` - With error handling
- `genkit-flow-cached` - With caching

#### Tool Snippets (5)

**Prefix:** `genkit-tool`
```typescript
import { defineTool } from '@genkit-ai/flow';
import { z } from 'zod';

export const ${1:toolName}Tool = defineTool(
  {
    name: '${1:toolName}',
    description: '${2:description}',
    inputSchema: z.object({
      ${3:param}: z.string(),
    }),
    outputSchema: z.object({
      ${4:result}: z.any(),
    }),
  },
  async (input) => {
    ${5:// Implementation}
    return { ${4:result}: null };
  }
);
```

**More Tool Snippets:**
- `genkit-tool-api` - API call tool
- `genkit-tool-db` - Database query tool
- `genkit-tool-file` - File operation tool
- `genkit-tool-calculation` - Math tool

#### Prompt Snippets (4)

- `genkit-prompt-simple` - Simple prompt
- `genkit-prompt-template` - Templated prompt
- `genkit-prompt-dotprompt` - .prompt file
- `genkit-prompt-multi-turn` - Conversation prompt

#### Schema Snippets (6)

- `genkit-schema-object` - Zod object schema
- `genkit-schema-array` - Array schema
- `genkit-schema-enum` - Enum schema
- `genkit-schema-union` - Union type
- `genkit-schema-optional` - Optional fields
- `genkit-schema-nested` - Nested objects

#### Test Snippets (4)

- `genkit-test-flow` - Flow test
- `genkit-test-tool` - Tool test
- `genkit-test-integration` - Integration test
- `genkit-test-e2e` - End-to-end test

#### Configuration Snippets (4)

- `genkit-config-full` - Full configuration
- `genkit-config-anthropic` - Anthropic setup
- `genkit-config-googleai` - Google AI setup
- `genkit-config-openai` - OpenAI setup

### Explorer Views

The extension adds custom views to VS Code's sidebar.

#### Flows View

**Location:** Activity Bar → Genkit icon

**Features:**
- 📁 List all flows in project
- ▶️ Run flow (click to run)
- 🔍 View flow details
- 📝 Edit flow code
- 🧪 Run tests
- 📊 View traces

**Actions:**
- Right-click flow → Run
- Right-click flow → Run with Input
- Right-click flow → Debug
- Right-click flow → View Tests
- Right-click flow → Delete

#### Models View

**Features:**
- List configured AI models
- Show usage statistics
- Display current costs
- Compare model performance

**Example:**
```
Models
├── 🟢 Claude 3.5 Sonnet
│   └── Requests: 1,234 | Tokens: 456K | Cost: $12.34
├── 🟢 Gemini 1.5 Pro
│   └── Requests: 567 | Tokens: 189K | Cost: $3.45
└── 🔴 GPT-4 (Not configured)
```

#### Deployments View

**Features:**
- List deployed services
- Show deployment status
- View URLs
- Monitor health

**Example:**
```
Deployments
├── 🟢 Production (Cloud Run)
│   ├── URL: https://my-service-xxx.run.app
│   ├── Status: Healthy
│   └── Last Deploy: 2 hours ago
└── 🟡 Staging (Firebase)
    ├── Status: Deploying...
    └── Progress: 75%
```

### Keyboard Shortcuts

**Default Shortcuts:**

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+G K` | Initialize Project |
| `Ctrl+Shift+G R` | Run Current Flow |
| `Ctrl+Shift+G D` | Open Developer UI |
| `Ctrl+Shift+G T` | Run Tests |
| `Ctrl+Shift+G L` | View Logs |

**Customize:** File → Preferences → Keyboard Shortcuts → Search "Genkit"

### Settings

**Access:** File → Preferences → Settings → Search "Genkit"

**Available Settings:**

```json
{
  // Auto-start dev server when opening project
  "genkit.autoStartDevServer": false,

  // Default port for Developer UI
  "genkit.devServerPort": 4000,

  // Show inline hints
  "genkit.inlineHints": true,

  // Auto-format on save
  "genkit.formatOnSave": true,

  // Default AI provider for new projects
  "genkit.defaultProvider": "anthropic",

  // Enable telemetry
  "genkit.telemetry": true,

  // Log level
  "genkit.logLevel": "info", // "debug" | "info" | "warn" | "error"

  // Auto-update dependencies
  "genkit.autoUpdate": false,

  // Show flow execution time
  "genkit.showExecutionTime": true,

  // Enable experimental features
  "genkit.experimental": false
}
```

### Debugging in VSCode

**Setup:**

1. **Create launch.json:**

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Genkit Dev Server",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "console": "integratedTerminal",
      "internalConsoleOptions": "neverOpen",
      "env": {
        "NODE_ENV": "development"
      }
    },
    {
      "type": "node",
      "request": "launch",
      "name": "Debug Specific Flow",
      "program": "${workspaceFolder}/node_modules/.bin/genkit",
      "args": ["flow:run", "myFlowName", "--input", "{}"],
      "console": "integratedTerminal"
    }
  ]
}
```

2. **Set Breakpoints:**
   - Click left margin in code
   - Or press `F9`

3. **Start Debugging:**
   - Press `F5`
   - Or click Run → Start Debugging

4. **Debug Features:**
   - Step through code
   - Inspect variables
   - View call stack
   - Evaluate expressions

---

## Building Your First AI Application

Let's build a complete application from scratch.

### Project: Smart Customer Support Bot

**Features:**
- Chatbot with conversation history
- RAG for knowledge base search
- Tool to check order status
- Sentiment analysis

### Step 1: Initialize Project

```bash
# Using Claude Code
/genkit-init customer-support-bot

# Choices:
# - Language: TypeScript
# - Provider: Claude
# - Template: Blank (we'll build from scratch)
```

### Step 2: Project Structure

```
customer-support-bot/
├── src/
│   ├── flows/
│   │   ├── chat.ts           # Main chat flow
│   │   ├── knowledge.ts      # Knowledge base RAG
│   │   └── sentiment.ts      # Sentiment analysis
│   ├── tools/
│   │   └── orders.ts         # Order status tool
│   ├── data/
│   │   └── knowledge-base.json
│   └── index.ts
├── tests/
├── .env
└── genkit.config.ts
```

### Step 3: Configuration

**genkit.config.ts:**
```typescript
import { defineConfig } from '@genkit-ai/core';
import { anthropic } from '@genkit-ai/anthropic';
import { dotprompt } from '@genkit-ai/dotprompt';

export default defineConfig({
  plugins: [
    anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    }),
    dotprompt(),
  ],
});
```

**.env:**
```bash
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
DATABASE_URL=postgresql://localhost/orders
```

### Step 4: Build Order Status Tool

**src/tools/orders.ts:**
```typescript
import { defineTool } from '@genkit-ai/flow';
import { z } from 'zod';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export const getOrderStatusTool = defineTool(
  {
    name: 'getOrderStatus',
    description: 'Get the status of a customer order by order number',
    inputSchema: z.object({
      orderNumber: z.string().regex(/^ORD-\d{6}$/, 'Invalid order format'),
    }),
    outputSchema: z.object({
      orderNumber: z.string(),
      status: z.enum(['pending', 'processing', 'shipped', 'delivered', 'cancelled']),
      items: z.array(z.object({
        name: z.string(),
        quantity: z.number(),
      })),
      estimatedDelivery: z.string().optional(),
      trackingNumber: z.string().optional(),
    }),
  },
  async (input) => {
    // Query database
    const order = await prisma.order.findUnique({
      where: { orderNumber: input.orderNumber },
      include: { items: true },
    });

    if (!order) {
      throw new Error(`Order ${input.orderNumber} not found`);
    }

    return {
      orderNumber: order.orderNumber,
      status: order.status,
      items: order.items.map(item => ({
        name: item.name,
        quantity: item.quantity,
      })),
      estimatedDelivery: order.estimatedDelivery?.toISOString(),
      trackingNumber: order.trackingNumber || undefined,
    };
  }
);
```

### Step 5: Build Knowledge Base RAG

**src/flows/knowledge.ts:**
```typescript
import { defineFlow } from '@genkit-ai/flow';
import { claude35Sonnet } from '@genkit-ai/anthropic';
import { embed, retrieve } from '@genkit-ai/ai';
import { z } from 'zod';

export const knowledgeSearchFlow = defineFlow(
  {
    name: 'knowledgeSearch',
    inputSchema: z.object({
      question: z.string(),
    }),
    outputSchema: z.object({
      answer: z.string(),
      sources: z.array(z.object({
        title: z.string(),
        category: z.string(),
      })),
      confidence: z.number(),
    }),
  },
  async (input) => {
    // Generate embeddings
    const embedding = await embed({
      embedder: 'textembedding-gecko',
      content: input.question,
    });

    // Search knowledge base
    const docs = await retrieve({
      retriever: 'knowledgeBase',
      query: embedding,
      options: { limit: 3 },
    });

    // Build context
    const context = docs
      .map(doc => `Category: ${doc.metadata.category}\nQ: ${doc.metadata.question}\nA: ${doc.content}`)
      .join('\n\n---\n\n');

    // Generate answer
    const result = await claude35Sonnet.generate({
      prompt: `You are a helpful customer support agent.

Knowledge Base:
${context}

Customer Question: ${input.question}

Provide a clear, friendly answer based on the knowledge base. If the answer isn't in the knowledge base, say "I'll need to escalate this to a human agent."`,
      config: {
        temperature: 0.3,
        maxOutputTokens: 512,
      },
    });

    // Calculate confidence
    const avgScore = docs.reduce((sum, doc) => sum + (doc.score || 0), 0) / docs.length;

    return {
      answer: result.text,
      sources: docs.map(doc => ({
        title: doc.metadata.title,
        category: doc.metadata.category,
      })),
      confidence: avgScore,
    };
  }
);
```

### Step 6: Build Sentiment Analysis

**src/flows/sentiment.ts:**
```typescript
import { defineFlow } from '@genkit-ai/flow';
import { claude35Sonnet } from '@genkit-ai/anthropic';
import { z } from 'zod';

export const sentimentAnalysisFlow = defineFlow(
  {
    name: 'sentimentAnalysis',
    inputSchema: z.object({
      message: z.string(),
    }),
    outputSchema: z.object({
      sentiment: z.enum(['positive', 'neutral', 'negative', 'urgent']),
      score: z.number().min(-1).max(1),
      escalate: z.boolean(),
      reasoning: z.string(),
    }),
  },
  async (input) => {
    const result = await claude35Sonnet.generate({
      prompt: `Analyze the sentiment of this customer message:

"${input.message}"

Respond in JSON format:
{
  "sentiment": "positive" | "neutral" | "negative" | "urgent",
  "score": -1 to 1 (where -1 is very negative, 1 is very positive),
  "escalate": true if this should be escalated to a manager,
  "reasoning": "brief explanation"
}`,
      config: {
        temperature: 0.1,
        maxOutputTokens: 256,
      },
    });

    // Parse JSON response
    const analysis = JSON.parse(result.text);

    return {
      sentiment: analysis.sentiment,
      score: analysis.score,
      escalate: analysis.escalate,
      reasoning: analysis.reasoning,
    };
  }
);
```

### Step 7: Build Main Chat Flow

**src/flows/chat.ts:**
```typescript
import { defineFlow } from '@genkit-ai/flow';
import { claude35Sonnet } from '@genkit-ai/anthropic';
import { z } from 'zod';
import { getOrderStatusTool } from '../tools/orders';
import { knowledgeSearchFlow } from './knowledge';
import { sentimentAnalysisFlow } from './sentiment';

export const chatFlow = defineFlow(
  {
    name: 'chat',
    inputSchema: z.object({
      message: z.string(),
      conversationHistory: z.array(z.object({
        role: z.enum(['user', 'assistant']),
        content: z.string(),
      })).optional(),
    }),
    outputSchema: z.object({
      response: z.string(),
      sentiment: z.object({
        sentiment: z.string(),
        escalate: z.boolean(),
      }),
      toolsUsed: z.array(z.string()),
    }),
  },
  async (input) => {
    // Step 1: Analyze sentiment
    const sentiment = await sentimentAnalysisFlow({
      message: input.message,
    });

    // Step 2: Build conversation context
    const history = input.conversationHistory || [];
    const conversationContext = history
      .map(msg => `${msg.role === 'user' ? 'Customer' : 'Agent'}: ${msg.content}`)
      .join('\n');

    // Step 3: Generate response with tools
    const systemPrompt = `You are a friendly and helpful customer support agent.

${conversationContext ? `Conversation History:\n${conversationContext}\n` : ''}

You have access to tools:
- getOrderStatus: Check order status by order number

Guidelines:
- Be friendly and professional
- Use tools when needed
- If the question is about products or policies, search the knowledge base first
- Always confirm order numbers before looking them up
- If you can't help, offer to escalate to a human agent

Customer: ${input.message}

Agent:`;

    const result = await claude35Sonnet.generate({
      prompt: systemPrompt,
      tools: [getOrderStatusTool],
      config: {
        temperature: 0.7,
        maxOutputTokens: 512,
      },
    });

    // Step 4: Check if we need to search knowledge base
    let finalResponse = result.text;
    const toolsUsed: string[] = result.toolCalls?.map(tc => tc.name) || [];

    // If no tools were used and it seems like a policy question
    if (toolsUsed.length === 0 && (
      input.message.toLowerCase().includes('how') ||
      input.message.toLowerCase().includes('what') ||
      input.message.toLowerCase().includes('why')
    )) {
      try {
        const knowledge = await knowledgeSearchFlow({
          question: input.message,
        });

        if (knowledge.confidence > 0.7) {
          finalResponse = knowledge.answer;
          toolsUsed.push('knowledgeSearch');
        }
      } catch (error) {
        console.error('Knowledge search failed:', error);
      }
    }

    return {
      response: finalResponse,
      sentiment: {
        sentiment: sentiment.sentiment,
        escalate: sentiment.escalate,
      },
      toolsUsed,
    };
  }
);
```

### Step 8: Entry Point

**src/index.ts:**
```typescript
import { genkit } from '@genkit-ai/core';
import { chatFlow } from './flows/chat';
import { knowledgeSearchFlow } from './flows/knowledge';
import { sentimentAnalysisFlow } from './flows/sentiment';

// Initialize Genkit
const ai = genkit({});

// Register flows
ai.defineFlow(chatFlow);
ai.defineFlow(knowledgeSearchFlow);
ai.defineFlow(sentimentAnalysisFlow);

// Start server
if (require.main === module) {
  ai.startFlowServer({
    port: 3000,
    cors: {
      origin: '*',
    },
  });

  console.log('Customer Support Bot running on http://localhost:3000');
}

export { ai };
```

### Step 9: Add Tests

**tests/chat.test.ts:**
```typescript
import { describe, it, expect } from 'vitest';
import { chatFlow } from '../src/flows/chat';

describe('Chat Flow', () => {
  it('should greet the user', async () => {
    const result = await chatFlow({
      message: 'Hello!',
    });

    expect(result.response).toBeTruthy();
    expect(result.sentiment.sentiment).toBe('positive');
  });

  it('should use order status tool', async () => {
    const result = await chatFlow({
      message: 'What is the status of order ORD-123456?',
    });

    expect(result.toolsUsed).toContain('getOrderStatus');
  });

  it('should search knowledge base', async () => {
    const result = await chatFlow({
      message: 'What is your return policy?',
    });

    expect(result.toolsUsed).toContain('knowledgeSearch');
  });

  it('should escalate negative sentiment', async () => {
    const result = await chatFlow({
      message: 'This is unacceptable! I demand a refund immediately!',
    });

    expect(result.sentiment.escalate).toBe(true);
    expect(result.sentiment.sentiment).toMatch(/negative|urgent/);
  });
});
```

### Step 10: Run and Test

```bash
# Install dependencies
npm install

# Start development server
npm run dev
# or
/genkit-run

# Open Developer UI
# http://localhost:4000

# Run tests
npm test
```

### Step 11: Deploy

```bash
# Deploy to Cloud Run
/genkit-deploy cloud-run

# Or Firebase
/genkit-deploy firebase
```

---

**[Continue to Part 2: Advanced Patterns, Testing, Deployment, Best Practices...]**

---

## Quick Reference

### Common Commands

```bash
# Project Setup
genkit init my-project
cd my-project
npm install

# Development
genkit start -- npm run dev
genkit flow:run flowName '{"input": "value"}'

# Testing
npm test
genkit eval:flow flowName

# Deployment
genkit deploy firebase
genkit deploy cloud-run

# Utilities
genkit --help
genkit config list
genkit --version
```

### Essential Code Patterns

**Define a Flow:**
```typescript
export const myFlow = defineFlow({
  name: 'myFlow',
  inputSchema: z.object({ input: z.string() }),
  outputSchema: z.object({ output: z.string() }),
}, async (input) => {
  // Implementation
  return { output: 'result' };
});
```

**Generate with AI:**
```typescript
const result = await claude35Sonnet.generate({
  prompt: 'Your prompt here',
  config: {
    temperature: 0.7,
    maxOutputTokens: 1024,
  },
});
```

**Define a Tool:**
```typescript
export const myTool = defineTool({
  name: 'myTool',
  description: 'Description',
  inputSchema: z.object({ param: z.string() }),
  outputSchema: z.object({ result: z.any() }),
}, async (input) => {
  // Implementation
  return { result: null };
});
```

---

**Document Version:** 1.0
**Last Updated:** October 2025
**Total Pages:** 90+

*This is Part 1 of the Developer Guide. Continue to the remaining sections for complete coverage.*
