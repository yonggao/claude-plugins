# Quick Start Guide

## One-Line Usage

```bash
python ~/.claude/skills/html-to-pdf/html_to_long_image.py your_file.html
```

## What You Get

- `your_file_fullpage.png` - Complete screenshot
- `your_file_fullpage.pdf` - Single-page PDF (no page breaks!)

## Common Tasks

### Convert HTML in current directory
```bash
python ~/.claude/skills/html-to-pdf/html_to_long_image.py report.html
```

### Convert and open immediately
```bash
python ~/.claude/skills/html-to-pdf/html_to_long_image.py report.html && open report_fullpage.pdf
```

### Batch convert all HTML files
```bash
for file in *.html; do
    python ~/.claude/skills/html-to-pdf/html_to_long_image.py "$file"
done
```

## Tips

1. **For presentations**: Use the PDF output (smaller, 1-2 MB)
2. **For high-quality images**: Use the PNG output (6-10 MB)
3. **First-time setup**: Run `playwright install chromium` once

## Comparison

| Method | Pages | Size | Best For |
|--------|-------|------|----------|
| Long Image (this skill) | 1 page | 1-2 MB | Online viewing, presentations |
| Standard A4 | 20+ pages | 5-6 MB | Printing, archiving |

## Success!

If you see this output, it worked:
```
✅ 成功生成长图！
   大小: 6263.9 KB

✅ PDF生成成功！大小: 1632.6 KB

💡 打开查看:
   长图: open your_file_fullpage.png
   PDF:  open your_file_fullpage.pdf
```
