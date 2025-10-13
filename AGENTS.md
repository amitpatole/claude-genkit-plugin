# Autonomous Agents Documentation

This repository uses **autonomous agents** that run 24/7 to manage deployments, monitor health, and maintain the codebase.

## Overview

Two primary agents operate continuously:

1. **Schedule Enforcement Agent** - Ensures all deployments occur during the approved time window
2. **Monitoring & Maintenance Agent** - Monitors health, fixes issues, and manages updates

## Agent 1: Schedule Enforcement Agent

### Purpose
Enforces strict deployment schedules to ensure all pushes, releases, and deployments occur only during the approved time window.

### Schedule
- **Runs:** Every 5 minutes (24/7)
- **Workflow:** `.github/workflows/schedule-enforcement-agent.yml`

### Deployment Window
**ALLOWED:** 10:00 PM - 8:00 AM EST
**BLOCKED:** 8:00 AM - 10:00 PM EST

### Features
- ✅ Checks all deployment workflows for schedule compliance
- ✅ Blocks deployments outside the allowed window
- ✅ Monitors recent workflow runs for violations
- ✅ Generates violation reports
- ✅ Provides real-time status updates
- ✅ Heartbeat monitoring to confirm agent is running

### Actions Taken
1. **Pre-deployment Check:** Every deployment workflow first checks if current time is within the window
2. **Block on Violation:** Exits with error code 1 if deployment attempted outside window
3. **Generate Reports:** Creates violation reports in `agent-reports/` directory
4. **Status Updates:** Updates `.github/agent-status/schedule-enforcement.txt` every 5 minutes

### How It Works
```bash
# Check if within deployment window (10 PM - 8 AM EST)
CURRENT_HOUR=$(TZ='America/New_York' date +%H)

# Hours 22-23 (10 PM - 11:59 PM) OR 0-7 (12 AM - 7:59 AM) = ALLOWED
# Hours 8-21 (8 AM - 9:59 PM) = BLOCKED

if [ "$CURRENT_HOUR" -ge 22 ] || [ "$CURRENT_HOUR" -lt 8 ]; then
  echo "✅ Within deployment window - Proceeding"
else
  echo "🚫 BLOCKED: Outside deployment window"
  exit 1
fi
```

### Modified Workflows
All deployment workflows now include schedule enforcement:
- `publish-vscode-extension.yml`
- `vscode-extension-ci.yml` (publish job)
- `vscode-extension-release.yml`

### Monitoring
Check agent status at any time:
- **Status File:** `.github/agent-status/schedule-enforcement.txt`
- **Violation Reports:** `agent-reports/violation-*.md`
- **GitHub Actions:** View runs of "Schedule Enforcement Agent (24x7)"

---

## Agent 2: Monitoring & Maintenance Agent

### Purpose
Continuously monitors the extension and plugin, automatically fixes issues, manages updates, and responds to user reports.

### Schedule
- **Runs:** Every 10 minutes (24/7)
- **Workflow:** `.github/workflows/monitoring-maintenance-agent.yml`
- **Also triggers on:** New issues, pull requests

### Features

#### 1. Health Monitoring
- ✅ Compilation checks (TypeScript → JavaScript)
- ✅ package.json validation
- ✅ Security vulnerability scanning
- ✅ Marketplace metrics tracking
- ✅ Issue/PR monitoring

#### 2. Automatic Fixes
- 🔧 **Compilation Failures:** Reinstalls dependencies, cleans build artifacts
- 🔧 **Security Vulnerabilities:** Runs `npm audit fix` automatically
- 🔧 **Outdated Dependencies:** Updates patch versions safely
- 🔧 **Known Issues:** Applies automatic fixes when patterns are detected

#### 3. Issue Management
- 💬 **Auto-responds** to bug reports with triage information
- 💬 **Auto-labels** issues (bug, enhancement, needs-triage)
- 💬 **Tracks** critical issues and alerts maintainers
- 💬 **Provides** troubleshooting guidance to users

#### 4. Feature Research
- 🔍 Tracks latest Firebase Genkit releases
- 🔍 Monitors feature requests
- 🔍 Analyzes marketplace trends
- 🔍 Identifies popular user requests

#### 5. Dependency Management
- 📦 Checks for outdated dependencies
- 📦 Auto-updates patch versions (safe updates)
- 📦 Stages updates for deployment window
- 📦 Generates update reports

