# VS Code Extension Screenshots & Visual Guide

This document describes the visual features and UI elements of the Genkit VS Code Extension. While we don't have actual screenshots yet, this guide describes what users will see.

---

## 1. Command Palette Integration

**What it looks like:**
```
╔═══════════════════════════════════════════════════════════════╗
║  > Genkit: [type command name]                               ║
╠═══════════════════════════════════════════════════════════════╣
║  🚀 Genkit: Setup CI/CD Pipeline                             ║
║  ✨ Genkit: Create RAG Flow                                  ║
║  🌍 Genkit: Configure Multi-Region Deployment                ║
║  ⚡ Genkit: Create Real-Time Flow                            ║
║  🔌 Genkit: Create Genkit Plugin                             ║
║  📊 Genkit: Open Developer UI                                 ║
║  🚢 Genkit: Deploy to Production                              ║
╚═══════════════════════════════════════════════════════════════╝
```

**How to use:**
- Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
- Type "Genkit"
- See all 34 commands organized by category
- Select command and follow interactive prompts

---

## 2. Genkit Explorer Sidebar

**What it looks like:**
```
╔═══════════════════════════════════════════════════════════════╗
║ GENKIT EXPLORER                                         [⟳]  ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║ ▶ FLOWS                                                      ║
║   └─ 📄 chatFlow (Chat)                                      ║
║   └─ 🔍 ragFlow (RAG)                                        ║
║   └─ ⚡ streamingFlow (Streaming)                            ║
║                                                               ║
║ ▶ DEPLOYMENTS                                                ║
║   └─ ✅ Production (v1.1.0) - Healthy                        ║
║   └─ ⏸  Staging (v1.0.5) - Idle                             ║
║                                                               ║
║ ▶ REGIONS                                                    ║
║   └─ 🌎 us-central1 (Primary) - 45% traffic                 ║
║   └─ 🌍 europe-west1 - 30% traffic                          ║
║   └─ 🌏 asia-east1 - 25% traffic                            ║
║                                                               ║
║ ▶ RAG PATTERNS                                               ║
║   └─ 🔍 Hybrid Search - 1,250 docs                          ║
║   └─ 📚 Hierarchical RAG - 834 docs                         ║
║   └─ 💬 Conversational RAG - Active                         ║
║                                                               ║
║ ▶ REAL-TIME                                                  ║
║   └─ 🔌 WebSocket - 42 connections                          ║
║   └─ 📡 Server-Sent Events - 18 streams                     ║
║                                                               ║
║ ▶ PLUGINS                                                    ║
║   └─ 📦 @genkit-ai/anthropic (v1.2.0)                       ║
║   └─ 📦 @genkit-ai/googleai (v1.1.5)                        ║
║   └─ 📦 my-custom-plugin (v1.0.0)                           ║
╚═══════════════════════════════════════════════════════════════╝
```

**Features:**
- Real-time status updates
- Click to navigate to code
- Right-click for context menu
- Refresh button updates all views
- Color-coded status indicators

---

## 3. CI/CD Setup Wizard

**Step 1 - Platform Selection:**
```
╔═══════════════════════════════════════════════════════════════╗
║  Setup CI/CD Pipeline                                        ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Select CI/CD platform:                                      ║
║                                                               ║
║  ▶ GitHub Actions                                            ║
║    Most popular, great ecosystem, easy setup                 ║
║                                                               ║
║  ○ GitLab CI                                                 ║
║    Built-in GitLab integration                               ║
║                                                               ║
║  ○ Azure Pipelines                                           ║
║    Microsoft ecosystem, Windows support                      ║
║                                                               ║
║  ○ CircleCI                                                  ║
║    Fast builds, Docker support                               ║
╚═══════════════════════════════════════════════════════════════╝
```

