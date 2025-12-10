#!/usr/bin/env python3
"""
Gemini Nano Banana Image Generator

Generate images using Google's Gemini 2.5 Flash Image model (Nano Banana).

Usage:
    python generate_image.py --prompt "Your description" --output "output.png"

Requirements:
    pip install google-genai pillow python-dotenv

Environment:
    GEMINI_API_KEY=your-api-key
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai not installed. Run: pip install google-genai")
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("Error: pillow not installed. Run: pip install pillow")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


# Model configuration
MODEL_ID = "gemini-2.5-flash-image"  # Nano Banana model (image generation)
MODEL_ID_PREVIEW = "gemini-2.5-flash-image-preview"  # Nano Banana Preview
MODEL_ID_PRO = "gemini-3-pro-image-preview"  # Nano Banana Pro (better text rendering)


def get_api_key() -> str:
    """Get Gemini API key from environment."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY or GOOGLE_API_KEY environment variable not set.")
        print("Get your API key from: https://aistudio.google.com/app/apikey")
        sys.exit(1)
    return api_key


def generate_image(
    prompt: str,
    output_path: str,
    model: str = MODEL_ID,
    reference_image: str = None,
    reference_images: list = None,
    aspect_ratio: str = None,
) -> str:
    """
    Generate an image using Gemini Nano Banana model.

    Args:
        prompt: Text description of the image to generate
        output_path: Path to save the generated image
        model: Model ID to use
        reference_image: Optional path to reference image for editing (single)
        reference_images: Optional list of paths to reference images (multiple)
        aspect_ratio: Optional aspect ratio (e.g., "9:16", "16:9", "1:1")

    Returns:
        Path to the saved image on success, or error message on failure
    """
    api_key = get_api_key()

    # Initialize client
    client = genai.Client(api_key=api_key)

    # Prepare contents - images first, then prompt
    contents = []

    # Collect all reference images
    all_ref_images = []
    if reference_images:
        all_ref_images.extend(reference_images)
    if reference_image:
        all_ref_images.append(reference_image)

    # Add all reference images first
    for i, img_path in enumerate(all_ref_images):
        if img_path and os.path.exists(img_path):
            try:
                ref_img = Image.open(img_path)
                contents.append(ref_img)
                print(f"Using reference image {i+1}: {img_path}")
            except Exception as e:
                print(f"Warning: Could not load reference image {img_path}: {e}")

    # Add prompt after images
    contents.append(prompt)

    if aspect_ratio:
        print(f"Aspect ratio: {aspect_ratio}")

    print(f"Generating image with model: {model}")
    print(f"Prompt: {prompt[:100]}...")

    try:
        # Generate content
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            ),
        )

        # Process response
        image_saved = False
        text_response = []

        for part in response.candidates[0].content.parts:
            if hasattr(part, 'text') and part.text:
                text_response.append(part.text)
            elif hasattr(part, 'inline_data') and part.inline_data:
                # Save image
                output_dir = os.path.dirname(output_path)
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)

                # Get image data
                image_data = part.inline_data.data
                mime_type = part.inline_data.mime_type

                # Determine file extension
                ext = ".png"
                if "jpeg" in mime_type or "jpg" in mime_type:
                    ext = ".jpg"
                elif "webp" in mime_type:
                    ext = ".webp"

                # Ensure correct extension
                if not output_path.lower().endswith(ext):
                    base = os.path.splitext(output_path)[0]
                    output_path = f"{base}{ext}"

                # Save image bytes
                with open(output_path, "wb") as f:
                    f.write(image_data)

                image_saved = True
                print(f"Image saved to: {output_path}")

        if text_response:
            print(f"Model response: {' '.join(text_response)}")

        if image_saved:
            return output_path
        else:
            return "Error: No image was generated. The model may have returned only text."

    except Exception as e:
        error_msg = str(e)
        if "SAFETY" in error_msg.upper() or "BLOCKED" in error_msg.upper():
            return f"Error: Content blocked by safety filters. Try modifying your prompt.\nDetails: {error_msg}"
        elif "API_KEY" in error_msg.upper() or "AUTHENTICATION" in error_msg.upper():
            return f"Error: API key issue. Check your GEMINI_API_KEY.\nDetails: {error_msg}"
        else:
            return f"Error: {error_msg}"


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Gemini Nano Banana model"
    )
    parser.add_argument(
        "--prompt", "-p",
        type=str,
        required=True,
        help="Text description of the image to generate"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Output file path (default: output/image_TIMESTAMP.png)"
    )
    parser.add_argument(
        "--model", "-m",
        type=str,
        default=MODEL_ID,
        choices=[MODEL_ID, MODEL_ID_PREVIEW, MODEL_ID_PRO],
        help=f"Model to use (default: {MODEL_ID})"
    )
    parser.add_argument(
        "--reference", "-r",
        type=str,
        action="append",
        default=None,
        help="Reference image for editing/style transfer (can be used multiple times)"
    )
    parser.add_argument(
        "--aspect-ratio", "-a",
        type=str,
        default=None,
        help="Aspect ratio (e.g., '9:16', '16:9', '1:1')"
    )

    args = parser.parse_args()

    # Generate default output path if not provided
    if args.output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("output", exist_ok=True)
        args.output = f"output/image_{timestamp}.png"

    # Generate image
    result = generate_image(
        prompt=args.prompt,
        output_path=args.output,
        model=args.model,
        reference_images=args.reference,
        aspect_ratio=args.aspect_ratio,
    )

    print(f"\nResult: {result}")

    # Return exit code
    if result.startswith("Error"):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
