#!/usr/bin/env python3
"""
Batch Image Generator for Fiverr Gigs

Generate multiple images from a configuration file using Gemini Nano Banana.

Usage:
    python batch_generate.py --config prompts.json --output-dir output/fiverr

Requirements:
    pip install google-genai pillow python-dotenv

Configuration file format (JSON):
{
    "images": [
        {
            "name": "ai_agent_1",
            "prompt": "Your detailed prompt here",
            "category": "ai-agent-gig"
        }
    ]
}
"""

import argparse
import json
import os
import sys
import time
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
    pass


# Model configuration
MODEL_ID = "gemini-3-pro-image-preview"  # Nano Banana Pro (better text, 16:9 output)
MODEL_ID_FLASH = "gemini-2.5-flash-image"  # Nano Banana Flash (faster, square output)

# Fiverr image prompts
FIVERR_PROMPTS = {
    "profile_banner": {
        "name": "profile_banner",
        "prompt": """Create a professional banner image for a tech consulting agency called Guang Digital.
Design elements: Modern, clean dark blue and white color scheme.
Abstract tech patterns with circuits, nodes, and data flow lines in the background.
Subtle AI and technology icons floating: brain icon, code brackets, cloud, gear.
Professional and premium feel, corporate tech aesthetic similar to McKinsey or Accenture.
High contrast, suitable for text overlay. Landscape orientation 16:9 aspect ratio.""",
        "category": "profile"
    },
    "ai_agent_1": {
        "name": "ai_agent_architecture",
        "prompt": """Create a professional technical illustration showing an AI agent system architecture.
Central brain icon representing Claude AI in the middle.
Connected nodes showing the flow: User Input on left, AI Agent Processing in center,
Knowledge Base (visualized as geometric shapes with data points) below,
and Response Output on right.
Use modern tech color palette: deep blue (#1E40AF), electric purple (#7C3AED),
cyan accents (#06B6D4).
Clean dark gradient background (#0F172A to #1E293B).
Professional enterprise-grade aesthetic with glowing connection lines.
Include subtle RAG flow arrows. Landscape 16:9 aspect ratio.""",
        "category": "ai-agent-gig"
    },
    "ai_agent_2": {
        "name": "multi_agent_system",
        "prompt": """Create a visualization of a multi-agent AI system for enterprise use.
Four different AI agent icons arranged in a diamond pattern, each with different colors:
Blue agent for Analysis, Purple agent for Search, Teal agent for Response, Orange agent for Learning.
All agents connected to a central orchestration hub with glowing lines.
Modern glassmorphism UI elements floating around.
Dark mode background with subtle grid pattern.
Data flow lines connecting agents in a network pattern.
Professional corporate tech style, futuristic but not sci-fi.
Landscape 16:9 aspect ratio.""",
        "category": "ai-agent-gig"
    },
    "ai_agent_3": {
        "name": "rag_knowledge_system",
        "prompt": """Create a technical illustration of a RAG (Retrieval Augmented Generation) knowledge system.
Left side: Stack of document and file icons representing source materials.
Center: Arrow flowing into a 3D cube visualization of a Vector Database with floating data points inside.
Center-right: Large AI brain icon processing the information.
Right side: Chat bubble and response interface.
Color scheme: Professional blue (#1E40AF), white, with gold/orange (#F59E0B) accents for highlights.
Clean modern infographic style with enterprise software feel.
Subtle floating keywords: Semantic Search, Knowledge Base, 150K+ Documents.
Landscape 16:9 aspect ratio.""",
        "category": "ai-agent-gig"
    },
    "fullstack_1": {
        "name": "fullstack_architecture",
        "prompt": """Create a professional full-stack web development architecture diagram.
Three-tier architecture visualization arranged vertically:
Top tier: Frontend layer with React logo, browser window, and mobile phone icons.
Middle tier: API Gateway and Backend with server icons, Python and Node.js logos.
Bottom tier: Database layer with PostgreSQL elephant, MongoDB leaf, and Redis icons.
Bidirectional arrows connecting all tiers with glowing blue lines.
Cloud icons (AWS orange, Azure blue) floating in the background corners.
Modern dark theme (#0F172A) with gradient background.
Professional enterprise aesthetic. Landscape 16:9 aspect ratio.""",
        "category": "fullstack-gig"
    },
    "fullstack_2": {
        "name": "web_dashboard",
        "prompt": """Create a mockup showing a modern web application admin dashboard.
Sleek dark mode UI design with multiple panels:
Left: Sidebar navigation with icons for Dashboard, Users, Analytics, Settings.
Top: Header with search bar, user profile avatar, and notification bell.
Main area: Cards showing Revenue line chart (going up), User statistics donut chart,
Activity feed with recent events, and a data table.
Modern glassmorphism design elements with subtle transparency.
Color scheme: Dark background (#0F172A), blue (#3B82F6) and purple (#8B5CF6) accent colors.
Professional SaaS application feel. Landscape 16:9 aspect ratio.""",
        "category": "fullstack-gig"
    },
    "fullstack_3": {
        "name": "devops_pipeline",
        "prompt": """Create a CI/CD pipeline and DevOps visualization.
Linear flow from left to right showing the deployment pipeline:
Code (Git branch icon) → Build (gear/cog icon) → Test (checkmark in circle) →
Deploy (rocket icon) → Monitor (graph/chart icon).
Each stage connected by arrows with progress indicators.
Docker whale and Kubernetes wheel logos integrated along the pipeline.
Cloud server icons at the end representing deployment targets.
Modern tech aesthetic with dark background.
Glowing blue and green connection lines showing successful flow.
Professional DevOps/Platform engineering feel. Landscape 16:9 aspect ratio.""",
        "category": "fullstack-gig"
    },
    "iot_1": {
        "name": "iot_architecture",
        "prompt": """Create an Industrial IoT platform architecture visualization.
Bottom layer: Row of industrial sensors and device icons including temperature gauge,
pressure meter, current sensor, and machinery silhouettes.
Middle layer: Edge gateway hub as a central box collecting data with antenna icon.
Top layer: Cloud platform with analytics dashboard screens showing graphs.
Data flow arrows going upward from devices through gateway to cloud.
Labels along the path: MQTT, Kafka, InfluxDB.
Industrial color scheme: Steel blue (#475569), orange warning colors (#F59E0B),
white accents on dark background.
Professional industrial technology aesthetic. Landscape 16:9 aspect ratio.""",
        "category": "iot-gig"
    },
    "iot_2": {
        "name": "iot_monitoring_dashboard",
        "prompt": """Create an industrial IoT monitoring dashboard visualization.
Dark theme industrial control room aesthetic:
Top row: Multiple real-time gauge displays showing temperature, pressure, and current readings.
Middle: Large time-series line chart showing sensor data over time with normal range bands.
Left panel: Device status cards in a grid - green for healthy, yellow for warning, red for critical.
Right panel: World map view showing device locations as dots.
Bottom: Alert notification panel with recent warnings.
Display metrics prominently: 1000+ Devices, 99.95% Uptime, <500ms Latency.
Professional SCADA/HMI style interface. Landscape 16:9 aspect ratio.""",
        "category": "iot-gig"
    },
    "iot_3": {
        "name": "ai_anomaly_detection",
        "prompt": """Create a visualization of AI-powered anomaly detection for industrial systems.
Main element: Large time-series graph showing sensor readings with normal blue pattern
and a highlighted red anomaly spike in the middle.
AI brain icon analyzing the data stream with connecting lines to the graph.
Alert and warning icons appearing where anomalies are detected.
Side panel: Machine health indicator showing predictive maintenance status.
Claude AI badge in corner indicating AI-powered analysis.
Industrial machinery silhouettes in subtle background.
Color scheme: Dark blue background (#0F172A), red (#EF4444) for anomalies,
green (#22C55E) for normal readings, purple for AI elements.
Professional predictive analytics aesthetic. Landscape 16:9 aspect ratio.""",
        "category": "iot-gig"
    }
}


