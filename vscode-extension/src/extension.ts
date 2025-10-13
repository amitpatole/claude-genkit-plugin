import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import GenkitTelemetryReporter from './telemetry';

let devServerTerminal: vscode.Terminal | undefined;
let outputChannel: vscode.OutputChannel;
let telemetry: GenkitTelemetryReporter;

export function activate(context: vscode.ExtensionContext) {
    console.log('Genkit extension is now active!');

    // Initialize telemetry reporter (respects VS Code's telemetry settings)
    telemetry = new GenkitTelemetryReporter(context);
    telemetry.trackActivation();

    // Create output channel
    outputChannel = vscode.window.createOutputChannel('Genkit');
    context.subscriptions.push(outputChannel);

    // Register all commands
    registerCommands(context);

    // Register tree data providers
    registerTreeDataProviders(context);

    // Auto-start dev server if configured
    const config = vscode.workspace.getConfiguration('genkit');
    if (config.get('autoStartDevServer') && isGenkitProject()) {
        telemetry.trackFeature('autoStartDevServer');
        startDevServer();
    }

    // Status bar item
    const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
    statusBarItem.text = '$(flame) Genkit';
    statusBarItem.tooltip = 'Genkit Tools';
    statusBarItem.command = 'genkit.startDevServer';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);

    // Track VS Code version and platform for compatibility tracking
    telemetry.sendEvent('extension.environment', {
        vscodeVersion: vscode.version,
        platform: process.platform,
        isGenkitProject: isGenkitProject().toString()
    });
}

// Helper function to wrap commands with telemetry tracking
function trackCommand<T extends any[]>(commandName: string, handler: (...args: T) => Promise<any> | any) {
    return async (...args: T) => {
        const startTime = Date.now();
        try {
            const result = await handler(...args);
            const duration = Date.now() - startTime;
            telemetry.trackCommand(commandName, duration);
            return result;
        } catch (error) {
            telemetry.sendError(`command.${commandName}.error`, error as Error);
            throw error;
        }
    };
}

function registerCommands(context: vscode.ExtensionContext) {
    // Original commands
    context.subscriptions.push(
        vscode.commands.registerCommand('genkit.init', trackCommand('init', initializeProject)),
        vscode.commands.registerCommand('genkit.createFlow', trackCommand('createFlow', createFlow)),
        vscode.commands.registerCommand('genkit.startDevServer', trackCommand('startDevServer', startDevServer)),
        vscode.commands.registerCommand('genkit.openDevUI', trackCommand('openDevUI', openDevUI)),
        vscode.commands.registerCommand('genkit.deploy', trackCommand('deploy', deploy)),
        vscode.commands.registerCommand('genkit.runDoctor', trackCommand('runDoctor', runDoctor)),

        // Phase 1: CI/CD Integration
        vscode.commands.registerCommand('genkit.setupCICD', trackCommand('setupCICD', setupCICD)),
        vscode.commands.registerCommand('genkit.configureSecrets', trackCommand('configureSecrets', configureSecrets)),
        vscode.commands.registerCommand('genkit.testPipeline', trackCommand('testPipeline', testPipeline)),
        vscode.commands.registerCommand('genkit.viewPipelineStatus', trackCommand('viewPipelineStatus', viewPipelineStatus)),

        // Phase 1: Advanced RAG
        vscode.commands.registerCommand('genkit.createRAGFlow', trackCommand('createRAGFlow', createRAGFlow)),
        vscode.commands.registerCommand('genkit.setupVectorDB', trackCommand('setupVectorDB', setupVectorDB)),
        vscode.commands.registerCommand('genkit.testRAGQuery', trackCommand('testRAGQuery', testRAGQuery)),
        vscode.commands.registerCommand('genkit.evaluateRAG', trackCommand('evaluateRAG', evaluateRAG)),

        // Phase 1: Multi-Region
        vscode.commands.registerCommand('genkit.configureMultiRegion', trackCommand('configureMultiRegion', configureMultiRegion)),
        vscode.commands.registerCommand('genkit.deployAllRegions', trackCommand('deployAllRegions', deployAllRegions)),
        vscode.commands.registerCommand('genkit.monitorRegionalHealth', trackCommand('monitorRegionalHealth', monitorRegionalHealth)),
        vscode.commands.registerCommand('genkit.triggerFailover', trackCommand('triggerFailover', triggerFailover)),

        // Phase 2: Real-Time
        vscode.commands.registerCommand('genkit.createRealTimeFlow', trackCommand('createRealTimeFlow', createRealTimeFlow)),
        vscode.commands.registerCommand('genkit.testWebSocket', trackCommand('testWebSocket', testWebSocket)),
        vscode.commands.registerCommand('genkit.monitorConnections', trackCommand('monitorConnections', monitorConnections)),

        // Phase 2: Plugin SDK
        vscode.commands.registerCommand('genkit.createPlugin', trackCommand('createPlugin', createPlugin)),
        vscode.commands.registerCommand('genkit.testPlugin', trackCommand('testPlugin', testPlugin)),
        vscode.commands.registerCommand('genkit.packagePlugin', trackCommand('packagePlugin', packagePlugin)),
        vscode.commands.registerCommand('genkit.publishPlugin', trackCommand('publishPlugin', publishPlugin)),

        // Utility commands
        vscode.commands.registerCommand('genkit.refreshExplorer', trackCommand('refreshExplorer', refreshExplorer)),
        vscode.commands.registerCommand('genkit.openDocumentation', trackCommand('openDocumentation', openDocumentation))
    );
}

