# Telemetry and Privacy

## Overview

The Genkit VS Code extension collects anonymized usage data to help us improve the product. **We respect your privacy** and follow VS Code's built-in telemetry preferences.

## What We Collect

### ✅ Data We DO Collect (Anonymized)

1. **Extension Usage**
   - Extension activation/deactivation events
   - Command execution (which commands, not the data)
   - Feature usage frequency
   - Extension version and VS Code version
   - Operating system and platform

2. **Performance Metrics**
   - Command execution duration
   - Operation completion times
   - Error occurrence rates

3. **Error Information**
   - Error types and categories
   - Sanitized error messages (no personal data)
   - Extension performance issues

### ❌ Data We DO NOT Collect

- ✗ File names, paths, or content
- ✗ User names or email addresses
- ✗ Project names or structures
- ✗ API keys or credentials
- ✗ IP addresses or geographic location
- ✗ Any personally identifiable information (PII)
- ✗ User-generated content or code
- ✗ Environment variables or secrets

## How to Control Telemetry

### Option 1: VS Code Settings (Recommended)

We respect VS Code's global telemetry settings. Change your preference in VS Code:

**Using Settings UI:**
1. Open Settings: `File` → `Preferences` → `Settings` (or `Code` → `Preferences` → `Settings` on Mac)
2. Search for "telemetry"
3. Set **`telemetry.telemetryLevel`** to your preference:
   - `all` - Send all telemetry (default)
   - `error` - Send error telemetry only
   - `crash` - Send crash reports only
   - `off` - Disable all telemetry

**Using settings.json:**
```json
{
  "telemetry.telemetryLevel": "off"
}
```

### Option 2: Command Line

```bash
code --telemetry-level off
```

### Option 3: Environment Variable

```bash
export VSCODE_TELEMETRY_LEVEL=off
```

## Telemetry Implementation Details

### Technology Used

- **Package**: `@vscode/extension-telemetry`
- **Backend**: Azure Application Insights (Microsoft)
- **Data Retention**: 90 days
- **Compliance**: GDPR, CCPA compliant

### Privacy Safeguards

1. **No PII Collection**: Our code explicitly sanitizes all data before sending
2. **Path Sanitization**: File paths are replaced with `[PATH]` placeholders
3. **Error Sanitization**: Error messages are scrubbed of user-specific information
4. **VS Code Integration**: Respects `telemetry.telemetryLevel` settings automatically
5. **Open Source**: Our telemetry code is publicly auditable

### Example Sanitization

**Before:**
```
Error: Cannot find file /Users/john/projects/my-app/src/index.ts
Email: john.doe@example.com sent request from 192.168.1.1
```

**After:**
```
Error: Cannot find file [PATH]
Email: [EMAIL] sent request from [IP]
```

## Telemetry Data Examples

### Extension Activation
```json
{
  "eventName": "extension.activated",
  "properties": {
    "extensionVersion": "1.1.1",
    "vscodeVersion": "1.85.0",
    "platform": "linux",
    "arch": "x64"
  }
}
```

### Command Execution
```json
{
  "eventName": "command.executed",
  "properties": {
    "command": "createRAGFlow",
    "extensionVersion": "1.1.1"
  },
  "measurements": {
    "duration": 1250
  }
}
```

### Error Reporting
```json
{
  "eventName": "command.setupCICD.error",
  "properties": {
    "errorMessage": "Failed to create directory [PATH]",
    "errorType": "FileSystemError",
    "extensionVersion": "1.1.1"
  }
}
```

## Why We Collect Telemetry

### Benefits to You

1. **Better Extension**: We fix bugs that actually affect users
2. **Feature Prioritization**: We improve features you actually use
3. **Performance**: We optimize commands you run frequently
4. **Compatibility**: We ensure support for your OS/VS Code version

### What We Learn

- Which commands are most popular
- Which features cause errors
- Performance bottlenecks
- Compatibility issues with different VS Code versions

## Data Access and Storage

### Who Has Access?

- **Developers**: Core maintainers (anonymized data only)
- **No Third Parties**: Data is never sold or shared outside Microsoft Azure
- **Your Organization**: If using managed VS Code, your IT admin may have their own telemetry policies

### Where Is Data Stored?

- **Location**: Microsoft Azure (US region)
- **Retention**: 90 days
- **Encryption**: In transit and at rest

## Transparency and Accountability

### Open Source

Our telemetry implementation is fully open source:
- [`src/telemetry.ts`](src/telemetry.ts) - Telemetry reporter class
- [`src/extension.ts`](src/extension.ts) - Integration with commands

You can audit exactly what data is collected and how it's sanitized.

### Compliance

- ✅ **GDPR** compliant (EU privacy regulation)
- ✅ **CCPA** compliant (California privacy law)
- ✅ **Microsoft Privacy Statement** compliant
- ✅ **VS Code Extension Guidelines** compliant

## Frequently Asked Questions

### Q: Is telemetry enabled by default?

A: Yes, if your VS Code telemetry setting is `all` or `error`. You can disable it anytime through VS Code settings.

### Q: Can I see what data is being sent?

A: Yes! The telemetry implementation is open source. You can also use network monitoring tools to inspect outgoing requests.

### Q: Does telemetry affect extension performance?

A: No. Telemetry is asynchronous and non-blocking. It adds negligible overhead (<1ms).

### Q: What if I don't want telemetry but still want error reporting?

A: Set `telemetry.telemetryLevel` to `error`. You'll help us fix bugs without sharing usage data.

### Q: Can I request deletion of my telemetry data?

A: Since all data is anonymized, we cannot identify individual users. However, all telemetry data is automatically deleted after 90 days.

### Q: Is telemetry required to use the extension?

A: **No!** The extension works perfectly with telemetry disabled.

## Contact

### Privacy Concerns

If you have privacy concerns or questions:
- **Email**: amit.patole@gmail.com
- **GitHub Issues**: https://github.com/amitpatole/claude-genkit-plugin/issues
- **Label**: Use the `privacy` label

### Data Deletion Requests

While data is anonymized and cannot be linked to individuals, you can:
1. Disable telemetry (see above)
2. Contact us at amit.patole@gmail.com for questions

## Changes to This Policy

We will notify users of any material changes to our telemetry practices via:
- Extension update notifications
- GitHub repository announcements
- README updates

**Last Updated**: October 13, 2025

## Summary

✅ **Your privacy is our priority**
✅ **No personal data collected**
✅ **Respects VS Code settings**
✅ **Easy to disable**
✅ **Fully transparent**
✅ **GDPR/CCPA compliant**

**Telemetry helps us build a better extension for everyone. Thank you for your support!**
