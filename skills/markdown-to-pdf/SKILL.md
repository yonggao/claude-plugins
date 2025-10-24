# Markdown to PDF Converter Skill

This skill helps you convert Markdown files to PDF format with support for both document-style and presentation-style outputs using Marp.

## When to Use This Skill

Use this skill when the user wants to:
- Convert Markdown (.md) files to PDF presentations
- Generate slide decks from Markdown
- Create professional PDFs from documentation
- Export README files as PDFs
- Generate presentation-ready slides with Marp themes

## Available Conversion Methods

### Method 1: Marp Presentation (Recommended)
Best for: Presentations, slide decks, visual content

**Command:**
```bash
python marp_to_pdf.py input.md
```

**Features:**
- Beautiful presentation slides from Markdown
- Multiple built-in themes (default, gaia, uncover)
- Automatic slide breaks with `---`
- Support for presenter notes
- Code syntax highlighting
- Chinese/CJK character support
- Outputs: `input.pdf`

### Method 2: Marp with Custom Theme
Best for: Branded presentations, custom styling

**Command:**
```bash
python marp_to_pdf.py input.md --theme gaia
```

**Supported Themes:**
- `default` - Clean and simple
- `gaia` - Modern and colorful
- `uncover` - Minimalist and elegant

## Required Dependencies

The skill requires Marp CLI via npm:

```bash
# Install Node.js first (if not installed)
# Then install Marp CLI globally
npm install -g @marp-team/marp-cli

# Or use npx (no installation needed)
npx @marp-team/marp-cli --version
```

## Marp Markdown Syntax

### Basic Slide Structure

```markdown
---
marp: true
theme: default
---

# Title Slide

Your presentation content

---

## Second Slide

- Bullet point 1
- Bullet point 2

---

## Code Example

\`\`\`python
def hello():
    print("Hello, World!")
\`\`\`
```

### Slide Directives

```markdown
<!-- _class: lead -->
# Centered Title Slide

<!-- _class: invert -->
## Inverted Color Slide

<!-- backgroundColor: #123456 -->
## Custom Background
```

### Presenter Notes

```markdown
## Slide Title

Slide content here

<!--
These are presenter notes
They won't appear in the PDF
-->
```

## Step-by-Step Instructions

### For Standard Marp Presentation:

1. **Create Markdown file with Marp frontmatter:**
   ```markdown
   ---
   marp: true
   theme: default
   ---

   # Your Title

   ---

   ## Content
   ```

2. **Run the converter:**
   ```bash
   python ~/.claude/skills/markdown-to-pdf/marp_to_pdf.py presentation.md
   ```

3. **Open the result:**
   ```bash
   open presentation.pdf
   ```

### For Custom Themed Presentation:

1. **Run with theme option:**
   ```bash
   python ~/.claude/skills/markdown-to-pdf/marp_to_pdf.py slides.md --theme gaia
   ```

2. **View the PDF:**
   ```bash
   open slides.pdf
   ```

## Supported Markdown Features

✅ **Headers** (slide titles)
✅ **Bold, Italic, Strikethrough**
✅ **Lists** (ordered, unordered, nested)
✅ **Code blocks** with syntax highlighting
✅ **Inline code**
✅ **Tables**
✅ **Images** (auto-scaled to fit slides)
✅ **Links**
✅ **Blockquotes**
✅ **Math equations** (KaTeX)
✅ **Emojis** 😊
✅ **Slide backgrounds**
✅ **Custom CSS**
✅ **Chinese/CJK characters**

## Marp-Specific Features

### Two-Column Layout

```markdown
<div class="columns">
<div>

## Left Column

Content here

</div>
<div>

## Right Column

Content here

</div>
</div>
```

### Image Sizing

```markdown
![width:500px](image.png)
![height:300px](image.png)
![bg](background-image.png)
```

### Slide Backgrounds

```markdown
![bg](background.jpg)
![bg left](left-background.jpg)
![bg right](right-background.jpg)
```

## Troubleshooting

### Issue: Marp CLI not found

**Solution:**
```bash
npm install -g @marp-team/marp-cli
# Or use npx without installation
npx @marp-team/marp-cli --version
```

### Issue: Slides not breaking correctly

**Solution:** Ensure you use `---` to separate slides:
```markdown
# Slide 1

---

# Slide 2
```

### Issue: Theme not applied

**Solution:** Add Marp frontmatter at the top:
```markdown
---
marp: true
theme: gaia
---
```

### Issue: Chinese characters not displaying

**Solution:** Marp automatically handles system fonts for CJK characters.

## Output Files

After conversion, you'll get:

**Marp Method:**
- `filename.pdf` - Presentation-style PDF with slides

**Optional HTML output:**
- `filename.html` - Interactive HTML presentation

## Best Practices

1. **For presentations:** Use Marp with clear slide breaks
   - One main idea per slide
   - Use `---` to separate slides
   - Choose appropriate theme

2. **For code demonstrations:**
   - Use syntax highlighting with language tags
   - Keep code snippets concise per slide

3. **For visual impact:**
   - Use background images
   - Apply custom themes
   - Use the `_class: lead` for title slides

## Examples

### Example 1: Simple Presentation
```bash
python ~/.claude/skills/markdown-to-pdf/marp_to_pdf.py slides.md
# Output: slides.pdf
```

### Example 2: Gaia Theme Presentation
```bash
python ~/.claude/skills/markdown-to-pdf/marp_to_pdf.py slides.md --theme gaia
```

### Example 3: Generate HTML and PDF
```bash
python ~/.claude/skills/markdown-to-pdf/marp_to_pdf.py slides.md --html
# Output: slides.pdf and slides.html
```

### Example 4: Batch Convert Multiple Presentations
```bash
for file in *.md; do
    python ~/.claude/skills/markdown-to-pdf/marp_to_pdf.py "$file"
done
```

## Sample Marp Markdown

```markdown
---
marp: true
theme: gaia
paginate: true
---

<!-- _class: lead -->

# My Presentation
## Subtitle Here

Your Name
Date

---

## Agenda

1. Introduction
2. Main Content
3. Conclusion

---

## Code Example

\`\`\`python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
\`\`\`

---

<!-- _class: lead -->

# Thank You!

Questions?
```

## Performance Expectations

- **Processing Speed**: ~2-5 seconds for typical presentations
- **Memory Usage**: ~100-200 MB during conversion
- **PDF File Size**: 500KB - 5MB depending on images

## Success Criteria

A successful conversion should:
1. ✅ Generate PDF without errors
2. ✅ Create proper slide breaks
3. ✅ Apply theme correctly
4. ✅ Display code with syntax highlighting
5. ✅ Handle Chinese/CJK characters correctly
6. ✅ Scale images appropriately
7. ✅ Maintain visual consistency

## Quick Reference

| Need | Command | Output |
|------|---------|--------|
| Default theme | `marp_to_pdf.py file.md` | PDF with default theme |
| Gaia theme | `marp_to_pdf.py file.md --theme gaia` | PDF with Gaia theme |
| Uncover theme | `marp_to_pdf.py file.md --theme uncover` | PDF with Uncover theme |
| HTML output | `marp_to_pdf.py file.md --html` | PDF + HTML presentation |

## Additional Resources

- [Marp Official Documentation](https://marp.app/)
- [Marp CLI Documentation](https://github.com/marp-team/marp-cli)
- [Marp Themes Gallery](https://github.com/marp-team/marp-core/tree/main/themes)