### Actions Taken

#### Automatic Fixes (Staged for Deployment Window)
All automated fixes respect the deployment schedule:
```bash
CURRENT_HOUR=$(TZ='America/New_York' date +%H)
if [ "$CURRENT_HOUR" -ge 22 ] || [ "$CURRENT_HOUR" -lt 8 ]; then
  git push  # Push immediately during window
else
  echo "⏰ Staged for deployment window (10 PM - 8 AM EST)"
fi
```

#### Compilation Failure Response
```bash
1. Detects compilation failure
2. Removes node_modules and out directories
3. Reinstalls dependencies (npm install)
4. Recompiles (npm run compile)
5. If successful: Commits and pushes fix
6. If failed: Creates issue for manual review
```

#### Security Vulnerability Response
```bash
1. Detects vulnerabilities via npm audit
2. Runs npm audit fix
3. Tests compilation after fix
4. If successful: Commits and stages for deployment window
5. If failed: Creates high-priority issue
```

#### Issue Auto-Response
When a new issue is opened:
- **Bug reports:** Auto-labels, provides troubleshooting steps, triages
- **Feature requests:** Auto-labels, explains review process, gathers feedback
- **Questions:** Provides links to documentation

### Monitoring
- **Status File:** `.github/agent-status/maintenance-agent.txt`
- **Health Reports:** `agent-reports/maintenance-*.md`
- **GitHub Actions:** View runs of "Monitoring & Maintenance Agent (24x7)"

---

## Agent Status Monitoring

### Real-Time Status
Both agents update heartbeat files every run:

```bash
# Schedule Enforcement Agent
cat .github/agent-status/schedule-enforcement.txt
# Output: Schedule Enforcement Agent: ACTIVE - 2025-10-13 22:45:00 EST

# Maintenance Agent
cat .github/agent-status/maintenance-agent.txt
# Output: Monitoring & Maintenance Agent: ACTIVE - 2025-10-13 22:50:00 EST
```

### Check if Agents are Running
```bash
# View recent workflow runs
gh run list --workflow="Schedule Enforcement Agent (24x7)" --limit 5
gh run list --workflow="Monitoring & Maintenance Agent (24x7)" --limit 5
```

### View Agent Logs
```bash
# Get latest run ID
RUN_ID=$(gh run list --workflow="Schedule Enforcement Agent (24x7)" --limit 1 --json databaseId --jq '.[0].databaseId')

# View logs
gh run view $RUN_ID --log
```

---

## Schedule Configuration

### Current Schedule

| Time (EST) | Deployments | Agents Running |
|------------|-------------|----------------|
| 10:00 PM - 11:59 PM | ✅ ALLOWED | ✅ Active |
| 12:00 AM - 7:59 AM | ✅ ALLOWED | ✅ Active |
| 8:00 AM - 9:59 PM | 🚫 BLOCKED | ✅ Active |

### Modifying the Schedule

To change the deployment window, update the time check in these files:

1. `.github/workflows/schedule-enforcement-agent.yml`
2. `.github/workflows/publish-vscode-extension.yml`
3. `.github/workflows/vscode-extension-ci.yml`
4. `.github/workflows/vscode-extension-release.yml`
5. `.github/workflows/monitoring-maintenance-agent.yml`

Find this block and modify the hour checks:
```bash
CURRENT_HOUR=$(TZ='America/New_York' date +%H)

# Change these numbers to adjust window
# Currently: 22 (10 PM) to 8 (8 AM)
if [ "$CURRENT_HOUR" -ge 22 ] || [ "$CURRENT_HOUR" -lt 8 ]; then
  # ALLOWED
else
  # BLOCKED
fi
```

---

## Manual Overrides

### Force Deployment Outside Window (Emergency Only)
If you absolutely must deploy outside the schedule:

```bash
# Option 1: Workflow dispatch with manual approval
gh workflow run publish-vscode-extension.yml

# Option 2: Temporarily disable schedule check
# Edit workflow file and comment out the schedule check step
```

**⚠️ WARNING:** This should only be used for critical hotfixes!

### Disable an Agent
To temporarily disable an agent:

```bash
# Option 1: Disable via GitHub UI
# Go to: Actions → [Agent Name] → ... → Disable workflow

# Option 2: Delete/rename workflow file
mv .github/workflows/schedule-enforcement-agent.yml \
   .github/workflows/schedule-enforcement-agent.yml.disabled
```

