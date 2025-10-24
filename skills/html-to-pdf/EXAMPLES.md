# Usage Examples

## Real-World Examples

### Example 1: Business Plan Report
```bash
# Original file: 202510_Alpha_Intelligence_BP.html (71 KB)
python ~/.claude/skills/html-to-pdf/html_to_long_image.py 202510_Alpha_Intelligence_BP.html

# Output:
# - 202510_Alpha_Intelligence_BP_fullpage.png (6.1 MB)
# - 202510_Alpha_Intelligence_BP_fullpage.pdf (1.6 MB, 1 page)
```

**Result**: Single-page PDF with no page breaks, perfect for online presentation!

### Example 2: Simple Test
```bash
# Create test HTML
echo '<h1>Test</h1><p>Hello World</p>' > test.html

# Convert
python ~/.claude/skills/html-to-pdf/html_to_long_image.py test.html

# Output:
# - test_fullpage.png (12 KB)
# - test_fullpage.pdf (20 KB)
```

### Example 3: Multi-File Batch Conversion
```bash
# Convert all HTML files in a directory
cd /path/to/html/files

for file in *.html; do
    echo "Converting $file..."
    python ~/.claude/skills/html-to-pdf/html_to_long_image.py "$file"
done

# Check results
ls -lh *_fullpage.pdf
```

### Example 4: With Custom Path
```bash
# Specify full paths
python ~/.claude/skills/html-to-pdf/html_to_long_image.py \
    /Users/yonggao/Documents/report.html
```

## Integration Examples

### Use in Shell Script
```bash
#!/bin/bash
# convert_reports.sh

HTML_CONVERTER=~/.claude/skills/html-to-pdf/html_to_long_image.py

for report in reports/*.html; do
    python "$HTML_CONVERTER" "$report"
    echo "✓ Converted: $report"
done

echo "All reports converted!"
```

### Use in Makefile
```makefile
# Makefile
CONVERTER = python ~/.claude/skills/html-to-pdf/html_to_long_image.py

%.pdf: %.html
	$(CONVERTER) $<

all: report.pdf presentation.pdf

clean:
	rm -f *_fullpage.pdf *_fullpage.png
```

### Use in Python Script
```python
import subprocess
import sys

def convert_html_to_pdf(html_file):
    """Convert HTML to PDF using the skill."""
    converter = "~/.claude/skills/html-to-pdf/html_to_long_image.py"
    result = subprocess.run(
        [sys.executable, converter, html_file],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

# Usage
if convert_html_to_pdf("report.html"):
    print("Success!")
```

## Comparison with Original Files

| File | Type | Size | Pages | Notes |
|------|------|------|-------|-------|
| 202510_Alpha_Intelligence_BP.html | HTML | 71 KB | - | Source file |
| 202510_Alpha_Intelligence_BP_fullpage.png | PNG | 6.1 MB | 1 | High-quality screenshot |
| 202510_Alpha_Intelligence_BP_fullpage.pdf | PDF | 1.6 MB | 1 | **Best for viewing** |
| 202510_Alpha_Intelligence_BP_final.pdf | PDF | 5.7 MB | 22 | Multi-page (with breaks) |

## Performance Data

Based on real usage:

| HTML Size | Processing Time | PNG Size | PDF Size |
|-----------|----------------|----------|----------|
| 71 KB | ~5 seconds | 6.1 MB | 1.6 MB |
| 5 KB | ~3 seconds | 12 KB | 20 KB |
| 200 KB | ~8 seconds | 15 MB | 4 MB |

## Tips & Tricks

### Optimize for File Size
The PNG is always larger than the PDF. If you only need the PDF:
```bash
# Generate both, then delete PNG
python ~/.claude/skills/html-to-pdf/html_to_long_image.py report.html
rm report_fullpage.png
```

### Preview Before Converting
```bash
# Open HTML in browser first
open report.html

# Then convert
python ~/.claude/skills/html-to-pdf/html_to_long_image.py report.html
```

### Auto-open Result
```bash
python ~/.claude/skills/html-to-pdf/html_to_long_image.py report.html && \
    open report_fullpage.pdf
```

### Check Page Count
```bash
python -c "
from pypdf import PdfReader
r = PdfReader('report_fullpage.pdf')
print(f'Pages: {len(r.pages)}')
"
```

## Troubleshooting Examples

### Problem: Script not found
```bash
# Solution: Use full path
python ~/.claude/skills/html-to-pdf/html_to_long_image.py file.html
```

### Problem: Permission denied
```bash
# Solution: Make executable
chmod +x ~/.claude/skills/html-to-pdf/html_to_long_image.py
```

### Problem: Playwright not installed
```bash
# Solution: Install dependencies
pip install playwright pillow pypdf
playwright install chromium
```

### Problem: Content appears cut off
```bash
# This is automatically handled by the script which:
# 1. Scrolls through entire page
# 2. Waits for animations
# 3. Forces all content visible
# No action needed!
```
