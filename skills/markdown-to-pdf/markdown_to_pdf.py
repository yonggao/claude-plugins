#!/usr/bin/env python3
"""
Markdown to PDF Converter
Converts Markdown files directly to PDF with proper formatting and syntax highlighting.
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """Check and install required dependencies."""
    required = {
        'markdown': 'markdown',
        'weasyprint': 'weasyprint',
        'pygments': 'pygments'
    }

    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"📦 Installing missing dependencies: {', '.join(missing)}")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
        print("✅ Dependencies installed!\n")

check_dependencies()

import markdown
from weasyprint import HTML, CSS
from markdown.extensions import fenced_code, tables, codehilite, toc

def get_css_style():
    """Return CSS styling for the PDF."""
    return """
    @page {
        size: A4;
        margin: 2cm;
    }

    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #333;
        max-width: 100%;
    }

    h1, h2, h3, h4, h5, h6 {
        font-weight: 600;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
        color: #000;
        page-break-after: avoid;
    }

    h1 {
        font-size: 24pt;
        border-bottom: 2px solid #eee;
        padding-bottom: 0.3em;
    }

    h2 {
        font-size: 20pt;
        border-bottom: 1px solid #eee;
        padding-bottom: 0.3em;
    }

    h3 { font-size: 16pt; }
    h4 { font-size: 14pt; }
    h5 { font-size: 12pt; }
    h6 { font-size: 11pt; }

    p {
        margin: 0.8em 0;
    }

    a {
        color: #0366d6;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }

    code {
        font-family: "SF Mono", Monaco, Menlo, Consolas, "Courier New", monospace;
        font-size: 9.5pt;
        background-color: #f6f8fa;
        padding: 0.2em 0.4em;
        border-radius: 3px;
    }

    pre {
        background-color: #f6f8fa;
        padding: 1em;
        border-radius: 5px;
        overflow-x: auto;
        page-break-inside: avoid;
        margin: 1em 0;
    }

    pre code {
        background-color: transparent;
        padding: 0;
        font-size: 9pt;
    }

    blockquote {
        margin: 1em 0;
        padding-left: 1em;
        border-left: 4px solid #ddd;
        color: #666;
    }

    ul, ol {
        margin: 0.8em 0;
        padding-left: 2em;
    }

    li {
        margin: 0.3em 0;
    }

    table {
        border-collapse: collapse;
        width: 100%;
        margin: 1em 0;
        page-break-inside: avoid;
    }

    th, td {
        border: 1px solid #ddd;
        padding: 0.5em 0.8em;
        text-align: left;
    }

    th {
        background-color: #f6f8fa;
        font-weight: 600;
    }

    tr:nth-child(even) {
        background-color: #f9f9f9;
    }

    img {
        max-width: 100%;
        height: auto;
        display: block;
        margin: 1em 0;
    }

    hr {
        border: none;
        border-top: 1px solid #eee;
        margin: 2em 0;
    }

    /* Syntax highlighting styles */
    .codehilite {
        background-color: #f6f8fa;
        border-radius: 5px;
        padding: 1em;
        margin: 1em 0;
        page-break-inside: avoid;
    }

    .codehilite .hll { background-color: #ffffcc }
    .codehilite .c { color: #6a737d; font-style: italic } /* Comment */
    .codehilite .k { color: #d73a49; font-weight: bold } /* Keyword */
    .codehilite .o { color: #d73a49 } /* Operator */
    .codehilite .cm { color: #6a737d; font-style: italic } /* Comment.Multiline */
    .codehilite .cp { color: #d73a49; font-weight: bold } /* Comment.Preproc */
    .codehilite .c1 { color: #6a737d; font-style: italic } /* Comment.Single */
    .codehilite .cs { color: #6a737d; font-style: italic } /* Comment.Special */
    .codehilite .kc { color: #005cc5; font-weight: bold } /* Keyword.Constant */
    .codehilite .kd { color: #d73a49; font-weight: bold } /* Keyword.Declaration */
    .codehilite .kn { color: #d73a49; font-weight: bold } /* Keyword.Namespace */
    .codehilite .kp { color: #d73a49; font-weight: bold } /* Keyword.Pseudo */
    .codehilite .kr { color: #d73a49; font-weight: bold } /* Keyword.Reserved */
    .codehilite .kt { color: #d73a49; font-weight: bold } /* Keyword.Type */
    .codehilite .m { color: #005cc5 } /* Literal.Number */
    .codehilite .s { color: #032f62 } /* Literal.String */
    .codehilite .na { color: #6f42c1 } /* Name.Attribute */
    .codehilite .nb { color: #005cc5 } /* Name.Builtin */
    .codehilite .nc { color: #6f42c1; font-weight: bold } /* Name.Class */
    .codehilite .nf { color: #6f42c1; font-weight: bold } /* Name.Function */
    .codehilite .nn { color: #6f42c1 } /* Name.Namespace */
    .codehilite .nt { color: #22863a } /* Name.Tag */
    .codehilite .nv { color: #e36209 } /* Name.Variable */
    """

def convert_markdown_to_pdf(input_file, output_file=None):
    """Convert Markdown file to PDF."""

    # Validate input file
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file '{input_file}' not found!")
        return False

    # Determine output file
    if output_file is None:
        output_file = Path(input_file).with_suffix('.pdf')

    print("=" * 70)
    print("Markdown转PDF工具")
    print("=" * 70)
    print(f"\n📄 转换Markdown为PDF")
    print(f"   输入: {input_file}")
    print(f"   输出: {output_file}\n")

    try:
        # Read markdown file
        print("⏳ 读取Markdown文件...")
        with open(input_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Convert markdown to HTML with extensions
        print("🔄 转换Markdown为HTML...")
        md = markdown.Markdown(extensions=[
            'fenced_code',
            'tables',
            'codehilite',
            'toc',
            'nl2br',
            'sane_lists'
        ], extension_configs={
            'codehilite': {
                'css_class': 'codehilite',
                'linenums': False,
                'guess_lang': True
            }
        })

        html_content = md.convert(md_content)

        # Wrap in HTML document
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{Path(input_file).stem}</title>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        # Convert HTML to PDF
        print("📄 生成PDF...")
        HTML(string=full_html, base_url=str(Path(input_file).parent.absolute())).write_pdf(
            output_file,
            stylesheets=[CSS(string=get_css_style())]
        )

        # Get file size
        size_kb = os.path.getsize(output_file) / 1024

        print(f"\n✅ 成功生成PDF！")
        print(f"   大小: {size_kb:.1f} KB")
        print(f"\n💡 打开查看:")
        print(f"   open {output_file}")

        return True

    except Exception as e:
        print(f"\n❌ 转换失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python markdown_to_pdf.py input.md [output.pdf]")
        print("\nExamples:")
        print("  python markdown_to_pdf.py README.md")
        print("  python markdown_to_pdf.py docs.md custom_output.pdf")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    success = convert_markdown_to_pdf(input_file, output_file)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
