# HTML to PDF/PNG Converter Skill

A Claude Code skill for converting HTML files to PDF and PNG formats.

## Installation

This skill is already installed in your `~/.claude/skills/html-to-pdf/` directory.

## Usage

Claude Code will automatically suggest using this skill when you ask questions like:

- "Convert this HTML to PDF"
- "Generate a PDF from the BP report"
- "Create a long image from this HTML"
- "Export this webpage as PDF"

## Manual Usage

You can also run the scripts directly:

```bash
# Convert HTML to single-page PDF (no page breaks)
python ~/.claude/skills/html-to-pdf/html_to_long_image.py your_file.html

# This will generate:
# - your_file_fullpage.png (screenshot)
# - your_file_fullpage.pdf (single-page PDF)
```

## Dependencies

The scripts will auto-install required dependencies:
- playwright
- Pillow
- pypdf

On first run, you may need to install Chromium:
```bash
playwright install chromium
```

## Output

The converter generates two files:
1. **PNG Screenshot**: Full-page screenshot as PNG image
2. **PDF Document**: Single-page PDF converted from the PNG

## Features

- ✅ No page breaks (single-page PDF)
- ✅ Preserves all CSS styling, gradients, and colors
- ✅ Handles Chinese/CJK characters
- ✅ Disables animations for complete rendering
- ✅ Auto-loads lazy content
- ✅ Zero margins for seamless appearance

## File Sizes

Typical output sizes:
- PNG: 6-10 MB
- PDF: 1-2 MB

## Troubleshooting

### Playwright browser not found
```bash
playwright install chromium
```

### Permission errors
```bash
chmod +x ~/.claude/skills/html-to-pdf/html_to_long_image.py
```

## Examples

```bash
# Example 1: Convert BP report
python ~/.claude/skills/html-to-pdf/html_to_long_image.py 202510_Alpha_Intelligence_BP.html

# Example 2: Convert with relative path
cd /path/to/your/project
python ~/.claude/skills/html-to-pdf/html_to_long_image.py report.html
```

## Quick Test

Test the skill is working:

```bash
# Create a simple test HTML
echo '<h1>Test</h1><p>Hello World</p>' > test.html

# Convert it
python ~/.claude/skills/html-to-pdf/html_to_long_image.py test.html

# Check outputs
ls -lh test_fullpage.*
```