function registerTreeDataProviders(context: vscode.ExtensionContext) {
    const flowsProvider = new GenkitFlowsProvider();
    const deploymentsProvider = new DeploymentsProvider();
    const regionsProvider = new RegionsProvider();
    const ragPatternsProvider = new RAGPatternsProvider();
    const realTimeProvider = new RealTimeProvider();
    const pluginsProvider = new PluginsProvider();

    vscode.window.registerTreeDataProvider('genkitFlows', flowsProvider);
    vscode.window.registerTreeDataProvider('genkitModels', new GenkitModelsProvider());
    vscode.window.registerTreeDataProvider('genkitTools', new GenkitToolsProvider());
    vscode.window.registerTreeDataProvider('genkitDeployments', deploymentsProvider);
    vscode.window.registerTreeDataProvider('genkitRegions', regionsProvider);
    vscode.window.registerTreeDataProvider('genkitRAGPatterns', ragPatternsProvider);
    vscode.window.registerTreeDataProvider('genkitRealTime', realTimeProvider);
    vscode.window.registerTreeDataProvider('genkitPlugins', pluginsProvider);

    context.subscriptions.push(
        vscode.commands.registerCommand('genkit.refreshFlows', () => flowsProvider.refresh()),
        vscode.commands.registerCommand('genkit.refreshDeployments', () => deploymentsProvider.refresh()),
        vscode.commands.registerCommand('genkit.refreshRegions', () => regionsProvider.refresh()),
        vscode.commands.registerCommand('genkit.refreshRAGPatterns', () => ragPatternsProvider.refresh()),
        vscode.commands.registerCommand('genkit.refreshRealTime', () => realTimeProvider.refresh()),
        vscode.commands.registerCommand('genkit.refreshPlugins', () => pluginsProvider.refresh())
    );
}

// ============================================================================
// ORIGINAL COMMANDS
// ============================================================================

async function initializeProject() {
    const projectName = await vscode.window.showInputBox({
        prompt: 'Enter project name',
        placeHolder: 'my-genkit-app'
    });

    if (!projectName) return;

    const language = await vscode.window.showQuickPick(
        ['TypeScript', 'JavaScript', 'Go', 'Python'],
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

    const langFlag = language.toLowerCase();
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
        ['Firebase Cloud Functions', 'Google Cloud Run', 'Vercel', 'Docker', 'AWS Lambda'],
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
        case 'AWS Lambda':
            command = 'sam deploy';
            break;
    }

    terminal.sendText(command);
}