**Step 2 - Deployment Target:**
```
╔═══════════════════════════════════════════════════════════════╗
║  Setup CI/CD Pipeline                                        ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Select deployment target:                                   ║
║                                                               ║
║  ▶ Firebase Cloud Functions                                  ║
║    Serverless functions on Firebase                          ║
║                                                               ║
║  ○ Google Cloud Run                                          ║
║    Containerized serverless on GCP                           ║
║                                                               ║
║  ○ Vercel                                                    ║
║    Zero-config, global CDN                                   ║
║                                                               ║
║  ○ AWS Lambda                                                ║
║    Serverless on AWS                                         ║
║                                                               ║
║  ○ Docker                                                    ║
║    Self-hosted containers                                    ║
╚═══════════════════════════════════════════════════════════════╝
```

**Result:**
```
✅ Created .github/workflows/deploy.yml
✅ Next steps:
   1. Configure secrets in GitHub repository settings
   2. Push changes to trigger pipeline
   3. Monitor deployment in Actions tab
```

---

## 4. RAG Flow Creation Wizard

**Pattern Selection:**
```
╔═══════════════════════════════════════════════════════════════╗
║  Create RAG Flow                                             ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Choose RAG pattern:                                         ║
║                                                               ║
║  ▶ Hybrid Search (Recommended)                               ║
║    Semantic + Keyword search                                 ║
║    Best for: Technical docs, product search                  ║
║                                                               ║
║  ○ Hierarchical RAG                                          ║
║    Multi-level retrieval                                     ║
║    Best for: Long documents, research papers                 ║
║                                                               ║
║  ○ Conversational RAG                                        ║
║    Context-aware with conversation history                   ║
║    Best for: Chatbots, customer support                      ║
║                                                               ║
║  ○ Multi-Query RAG                                           ║
║    Query expansion for better coverage                       ║
║    Best for: Complex queries, research                       ║
║                                                               ║
║  [View all 8 patterns →]                                     ║
╚═══════════════════════════════════════════════════════════════╝
```

**Code Generation:**
```typescript
// ✅ Generated: src/flows/hybridSearchRAG.ts

import { defineFlow } from '@genkit-ai/flow';
import { z } from 'zod';

export const hybridSearchRAG = defineFlow(
  {
    name: 'hybridSearchRAG',
    inputSchema: z.object({
      query: z.string(),
      semanticWeight: z.number().default(0.7),
      keywordWeight: z.number().default(0.3),
    }),
    outputSchema: z.object({
      answer: z.string(),
      sources: z.array(z.object({
        id: z.string(),
        score: z.number()
      })),
    }),
  },
  async (input) => {
    // Semantic search
    const semanticResults = await vectorStore.search(input.query);

    // Keyword search
    const keywordResults = await fullTextSearch.search(input.query);

    // Combine and rerank
    const combined = rerank(semanticResults, keywordResults, {
      semanticWeight: input.semanticWeight,
      keywordWeight: input.keywordWeight,
    });

    const answer = await model.generate({
      context: combined.map(r => r.content).join('\n\n'),
      question: input.query,
    });

    return { answer: answer.text, sources: combined };
  }
);
```

---

## 5. Multi-Region Configuration

**Region Selection:**
```
╔═══════════════════════════════════════════════════════════════╗
║  Configure Multi-Region Deployment                           ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Step 1: Choose deployment strategy                          ║
║                                                               ║
║  ▶ Active-Active                                             ║
║    All regions serve traffic (Best performance)              ║
║    Traffic split: Automatic load balancing                   ║
║                                                               ║
║  ○ Active-Passive                                            ║
║    Primary + failover regions (Cost-effective)               ║
║    Failover: Automatic on health check failure              ║
║                                                               ║
║  ○ Geo-Routing                                               ║
║    Route by user location (Optimal latency)                  ║
║    Routing: Based on geographic proximity                    ║
╚═══════════════════════════════════════════════════════════════╝
```

**Traffic Configuration:**
```
╔═══════════════════════════════════════════════════════════════╗
║  Multi-Region Traffic Distribution                           ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  🌎 us-central1 (Primary)                                    ║
║  ████████████████░░░░░░ 40%   [Adjust]                       ║
║                                                               ║
║  🌍 europe-west1                                             ║
║  ████████████░░░░░░░░░░ 35%   [Adjust]                       ║
║                                                               ║
║  🌏 asia-east1                                               ║
║  ██████░░░░░░░░░░░░░░░░ 25%   [Adjust]                       ║
║                                                               ║
║  Total: 100%                                                 ║
║                                                               ║
║  [Apply Configuration]  [Cancel]                             ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 6. Code Snippets in Action

**Typing `grag-hybrid` in editor:**
```typescript
// Before (cursor position: |)
|

