#!/usr/bin/env python3
"""
Claude Chain of Thought Viewer
Shows Claude's tool calls and reasoning steps in real-time
"""

import os
import sys
import time
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class ChainViewer:
    def __init__(self, update_interval=0.5):
        self.update_interval = update_interval
        self.last_positions = {}
        self.tool_icons = {
            'Read': '📖',
            'Write': '✍️',
            'Edit': '✏️',
            'Glob': '🔍',
            'Grep': '🔎',
            'Bash': '⚡',
            'Task': '🤖',
            'WebFetch': '🌐',
            'WebSearch': '🔍',
            'EnterPlanMode': '📋',
            'ExitPlanMode': '✅',
        }

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')

    def get_active_task_files(self):
        """Get currently active task output files"""
        tmp_claude = Path("/tmp/claude")
        if not tmp_claude.exists():
            return []

        task_files = list(tmp_claude.rglob("tasks/*.output"))
        # Sort by modification time, most recent first
        task_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

        # Only return files modified in last 10 minutes
        recent = []
        now = time.time()
        for f in task_files:
            if now - f.stat().st_mtime < 600:  # 10 minutes
                recent.append(f)

        return recent[:3]  # Top 3 most recent

    def extract_tool_calls(self, lines):
        """Extract tool calls and their parameters from output"""
        tool_calls = []

        # Common patterns in Claude output
        patterns = [
            # Tool invocation patterns
            (r'(?:Invoking|Calling|Using|Running)\s+(\w+)\s+(?:tool|with)', 'tool_call'),
            # File operations
            (r'(?:Reading|Writing|Editing)\s+(.+?)(?:\s|$)', 'file_op'),
            # Search patterns
            (r'(?:Searching|Grepping|Globbing)\s+for\s+(.+?)(?:\s|$)', 'search'),
            # Bash commands
            (r'Running command:\s*(.+?)$', 'bash'),
            # Thinking indicators
            (r'(?:Analyzing|Exploring|Investigating|Checking)\s+(.+?)(?:\s|$)', 'thinking'),
        ]

        for line in lines:
            line = line.strip()
            if not line or len(line) < 5:
                continue

            for pattern, call_type in patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    tool_calls.append({
                        'type': call_type,
                        'content': match.group(1) if match.groups() else line,
                        'raw': line[:100]
                    })
                    break

        return tool_calls

    def format_chain_step(self, step, index):
        """Format a single chain step for display"""
        icon = '🔹'
        if step['type'] == 'tool_call':
            icon = self.tool_icons.get(step['content'], '🔧')
        elif step['type'] == 'file_op':
            icon = '📄'
        elif step['type'] == 'search':
            icon = '🔍'
        elif step['type'] == 'bash':
            icon = '⚡'
        elif step['type'] == 'thinking':
            icon = '💭'

        return f"{icon} {step['raw']}"

    def get_new_content(self, file_path):
        """Get only new content from a file since last read"""
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()

            # Track position in file
            last_pos = self.last_positions.get(str(file_path), 0)
            new_lines = lines[last_pos:]
            self.last_positions[str(file_path)] = len(lines)

            return new_lines
        except:
            return []

    def view(self):
        """Main viewing loop"""
        print("🧠 CLAUDE CHAIN OF THOUGHT VIEWER")
        print("=" * 80)
        print("Starting... watching for Claude activity\n")

        step_counter = 0

        try:
            while True:
                task_files = self.get_active_task_files()

                if not task_files:
                    # Clear and show waiting message
                    if step_counter == 0:
                        print("⏳ Waiting for Claude to start thinking...")
                    time.sleep(self.update_interval)
                    continue

                # Process new content from active files
                for task_file in task_files:
                    new_lines = self.get_new_content(task_file)

                    if not new_lines:
                        continue

                    # Show task file name on first output
                    if step_counter == 0 or str(task_file) not in self.last_positions:
                        print(f"\n{'─' * 80}")
                        print(f"📋 Task: {task_file.name}")
                        print(f"{'─' * 80}\n")

                    # Extract and display tool calls
                    tool_calls = self.extract_tool_calls(new_lines)

                    for call in tool_calls:
                        step_counter += 1
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        print(f"[{timestamp}] {self.format_chain_step(call, step_counter)}")

                    # Also show raw output if it looks interesting
                    for line in new_lines:
                        line = line.strip()
                        # Show lines that look like status updates
                        if any(keyword in line.lower() for keyword in
                               ['error', 'success', 'complete', 'found', 'failed', 'done']):
                            if len(line) > 10:
                                timestamp = datetime.now().strftime("%H:%M:%S")
                                print(f"[{timestamp}] 💬 {line[:100]}")

                time.sleep(self.update_interval)

        except KeyboardInterrupt:
            print("\n\n👋 Chain viewer stopped")
            print(f"📊 Total steps observed: {step_counter}\n")
            sys.exit(0)

if __name__ == "__main__":
    viewer = ChainViewer(update_interval=0.5)
    viewer.view()