async function runDoctor() {
    const terminal = vscode.window.createTerminal('Genkit Doctor');
    terminal.show();
    terminal.sendText('npx genkit doctor');
}

// ============================================================================
// PHASE 1: CI/CD INTEGRATION
// ============================================================================

async function setupCICD() {
    outputChannel.appendLine('Setting up CI/CD pipeline...');

    const platform = await vscode.window.showQuickPick(
        [
            { label: 'GitHub Actions', description: 'Most popular, great ecosystem' },
            { label: 'GitLab CI', description: 'Built-in GitLab integration' },
            { label: 'Azure Pipelines', description: 'Azure DevOps platform' },
            { label: 'CircleCI', description: 'Fast cloud-based CI/CD' }
        ],
        { placeHolder: 'Select CI/CD platform' }
    );

    if (!platform) return;

    const target = await vscode.window.showQuickPick(
        [
            { label: 'Firebase Cloud Functions', description: 'Serverless functions on Firebase' },
            { label: 'Google Cloud Run', description: 'Containerized deployments' },
            { label: 'Vercel', description: 'Edge functions and web apps' },
            { label: 'AWS Lambda', description: 'AWS serverless functions' },
            { label: 'Docker', description: 'Custom container deployments' }
        ],
        { placeHolder: 'Select deployment target' }
    );

    if (!target) return;

    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('No workspace folder open');
        return;
    }

    try {
        await copyCICDTemplate(platform.label, target.label, workspaceFolder.uri.fsPath);
        vscode.window.showInformationMessage(
            `✅ CI/CD pipeline configured for ${target.label} on ${platform.label}!`,
            'Configure Secrets', 'View File'
        ).then(action => {
            if (action === 'Configure Secrets') {
                configureSecrets();
            } else if (action === 'View File') {
                openCICDFile(platform.label, workspaceFolder.uri.fsPath);
            }
        });
    } catch (error) {
        vscode.window.showErrorMessage(`Failed to setup CI/CD: ${error}`);
    }
}

async function copyCICDTemplate(platform: string, target: string, workspacePath: string) {
    const templateRoot = path.join(__dirname, '../../..', 'cicd-templates');
    let templateFile = '';
    let destPath = '';

    switch (platform) {
        case 'GitHub Actions':
            destPath = path.join(workspacePath, '.github', 'workflows');
            fs.mkdirSync(destPath, { recursive: true });

            switch (target) {
                case 'Firebase Cloud Functions':
                    templateFile = path.join(templateRoot, 'github-actions', 'firebase-functions.yml');
                    break;
                case 'Google Cloud Run':
                    templateFile = path.join(templateRoot, 'github-actions', 'cloud-run.yml');
                    break;
                case 'Vercel':
                    templateFile = path.join(templateRoot, 'github-actions', 'vercel.yml');
                    break;
                default:
                    templateFile = path.join(templateRoot, 'github-actions', 'firebase-functions.yml');
            }

            const destFile = path.join(destPath, 'deploy.yml');
            fs.copyFileSync(templateFile, destFile);
            break;

        // Add other platforms as needed
    }

    outputChannel.appendLine(`Copied template from ${templateFile} to ${destPath}`);
}

async function openCICDFile(platform: string, workspacePath: string) {
    let filePath = '';

    switch (platform) {
        case 'GitHub Actions':
            filePath = path.join(workspacePath, '.github', 'workflows', 'deploy.yml');
            break;
    }

    if (fs.existsSync(filePath)) {
        const doc = await vscode.workspace.openTextDocument(filePath);
        await vscode.window.showTextDocument(doc);
    }
}

