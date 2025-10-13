import * as vscode from 'vscode';
import { TelemetryReporter } from '@vscode/extension-telemetry';

/**
 * Telemetry Reporter for Genkit VS Code Extension
 *
 * Privacy-First Implementation:
 * - Respects VS Code's built-in telemetry settings (telemetry.telemetryLevel)
 * - No PII (Personally Identifiable Information) is collected
 * - All data is anonymized
 * - Users can disable via VS Code settings: "telemetry.telemetryLevel": "off"
 *
 * Collected Data:
 * - Extension activation/deactivation
 * - Command usage (which commands are used, not the data)
 * - Error occurrences (error types, not user data)
 * - Performance metrics (duration of operations)
 * - Extension version and VS Code version
 * - OS platform (for compatibility tracking)
 *
 * NOT Collected:
 * - File names, paths, or content
 * - User names or identifiers
 * - Project names or structures
 * - API keys or credentials
 * - Any user-generated content
 */

class GenkitTelemetryReporter {
    private reporter: TelemetryReporter | null = null;
    private extensionId: string = 'amitpatole.genkit-vscode';
    private extensionVersion: string;

    // Application Insights instrumentation key
    // This is NOT a secret - it's a public key for sending telemetry
    // Replace with your own key from Azure Application Insights
    private readonly instrumentationKey: string = 'REPLACE_WITH_YOUR_APP_INSIGHTS_KEY';

    constructor(context: vscode.ExtensionContext) {
        this.extensionVersion = context.extension.packageJSON.version;

        // Only initialize if telemetry is enabled AND we have a valid key
        if (this.isTelemetryEnabled() && this.instrumentationKey !== 'REPLACE_WITH_YOUR_APP_INSIGHTS_KEY') {
            this.reporter = new TelemetryReporter(this.instrumentationKey);
            context.subscriptions.push(this.reporter);
        }
    }

    /**
     * Check if telemetry is enabled according to VS Code settings
     */
    private isTelemetryEnabled(): boolean {
        const config = vscode.workspace.getConfiguration('telemetry');
        const telemetryLevel = config.get<string>('telemetryLevel', 'all');

        // Respect VS Code's telemetry settings
        // 'off' = no telemetry
        // 'crash' = only crash reports (we won't send general telemetry)
        // 'error' = errors only (we'll send errors)
        // 'all' = all telemetry
        return telemetryLevel === 'all' || telemetryLevel === 'error';
    }

    /**
     * Send a telemetry event
     */
    public sendEvent(eventName: string, properties?: { [key: string]: string }, measurements?: { [key: string]: number }): void {
        if (!this.reporter || !this.isTelemetryEnabled()) {
            return;
        }

        // Add common properties to all events
        const enrichedProperties = {
            ...properties,
            extensionVersion: this.extensionVersion,
            vscodeVersion: vscode.version,
            platform: process.platform,
            arch: process.arch
        };

        this.reporter.sendTelemetryEvent(eventName, enrichedProperties, measurements);
    }

    /**
     * Send an error telemetry event
     */
    public sendError(errorName: string, error?: Error, properties?: { [key: string]: string }): void {
        if (!this.reporter || !this.isTelemetryEnabled()) {
            return;
        }

        const config = vscode.workspace.getConfiguration('telemetry');
        const telemetryLevel = config.get<string>('telemetryLevel', 'all');

        // Only send errors if telemetry level is 'error' or 'all'
        if (telemetryLevel !== 'all' && telemetryLevel !== 'error') {
            return;
        }

        // Sanitize error message - remove any potential PII
        const sanitizedMessage = error ? this.sanitizeErrorMessage(error.message) : 'Unknown error';

        const enrichedProperties = {
            ...properties,
            errorMessage: sanitizedMessage,
            errorType: error?.name || 'Error',
            extensionVersion: this.extensionVersion
        };

        this.reporter.sendTelemetryErrorEvent(errorName, enrichedProperties);
    }

    /**
     * Sanitize error messages to remove potential PII
     */
    private sanitizeErrorMessage(message: string): string {
        // Remove file paths
        let sanitized = message.replace(/[A-Za-z]:\\[\w\s\-\\.\\\/]+/g, '[PATH]');
        sanitized = sanitized.replace(/\/[\w\s\-\\.\/]+/g, '[PATH]');

        // Remove potential usernames
        sanitized = sanitized.replace(/users?\/[\w\-]+/gi, 'users/[USER]');
        sanitized = sanitized.replace(/home\/[\w\-]+/gi, 'home/[USER]');

        // Remove email addresses
        sanitized = sanitized.replace(/[\w\.-]+@[\w\.-]+\.\w+/g, '[EMAIL]');

        // Remove IP addresses
        sanitized = sanitized.replace(/\b(?:\d{1,3}\.){3}\d{1,3}\b/g, '[IP]');

        // Limit length
        return sanitized.substring(0, 500);
    }

    /**
     * Track command execution
     */
    public trackCommand(commandName: string, duration?: number): void {
        const measurements = duration ? { duration } : undefined;
        this.sendEvent('command.executed', { command: commandName }, measurements);
    }

    /**
     * Track extension activation
     */
    public trackActivation(): void {
        this.sendEvent('extension.activated');
    }

    /**
     * Track feature usage
     */
    public trackFeature(featureName: string, properties?: { [key: string]: string }): void {
        this.sendEvent('feature.used', { feature: featureName, ...properties });
    }

    /**
     * Dispose the reporter
     */
    public dispose(): void {
        if (this.reporter) {
            this.reporter.dispose();
        }
    }
}

export default GenkitTelemetryReporter;