// Type: grag-hybrid [Tab]

// After:
import { defineFlow } from '@genkit-ai/flow';
import { z } from 'zod';

export const hybridSearchRAG = defineFlow(
  {
    name: 'hybridSearchRAG',
    inputSchema: z.object({
      query: z.string(),
      semanticWeight: z.number().default(0.7),
      keywordWeight: z.number().default(0.3),
    }),
    outputSchema: z.object({
      answer: z.string(),
      sources: z.array(z.object({ id: z.string(), score: z.number() })),
    }),
  },
  async (input) => {
    // [Tab through placeholders to customize]
    |
  }
);
```

**IntelliSense showing available snippets:**
```
╔═══════════════════════════════════════════════════════════════╗
║  g|                                                           ║
╠═══════════════════════════════════════════════════════════════╣
║  📄 gflow - Create a new Genkit flow                         ║
║  🔧 gtool - Create a new Genkit tool                         ║
║  🔍 grag - Create a RAG flow with Genkit                     ║
║  🔍 grag-hybrid - Hybrid Search RAG (semantic + keyword)     ║
║  📚 grag-hierarchical - Hierarchical RAG (multi-level)       ║
║  💬 grag-conversational - Conversational RAG (context-aware) ║
║  🔌 gwebsocket - WebSocket real-time flow                    ║
║  📡 gsse - Server-Sent Events streaming flow                 ║
║  🧩 gplugin-model - Custom model plugin                      ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 7. Real-Time Connection Monitoring

**WebSocket Dashboard (Webview):**
```
╔═══════════════════════════════════════════════════════════════╗
║  Real-Time Connection Monitor                          [✕]  ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  🔌 WebSocket Connections: 42 active                         ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   ║
║  📈 Peak: 87 | Avg: 35                                       ║
║                                                               ║
║  Recent Connections:                                         ║
║  ┌────────────────────────────────────────────────────────┐  ║
║  │ ID: ws_a1b2c3  │ Connected: 2m ago  │ Latency: 45ms  │  ║
║  │ ID: ws_d4e5f6  │ Connected: 5m ago  │ Latency: 32ms  │  ║
║  │ ID: ws_g7h8i9  │ Connected: 8m ago  │ Latency: 28ms  │  ║
║  └────────────────────────────────────────────────────────┘  ║
║                                                               ║
║  📡 Server-Sent Events: 18 active streams                    ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   ║
║  📊 Messages sent: 1,247 | Throughput: 42 msg/sec           ║
║                                                               ║
║  [Refresh]  [Export Logs]  [Close All]                      ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 8. Plugin Creation Flow

**Plugin Type Selection:**
```
╔═══════════════════════════════════════════════════════════════╗
║  Create Genkit Plugin                                        ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  What type of plugin do you want to create?                  ║
║                                                               ║
║  ▶ Model Plugin                                              ║
║    Integrate a custom AI model                               ║
║                                                               ║
║  ○ Flow Plugin                                               ║
║    Create reusable flow templates                            ║
║                                                               ║
║  ○ Tool Plugin                                               ║
║    Add custom tools for AI agents                            ║
║                                                               ║
║  ○ Retriever Plugin                                          ║
║    Custom vector/document retrieval                          ║
╚═══════════════════════════════════════════════════════════════╝
```

**Generated Structure:**
```
✅ Created plugin: my-custom-model/

my-custom-model/
├── package.json
├── README.md
├── tsconfig.json
├── src/
│   ├── index.ts
│   └── model.ts
└── __tests__/
    └── model.test.ts

✅ Next steps:
   1. cd my-custom-model
   2. npm install
   3. Implement your model in src/model.ts
   4. Test with: npm test
   5. Publish with: npm publish