def get_api_key() -> str:
    """Get Gemini API key from environment."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)
    return api_key


def generate_single_image(client, prompt: str, output_path: str) -> dict:
    """Generate a single image and save it."""
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            ),
        )

        # Process response
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                # Save image
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                image_data = part.inline_data.data
                with open(output_path, "wb") as f:
                    f.write(image_data)

                return {"success": True, "path": output_path}

        return {"success": False, "error": "No image generated"}

    except Exception as e:
        return {"success": False, "error": str(e)}


def batch_generate(output_dir: str, prompts: dict = None, delay: float = 2.0) -> dict:
    """
    Generate multiple images from prompts.

    Args:
        output_dir: Directory to save generated images
        prompts: Dictionary of prompts (uses FIVERR_PROMPTS if None)
        delay: Delay between API calls in seconds

    Returns:
        Dictionary with results for each image
    """
    if prompts is None:
        prompts = FIVERR_PROMPTS

    api_key = get_api_key()
    client = genai.Client(api_key=api_key)

    results = {
        "total": len(prompts),
        "success": 0,
        "failed": 0,
        "images": []
    }

    print(f"\nGenerating {len(prompts)} images...")
    print(f"Output directory: {output_dir}")
    print("-" * 50)

    for i, (key, config) in enumerate(prompts.items(), 1):
        name = config.get("name", key)
        prompt = config["prompt"]
        category = config.get("category", "general")

        # Create category subdirectory
        category_dir = os.path.join(output_dir, category)
        output_path = os.path.join(category_dir, f"{name}.png")

        print(f"\n[{i}/{len(prompts)}] Generating: {name}")
        print(f"Category: {category}")
        print(f"Prompt: {prompt[:80]}...")

        result = generate_single_image(client, prompt, output_path)

        if result["success"]:
            print(f"✓ Saved: {result['path']}")
            results["success"] += 1
            results["images"].append({
                "name": name,
                "category": category,
                "path": result["path"],
                "status": "success"
            })
        else:
            print(f"✗ Failed: {result['error']}")
            results["failed"] += 1
            results["images"].append({
                "name": name,
                "category": category,
                "error": result["error"],
                "status": "failed"
            })

        # Rate limiting delay
        if i < len(prompts):
            print(f"Waiting {delay}s before next request...")
            time.sleep(delay)

    print("\n" + "=" * 50)
    print(f"BATCH COMPLETE")
    print(f"Success: {results['success']}/{results['total']}")
    print(f"Failed: {results['failed']}/{results['total']}")
    print("=" * 50)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Batch generate images for Fiverr gigs using Gemini"
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default="output/fiverr-images",
        help="Output directory for generated images"
    )
    parser.add_argument(
        "--config", "-c",
        type=str,
        default=None,
        help="JSON config file with custom prompts (optional)"
    )
    parser.add_argument(
        "--delay", "-d",
        type=float,
        default=2.0,
        help="Delay between API calls in seconds (default: 2.0)"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available default prompts and exit"
    )
    parser.add_argument(
        "--single", "-s",
        type=str,
        default=None,
        help="Generate only a single image by key name"
    )

    args = parser.parse_args()

    # List prompts
    if args.list:
        print("\nAvailable Fiverr image prompts:")
        print("-" * 50)
        for key, config in FIVERR_PROMPTS.items():
            print(f"\n{key}:")
            print(f"  Name: {config['name']}")
            print(f"  Category: {config['category']}")
            print(f"  Prompt: {config['prompt'][:100]}...")
        sys.exit(0)

    # Load custom config if provided
    prompts = FIVERR_PROMPTS
    if args.config:
        try:
            with open(args.config, 'r') as f:
                custom_prompts = json.load(f)
                if "images" in custom_prompts:
                    prompts = {img["name"]: img for img in custom_prompts["images"]}
                else:
                    prompts = custom_prompts
            print(f"Loaded {len(prompts)} prompts from {args.config}")
        except Exception as e:
            print(f"Error loading config: {e}")
            sys.exit(1)

    # Generate single image
    if args.single:
        if args.single in prompts:
            prompts = {args.single: prompts[args.single]}
        else:
            print(f"Error: '{args.single}' not found in prompts")
            print(f"Available: {', '.join(prompts.keys())}")
            sys.exit(1)

    # Run batch generation
    results = batch_generate(
        output_dir=args.output_dir,
        prompts=prompts,
        delay=args.delay
    )

    # Exit with appropriate code
    if results["failed"] > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
