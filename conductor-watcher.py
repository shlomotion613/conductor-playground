#!/usr/bin/env python3
"""
Conductor Activity Notifier
Watches for Claude/Conductor output and sends macOS notifications
"""

import subprocess
import time
import os
import sys
from pathlib import Path
from datetime import datetime

class ConductorWatcher:
    def __init__(self, check_interval=2, thinking_threshold=5):
        self.check_interval = check_interval
        self.thinking_threshold = thinking_threshold
        self.last_output_time = None
        self.last_content_hash = None
        self.was_thinking = False

    def send_notification(self, message, subtitle=""):
        """Send macOS notification - non-blocking banner style"""
        try:
            # Use terminal-notifier with non-blocking banner that auto-dismisses
            cmd = [
                'terminal-notifier',
                '-message', message,
                '-title', 'Conductor Alert',
                '-sound', 'Glass',
                '-group', 'conductor-watcher',  # Group notifications so they stack
                '-timeout', '5'  # Auto-dismiss after 5 seconds
            ]
            if subtitle:
                cmd.extend(['-subtitle', subtitle])

            # Run in background, don't wait for it
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        except Exception as e:
            print(f"Failed to send notification: {e}")

    def get_terminal_content(self):
        """
        Get terminal content. This monitors various possible sources:
        1. Conductor's terminal output files
        2. Recent log files in /tmp
        3. Task output files
        """
        possible_locations = [
            "/tmp/conductor_output.log",
            Path.home() / ".conductor" / "output.log",
            "/tmp/claude",
        ]

        content = ""

        # Check for task output files
        tmp_claude = Path("/tmp/claude")
        if tmp_claude.exists():
            # Get most recently modified task output
            task_files = list(tmp_claude.rglob("tasks/*.output"))
            if task_files:
                latest_file = max(task_files, key=lambda f: f.stat().st_mtime)
                try:
                    content += latest_file.read_text()
                except:
                    pass

        # Check other locations
        for loc in possible_locations:
            try:
                path = Path(loc)
                if path.is_file():
                    content += path.read_text()
            except:
                pass

        return content

    def watch(self):
        """Main watching loop"""
        print("🔔 Conductor Notifier Started")
        print(f"Monitoring for Claude output activity...")
        print(f"Check interval: {self.check_interval}s")
        print(f"Thinking threshold: {self.thinking_threshold}s")
        print("Press Ctrl+C to stop\n")

        try:
            while True:
                current_content = self.get_terminal_content()
                current_hash = hash(current_content)
                current_time = time.time()

                # Check if content has changed
                if self.last_content_hash is not None and current_hash != self.last_content_hash:
                    time_since_last = current_time - self.last_output_time if self.last_output_time else 0
                    timestamp = datetime.now().strftime("%H:%M:%S")

                    print(f"[{timestamp}] ✨ New output detected!")

                    # If we were in "thinking" mode (no output for a while), send notification
                    if self.was_thinking:
                        self.send_notification("Claude has responded!", "Check Conductor")
                        print(f"[{timestamp}] 🔔 Notification sent")
                        self.was_thinking = False

                    self.last_output_time = current_time

                # Update thinking state
                if self.last_output_time:
                    idle_time = current_time - self.last_output_time
                    if idle_time >= self.thinking_threshold and not self.was_thinking:
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        print(f"[{timestamp}] 🤔 Claude appears to be thinking...")
                        self.was_thinking = True

                self.last_content_hash = current_hash
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            print("\n\n👋 Notifier stopped")
            sys.exit(0)

if __name__ == "__main__":
    watcher = ConductorWatcher()
    watcher.watch()
