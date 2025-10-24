#!/bin/bash

# Claude Code Status Line with Cost and Usage Metrics
# Displays model, project info, git status, and usage metrics
# Make script executable: chmod +x ~/.claude/statusline-metrics.sh

# Read JSON input from stdin
input=$(cat)

# Extract basic information
model=$(echo "$input" | jq -r '.model.display_name')
model_id=$(echo "$input" | jq -r '.model.id')
project_dir=$(echo "$input" | jq -r '.workspace.project_dir')
current_dir=$(echo "$input" | jq -r '.workspace.current_dir')
session_id=$(echo "$input" | jq -r '.session_id')
transcript_path=$(echo "$input" | jq -r '.transcript_path')
output_style=$(echo "$input" | jq -r '.output_style.name')
version=$(echo "$input" | jq -r '.version')

# Calculate relative directory
rel_dir=$(python3 -c "import os; print(os.path.relpath('$current_dir', '$project_dir'))" 2>/dev/null || basename "$current_dir")

# Get git information if available
git_info=""
if [ -d "$current_dir/.git" ] || git -C "$current_dir" rev-parse --git-dir >/dev/null 2>&1; then
    branch=$(git -C "$current_dir" branch --show-current 2>/dev/null || echo 'detached')
    # Check for uncommitted changes
    if ! git -C "$current_dir" diff-index --quiet HEAD -- 2>/dev/null; then
        git_info="git:${branch}*"
    else
        git_info="git:${branch}"
    fi
fi

# Extract usage metrics from transcript if available
usage_info=""
if [ -f "$transcript_path" ] && [ -r "$transcript_path" ]; then
    # Count total messages and get last few lines for recent metrics
    total_messages=$(grep -c '"role":' "$transcript_path" 2>/dev/null || echo "0")
    
    # Look for token usage in the last part of the transcript
    input_tokens=""
    output_tokens=""
    
    # Extract the most recent usage data (last 50 lines should contain latest metrics)
    recent_data=$(tail -50 "$transcript_path" 2>/dev/null)
    
    # Try to extract token counts from usage blocks
    if echo "$recent_data" | grep -q '"input_tokens"'; then
        input_tokens=$(echo "$recent_data" | grep '"input_tokens"' | tail -1 | sed 's/.*"input_tokens"[[:space:]]*:[[:space:]]*\([0-9]*\).*/\1/')
        output_tokens=$(echo "$recent_data" | grep '"output_tokens"' | tail -1 | sed 's/.*"output_tokens"[[:space:]]*:[[:space:]]*\([0-9]*\).*/\1/')
    fi
    
    # Build usage info string
    if [ -n "$input_tokens" ] && [ -n "$output_tokens" ]; then
        total_tokens=$((input_tokens + output_tokens))
        # Estimate cost (rough approximation for Sonnet 4)
        # Input: $3/1M tokens, Output: $15/1M tokens
        cost_estimate=$(python3 -c "print(f'{($input_tokens * 3 + $output_tokens * 15) / 1000000:.4f}')" 2>/dev/null || echo "0.0000")
        usage_info="msgs:${total_messages} | tok:${total_tokens} | cost:\$${cost_estimate}"
    else
        usage_info="msgs:${total_messages}"
    fi
fi

# Get system load (optional, lightweight)
load_avg=$(uptime | sed 's/.*load averages: \([0-9.]*\).*/\1/' 2>/dev/null)

# Build the status line
status_parts=()

# Model info (shortened for space)
case "$model" in
    *"Claude 3.5 Sonnet"*) model_short="Sonnet 3.5" ;;
    *"Sonnet 4"*) model_short="Sonnet 4" ;;
    *"Claude"*) model_short=$(echo "$model" | sed 's/Claude //' | sed 's/ .*//') ;;
    *) model_short="$model" ;;
esac

status_parts+=("$model_short")

# Directory info
if [ "$rel_dir" = "." ]; then
    status_parts+=("$(basename "$project_dir")")
else
    status_parts+=("$rel_dir")
fi

# Git info
if [ -n "$git_info" ]; then
    status_parts+=("$git_info")
fi

# Usage info
if [ -n "$usage_info" ]; then
    status_parts+=("$usage_info")
fi

# Output style if not default
if [ "$output_style" != "default" ] && [ "$output_style" != "null" ] && [ -n "$output_style" ]; then
    status_parts+=("style:$output_style")
fi

# System load (if available and reasonable)
if [ -n "$load_avg" ] && [ "$load_avg" != "load" ]; then
    status_parts+=("load:$load_avg")
fi

# Join all parts with " | "
IFS=" | "
printf "%s" "${status_parts[*]}"