# Agent Status Directory

This directory contains real-time status files for all autonomous agents.

## Files

- `schedule-enforcement.txt` - Schedule Enforcement Agent heartbeat
- `maintenance-agent.txt` - Monitoring & Maintenance Agent heartbeat

## Format

Each file contains a single line with:
```
[Agent Name]: [STATUS] - [Timestamp in EST]
```

Example:
```
Schedule Enforcement Agent: ACTIVE - 2025-10-13 22:45:00 EST
```

## Updates

- Schedule Enforcement Agent: Every 5 minutes
- Maintenance Agent: Every 10 minutes

## Monitoring

Check agent status:
```bash
cat .github/agent-status/schedule-enforcement.txt
cat .github/agent-status/maintenance-agent.txt
```

If timestamp is more than 1 hour old, the agent may not be running properly.
