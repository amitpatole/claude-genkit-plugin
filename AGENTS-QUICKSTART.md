# Autonomous Agents - Quick Start Guide

## 🚀 Overview

This repository has **2 autonomous agents** running 24/7:

1. **Schedule Enforcement Agent** - Blocks deployments outside 10 PM - 8 AM EST
2. **Monitoring & Maintenance Agent** - Fixes issues, updates dependencies, responds to users

## ⚡ Quick Commands

### Check Agent Status
```bash
# View all agent statuses
cat .github/agent-status/*.txt

# Check schedule enforcement
cat .github/agent-status/schedule-enforcement.txt

# Check maintenance agent
cat .github/agent-status/maintenance-agent.txt
```

### View Recent Reports
```bash
# Latest violation report
cat $(ls -t agent-reports/violation-*.md 2>/dev/null | head -1)

# Latest maintenance report
cat $(ls -t agent-reports/maintenance-*.md 2>/dev/null | head -1)

# All reports from today
ls -lt agent-reports/*-$(date +%Y-%m-%d)*.md
```

### Check Deployment Window
```bash
# Check if currently in deployment window
HOUR=$(TZ='America/New_York' date +%H)
if [ "$HOUR" -ge 22 ] || [ "$HOUR" -lt 8 ]; then
  echo "✅ ALLOWED - Deployments permitted"
else
  echo "🚫 BLOCKED - Wait until 10 PM EST"
fi
```

### View Agent Logs
```bash
# Schedule enforcement logs
gh run list --workflow="Schedule Enforcement Agent (24x7)" --limit 5
gh run view $(gh run list --workflow="Schedule Enforcement Agent (24x7)" --limit 1 --json databaseId --jq '.[0].databaseId')

# Maintenance agent logs
gh run list --workflow="Monitoring & Maintenance Agent (24x7)" --limit 5
gh run view $(gh run list --workflow="Monitoring & Maintenance Agent (24x7)" --limit 1 --json databaseId --jq '.[0].databaseId')
```

## 📋 Deployment Schedule

| Time (EST) | Status | Can Deploy? |
|------------|--------|-------------|
| 10:00 PM - 11:59 PM | ✅ ALLOWED | Yes |
| 12:00 AM - 7:59 AM | ✅ ALLOWED | Yes |
| 8:00 AM - 9:59 PM | 🚫 BLOCKED | No |

## 🎯 What Each Agent Does

### Schedule Enforcement Agent
- ✅ Runs every 5 minutes
- ✅ Checks if deployments are in allowed window
- ✅ Blocks deployments from 8 AM - 10 PM EST
- ✅ Creates violation reports
- ✅ Updates heartbeat status

### Maintenance Agent
- ✅ Runs every 10 minutes
- ✅ Monitors extension health (compilation, security)
- ✅ Auto-fixes compilation errors
- ✅ Auto-updates dependencies (patch versions)
- ✅ Auto-fixes security vulnerabilities
- ✅ Responds to GitHub issues automatically
- ✅ Tracks marketplace metrics
- ✅ Researches new features

## 🔧 Common Tasks

### Deploy a New Version
```bash
# Wait until 10 PM EST, then:
cd vscode-extension

# Update version
npm version patch  # or minor/major

# Commit and push (will trigger deployment)
git add package.json package-lock.json
git commit -m "chore: bump version to $(node -p 'require(\"./package.json\").version')"
git push

# Deployment will proceed automatically if within window
```

### Force Emergency Deployment (Override Schedule)
⚠️ **USE ONLY FOR CRITICAL HOTFIXES!**

```bash
# Option 1: Manual workflow dispatch (bypasses time check if you're admin)
gh workflow run publish-vscode-extension.yml

# Option 2: Create emergency override commit
git commit -m "fix: critical security patch [emergency-deploy]"
git push
```

