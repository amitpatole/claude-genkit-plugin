# Plugin SDK for Genkit Extensions

Build and publish your own Genkit plugins with this comprehensive SDK.

## 🎯 Overview

The Plugin SDK provides everything you need to create, test, and publish Genkit plugins:
- 🔧 Plugin development framework
- 📦 Packaging and distribution tools
- 🧪 Testing utilities
- 📚 Documentation generators
- 🚀 Publishing workflow

## 🚀 Quick Start

### Create a New Plugin

```bash
npx create-genkit-plugin my-awesome-plugin
cd my-awesome-plugin
npm install
npm run dev
```

### Plugin Structure

```
my-awesome-plugin/
├── src/
│   ├── index.ts          # Main entry point
│   ├── flows/            # Custom flows
│   ├── models/           # AI model integrations
│   ├── tools/            # Custom tools
│   └── utils/            # Helper functions
├── tests/
│   ├── flows.test.ts
│   └── integration.test.ts
├── package.json
├── tsconfig.json
└── README.md
```

## 📝 Plugin Template

```typescript
// src/index.ts
import { GenkitPlugin, definePlugin } from '@genkit-ai/core';

export const myPlugin = definePlugin({
  name: 'my-awesome-plugin',
  version: '1.0.0',
  description: 'My awesome Genkit plugin',

  // Initialize plugin
  async initialize(config) {
    // Setup code
  },

  // Register flows
  flows: [
    // Your flows
  ],

  // Register models
  models: [
    // Your models
  ],

  // Register tools
  tools: [
    // Your tools
  ],
});

export default myPlugin;
```

## 🔧 Plugin Types

### 1. Model Plugins
Integrate new AI models:

```typescript
import { defineModel } from '@genkit-ai/ai/model';

export const customModel = defineModel({
  name: 'custom/model-v1',
  label: 'Custom Model',
  supports: {
    multiturn: true,
    media: false,
    tools: true,
    systemRole: true,
  },
}, async (request) => {
  // Model implementation
  return {
    candidates: [{
      index: 0,
      finishReason: 'stop',
      message: { role: 'model', content: [] },
    }],
    usage: { inputTokens: 0, outputTokens: 0 },
  };
});
```

### 2. Flow Plugins
Add reusable flows:

```typescript
import { defineFlow } from '@genkit-ai/flow';

export const customFlow = defineFlow({
  name: 'custom-flow',
  inputSchema: z.object({ /* ... */ }),
  outputSchema: z.object({ /* ... */ }),
}, async (input) => {
  // Flow logic
});
```

### 3. Tool Plugins
Create custom tools:

```typescript
import { defineTool } from '@genkit-ai/ai/tool';

export const customTool = defineTool({
  name: 'customTool',
  description: 'Does something useful',
  inputSchema: z.object({ /* ... */ }),
  outputSchema: z.object({ /* ... */ }),
}, async (input) => {
  // Tool implementation
});
```

### 4. Retriever Plugins
Add data sources:

```typescript
import { defineRetriever } from '@genkit-ai/ai/retriever';

export const customRetriever = defineRetriever({
  name: 'customRetriever',
  configSchema: z.object({ /* ... */ }),
}, async (query, options) => {
  // Retrieval logic
  return { documents: [] };
});
```

## 📦 Publishing

### 1. Prepare Package

```json
{
  "name": "@your-scope/genkit-plugin-awesome",
  "version": "1.0.0",
  "description": "My awesome Genkit plugin",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "keywords": ["genkit", "plugin", "ai"],
  "peerDependencies": {
    "@genkit-ai/core": "^0.5.0"
  }
}
```

### 2. Build and Test

```bash
npm run build
npm test
npm run lint
```

### 3. Publish to npm

```bash
npm publish --access public
```

## 🧪 Testing

### Unit Tests

```typescript
import { runFlow } from '@genkit-ai/flow';
import { customFlow } from '../src';

describe('Custom Flow', () => {
  it('should process input correctly', async () => {
    const result = await runFlow(customFlow, { input: 'test' });
    expect(result).toBeDefined();
  });
});
```

### Integration Tests

```typescript
import { configureGenkit } from '@genkit-ai/core';
import { myPlugin } from '../src';

describe('Plugin Integration', () => {
  beforeAll(() => {
    configureGenkit({ plugins: [myPlugin()] });
  });

  it('should register flows', async () => {
    // Test flow registration
  });
});
```

## 📚 Documentation

### Auto-Generate Docs

```bash
npm run docs:generate
```

### Documentation Template

```markdown
# My Awesome Plugin

## Installation
\`\`\`bash
npm install @your-scope/genkit-plugin-awesome
\`\`\`

## Usage
\`\`\`typescript
import { myPlugin } from '@your-scope/genkit-plugin-awesome';
import { configureGenkit } from '@genkit-ai/core';

configureGenkit({
  plugins: [myPlugin({ /* config */ })],
});
\`\`\`

## API Reference
<!-- Auto-generated -->
```

## 🔐 Best Practices

### 1. Configuration
- Use environment variables
- Validate config with Zod
- Provide sensible defaults

### 2. Error Handling
- Catch and wrap errors
- Provide helpful error messages
- Log errors appropriately

### 3. Testing
- Unit test all functions
- Integration test plugin lifecycle
- Test error cases

### 4. Documentation
- Clear README
- API documentation
- Usage examples

### 5. Versioning
- Follow semver
- Document breaking changes
- Maintain changelog

## 📊 Plugin Marketplace

Submit your plugin to the marketplace:

```bash
npm run plugin:submit
```

### Submission Checklist
- [ ] Tests passing
- [ ] Documentation complete
- [ ] README with examples
- [ ] LICENSE file
- [ ] package.json metadata
- [ ] TypeScript types
- [ ] Peer dependencies specified

## 🎨 Examples

### Complete Plugin Example

```typescript
import { GenkitPlugin } from '@genkit-ai/core';
import { defineFlow } from '@genkit-ai/flow';
import { z } from 'zod';

export interface MyPluginConfig {
  apiKey: string;
  endpoint?: string;
}

export function myPlugin(config: MyPluginConfig): GenkitPlugin {
  if (!config.apiKey) {
    throw new Error('API key required');
  }

  const endpoint = config.endpoint || 'https://api.example.com';

  // Define flows
  const exampleFlow = defineFlow({
    name: 'example-flow',
    inputSchema: z.string(),
    outputSchema: z.string(),
  }, async (input) => {
    const response = await fetch(`${endpoint}/process`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${config.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: input }),
    });
    return response.json();
  });

  return {
    name: 'my-plugin',
    flows: [exampleFlow],
    initializer: async () => {
      // Plugin initialization
      console.log('Plugin initialized');
    },
  };
}
```

## 🆘 Troubleshooting

### Common Issues

**Plugin not loading**
- Check peer dependencies
- Verify plugin registration
- Check for initialization errors

**Type errors**
- Ensure TypeScript version compatibility
- Check @genkit-ai/core version

**Test failures**
- Mock external dependencies
- Use proper async handling
- Check test environment setup

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/amitpatole/claude-genkit-plugin/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/amitpatole/claude-genkit-plugin/discussions)
- 📧 **Email**: amit.patole@gmail.com

---

**Build amazing Genkit plugins!** 🚀