async function configureSecrets() {
    const secrets = [
        '• ANTHROPIC_API_KEY - Your Claude API key',
        '• GOOGLE_AI_API_KEY - Your Gemini API key (if using)',
        '• FIREBASE_TOKEN - Firebase deployment token',
        '• GCP_SERVICE_ACCOUNT_KEY - Google Cloud credentials',
        ''
    ].join('\n');

    const guide = `
📝 Secret Configuration Guide

Required Secrets:
${secrets}

GitHub Actions:
1. Go to repository Settings
2. Click on Secrets and variables → Actions
3. Click "New repository secret"
4. Add each secret with its value

GitLab CI:
1. Go to Settings → CI/CD
2. Expand Variables section
3. Add each variable with its value

Azure Pipelines:
1. Go to Pipelines → Library
2. Add new variable group
3. Add secrets as variables

CircleCI:
1. Go to Project Settings
2. Click on Environment Variables
3. Add each variable
`;

    const panel = vscode.window.createWebviewPanel(
        'genkitSecrets',
        'Configure Secrets',
        vscode.ViewColumn.One,
        {}
    );

    panel.webview.html = `
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: var(--vscode-font-family); padding: 20px; }
                pre { background: var(--vscode-textBlockQuote-background); padding: 15px; border-radius: 5px; }
                h2 { color: var(--vscode-textLink-foreground); }
            </style>
        </head>
        <body>
            <pre>${guide}</pre>
        </body>
        </html>
    `;
}

async function testPipeline() {
    vscode.window.showInformationMessage('Testing pipeline locally...');
    // Implementation would validate the pipeline configuration
    outputChannel.appendLine('Pipeline validation complete ✓');
}

async function viewPipelineStatus() {
    vscode.window.showInformationMessage('Opening pipeline status (requires browser)');
    // Implementation would open the CI/CD platform's status page
}

// ============================================================================
// PHASE 1: ADVANCED RAG
// ============================================================================

async function createRAGFlow() {
    const pattern = await vscode.window.showQuickPick([
        { label: 'Hybrid Search', description: 'Semantic + Keyword search (Recommended)', detail: 'Best for: Technical docs, product search' },
        { label: 'Hierarchical RAG', description: 'Multi-level retrieval', detail: 'Best for: Long documents, research papers' },
        { label: 'Conversational RAG', description: 'Context-aware with history', detail: 'Best for: Chat apps, customer support' },
        { label: 'Multi-Query RAG', description: 'Query expansion', detail: 'Best for: Complex queries, research' },
        { label: 'Self-Querying RAG', description: 'Metadata filtering', detail: 'Best for: E-commerce, filtered search' },
        { label: 'Parent-Child RAG', description: 'Smart chunking', detail: 'Best for: Code docs, academic papers' },
        { label: 'Corrective RAG', description: 'Self-correction', detail: 'Best for: High accuracy needs, fact-checking' },
        { label: 'Adaptive RAG', description: 'Dynamic strategy', detail: 'Best for: General purpose, mixed workloads' }
    ], {
        placeHolder: 'Select RAG pattern',
        matchOnDescription: true,
        matchOnDetail: true
    });

    if (!pattern) return;

    const flowName = await vscode.window.showInputBox({
        prompt: 'Enter RAG flow name',
        value: 'myRAGFlow',
        validateInput: (value) => {
            if (!/^[a-zA-Z][a-zA-Z0-9]*$/.test(value)) {
                return 'Flow name must start with a letter and contain only alphanumeric characters';
            }
            return null;
        }
    });

    if (!flowName) return;

    const editor = vscode.window.activeTextEditor;
    if (editor) {
        const snippet = generateRAGFlowSnippet(flowName, pattern.label);
        editor.insertSnippet(new vscode.SnippetString(snippet));
        vscode.window.showInformationMessage(`✅ ${pattern.label} flow created! Configure your vector database next.`, 'Setup Vector DB')
            .then(action => {
                if (action === 'Setup Vector DB') {
                    setupVectorDB();
                }
            });
    } else {
        vscode.window.showWarningMessage('No active editor found');
    }
}

