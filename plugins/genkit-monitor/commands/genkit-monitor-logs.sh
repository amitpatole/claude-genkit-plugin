#!/bin/bash
echo "Genkit Flow Logs"
echo "Viewing logs from logs/combined.log..."
tail -f logs/combined.log 2>/dev/null || echo "No logs found. Run flows to generate logs."