```

---

## 9. Settings Panel

**VS Code Settings UI:**
```
╔═══════════════════════════════════════════════════════════════╗
║  Settings > Extensions > Genkit                              ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  CI/CD                                                       ║
║  ┌────────────────────────────────────────────────────────┐  ║
║  │ Platform: [github-actions ▼]                           │  ║
║  │ Auto Setup: [✓] Enable automatic CI/CD setup          │  ║
║  └────────────────────────────────────────────────────────┘  ║
║                                                               ║
║  RAG Configuration                                           ║
║  ┌────────────────────────────────────────────────────────┐  ║
║  │ Default Pattern: [hybrid-search ▼]                     │  ║
║  │ Vector Database: [pinecone ▼]                          │  ║
║  │ Embedding Model: [text-embedding-004]                  │  ║
║  └────────────────────────────────────────────────────────┘  ║
║                                                               ║
║  Multi-Region Deployment                                     ║
║  ┌────────────────────────────────────────────────────────┐  ║
║  │ Enable Multi-Region: [✓]                               │  ║
║  │ Default Target: [cloud-run ▼]                          │  ║
║  │ Regions: [us-central1, europe-west1, asia-east1]      │  ║
║  └────────────────────────────────────────────────────────┘  ║
║                                                               ║
║  Explorer                                                    ║
║  ┌────────────────────────────────────────────────────────┐  ║
║  │ Show Metrics: [✓]                                      │  ║
║  │ Auto Refresh: [✓]                                      │  ║
║  │ Refresh Interval: [5000] ms                            │  ║
║  └────────────────────────────────────────────────────────┘  ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 10. Status Bar Integration

**Bottom status bar shows:**
```
╔═══════════════════════════════════════════════════════════════╗
║ TypeScript ✓ | Genkit: 3 flows | Dev Server: ● Running      ║
║                                                         4:35 PM║
╚═══════════════════════════════════════════════════════════════╝
```

**Click "Dev Server: ● Running" for menu:**
```
╔═══════════════════════════════════════════════════════════════╗
║  Genkit Dev Server                                           ║
╠═══════════════════════════════════════════════════════════════╣
║  Status: Running on port 4000                                ║
║                                                               ║
║  ○ Open Developer UI                                         ║
║  ○ View Server Logs                                          ║
║  ● Stop Server                                               ║
║  ○ Restart Server                                            ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## Visual Design Elements

### Color Scheme
- **Primary**: Google Blue (#4285F4)
- **Success**: Green (#34A853)
- **Warning**: Yellow (#FBBC04)
- **Error**: Red (#EA4335)
- **Text**: VS Code theme colors

### Icons
- 🚀 Deployments
- 🔍 RAG/Search
- 🌍 Regions/Global
- ⚡ Real-time
- 🔌 Plugins/Connections
- 📊 Analytics/Metrics
- ✅ Success states
- ⚠️  Warnings

### UI Patterns
- **Interactive wizards** with step-by-step guidance
- **Tree views** with expand/collapse
- **Webview panels** for complex visualizations
- **Quick Pick menus** for selections
- **Input boxes** with validation
- **Progress notifications** for long-running tasks

---

## User Experience Highlights

1. **Discoverability**: All commands in Command Palette with clear categories
2. **Guidance**: Interactive wizards guide users through complex setups
3. **Feedback**: Progress notifications and status indicators
4. **Flexibility**: Multiple ways to accomplish tasks (commands, sidebar, snippets)
5. **Performance**: Lazy loading, efficient refreshes, caching
6. **Accessibility**: Keyboard shortcuts, screen reader support
7. **Customization**: Extensive settings for personalization

---

## Coming in v1.2.0

Future visual enhancements:
- **Interactive dashboards** with charts and graphs
- **Visual RAG debugger** showing query → retrieval → generation flow
- **Pipeline visualization** with step-by-step execution view
- **Live preview** of WebSocket/SSE connections
- **Metric timelines** with historical data

---

**Note**: Actual screenshots will be captured and added when the extension is running in VS Code.