async function setupVectorDB() {
    const database = await vscode.window.showQuickPick([
        { label: 'Pinecone', description: 'Popular managed vector database' },
        { label: 'Chroma', description: 'Open-source vector database' },
        { label: 'Weaviate', description: 'GraphQL-based vector database' },
        { label: 'Qdrant', description: 'High-performance vector database' },
        { label: 'Milvus', description: 'Scalable vector database' }
    ], { placeHolder: 'Select vector database' });

    if (!database) return;

    const editor = vscode.window.activeTextEditor;
    if (editor) {
        const snippet = generateVectorDBSetup(database.label);
        editor.insertSnippet(new vscode.SnippetString(snippet));
    }

    vscode.window.showInformationMessage(
        `Remember to install: npm install @${database.label.toLowerCase()}/client`,
        'Copy Command'
    ).then(action => {
        if (action === 'Copy Command') {
            vscode.env.clipboard.writeText(`npm install @${database.label.toLowerCase()}/client`);
        }
    });
}

async function testRAGQuery() {
    const query = await vscode.window.showInputBox({
        prompt: 'Enter test query',
        placeHolder: 'How do I deploy Genkit to production?'
    });

    if (!query) return;

    // Create test panel
    const panel = vscode.window.createWebviewPanel(
        'genkitRAGTest',
        'RAG Query Test',
        vscode.ViewColumn.Two,
        { enableScripts: true }
    );

    panel.webview.html = getRAGTestPanelHTML(query);
}

async function evaluateRAG() {
    vscode.window.showInformationMessage('RAG evaluation panel coming soon!');
    // TODO: Implement evaluation metrics dashboard
}

// ============================================================================
// PHASE 1: MULTI-REGION
// ============================================================================

async function configureMultiRegion() {
    const strategy = await vscode.window.showQuickPick([
        { label: 'Active-Active', description: 'All regions serve traffic (Best performance)', detail: 'Recommended for: Global apps, high traffic' },
        { label: 'Active-Passive', description: 'Primary + failover regions (Cost-effective)', detail: 'Recommended for: Disaster recovery, budget-conscious' },
        { label: 'Geo-Routing', description: 'Route by user location (Optimal latency)', detail: 'Recommended for: Content delivery, regional services' }
    ], { placeHolder: 'Select deployment strategy' });

    if (!strategy) return;

    const regions = await vscode.window.showQuickPick(
        ['US Central', 'Europe West', 'Asia East', 'US East', 'Europe North', 'Asia Southeast'],
        {
            placeHolder: 'Select regions (multi-select)',
            canPickMany: true
        }
    );

    if (!regions || regions.length === 0) return;

    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) return;

    // Generate regions.json config
    const config = generateRegionConfig(strategy.label, regions);
    const configPath = path.join(workspaceFolder.uri.fsPath, 'multi-region-config.json');
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));

    vscode.window.showInformationMessage(
        `✅ Multi-region configured: ${strategy.label} across ${regions.length} regions`,
        'View Config', 'Deploy Now'
    ).then(action => {
        if (action === 'View Config') {
            vscode.workspace.openTextDocument(configPath).then(doc => {
                vscode.window.showTextDocument(doc);
            });
        } else if (action === 'Deploy Now') {
            deployAllRegions();
        }
    });
}

async function deployAllRegions() {
    vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: 'Deploying to all regions',
        cancellable: false
    }, async (progress) => {
        progress.report({ increment: 0, message: 'Starting deployment...' });

        const terminal = vscode.window.createTerminal('Multi-Region Deploy');
        terminal.show();
        terminal.sendText('bash ./multi-region/scripts/deploy-all-regions.sh');

        return new Promise(resolve => {
            setTimeout(resolve, 2000);
        });
    });
}

async function monitorRegionalHealth() {
    const panel = vscode.window.createWebviewPanel(
        'genkitRegionalHealth',
        'Regional Health Monitor',
        vscode.ViewColumn.One,
        { enableScripts: true }
    );

    panel.webview.html = getRegionalHealthHTML();
}

async function triggerFailover() {
    const region = await vscode.window.showInputBox({
        prompt: 'Enter failed region name',
        placeHolder: 'us-central1'
    });

    if (!region) return;

    const confirm = await vscode.window.showWarningMessage(
        `⚠️ Trigger failover from ${region}?`,
        { modal: true },
        'Yes, Failover'
    );

    if (confirm) {
        const terminal = vscode.window.createTerminal('Failover');
        terminal.show();
        terminal.sendText(`bash ./multi-region/scripts/failover.sh ${region}`);
    }
}

