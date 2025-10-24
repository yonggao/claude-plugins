#!/usr/bin/env python3
"""
Marp Markdown to PDF Converter
Converts Markdown files to beautiful presentation PDFs using Marp CLI.
"""

import sys
import os
import subprocess
import shutil
from pathlib import Path
import argparse

def check_marp_cli():
    """Check if Marp CLI is installed."""
    # Try marp-cli
    if shutil.which('marp'):
        return 'marp'

    # Try npx
    if shutil.which('npx'):
        try:
            result = subprocess.run(
                ['npx', '@marp-team/marp-cli', '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return 'npx'
        except:
            pass

    return None

def install_instructions():
    """Print installation instructions."""
    print("\n❌ Marp CLI not found!")
    print("\n请安装Marp CLI:")
    print("\n方法1: 使用npm全局安装")
    print("  npm install -g @marp-team/marp-cli")
    print("\n方法2: 使用npx (无需安装)")
    print("  npx @marp-team/marp-cli --version")
    print("\n方法3: 使用Homebrew (macOS)")
    print("  brew install marp-cli")
    print()

def convert_markdown_to_pdf(input_file, output_file=None, theme='default', html_output=False):
    """Convert Markdown to PDF using Marp."""

    # Validate input file
    if not os.path.exists(input_file):
        print(f"❌ 错误: 输入文件 '{input_file}' 不存在!")
        return False

    # Check Marp CLI
    marp_cmd = check_marp_cli()
    if not marp_cmd:
        install_instructions()
        return False

    # Determine output file
    if output_file is None:
        output_file = Path(input_file).with_suffix('.pdf')

    print("=" * 70)
    print("Marp Markdown转PDF工具")
    print("=" * 70)
    print(f"\n📄 转换Markdown为演示文稿PDF")
    print(f"   输入: {input_file}")
    print(f"   输出: {output_file}")
    print(f"   主题: {theme}\n")

    try:
        # Build Marp command
        if marp_cmd == 'marp':
            cmd = ['marp']
        else:  # npx
            cmd = ['npx', '@marp-team/marp-cli']

        cmd.extend([
            input_file,
            '--pdf',
            '--allow-local-files',
            '--theme', theme,
            '-o', str(output_file)
        ])

        # Run Marp conversion
        print("⏳ 生成PDF...")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            print(f"❌ 转换失败!")
            print(f"错误信息: {result.stderr}")
            return False

        # Get file size
        if os.path.exists(output_file):
            size_kb = os.path.getsize(output_file) / 1024
            print(f"\n✅ 成功生成PDF!")
            print(f"   大小: {size_kb:.1f} KB")

        # Generate HTML if requested
        if html_output:
            html_file = Path(output_file).with_suffix('.html')
            print(f"\n📄 生成HTML版本...")

            html_cmd = cmd.copy()
            # Remove --pdf and change output
            html_cmd = [c for c in html_cmd if c != '--pdf']
            html_cmd[-1] = str(html_file)

            result = subprocess.run(
                html_cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0 and os.path.exists(html_file):
                html_size_kb = os.path.getsize(html_file) / 1024
                print(f"✅ HTML生成成功!")
                print(f"   大小: {html_size_kb:.1f} KB")
                print(f"\n💡 打开查看:")
                print(f"   PDF:  open {output_file}")
                print(f"   HTML: open {html_file}")
            else:
                print(f"\n💡 打开查看:")
                print(f"   PDF:  open {output_file}")
        else:
            print(f"\n💡 打开查看:")
            print(f"   open {output_file}")

        return True

    except subprocess.TimeoutExpired:
        print("\n❌ 转换超时!")
        return False
    except Exception as e:
        print(f"\n❌ 转换失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def ensure_marp_frontmatter(input_file):
    """Check if Markdown has Marp frontmatter, add if missing."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has marp frontmatter
    if content.startswith('---\nmarp:') or 'marp: true' in content[:100]:
        return False  # Already has frontmatter

    # Add Marp frontmatter
    frontmatter = """---
marp: true
theme: default
paginate: true
---

"""

    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)

    return True  # Added frontmatter

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Convert Markdown to PDF presentation using Marp'
    )
    parser.add_argument('input', help='Input Markdown file')
    parser.add_argument('output', nargs='?', help='Output PDF file (optional)')
    parser.add_argument(
        '--theme',
        choices=['default', 'gaia', 'uncover'],
        default='default',
        help='Marp theme to use'
    )
    parser.add_argument(
        '--html',
        action='store_true',
        help='Also generate HTML output'
    )
    parser.add_argument(
        '--add-frontmatter',
        action='store_true',
        help='Add Marp frontmatter if missing'
    )

    args = parser.parse_args()

    # Add frontmatter if requested
    if args.add_frontmatter:
        if ensure_marp_frontmatter(args.input):
            print("✅ 已添加Marp前置元数据\n")

    success = convert_markdown_to_pdf(
        args.input,
        args.output,
        args.theme,
        args.html
    )

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