### Check Why Deployment Was Blocked
```bash
# View latest violation report
cat $(ls -t agent-reports/violation-*.md | head -1)

# Check current time vs allowed window
TZ='America/New_York' date '+Current time: %H:%M EST'
echo "Allowed: 22:00-08:00 EST (10 PM - 8 AM)"
```

### View Agent Health
```bash
# Check when agents last ran
echo "Schedule Enforcement:"
cat .github/agent-status/schedule-enforcement.txt
echo ""
echo "Maintenance Agent:"
cat .github/agent-status/maintenance-agent.txt

# If timestamp is >1 hour old, agent may be down
```

### See What Maintenance Agent Fixed
```bash
# View recent commits by agents
git log --author="github-actions[bot]" --oneline -10

# View specific fix
git show [commit-hash]
```

## 🐛 Troubleshooting

### Agent Not Running
```bash
# Check workflow status
gh workflow list | grep "24x7"

# View recent failures
gh run list --workflow="Schedule Enforcement Agent (24x7)" --status failure
gh run list --workflow="Monitoring & Maintenance Agent (24x7)" --status failure

# View failure details
gh run view [RUN_ID] --log
```

### Deployment Blocked But It's Within Window
```bash
# Verify your system time matches EST
TZ='America/New_York' date '+%Y-%m-%d %H:%M:%S %Z'

# Check workflow logs
gh run view [RUN_ID] --log | grep "deployment schedule"

# Manual override if needed
gh workflow run publish-vscode-extension.yml
```

### Agent Pushed Bad Fix
```bash
# Revert agent commit
git revert [commit-hash]
git push

# Or rollback to before agent fix
git reset --hard [good-commit-hash]
git push --force  # ⚠️ Use carefully!
```

## 📊 Monitoring Dashboard

### Real-Time Metrics
```bash
# Extension health
cd vscode-extension
npm run compile  # Should succeed
npm audit         # Should show 0 vulnerabilities

# Marketplace stats
node scripts/fetch-marketplace-stats.js

# Repository health
gh issue list --state open
gh pr list --state open
```

### Agent Performance
```bash
# Total runs today
gh run list --workflow="Schedule Enforcement Agent (24x7)" \
  --created "$(date +%Y-%m-%d)" --json status --jq 'length'

gh run list --workflow="Monitoring & Maintenance Agent (24x7)" \
  --created "$(date +%Y-%m-%d)" --json status --jq 'length'

# Success rate
gh run list --workflow="Monitoring & Maintenance Agent (24x7)" \
  --limit 100 --json conclusion --jq '[.[] | .conclusion] | group_by(.) | map({status: .[0], count: length})'
```

## 🎓 Learn More

- **Full Documentation:** [`AGENTS.md`](./AGENTS.md)
- **Configuration:** [`.github/agents-config.yml`](./.github/agents-config.yml)
- **Schedule Enforcement:** [`.github/workflows/schedule-enforcement-agent.yml`](./.github/workflows/schedule-enforcement-agent.yml)
- **Maintenance Agent:** [`.github/workflows/monitoring-maintenance-agent.yml`](./.github/workflows/monitoring-maintenance-agent.yml)

## 🆘 Support

If agents are misbehaving:

1. **Check status files** in `.github/agent-status/`
2. **Review reports** in `agent-reports/`
3. **View workflow logs** via `gh run view`
4. **Open an issue** (Maintenance Agent will auto-respond!)

---

**Quick Reference Card:**

```
✅ ALLOWED HOURS:  10 PM - 8 AM EST
🚫 BLOCKED HOURS:  8 AM - 10 PM EST

📁 Status:   .github/agent-status/*.txt
📁 Reports:  agent-reports/*.md
📁 Config:   .github/agents-config.yml
📁 Docs:     AGENTS.md

🔍 Check:    cat .github/agent-status/*.txt
📊 Reports:  ls -lt agent-reports/
🚀 Deploy:   Wait until 10 PM EST, then git push
🐛 Logs:     gh run list --workflow="...(24x7)"
```

---

**Last Updated:** 2025-10-13
**Agent Version:** 1.0.0
