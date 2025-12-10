# Claude Code Plugins

A collection of custom plugins, skills, and configurations for [Claude Code](https://claude.ai/code) - Anthropic's official CLI for Claude.

## Overview

This repository contains personal customizations and extensions for Claude Code, including:

- **Commands**: Custom slash commands for project-specific workflows
- **Agents**: Specialized AI agents for different roles and tasks
- **Skills**: Reusable capabilities that extend Claude Code's functionality
- **Statusline**: Custom status line scripts for enhanced CLI experience
- **Documentation**: Guides and examples for using these plugins

## Contents

### Commands

Custom slash commands for automated workflows and analysis tasks.

#### 1. Team Analytics (`/team_analytics`)

Analyze team's git commit history across all repositories for activity, performance, and working areas per developer.

**Features:**
- Repository discovery across subdirectories
- Per-developer contribution analysis
- Code change statistics and patterns
- Cross-repository collaboration tracking
- Team velocity and health metrics
- Customizable time period analysis

**Usage:**
```bash
/team_analytics "90 days ago"
```

#### 2. Agent Workflow (`/agent-workflow`)

Manage and orchestrate multi-agent workflows for complex tasks.

#### 3. CII Daily Report (`/cii_daily_report`)

Generate comprehensive daily reports for Customer Intelligence & Insights.

**Installation:**
```bash
# Copy commands to project .claude directory
cp commands/*.md /path/to/your/project/.claude/commands/
```

### Agents

Specialized AI agents with role-specific expertise and capabilities. These agents can be invoked to handle specific tasks with domain expertise.

#### Engineering & Architecture

- **Chief Architect** - High-level system design and technical strategy
- **Senior Frontend Architect** - Frontend architecture and best practices
- **Senior Backend Architect** - Backend system design and optimization
- **DevOps Infrastructure Engineer** - Infrastructure, CI/CD, and deployment
- **AI Engineer Expert** - AI/ML integration and optimization
- **Energy AI Model Engineer** - Energy system modeling and optimization

#### Product & Planning

- **Project Manager** - Project planning, metrics analysis, and KPI tracking
- **Business Analyst** - Requirements analysis and business process modeling
- **Engineering Director** - Technical leadership and team management
- **Data Analyst** - Data analysis, visualization, and insights

#### Development & Quality

- **QA Platform Manager** - Quality assurance and testing strategies
- **Refactor Agent** - Code refactoring and optimization

#### UI/UX

- **UI/UX Master** - User interface and experience design

#### Specification Workflow

A complete specification development workflow with specialized agents:

- **Spec Orchestrator** - Coordinates the specification workflow
- **Spec Planner** - Plans specification structure and scope
- **Spec Architect** - Designs technical architecture for specifications
- **Spec Analyst** - Analyzes requirements and constraints
- **Spec Developer** - Develops detailed specifications
- **Spec Reviewer** - Reviews specifications for quality
- **Spec Validator** - Validates specifications against requirements
- **Spec Tester** - Tests specification implementations

**Installation:**
```bash
# Copy agents to project .claude directory
cp -r agents /path/to/your/project/.claude/
```

**Usage:**
Within Claude Code, reference agents using the Task tool or by mentioning them in your requests:
```
> I need help with frontend architecture
> Use the project-manager agent to break down this project
> Let's use the spec-orchestrator to plan our API specification
```

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

#### 2. Gemini Image Generator (`skills/gemini-image-generator/`)

Generate images using Google Gemini models (2.0 Flash & 3.0 Pro).

**Features:**
- Single image generation with customizable prompts
- Batch generation from text file prompts
- Support for multiple Gemini model versions
- Text rendering support (Pro model)
- Up to 14 reference images for editing (Pro model)

**Usage:**
```bash
# Single image
python generate_image.py --prompt "A modern tech banner" --output "banner.png"

# Batch generation
python batch_generate.py --config prompts.md --output-dir output/
```

**Dependencies:**
- google-genai
- pillow
- python-dotenv

[Full Documentation](skills/gemini-image-generator/SKILL.md)

#### 3. Markdown to PDF (`skills/markdown-to-pdf/`)

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

### Method 1: Plugin Marketplace (Recommended)

The easiest way to install these plugins is through Claude Code's built-in plugin system:

1. **Add the marketplace:**
   ```bash
   # Using GitHub repository
   /plugin marketplace add https://github.com/yonggao/claude-plugins

   # Or using local path
   /plugin marketplace add /path/to/claude-plugins
   ```

2. **Install plugins:**
   ```bash
   # Open interactive plugin manager
   /plugin

   # Or install specific plugins
   /plugin install html-to-pdf@claude-plugins
   /plugin install markdown-to-pdf@claude-plugins
   /plugin install team-analytics@claude-plugins
   /plugin install specialized-agents@claude-plugins
   /plugin install custom-statusline@claude-plugins
   ```

3. **Install dependencies:**
   ```bash
   # For HTML to PDF skill
   pip install playwright pillow pypdf
   playwright install chromium

   # For Markdown to PDF skill
   npm install -g @marp-team/marp-cli
   ```

4. **Verify installation:**
   ```bash
   # Check that commands are available
   /help
   ```

### Method 2: Manual Installation

If you prefer manual installation:

1. **Clone this repository:**
   ```bash
   git clone https://github.com/yonggao/claude-plugins.git
   cd claude-plugins
   ```

2. **Install components:**
   ```bash
   # Commands (project-specific)
   cp commands/*.md /path/to/your/project/.claude/commands/

   # Agents (project-specific)
   cp -r agents /path/to/your/project/.claude/

   # Skills (global)
   cp -r skills/html-to-pdf ~/.claude/skills/
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

### Team Setup

For team-wide plugin deployment, add to your project's `.claude/settings.json`:

```json
{
  "marketplaces": [
    {
      "path": "https://github.com/yonggao/claude-plugins"
    }
  ],
  "plugins": [
    {
      "name": "html-to-pdf",
      "marketplace": "claude-plugins"
    },
    {
      "name": "markdown-to-pdf",
      "marketplace": "claude-plugins"
    },
    {
      "name": "specialized-agents",
      "marketplace": "claude-plugins"
    }
  ]
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
├── commands/                          # Custom slash commands
│   ├── team_analytics.md              # Git team analytics
│   ├── agent-workflow.md              # Agent workflow orchestration
│   └── cii_daily_report.md            # CII daily reporting
├── agents/                            # Specialized AI agents
│   ├── chief-architect.md             # System architecture
│   ├── project-manager.md             # Project management
│   ├── data-analyst.md                # Data analysis
│   ├── frontend/                      # Frontend specialists
│   ├── backend/                       # Backend specialists
│   ├── spec-agents/                   # Specification workflow
│   ├── ui-ux/                         # UI/UX design
│   └── utility/                       # Utility agents
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
