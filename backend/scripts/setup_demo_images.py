"""
Setup Demo Images for Cooking Techniques
Uses placeholder images to demonstrate end-to-end functionality
In production, these would be replaced with real Wikimedia Commons images
"""
import os
import sys
import json
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import get_db_context
from app.models import CookingAction

# Priority techniques for demo
DEMO_TECHNIQUES = [
    "dice", "chop", "slice", "mince", "grate", "peel",
    "whisk", "stir", "fold", "toss",
    "sauté", "roast", "bake", "grill", "sear",
    "boil", "simmer", "steam", "toast"
]

# Color palette for technique categories
COLORS = {
    "cutting-prep": "#3B82F6",  # Blue
    "mixing-combining": "#10B981",  # Green
    "dry-heat-cooking": "#F59E0B",  # Orange
    "moist-heat-cooking": "#8B5CF6",  # Purple
    "finishing-presentation": "#EC4899"  # Pink
}


def create_placeholder_image(technique_name, category, size=(800, 600)):
    """Create a simple placeholder image"""
    # Create image with category color
    color = COLORS.get(category, "#6B7280")
    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)

    # Try to use a nice font, fall back to default
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw text
    text = technique_name.upper()

    # Get text size and position (center)
    bbox = draw.textbbox((0, 0), text, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    position = ((size[0] - text_width) / 2, (size[1] - text_height) / 2)

    # Draw white text with shadow
    shadow_offset = 3
    draw.text((position[0] + shadow_offset, position[1] + shadow_offset), text, fill="#00000080", font=font_large)
    draw.text(position, text, fill="white", font=font_large)

    # Add subtitle
    subtitle = "Cooking Technique"
    bbox_sub = draw.textbbox((0, 0), subtitle, font=font_small)
    sub_width = bbox_sub[2] - bbox_sub[0]
    sub_position = ((size[0] - sub_width) / 2, position[1] + text_height + 20)
    draw.text(sub_position, subtitle, fill="white", font=font_small)

    return img


def main():
    """Main execution"""
    print("="*70)
    print("Setting Up Demo Images for Cooking Techniques")
    print("="*70)
    print()

    # Create image directory
    backend_dir = Path(__file__).parent.parent
    static_dir = backend_dir / "static"
    images_dir = static_dir / "images" / "techniques"

    print(f"Creating directories at: {images_dir}")
    images_dir.mkdir(parents=True, exist_ok=True)

    successful = 0
    failed = 0
    metadata = {}

    with get_db_context() as db:
        # Get actions from database
        actions = db.query(CookingAction).filter(
            CookingAction.canonical_name.in_(DEMO_TECHNIQUES)
        ).all()

        print(f"Found {len(actions)} techniques to process\n")

        for action in actions:
            technique = action.canonical_name
            category = action.category

            print(f"📸 Creating image for: {technique}")

            try:
                # Create placeholder image
                img = create_placeholder_image(technique, category)

                # Save image
                filename = f"{technique}-demo.jpg"
                filepath = images_dir / filename
                img.save(filepath, 'JPEG', quality=85)

                # Build web-accessible URL
                relative_path = f"/static/images/techniques/{filename}"

                # Create attribution
                attribution = "Demo placeholder image. In production, this would be a real image from Wikimedia Commons."

                # Update database
                action.image_url = relative_path
                action.thumbnail_url = relative_path
                action.attribution = attribution
                action.license = "Demo"

                metadata[technique] = {
                    "image_url": relative_path,
                    "attribution": attribution,
                    "license": "Demo",
                    "category": category
                }

                successful += 1
                print(f"    ✅ Created: {filename}")
                print(f"    📁 Category: {category}")

            except Exception as e:
                print(f"    ❌ Failed: {e}")
                failed += 1

            print()

        # Commit database changes
        db.commit()
        print("💾 Database updated with demo images")

    # Save metadata
    metadata_file = backend_dir / "data" / "metadata" / "demo_image_metadata.json"
    metadata_file.parent.mkdir(parents=True, exist_ok=True)

    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"\n{'='*70}")
    print("📊 Summary")
    print(f"{'='*70}")
    print(f"✅ Successfully created: {successful} images")
    print(f"❌ Failed: {failed}")
    print(f"📁 Images saved to: {images_dir}")
    print(f"📄 Metadata saved to: {metadata_file}")
    print(f"\n🎉 Demo image setup complete!")
    print(f"{'='*70}")
    print()
    print("💡 These are placeholder images for demonstration.")
    print("   In production, replace with real images from Wikimedia Commons.")
    print()


if __name__ == "__main__":
    main()
