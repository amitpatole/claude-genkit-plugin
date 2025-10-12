import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

let devServerTerminal: vscode.Terminal | undefined;

export function activate(context: vscode.ExtensionContext) {
    console.log('Genkit extension is now active!');

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('genkit.init', initializeProject),
        vscode.commands.registerCommand('genkit.createFlow', createFlow),
        vscode.commands.registerCommand('genkit.startDevServer', startDevServer),
        vscode.commands.registerCommand('genkit.openDevUI', openDevUI),
        vscode.commands.registerCommand('genkit.deploy', deploy),
        vscode.commands.registerCommand('genkit.runDoctor', runDoctor)
    );

    // Register tree data providers
    const flowsProvider = new GenkitFlowsProvider();
    vscode.window.registerTreeDataProvider('genkitFlows', flowsProvider);

    // Auto-start dev server if configured
    const config = vscode.workspace.getConfiguration('genkit');
    if (config.get('autoStartDevServer') && isGenkitProject()) {
        startDevServer();
    }

    // Status bar item
    const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
    statusBarItem.text = '$(flame) Genkit';
    statusBarItem.tooltip = 'Genkit Tools';
    statusBarItem.command = 'genkit.startDevServer';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);
}

async function initializeProject() {
    const projectName = await vscode.window.showInputBox({
        prompt: 'Enter project name',
        placeHolder: 'my-genkit-app'
    });

    if (!projectName) return;

    const language = await vscode.window.showQuickPick(
        ['TypeScript', 'JavaScript'],
        { placeHolder: 'Select language' }
    );

    if (!language) return;

    const provider = await vscode.window.showQuickPick(
        ['Anthropic Claude', 'Google Gemini', 'OpenAI GPT', 'Multiple'],
        { placeHolder: 'Select AI provider' }
    );

    if (!provider) return;

    const terminal = vscode.window.createTerminal('Genkit Init');
    terminal.show();

    const langFlag = language === 'TypeScript' ? 'typescript' : 'javascript';
    terminal.sendText(`npx genkit init ${projectName} --lang=${langFlag}`);

    vscode.window.showInformationMessage(`Initializing Genkit project: ${projectName}`);
}

async function createFlow() {
    const flowName = await vscode.window.showInputBox({
        prompt: 'Enter flow name',
        placeHolder: 'myFlow'
    });

    if (!flowName) return;

    const template = await vscode.window.showQuickPick(
        ['Simple Chat', 'RAG', 'Tool Calling', 'Multi-step', 'Streaming', 'Empty'],
        { placeHolder: 'Select flow template' }
    );

    if (!template) return;

    const editor = vscode.window.activeTextEditor;
    if (editor) {
        const snippet = generateFlowSnippet(flowName, template);
        editor.insertSnippet(new vscode.SnippetString(snippet));
    } else {
        vscode.window.showWarningMessage('No active editor found');
    }
}

async function startDevServer() {
    if (devServerTerminal) {
        devServerTerminal.dispose();
    }

    const config = vscode.workspace.getConfiguration('genkit');
    const port = config.get('devServerPort', 4000);

    devServerTerminal = vscode.window.createTerminal('Genkit Dev Server');
    devServerTerminal.show();
    devServerTerminal.sendText(`npx genkit start --port=${port}`);

    vscode.window.showInformationMessage(`Genkit dev server starting on port ${port}`);
}

async function openDevUI() {
    const config = vscode.workspace.getConfiguration('genkit');
    const port = config.get('devServerPort', 4000);
    const url = `http://localhost:${port}`;

    vscode.env.openExternal(vscode.Uri.parse(url));
}

async function deploy() {
    const platform = await vscode.window.showQuickPick(
        ['Firebase Cloud Functions', 'Google Cloud Run', 'Vercel', 'Docker'],
        { placeHolder: 'Select deployment platform' }
    );

    if (!platform) return;

    const terminal = vscode.window.createTerminal('Genkit Deploy');
    terminal.show();

    let command = '';
    switch (platform) {
        case 'Firebase Cloud Functions':
            command = 'firebase deploy --only functions';
            break;
        case 'Google Cloud Run':
            command = 'gcloud run deploy';
            break;
        case 'Vercel':
            command = 'vercel deploy';
            break;
        case 'Docker':
            command = 'docker build -t genkit-app .';
            break;
    }

    terminal.sendText(command);
}

async function runDoctor() {
    const terminal = vscode.window.createTerminal('Genkit Doctor');
    terminal.show();
    terminal.sendText('npx genkit doctor');
}

