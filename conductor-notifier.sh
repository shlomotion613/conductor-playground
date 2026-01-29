#!/bin/bash

# Conductor Activity Notifier
# Monitors Conductor terminal output and sends notifications when Claude responds

CHECK_INTERVAL=2  # Check every 2 seconds
LAST_LINE_COUNT=0
NOTIFICATION_TITLE="Conductor Alert"

# Function to send macOS notification
send_notification() {
    local message="$1"
    osascript -e "display notification \"$message\" with title \"$NOTIFICATION_TITLE\" sound name \"Glass\""
}

# Function to get terminal output line count
get_line_count() {
    # Try to get Conductor terminal output from the GetTerminalOutput tool location
    # This is a placeholder - we'll monitor a log file or output file
    if [ -f "/tmp/conductor_output.log" ]; then
        wc -l < "/tmp/conductor_output.log" 2>/dev/null || echo 0
    else
        echo 0
    fi
}

echo "🔔 Conductor Notifier Started"
echo "Monitoring for Claude output activity..."
echo "Press Ctrl+C to stop"
echo ""

IDLE_TIME=0
THINKING_THRESHOLD=5  # Consider "thinking" if no output for 5 seconds

while true; do
    CURRENT_LINE_COUNT=$(get_line_count)

    if [ "$CURRENT_LINE_COUNT" -gt "$LAST_LINE_COUNT" ]; then
        # New output detected
        NEW_LINES=$((CURRENT_LINE_COUNT - LAST_LINE_COUNT))
        echo "[$(date '+%H:%M:%S')] ✨ New output detected! ($NEW_LINES new lines)"

        # Only notify if we were in "thinking" mode (idle for a while)
        if [ "$IDLE_TIME" -ge "$THINKING_THRESHOLD" ]; then
            send_notification "Claude has responded! Check Conductor."
        fi

        LAST_LINE_COUNT=$CURRENT_LINE_COUNT
        IDLE_TIME=0
    else
        IDLE_TIME=$((IDLE_TIME + CHECK_INTERVAL))
    fi

    sleep $CHECK_INTERVAL
done
