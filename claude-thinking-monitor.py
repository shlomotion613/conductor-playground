#!/usr/bin/env python3
"""
Claude Thinking Monitor
Shows real-time activity of what Claude is doing in Conductor workspaces
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime
import json

class ThinkingMonitor:
    def __init__(self, workspace_path=None, update_interval=1):
        self.workspace_path = workspace_path or os.getcwd()
        self.update_interval = update_interval
        self.last_seen_files = set()
        self.file_timestamps = {}

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')

    def get_recent_task_files(self):
        """Get recently modified task output files"""
        tmp_claude = Path("/tmp/claude")
        if not tmp_claude.exists():
            return []

        task_files = []
        # Look for task output files
        for pattern in ["**/*.output", "**/*.log"]:
            task_files.extend(tmp_claude.glob(pattern))

        # Sort by modification time, most recent first
        task_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        return task_files[:5]  # Top 5 most recent

    def read_last_lines(self, file_path, n=20):
        """Read last N lines from a file"""
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                return lines[-n:] if len(lines) > n else lines
        except:
            return []

    def format_timestamp(self, timestamp):
        """Format Unix timestamp to readable time"""
        return datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")

    def extract_activity(self, lines):
        """Extract meaningful activity from output lines"""
        activities = []
        keywords = [
            'Reading', 'Writing', 'Editing', 'Searching', 'Running',
            'Glob', 'Grep', 'Task', 'Bash', 'Tool', 'Agent',
            'Error', 'Warning', 'Success', 'Failed', 'Completed'
        ]

        for line in lines:
            line_lower = line.lower()
            for keyword in keywords:
                if keyword.lower() in line_lower:
                    activities.append(line.strip())
                    break

        return activities[-10:] if activities else ["No recent activity detected"]

    def monitor(self):
        """Main monitoring loop"""
        try:
            while True:
                self.clear_screen()
                print("=" * 80)
                print("🔍 CLAUDE THINKING MONITOR")
                print("=" * 80)
                print(f"📁 Workspace: {self.workspace_path}")
                print(f"⏰ Updated: {datetime.now().strftime('%H:%M:%S')}")
                print(f"Press Ctrl+C to stop\n")

                task_files = self.get_recent_task_files()

                if not task_files:
                    print("⚠️  No active Claude tasks detected")
                    print("\nWaiting for Claude activity...")
                else:
                    for i, task_file in enumerate(task_files, 1):
                        mod_time = task_file.stat().st_mtime
                        age_seconds = time.time() - mod_time

                        print(f"\n{'─' * 80}")
                        print(f"📄 Task {i}: {task_file.name}")
                        print(f"⏱️  Last activity: {self.format_timestamp(mod_time)} ({int(age_seconds)}s ago)")

                        # Determine status
                        if age_seconds < 5:
                            status = "🟢 ACTIVE - Claude is working..."
                        elif age_seconds < 30:
                            status = "🟡 RECENT - Activity within 30s"
                        elif age_seconds < 300:
                            status = "🟠 IDLE - No activity for a while"
                        else:
                            status = "⚪ STALE - Likely completed or stuck"

                        print(f"Status: {status}")

                        # Show recent activity
                        lines = self.read_last_lines(task_file, 30)
                        if lines:
                            print("\n📝 Recent activity:")
                            activities = self.extract_activity(lines)
                            for activity in activities[-5:]:
                                print(f"   • {activity[:75]}")

                        # Show raw tail for active tasks
                        if age_seconds < 10 and lines:
                            print("\n💭 Latest output:")
                            for line in lines[-3:]:
                                print(f"   {line.rstrip()[:75]}")

                print("\n" + "=" * 80)

                # Check for stuck processes
                stuck_count = sum(1 for f in task_files if (time.time() - f.stat().st_mtime) > 300)
                if stuck_count > 0:
                    print(f"\n⚠️  WARNING: {stuck_count} task(s) appear stuck (no activity >5 min)")

                time.sleep(self.update_interval)

        except KeyboardInterrupt:
            self.clear_screen()
            print("\n👋 Monitor stopped\n")
            sys.exit(0)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Monitor Claude thinking activity')
    parser.add_argument('--workspace', '-w', help='Workspace path to monitor')
    parser.add_argument('--interval', '-i', type=float, default=1, help='Update interval in seconds')
    args = parser.parse_args()

    monitor = ThinkingMonitor(workspace_path=args.workspace, update_interval=args.interval)
    monitor.monitor()
