# Telemetry Setup Guide

This guide explains how to configure Application Insights for telemetry tracking in the Genkit VS Code extension.

## Overview

The extension uses Azure Application Insights to collect anonymized usage data. This is **optional** and respects VS Code's telemetry settings.

## Setup Steps

### 1. Create Azure Application Insights Resource

#### Option A: Azure Portal (Recommended)

1. Go to [Azure Portal](https://portal.azure.com)
2. Click "+ Create a resource"
3. Search for "Application Insights"
4. Click "Create"
5. Fill in details:
   - **Subscription**: Your Azure subscription
   - **Resource Group**: Create new or use existing
   - **Name**: `genkit-vscode-telemetry`
   - **Region**: Choose your region (e.g., "East US")
   - **Workspace**: Create new or use existing Log Analytics workspace
6. Click "Review + Create"
7. Click "Create"

#### Option B: Azure CLI

```bash
# Login to Azure
az login

# Create resource group (if needed)
az group create --name genkit-vscode-rg --location eastus

# Create Application Insights
az monitor app-insights component create \
  --app genkit-vscode-telemetry \
  --location eastus \
  --resource-group genkit-vscode-rg \
  --application-type web
```

### 2. Get Connection String

#### Azure Portal:

1. Go to your Application Insights resource
2. Look for "Connection String" in the Essentials section (top of page)
3. Click "Copy" icon
4. Save this connection string - you'll need it next

#### Azure CLI:

```bash
az monitor app-insights component show \
  --app genkit-vscode-telemetry \
  --resource-group genkit-vscode-rg \
  --query connectionString \
  --output tsv
```

The connection string looks like:
```
InstrumentationKey=12345678-1234-1234-1234-123456789abc;IngestionEndpoint=https://eastus-8.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus.livediagnostics.monitor.azure.com/
```

### 3. Update Extension Code

Edit `src/telemetry.ts` and replace the placeholder:

```typescript
// Replace this line:
private readonly instrumentationKey: string = 'REPLACE_WITH_YOUR_APP_INSIGHTS_KEY';

// With your connection string:
private readonly instrumentationKey: string = 'InstrumentationKey=12345678-1234-1234-1234-123456789abc;IngestionEndpoint=https://eastus-8.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus.livediagnostics.monitor.azure.com/';
```

**⚠️ Important Security Notes:**
- The connection string is PUBLIC (included in the published extension)
- This is by design for client-side telemetry
- It cannot be used to access your Azure resources
- It can only send telemetry data (write-only)
- Do NOT use server-side API keys

### 4. Test Locally

```bash
# Compile the extension
npm run compile

# Open in VS Code
code .

# Press F5 to launch Extension Development Host

# Test a command in the dev host
# Check Application Insights for data (may take 2-5 minutes)
```

### 5. View Telemetry Data

#### In Azure Portal:

1. Go to your Application Insights resource
2. Click "Logs" in the left menu
3. Run queries:

```kusto
// View all events
customEvents
| where timestamp > ago(24h)
| project timestamp, name, customDimensions
| order by timestamp desc

// View command execution
customEvents
| where name == "command.executed"
| extend command = tostring(customDimensions.command)
| summarize count() by command
| order by count_ desc

// View errors
customEvents
| where name contains "error"
| project timestamp, name, customDimensions
| order by timestamp desc

// Performance metrics
customEvents
| where name == "command.executed"
| extend command = tostring(customDimensions.command), duration = todouble(customMeasurements.duration)
| summarize avg(duration), p95=percentile(duration, 95) by command
```

#### Sample Queries:

**Most Popular Commands:**
```kusto
customEvents
| where name == "command.executed"
| where timestamp > ago(7d)
| extend command = tostring(customDimensions.command)
| summarize executions = count() by command
| order by executions desc
| take 10
```

**Error Rate:**
```kusto
customEvents
| where timestamp > ago(24h)
| summarize
    total = count(),
    errors = countif(name contains "error")
| extend errorRate = (errors * 100.0) / total
| project errorRate, total, errors
```

**Extension Activations by Platform:**
```kusto
customEvents
| where name == "extension.activated"
| extend platform = tostring(customDimensions.platform)
| summarize count() by platform
```

## Privacy & Security

### What Gets Tracked

✅ **Allowed:**
- Command names (e.g., "createRAGFlow")
- Execution duration
- Error types (sanitized)
- VS Code version
- Platform (Windows/Mac/Linux)
- Extension version

❌ **Never Tracked:**
- File paths or names
- User names or emails
- API keys or credentials
- Code content
- Project names
- IP addresses (automatically anonymized by Application Insights)

### Data Retention

Configure data retention in Azure Portal:
1. Go to Application Insights resource
2. Click "Usage and estimated costs"
3. Click "Data Retention"
4. Set retention period (default: 90 days)

### GDPR Compliance

Application Insights is GDPR compliant:
- Data is anonymized
- Users can opt-out via VS Code settings
- Data is automatically deleted after retention period
- No cross-device tracking
- No personal identifiers collected

## Cost Considerations

Application Insights pricing (as of 2025):

- **First 5 GB/month**: FREE
- **Additional data**: ~$2.30/GB

For a VS Code extension:
- Small extension (<1000 users): **FREE**
- Medium extension (1000-10000 users): **$0-5/month**
- Large extension (10000+ users): **$5-20/month**

### Cost Optimization

1. **Sampling** - Reduce data volume:
```typescript
// In src/telemetry.ts, when creating TelemetryReporter
this.reporter = new TelemetryReporter(this.instrumentationKey, undefined, {
    samplingPercentage: 50  // Only send 50% of events
});
```

2. **Daily Cap** - Set in Azure Portal:
   - Go to Application Insights
   - "Usage and estimated costs" → "Daily cap"
   - Set limit (e.g., 1 GB/day)

3. **Filter Events** - Only track important events:
```typescript
// Only track specific commands
if (importantCommands.includes(commandName)) {
    telemetry.trackCommand(commandName, duration);
}
```

## Monitoring & Alerts

### Set Up Alerts

1. Go to Application Insights
2. Click "Alerts" → "+ Create" → "Alert rule"
3. Create alerts for:
   - **High Error Rate**: > 5% errors
   - **Slow Commands**: > 5 seconds duration
   - **No Data**: No events for 24 hours

### Dashboard

Create a dashboard:
1. Go to Application Insights
2. Click "Application Dashboard"
3. Pin queries to dashboard:
   - Total users (unique sessions)
   - Command usage breakdown
   - Error rate over time
   - Performance percentiles

## Troubleshooting

### No Data Showing Up

**Check 1: Connection String**
```typescript
// Verify in src/telemetry.ts
console.log('Telemetry enabled:', this.isTelemetryEnabled());
console.log('Has key:', this.instrumentationKey !== 'REPLACE_WITH_YOUR_APP_INSIGHTS_KEY');
```

**Check 2: VS Code Telemetry**
```bash
# Check VS Code settings
code --list-flags
# Should NOT show --telemetry-level off
```

**Check 3: Network**
```bash
# Test connectivity to Application Insights
curl -I https://dc.services.visualstudio.com/v2/track
# Should return 200 or 405
```

**Check 4: Wait Time**
- Application Insights has 2-5 minute delay
- Check "Logs" not "Metrics" for recent data

### High Costs

1. Check current usage:
   ```kusto
   customEvents
   | summarize count() by bin(timestamp, 1d)
   | render timechart
   ```

2. Enable sampling (see Cost Optimization above)

3. Filter verbose events

### Privacy Concerns

- All telemetry code is in `src/telemetry.ts` (open source)
- Review sanitization in `sanitizeErrorMessage()`
- Test with PII detector:
  ```typescript
  const testMessage = "User john.doe@example.com at /home/john/project";
  console.log(this.sanitizeErrorMessage(testMessage));
  // Should output: "User [EMAIL] at [PATH]"
  ```

## Alternative: No Telemetry

To disable telemetry completely:

### Option 1: Remove from Code

Delete or comment out in `src/extension.ts`:
```typescript
// telemetry = new GenkitTelemetryReporter(context);
// telemetry.trackActivation();
```

### Option 2: Environment Variable

Set instrumentationKey to empty:
```typescript
private readonly instrumentationKey: string = '';
```

### Option 3: Leave as Placeholder

Keep the placeholder:
```typescript
private readonly instrumentationKey: string = 'REPLACE_WITH_YOUR_APP_INSIGHTS_KEY';
```

Extension will work fine without telemetry - all calls are no-ops when not configured.

## Resources

- [Application Insights Documentation](https://docs.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview)
- [VS Code Extension Telemetry](https://code.visualstudio.com/api/extension-capabilities/telemetry)
- [@vscode/extension-telemetry Package](https://www.npmjs.com/package/@vscode/extension-telemetry)
- [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)
- [GDPR Compliance](https://docs.microsoft.com/en-us/azure/azure-monitor/logs/personal-data-mgmt)

## Support

Questions about telemetry setup?
- 📧 Email: amit.patole@gmail.com
- 💬 GitHub Discussions: https://github.com/amitpatole/claude-genkit-plugin/discussions
- 🐛 Issues: https://github.com/amitpatole/claude-genkit-plugin/issues

---

**Remember**: Telemetry helps improve the extension but is **completely optional**. Users can disable it anytime via VS Code settings.
