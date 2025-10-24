# Custom Statusline for Claude Code

Enhanced status line script that displays comprehensive metrics and information in your Claude Code CLI.

## Features

- **Model Information**: Displays current Claude model (e.g., Sonnet 4, Sonnet 3.5)
- **Project/Directory**: Shows current working directory relative to project root
- **Git Status**: Branch name with indicator for uncommitted changes (*)
- **Token Metrics**: Real-time input/output token counting
- **Cost Tracking**: Automatic cost calculation based on token usage
- **Message Count**: Total messages in current session
- **System Load**: Current system load average
- **Output Style**: Displays active output style if non-default

## Example Output

```
Sonnet 4 | alpha-intelligence | git:main* | msgs:15 | tok:42735 | cost:$0.7684 | load:2.5
```

## Installation

1. **Copy the script to Claude config directory:**
   ```bash
   cp statusline-metrics.sh ~/.claude/
   chmod +x ~/.claude/statusline-metrics.sh
   ```

2. **Update Claude settings:**

   Edit `~/.claude/settings.json` and add:
   ```json
   {
     "statusLine": {
       "command": "~/.claude/statusline-metrics.sh",
       "type": "command"
     }
   }
   ```

3. **Restart Claude Code** or start a new session

## Configuration

### Cost Rates

The script uses the following rates (configured in the script):
- **Input tokens**: $3 per 1M tokens
- **Output tokens**: $15 per 1M tokens

To adjust rates, edit the script at line 59:
```bash
cost_estimate=$(python3 -c "print(f'{($input_tokens * 3 + $output_tokens * 15) / 1000000:.4f}')")
```

### Model Display Names

The script automatically shortens model names for better readability:
- "Claude 3.5 Sonnet" → "Sonnet 3.5"
- "Sonnet 4" → "Sonnet 4"
- Other models display their primary name

## Technical Details

### Input Processing

The script receives JSON input from Claude Code via stdin:
```json
{
  "model": {
    "display_name": "Sonnet 4",
    "id": "claude-sonnet-4-5-20250929"
  },
  "workspace": {
    "project_dir": "/path/to/project",
    "current_dir": "/path/to/project/subdir"
  },
  "session_id": "...",
  "transcript_path": "...",
  "output_style": {...},
  "version": "..."
}
```

### Metrics Extraction

1. **Token Counting**: Parses transcript file for `input_tokens` and `output_tokens`
2. **Message Counting**: Counts `"role":` occurrences in transcript
3. **Git Status**: Uses `git` commands to check branch and changes
4. **System Load**: Extracts from `uptime` command

### Dependencies

- `jq` - JSON parsing
- `python3` - Path calculations and cost estimates
- `git` - Git status information
- Standard Unix tools (`grep`, `sed`, `tail`)

## Troubleshooting

### Issue: Status line not appearing

**Solution:**
1. Verify script is executable: `ls -l ~/.claude/statusline-metrics.sh`
2. Check settings.json syntax is valid
3. Restart Claude Code completely

### Issue: `jq: command not found`

**Solution:**
```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq
```

### Issue: Cost estimates not showing

**Causes:**
- Transcript file not accessible
- No recent token usage data

**Solution:**
- The script reads the last 50 lines of transcript
- Ensure Claude has permission to read transcript files

### Issue: Git status not showing

**Causes:**
- Not in a git repository
- Git not installed

**Solution:**
- Script gracefully handles missing git
- Git info only shows when available

## Customization

### Add Custom Metrics

You can extend the script to show additional metrics. Add new sections before line 110:

```bash
# Example: Add Python version
python_version=$(python3 --version 2>&1 | sed 's/Python /py:/')
if [ -n "$python_version" ]; then
    status_parts+=("$python_version")
fi
```

### Change Separator

Modify line 110 to use different separators:
```bash
IFS=" | "    # Default: pipe with spaces
IFS=" • "    # Alternative: bullet point
IFS=" / "    # Alternative: forward slash
```

### Conditional Display

Add logic to show/hide metrics based on conditions:
```bash
# Only show cost if over $0.10
if [ "$cost_estimate" != "0.0000" ] && (( $(echo "$cost_estimate > 0.10" | bc -l) )); then
    usage_info="msgs:${total_messages} | tok:${total_tokens} | cost:\$${cost_estimate}"
fi
```

## Performance

- **Execution Time**: ~50-100ms per update
- **Memory Usage**: <5MB
- **CPU Impact**: Negligible

The script is optimized to:
- Read only last 50 lines of transcript (not entire file)
- Use efficient text processing tools
- Cache git information when possible

## Integration with Claude Code

The statusline updates automatically when:
- Starting a new session
- Switching projects
- Model changes
- After each message exchange

## Advanced Features

### Session Cost Tracking

To track cumulative costs across sessions, you could modify the script to:
1. Store costs in a separate file
2. Read and accumulate on each run
3. Display daily/weekly totals

### Alert on High Usage

Add threshold alerts:
```bash
# Alert if session cost exceeds $5
if (( $(echo "$cost_estimate > 5.0" | bc -l) )); then
    echo "⚠️ High cost alert!"
fi
```

### Project-Specific Settings

Use different settings per project:
```bash
# Load project-specific config if exists
if [ -f "$project_dir/.claude-statusline.conf" ]; then
    source "$project_dir/.claude-statusline.conf"
fi
```

## Version History

- **v1.0** (2024-08): Initial release with basic metrics
- **v1.1** (2024-10): Added cost tracking and improved token parsing

## Contributing

Improvements welcome! Consider adding:
- Database logging for historical tracking
- More accurate cost models for different Claude versions
- Integration with external monitoring tools
- Custom themes/colors

## Related

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Claude Code Statusline Guide](https://docs.claude.com/en/docs/claude-code/statusline)

---

**Tip:** Combine with other Claude Code features like custom output styles and hooks for a fully customized CLI experience!
