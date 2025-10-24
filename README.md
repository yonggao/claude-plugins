# Claude Code Plugins

A collection of custom plugins, skills, and configurations for [Claude Code](https://claude.ai/code) - Anthropic's official CLI for Claude.

## Overview

This repository contains personal customizations and extensions for Claude Code, including:

- **Skills**: Reusable capabilities that extend Claude Code's functionality
- **Statusline**: Custom status line scripts for enhanced CLI experience
- **Documentation**: Guides and examples for using these plugins

## Contents

### Skills

#### 1. HTML to PDF (`skills/html-to-pdf/`)

Convert HTML files to PDF or PNG format with multiple rendering options.

**Features:**
- Multi-page PDF generation (A4 format)
- Single-page long-image PDF (no page breaks)
- Background colors and gradients preservation
- Chinese/CJK character support
- Multiple conversion methods with fallbacks

**Usage:**
```bash
# Standard multi-page PDF
python html_to_pdf_final.py input.html

# Single-page long image PDF
python html_to_long_image.py input.html
```

**Dependencies:**
- Playwright
- Pillow
- pypdf

[Full Documentation](skills/html-to-pdf/SKILL.md)

#### 2. Markdown to PDF (`skills/markdown-to-pdf/`)

Convert Markdown files to professional PDF presentations using Marp.

**Features:**
- Beautiful presentation slides from Markdown
- Multiple built-in themes (default, gaia, uncover)
- Code syntax highlighting
- Math equations support (KaTeX)
- Chinese/CJK character support
- Custom CSS and layouts

**Usage:**
```bash
# Default theme
python marp_to_pdf.py presentation.md

# Custom theme
python marp_to_pdf.py presentation.md --theme gaia
```

**Dependencies:**
- Marp CLI (`npm install -g @marp-team/marp-cli`)

[Full Documentation](skills/markdown-to-pdf/SKILL.md)

### Statusline

#### Custom Metrics Statusline (`statusline/statusline-metrics.sh`)

Enhanced status line displaying:
- Model information (Sonnet 4, etc.)
- Current project/directory
- Git branch and status
- Token usage metrics
- Cost estimates
- System load

**Features:**
- Real-time token counting
- Automatic cost calculation ($3/1M input, $15/1M output for Sonnet 4)
- Git status with uncommitted changes indicator
- Message count tracking
- System load monitoring

**Installation:**
```bash
# Copy to Claude config
cp statusline/statusline-metrics.sh ~/.claude/

# Make executable
chmod +x ~/.claude/statusline-metrics.sh

# Add to Claude settings
# Edit ~/.claude/settings.json:
{
  "statusLine": {
    "command": "~/.claude/statusline-metrics.sh",
    "type": "command"
  }
}
```

## Installation

### Prerequisites

- [Claude Code](https://claude.ai/code) installed
- Node.js (for Marp skill)
- Python 3.8+ (for conversion skills)

### Quick Start

1. **Clone this repository:**
   ```bash
   git clone https://github.com/yonggao/claude-plugins.git
   cd claude-plugins
   ```

2. **Install skills:**
   ```bash
   # HTML to PDF skill
   cp -r skills/html-to-pdf ~/.claude/skills/

   # Markdown to PDF skill
   cp -r skills/markdown-to-pdf ~/.claude/skills/

   # Install dependencies
   pip install playwright pillow pypdf
   playwright install chromium
   npm install -g @marp-team/marp-cli
   ```

3. **Install statusline:**
   ```bash
   cp statusline/statusline-metrics.sh ~/.claude/
   chmod +x ~/.claude/statusline-metrics.sh
   ```

4. **Configure Claude Code:**
   Edit `~/.claude/settings.json` to add the statusline:
   ```json
   {
     "statusLine": {
       "command": "~/.claude/statusline-metrics.sh",
       "type": "command"
     }
   }
   ```

## Usage Examples

### HTML to PDF Conversion

```bash
# Convert business plan to multi-page PDF
python ~/.claude/skills/html-to-pdf/html_to_pdf_final.py report.html

# Create single-page presentation PDF
python ~/.claude/skills/html-to-pdf/html_to_long_image.py report.html
```

### Markdown to PDF Presentation

```bash
# Create presentation with default theme
python ~/.claude/skills/markdown-to-pdf/marp_to_pdf.py slides.md

# Use Gaia theme
python ~/.claude/skills/markdown-to-pdf/marp_to_pdf.py slides.md --theme gaia
```

### Within Claude Code

Simply ask Claude to use these skills:

```
> Convert my HTML report to PDF
> Create a presentation from this Markdown file
> Export slides.md to PDF with the Gaia theme
```

## Directory Structure

```
claude-plugins/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── skills/                            # Claude Code skills
│   ├── html-to-pdf/                   # HTML to PDF converter
│   │   ├── SKILL.md                   # Skill definition
│   │   ├── README.md                  # Documentation
│   │   ├── QUICK_START.md             # Quick start guide
│   │   ├── EXAMPLES.md                # Usage examples
│   │   ├── html_to_long_image.py      # Long image converter
│   │   └── VERSION                    # Version info
│   └── markdown-to-pdf/               # Markdown to PDF converter
│       ├── SKILL.md                   # Skill definition
│       ├── markdown_to_pdf.py         # Basic converter
│       └── marp_to_pdf.py             # Marp converter
├── statusline/                        # Status line scripts
│   ├── statusline-metrics.sh          # Enhanced statusline
│   └── README.md                      # Statusline docs
└── docs/                              # Additional documentation
    └── CONTRIBUTING.md                # Contribution guidelines
```

## Development

### Creating New Skills

1. Create a new directory in `skills/`:
   ```bash
   mkdir -p skills/my-skill
   ```

2. Add a `SKILL.md` file with frontmatter:
   ```markdown
   ---
   name: my-skill
   description: Brief description of what the skill does
   ---

   # My Skill

   Detailed documentation...
   ```

3. Add your implementation files (Python, JavaScript, etc.)

4. Test with Claude Code

### Skill Requirements

- Must have a `SKILL.md` file with name and description
- Should include clear documentation and examples
- Should handle dependencies gracefully
- Should provide helpful error messages

## MCP Servers

This repository also documents MCP server configurations:

### Feishu/Lark MCP Server

Integrated in `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "lark-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "@larksuiteoapi/lark-mcp",
        "mcp",
        "-a", "YOUR_APP_ID",
        "-s", "YOUR_APP_SECRET",
        "--oauth"
      ]
    }
  }
}
```

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-skill`)
3. Commit your changes (`git commit -m 'Add amazing skill'`)
4. Push to the branch (`git push origin feature/amazing-skill`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) file for details

## Acknowledgments

- [Claude Code](https://claude.ai/code) by Anthropic
- [Marp](https://marp.app/) for Markdown presentations
- [Playwright](https://playwright.dev/) for HTML rendering

## Resources

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Creating Custom Skills](https://docs.claude.com/en/docs/claude-code/skills)
- [MCP Servers](https://modelcontextprotocol.io/)

## Support

For issues or questions:
- Open an issue in this repository
- Check the [Claude Code documentation](https://docs.claude.com/)
- Visit the [Claude Code GitHub issues](https://github.com/anthropics/claude-code/issues)

---

**Note:** This is a personal collection of Claude Code customizations. Modify and extend as needed for your own workflow.
