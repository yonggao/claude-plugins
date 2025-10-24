#!/usr/bin/env python3
"""
HTML转长图工具
将HTML渲染为一张完整的长图（PNG），然后可以转PDF
"""

import os
import sys
import time
from pathlib import Path


def html_to_long_image(html_path: str, output_path: str = None) -> str:
    """
    将HTML转换为一张完整的长图PNG。

    Args:
        html_path: HTML文件路径
        output_path: 输出图片路径（可选）

    Returns:
        生成的图片路径
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("正在安装 Playwright...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        from playwright.sync_api import sync_playwright

    if not os.path.exists(html_path):
        raise FileNotFoundError(f"HTML文件不存在: {html_path}")

    if output_path is None:
        html_file = Path(html_path)
        output_path = str(html_file.parent / f"{html_file.stem}_fullpage.png")

    print(f"\n📄 转换HTML为完整长图")
    print(f"   输入: {Path(html_path).name}")
    print(f"   输出: {Path(output_path).name}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1200, 'height': 800})

        # 加载HTML
        html_path_abs = str(Path(html_path).absolute())
        print("⏳ 加载HTML...")
        page.goto(f'file://{html_path_abs}', wait_until='networkidle')

        # 禁用所有动画
        print("🎨 禁用动画...")
        page.add_style_tag(content="""
            *, *::before, *::after {
                animation: none !important;
                transition: none !important;
            }
            .section, .cover {
                opacity: 1 !important;
                transform: none !important;
            }
        """)

        # 强制显示所有内容
        page.evaluate("""
            () => {
                document.querySelectorAll('.section, .cover').forEach(el => {
                    el.style.opacity = '1';
                    el.style.transform = 'none';
                });
            }
        """)

        # 滚动加载
        print("📜 加载所有内容...")
        total_height = page.evaluate("document.body.scrollHeight")
        for y in range(0, total_height, 1000):
            page.evaluate(f"window.scrollTo(0, {y})")
            time.sleep(0.1)

        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(0.5)

        # 截取完整页面
        print("📸 截取完整页面...")
        page.screenshot(path=output_path, full_page=True)

        browser.close()

    size_kb = os.path.getsize(output_path) / 1024
    print(f"\n✅ 成功生成长图！")
    print(f"   大小: {size_kb:.1f} KB\n")

    return str(output_path)


def image_to_pdf(image_path: str, pdf_path: str = None) -> str:
    """
    将图片转换为PDF。

    Args:
        image_path: 图片路径
        pdf_path: PDF输出路径（可选）

    Returns:
        生成的PDF路径
    """
    try:
        from PIL import Image
    except ImportError:
        print("正在安装 Pillow...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "-q"])
        from PIL import Image

    if pdf_path is None:
        image_file = Path(image_path)
        pdf_path = str(image_file.with_suffix('.pdf'))

    print(f"📄 转换图片为PDF: {Path(pdf_path).name}")

    # 打开图片并转换为PDF
    image = Image.open(image_path)

    # 转换为RGB（PDF需要）
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # 保存为PDF
    image.save(pdf_path, 'PDF', resolution=100.0)

    size_kb = os.path.getsize(pdf_path) / 1024
    print(f"✅ PDF生成成功！大小: {size_kb:.1f} KB\n")

    return str(pdf_path)


def main():
    default_html = "202510_Alpha_Intelligence_BP.html"
    html_path = sys.argv[1] if len(sys.argv) > 1 else default_html

    print("\n" + "=" * 70)
    print("HTML转完整长图工具 - 无分页断开")
    print("=" * 70)

    try:
        # 生成长图
        image_path = html_to_long_image(html_path)

        # 转换为PDF
        pdf_path = image_to_pdf(image_path)

        print(f"💡 打开查看:")
        print(f"   长图: open {Path(image_path).name}")
        print(f"   PDF:  open {Path(pdf_path).name}\n")

    except Exception as e:
        print(f"\n❌ 错误: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