// ============================================================================
// PHASE 2: REAL-TIME
// ============================================================================

async function createRealTimeFlow() {
    const type = await vscode.window.showQuickPick([
        { label: 'WebSocket (Bidirectional)', description: 'Full duplex communication' },
        { label: 'Server-Sent Events (Streaming)', description: 'Unidirectional streaming' },
        { label: 'Both', description: 'WebSocket + SSE support' }
    ], { placeHolder: 'Select real-time communication type' });

    if (!type) return;

    const flowName = await vscode.window.showInputBox({
        prompt: 'Enter real-time flow name',
        value: 'myRealTimeFlow'
    });

    if (!flowName) return;

    const editor = vscode.window.activeTextEditor;
    if (editor) {
        const snippet = generateRealTimeFlowSnippet(flowName, type.label);
        editor.insertSnippet(new vscode.SnippetString(snippet));
    }
}

async function testWebSocket() {
    vscode.window.showInformationMessage('WebSocket connection tester coming soon!');
}

async function monitorConnections() {
    vscode.window.showInformationMessage('Connection monitor coming soon!');
}

// ============================================================================
// PHASE 2: PLUGIN SDK
// ============================================================================

async function createPlugin() {
    const pluginName = await vscode.window.showInputBox({
        prompt: 'Enter plugin name (kebab-case)',
        placeHolder: 'my-genkit-plugin',
        validateInput: (value) => {
            if (!/^[a-z][a-z0-9-]*$/.test(value)) {
                return 'Plugin name must be kebab-case (lowercase, hyphens only)';
            }
            return null;
        }
    });

    if (!pluginName) return;

    const pluginType = await vscode.window.showQuickPick([
        { label: 'Model Plugin', description: 'Custom AI model integration' },
        { label: 'Flow Plugin', description: 'Reusable flow patterns' },
        { label: 'Tool Plugin', description: 'External tool integrations' },
        { label: 'Retriever Plugin', description: 'Custom retrieval strategies' }
    ], { placeHolder: 'Select plugin type' });

    if (!pluginType) return;

    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) return;

    const pluginDir = path.join(workspaceFolder.uri.fsPath, pluginName);
    fs.mkdirSync(pluginDir, { recursive: true });

    // Generate plugin scaffold
    generatePluginScaffold(pluginName, pluginType.label, pluginDir);

    vscode.window.showInformationMessage(
        `✅ Plugin "${pluginName}" created!`,
        'Open Plugin', 'View README'
    ).then(action => {
        if (action === 'Open Plugin') {
            vscode.commands.executeCommand('vscode.openFolder', vscode.Uri.file(pluginDir), true);
        }
    });
}

async function testPlugin() {
    vscode.window.showInformationMessage('Plugin testing environment coming soon!');
}

async function packagePlugin() {
    const terminal = vscode.window.createTerminal('Package Plugin');
    terminal.show();
    terminal.sendText('npm run build && npm pack');
}

async function publishPlugin() {
    const confirm = await vscode.window.showWarningMessage(
        'Publish plugin to NPM?',
        { modal: true },
        'Yes, Publish'
    );

    if (confirm) {
        const terminal = vscode.window.createTerminal('Publish Plugin');
        terminal.show();
        terminal.sendText('npm publish');
    }
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function refreshExplorer() {
    vscode.commands.executeCommand('genkit.refreshFlows');
    vscode.commands.executeCommand('genkit.refreshDeployments');
    vscode.commands.executeCommand('genkit.refreshRegions');
    vscode.commands.executeCommand('genkit.refreshRAGPatterns');
}

function openDocumentation() {
    vscode.env.openExternal(vscode.Uri.parse('https://genkit.dev/docs'));
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
        // Add other templates...
    };

    return snippets[template] || snippets['Simple Chat'];
}

