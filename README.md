# Conductor Claude Tools

Tools to monitor and get notified about Claude's activity in Conductor.

## 🔔 Activity Notifier

Get macOS notifications when Claude stops thinking and produces output.

**Quick Start:**
```bash
python3 conductor-watcher.py
```

## 🔍 Thinking Monitor

Real-time visualization of what Claude is doing (like the web app).

**Quick Start:**
```bash
python3 claude-thinking-monitor.py
```

This shows:
- Active tasks and their status (🟢 Active, 🟡 Recent, 🟠 Idle, ⚪ Stale)
- Last activity timestamp
- Recent actions (reading files, running commands, etc.)
- Warnings for stuck processes (>5 min idle)

## How It Works

The notifier monitors Conductor's terminal output and detects when:
1. Claude is "thinking" (no new output for 5+ seconds)
2. New output appears after a thinking period
3. Sends a macOS notification with sound when Claude responds

## Features

- 🔔 Native macOS notifications with sound
- 🤔 Detects when Claude is thinking vs. responding
- ⚡ Lightweight background monitoring
- 🎯 Configurable check intervals and thresholds

## Configuration

Edit the Python script to customize:
- `check_interval`: How often to check for updates (default: 2 seconds)
- `thinking_threshold`: How long before considering Claude "thinking" (default: 5 seconds)

## Requirements

- macOS (uses `osascript` for notifications)
- Python 3.6+ (for Python version)
- Bash (for shell version)

## Usage Tips

1. Run the watcher in a separate terminal window
2. Keep it running in the background while working in Conductor
3. You'll get notified when Claude finishes long tasks
4. Press Ctrl+C to stop the watcher

## Monitoring Sources

The watcher monitors:
- `/tmp/claude/tasks/*.output` - Task output files
- `/tmp/conductor_output.log` - General output log
- `~/.conductor/output.log` - User conductor logs

If Conductor uses different paths, you can modify the `possible_locations` list in the Python script.