function generateFlowSnippet(name: string, template: string): string {
    const snippets: { [key: string]: string } = {
        'Simple Chat': `
import { defineFlow } from '@genkit-ai/flow';
import { z } from 'zod';

export const ${name}Flow = defineFlow(
  {
    name: '${name}',
    inputSchema: z.object({
      message: z.string(),
    }),
    outputSchema: z.string(),
  },
  async (input) => {
    // TODO: Implement your chat logic here
    return \`Response to: \${input.message}\`;
  }
);`,
        'RAG': `
import { defineFlow } from '@genkit-ai/flow';
import { z } from 'zod';

export const ${name}Flow = defineFlow(
  {
    name: '${name}',
    inputSchema: z.object({
      question: z.string(),
    }),
    outputSchema: z.object({
      answer: z.string(),
      sources: z.array(z.string()),
    }),
  },
  async (input) => {
    // TODO: Implement RAG logic
    // 1. Retrieve relevant documents
    // 2. Generate answer with context
    return {
      answer: 'Answer here',
      sources: ['source1', 'source2'],
    };
  }
);`,
        'Tool Calling': `
import { defineFlow, defineTool } from '@genkit-ai/flow';
import { z } from 'zod';

const myTool = defineTool(
  {
    name: 'myTool',
    description: 'Tool description',
    inputSchema: z.object({
      param: z.string(),
    }),
    outputSchema: z.string(),
  },
  async (input) => {
    return \`Tool result: \${input.param}\`;
  }
);

export const ${name}Flow = defineFlow(
  {
    name: '${name}',
    inputSchema: z.object({
      request: z.string(),
    }),
    outputSchema: z.string(),
  },
  async (input) => {
    // TODO: Implement tool calling logic
    return 'Response';
  }
);`,
        'Multi-step': `
import { defineFlow } from '@genkit-ai/flow';
import { z } from 'zod';

export const ${name}Flow = defineFlow(
  {
    name: '${name}',
    inputSchema: z.object({
      input: z.string(),
    }),
    outputSchema: z.object({
      result: z.string(),
    }),
  },
  async (input) => {
    // Step 1
    const step1Result = await processStep1(input.input);

    // Step 2
    const step2Result = await processStep2(step1Result);

    // Step 3
    const finalResult = await processStep3(step2Result);

    return { result: finalResult };
  }
);

async function processStep1(input: string) { return input; }
async function processStep2(input: string) { return input; }
async function processStep3(input: string) { return input; }`,
        'Streaming': `
import { defineFlow } from '@genkit-ai/flow';
import { z } from 'zod';

export const ${name}Flow = defineFlow(
  {
    name: '${name}',
    inputSchema: z.object({
      prompt: z.string(),
    }),
    outputSchema: z.string(),
    streamSchema: z.string(),
  },
  async (input, { stream }) => {
    // TODO: Implement streaming logic
    const words = input.prompt.split(' ');
    for (const word of words) {
      stream(word + ' ');
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    return 'Complete response';
  }
);`,
        'Empty': `
import { defineFlow } from '@genkit-ai/flow';
import { z } from 'zod';

export const ${name}Flow = defineFlow(
  {
    name: '${name}',
    inputSchema: z.object({
      // Define your input schema
    }),
    outputSchema: z.object({
      // Define your output schema
    }),
  },
  async (input) => {
    // Implement your flow logic here
    return {};
  }
);`
    };

    return snippets[template] || snippets['Empty'];
}

function isGenkitProject(): boolean {
    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (!workspaceFolders) return false;

    for (const folder of workspaceFolders) {
        const configPath = path.join(folder.uri.fsPath, 'genkit.config.ts');
        const configPathJs = path.join(folder.uri.fsPath, 'genkit.config.js');
        if (fs.existsSync(configPath) || fs.existsSync(configPathJs)) {
            return true;
        }
    }
    return false;
}

class GenkitFlowsProvider implements vscode.TreeDataProvider<FlowItem> {
    getTreeItem(element: FlowItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: FlowItem): Thenable<FlowItem[]> {
        if (!element) {
            return Promise.resolve(this.getFlows());
        }
        return Promise.resolve([]);
    }

    private getFlows(): FlowItem[] {
        // TODO: Scan workspace for Genkit flows
        return [
            new FlowItem('chatFlow', 'Simple Chat Flow', vscode.TreeItemCollapsibleState.None),
            new FlowItem('ragFlow', 'RAG Flow', vscode.TreeItemCollapsibleState.None),
        ];
    }
}

class FlowItem extends vscode.TreeItem {
    constructor(
        public readonly flowName: string,
        public readonly description: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState
    ) {
        super(flowName, collapsibleState);
        this.tooltip = `${this.flowName} - ${this.description}`;
        this.iconPath = new vscode.ThemeIcon('symbol-function');
    }
}

export function deactivate() {
    if (devServerTerminal) {
        devServerTerminal.dispose();
    }
}