---

## Agent Reports

### Schedule Violation Reports
Located in `agent-reports/violation-*.md`

Example:
```markdown
# Schedule Violation Report

**Generated:** 2025-10-13 14:30:00 EST
**Deployment Window:** 10:00 PM - 8:00 AM EST

## Violations Detected
- Publish VS Code Extension - 2025-10-13T14:25:00Z
- VS Code Extension Release - 2025-10-13T14:28:00Z

## Action Required
Review the above deployments and ensure future deployments
occur during 10 PM - 8 AM EST window.
```

### Maintenance Reports
Located in `agent-reports/maintenance-*.md`

Example:
```markdown
# Maintenance Agent Report

**Generated:** 2025-10-13 22:50:00 EST

## Extension Health
- **Compilation:** success
- **package.json:** valid
- **Security Vulnerabilities:** 0

## Marketplace Metrics
- **Total Installs:** 15
- **Average Rating:** 5.0

## Issue Tracking
- **Open Issues:** 3
- **Critical Issues:** 0

## Actions Taken
- Auto-fix compilation: Not needed
- Dependency updates: Up to date
- Security fixes: Not needed
```

---

## Troubleshooting

### Agent Not Running
1. **Check workflow status:**
   ```bash
   gh workflow list
   ```

2. **View recent runs:**
   ```bash
   gh run list --workflow="Schedule Enforcement Agent (24x7)"
   ```

3. **Check for disabled workflows:**
   - Go to GitHub → Actions → Select workflow → Check if enabled

### Agent Failing
1. **View failure logs:**
   ```bash
   gh run view [RUN_ID] --log
   ```

2. **Common issues:**
   - Missing `GITHUB_TOKEN` permissions
   - Rate limiting from GitHub API
   - Git push conflicts

3. **Fix:**
   - Ensure repository has proper permissions
   - Wait for rate limit reset
   - Pull latest changes and retry

### False Positive Violations
If schedule enforcement is blocking valid deployments:

1. **Check your local timezone:**
   ```bash
   TZ='America/New_York' date '+%Y-%m-%d %H:%M:%S %Z'
   ```

2. **Verify deployment window logic**
3. **Check agent logs for time calculations**

---

## Cost & Performance

### GitHub Actions Usage
- **Schedule Enforcement:** ~2,880 runs/month (every 5 min)
- **Maintenance Agent:** ~4,320 runs/month (every 10 min)
- **Total:** ~7,200 runs/month

### Free Tier Limits
GitHub Actions free tier includes:
- **Public repositories:** Unlimited minutes ✅
- **Private repositories:** 2,000 minutes/month

**This repository uses public repositories, so agents run completely FREE! ✅**

### Performance Impact
- Each agent run: ~30-60 seconds
- No impact on repository performance
- Minimal API rate limit usage

---

## Security Considerations

### Permissions
Both agents require:
- `contents: write` - To commit fixes and reports
- `issues: write` - To manage issues
- `pull-requests: write` - To comment on PRs
- `actions: write` - To monitor workflows

### Secrets Required
- `GITHUB_TOKEN` - Automatically provided by GitHub Actions
- `PAT_TOKEN` - Personal Access Token for VS Code Marketplace (already configured)

### Safety Features
- ✅ All commits include `[skip ci]` to prevent infinite loops
- ✅ Fixes are staged during deployment window only
- ✅ Critical changes require manual review
- ✅ All actions are logged and auditable

---

## Future Enhancements

Planned features for agents:

### Schedule Enforcement Agent
- [ ] Email notifications for violations
- [ ] Slack/Discord integration
- [ ] Deployment queue system
- [ ] Holiday schedule support

### Maintenance Agent
- [ ] AI-powered issue triage
- [ ] Automatic PR creation for fixes
- [ ] Performance regression detection
- [ ] User feedback sentiment analysis
- [ ] Automatic feature prioritization
- [ ] Integration testing automation

---

## Support

If you have questions about the agents:

1. **Check agent status:** `.github/agent-status/`
2. **Review reports:** `agent-reports/`
3. **View logs:** GitHub Actions tab
4. **Open an issue:** Maintenance Agent will auto-respond!

---

**Last Updated:** 2025-10-13
**Agent Version:** 1.0.0
**Maintained by:** Autonomous Agents 🤖