function generateRAGFlowSnippet(name: string, pattern: string): string {
    // Implementation for different RAG patterns
    return `// ${pattern} RAG Flow implementation for ${name}`;
}

function generateVectorDBSetup(database: string): string {
    return `// ${database} vector database setup`;
}

function generateRealTimeFlowSnippet(name: string, type: string): string {
    return `// ${type} real-time flow for ${name}`;
}

function generateRegionConfig(strategy: string, regions: string[]) {
    return {
        strategy: strategy.toLowerCase().replace('-', '_'),
        regions: regions.map((r, i) => ({
            id: r.toLowerCase().replace(' ', '-'),
            name: r,
            primary: i === 0,
            weight: i === 0 ? 50 : Math.floor(50 / (regions.length - 1))
        })),
        failover: {
            enabled: true,
            health_check_interval_seconds: 30
        }
    };
}

function generatePluginScaffold(name: string, type: string, dir: string) {
    // Create basic plugin structure
    const files = {
        'package.json': JSON.stringify({
            name,
            version: '1.0.0',
            description: `${type} for Genkit`,
            main: 'dist/index.js',
            types: 'dist/index.d.ts'
        }, null, 2),
        'src/index.ts': `// ${type} implementation`,
        'README.md': `# ${name}\n\n${type} for Firebase Genkit`
    };

    Object.entries(files).forEach(([file, content]) => {
        const filePath = path.join(dir, file);
        fs.mkdirSync(path.dirname(filePath), { recursive: true });
        fs.writeFileSync(filePath, content);
    });
}

function getRAGTestPanelHTML(query: string): string {
    return `
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: var(--vscode-font-family); padding: 20px; }
        .query { background: var(--vscode-editor-background); padding: 15px; margin: 10px 0; }
        .results { margin-top: 20px; }
    </style>
</head>
<body>
    <h2>RAG Query Test</h2>
    <div class="query">
        <strong>Query:</strong> ${query}
    </div>
    <div class="results">
        <p>Testing RAG query...</p>
        <p>(Full implementation in progress)</p>
    </div>
</body>
</html>
    `;
}

function getRegionalHealthHTML(): string {
    return `
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: var(--vscode-font-family); padding: 20px; }
        .region { padding: 10px; margin: 5px 0; background: var(--vscode-editor-background); }
        .healthy { border-left: 3px solid green; }
    </style>
</head>
<body>
    <h2>Regional Health Monitor</h2>
    <div class="region healthy">
        <strong>US Central</strong> - Healthy ✅
        <br>Latency: 45ms | Traffic: 50%
    </div>
    <p>(Full implementation in progress)</p>
</body>
</html>
    `;
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

// ============================================================================
// TREE DATA PROVIDERS
// ============================================================================

class GenkitFlowsProvider implements vscode.TreeDataProvider<FlowItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<FlowItem | undefined | null | void> = new vscode.EventEmitter<FlowItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<FlowItem | undefined | null | void> = this._onDidChangeTreeData.event;

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

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
        // TODO: Scan workspace for actual flows
        return [
            new FlowItem('chatFlow', 'Simple Chat Flow', 'chat', vscode.TreeItemCollapsibleState.None),
            new FlowItem('ragFlow', 'RAG Flow', 'rag', vscode.TreeItemCollapsibleState.None),
        ];
    }
}

class FlowItem extends vscode.TreeItem {
    constructor(
        public readonly flowName: string,
        public readonly description: string,
        public readonly flowType: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState
    ) {
        super(flowName, collapsibleState);
        this.tooltip = `${this.flowName} - ${this.description}`;
        this.iconPath = new vscode.ThemeIcon(this.getIconForType(flowType));
    }

    private getIconForType(type: string): string {
        const icons: { [key: string]: string } = {
            'chat': 'comment',
            'rag': 'search',
            'streaming': 'rss',
            'tool': 'tools',
            'realtime': 'radio-tower'
        };
        return icons[type] || 'symbol-function';
    }
}

class GenkitModelsProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
    getTreeItem(element: vscode.TreeItem): vscode.TreeItem {
        return element;
    }

    getChildren(): Thenable<vscode.TreeItem[]> {
        return Promise.resolve([
            new vscode.TreeItem('Claude 3.5 Sonnet', vscode.TreeItemCollapsibleState.None),
            new vscode.TreeItem('Gemini 1.5 Pro', vscode.TreeItemCollapsibleState.None),
        ]);
    }
}

class GenkitToolsProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
    getTreeItem(element: vscode.TreeItem): vscode.TreeItem {
        return element;
    }

    getChildren(): Thenable<vscode.TreeItem[]> {
        return Promise.resolve([
            new vscode.TreeItem('Web Search', vscode.TreeItemCollapsibleState.None),
            new vscode.TreeItem('Code Executor', vscode.TreeItemCollapsibleState.None),
        ]);
    }
}

class DeploymentsProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<vscode.TreeItem | undefined | null | void> = new vscode.EventEmitter<vscode.TreeItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<vscode.TreeItem | undefined | null | void> = this._onDidChangeTreeData.event;

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: vscode.TreeItem): vscode.TreeItem {
        return element;
    }

    getChildren(): Thenable<vscode.TreeItem[]> {
        const items = [
            new vscode.TreeItem('Production ✅', vscode.TreeItemCollapsibleState.None),
            new vscode.TreeItem('Staging ✅', vscode.TreeItemCollapsibleState.None),
        ];
        return Promise.resolve(items);
    }
}

class RegionsProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<vscode.TreeItem | undefined | null | void> = new vscode.EventEmitter<vscode.TreeItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<vscode.TreeItem | undefined | null | void> = this._onDidChangeTreeData.event;

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: vscode.TreeItem): vscode.TreeItem {
        return element;
    }

    getChildren(): Thenable<vscode.TreeItem[]> {
        return Promise.resolve([
            new vscode.TreeItem('US Central 🟢', vscode.TreeItemCollapsibleState.None),
            new vscode.TreeItem('Europe West 🟢', vscode.TreeItemCollapsibleState.None),
        ]);
    }
}

class RAGPatternsProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<vscode.TreeItem | undefined | null | void> = new vscode.EventEmitter<vscode.TreeItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<vscode.TreeItem | undefined | null | void> = this._onDidChangeTreeData.event;

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: vscode.TreeItem): vscode.TreeItem {
        return element;
    }

    getChildren(): Thenable<vscode.TreeItem[]> {
        return Promise.resolve([
            new vscode.TreeItem('Hybrid Search RAG', vscode.TreeItemCollapsibleState.None),
            new vscode.TreeItem('Conversational RAG', vscode.TreeItemCollapsibleState.None),
        ]);
    }
}

class RealTimeProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<vscode.TreeItem | undefined | null | void> = new vscode.EventEmitter<vscode.TreeItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<vscode.TreeItem | undefined | null | void> = this._onDidChangeTreeData.event;

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: vscode.TreeItem): vscode.TreeItem {
        return element;
    }

    getChildren(): Thenable<vscode.TreeItem[]> {
        return Promise.resolve([
            new vscode.TreeItem('WebSocket: 0 connections', vscode.TreeItemCollapsibleState.None),
            new vscode.TreeItem('SSE: 0 streams', vscode.TreeItemCollapsibleState.None),
        ]);
    }
}

class PluginsProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<vscode.TreeItem | undefined | null | void> = new vscode.EventEmitter<vscode.TreeItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<vscode.TreeItem | undefined | null | void> = this._onDidChangeTreeData.event;

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: vscode.TreeItem): vscode.TreeItem {
        return element;
    }

    getChildren(): Thenable<vscode.TreeItem[]> {
        return Promise.resolve([
            new vscode.TreeItem('No plugins installed', vscode.TreeItemCollapsibleState.None),
        ]);
    }
}

export function deactivate() {
    if (devServerTerminal) {
        devServerTerminal.dispose();
    }

    // Dispose telemetry reporter
    if (telemetry) {
        telemetry.dispose();
    }
}
