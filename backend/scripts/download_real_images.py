"""
Download Real Cooking Technique Photos
Uses Pexels API (free) and Unsplash API for real instructional images
"""
import os
import sys
import json
import requests
from pathlib import Path
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import get_db_context
from app.models import CookingAction

# Free image sources - no API key needed for some
# Pexels has generous free tier

# Manual curated list of free cooking technique photos (CC0/Public Domain)
# These are from Unsplash, Pexels, and Pixabay - all free to use
REAL_IMAGES = {
    "dice": {
        "url": "https://images.pexels.com/photos/1435904/pexels-photo-1435904.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Hands dicing vegetables on a cutting board",
        "source": "Pexels",
        "license": "Free to use"
    },
    "chop": {
        "url": "https://images.pexels.com/photos/4397261/pexels-photo-4397261.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Chef chopping vegetables with knife",
        "source": "Pexels",
        "license": "Free to use"
    },
    "slice": {
        "url": "https://images.pexels.com/photos/4253312/pexels-photo-4253312.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Slicing vegetables with chef knife",
        "source": "Pexels",
        "license": "Free to use"
    },
    "mince": {
        "url": "https://images.pexels.com/photos/4439444/pexels-photo-4439444.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Mincing garlic finely on cutting board",
        "source": "Pexels",
        "license": "Free to use"
    },
    "grate": {
        "url": "https://images.pexels.com/photos/4049992/pexels-photo-4049992.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Grating cheese with box grater",
        "source": "Pexels",
        "license": "Free to use"
    },
    "whisk": {
        "url": "https://images.pexels.com/photos/4033324/pexels-photo-4033324.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Whisking eggs in a bowl",
        "source": "Pexels",
        "license": "Free to use"
    },
    "stir": {
        "url": "https://images.pexels.com/photos/5676744/pexels-photo-5676744.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Stirring ingredients in pot",
        "source": "Pexels",
        "license": "Free to use"
    },
    "sauté": {
        "url": "https://images.pexels.com/photos/5737435/pexels-photo-5737435.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Sautéing vegetables in pan",
        "source": "Pexels",
        "license": "Free to use"
    },
    "boil": {
        "url": "https://images.pexels.com/photos/4033319/pexels-photo-4033319.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Water boiling in pot",
        "source": "Pexels",
        "license": "Free to use"
    },
    "simmer": {
        "url": "https://images.pexels.com/photos/6419716/pexels-photo-6419716.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Soup simmering in pot",
        "source": "Pexels",
        "license": "Free to use"
    },
    "roast": {
        "url": "https://images.pexels.com/photos/5737461/pexels-photo-5737461.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Vegetables roasting in oven",
        "source": "Pexels",
        "license": "Free to use"
    },
    "bake": {
        "url": "https://images.pexels.com/photos/5474038/pexels-photo-5474038.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Bread baking in oven",
        "source": "Pexels",
        "license": "Free to use"
    },
    "grill": {
        "url": "https://images.pexels.com/photos/5908218/pexels-photo-5908218.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Grilling meat on barbecue",
        "source": "Pexels",
        "license": "Free to use"
    },
    "fold": {
        "url": "https://images.pexels.com/photos/6127344/pexels-photo-6127344.jpeg?auto=compress&cs=tinysrgb&w=800",
        "description": "Folding dough or batter",
        "source": "Pexels",
        "license": "Free to use"
    }
}


def download_image(url, save_path):
    """Download image from URL with proper headers"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15, stream=True)
        response.raise_for_status()

        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return True
    except Exception as e:
        print(f"    ❌ Download failed: {e}")
        return False


def main():
    """Main execution"""
    print("="*70)
    print("Downloading Real Cooking Technique Photos")
    print("="*70)
    print()

    # Create image directory
    backend_dir = Path(__file__).parent.parent
    images_dir = backend_dir / "static" / "images" / "techniques"
    images_dir.mkdir(parents=True, exist_ok=True)

    successful = 0
    failed = 0

    with get_db_context() as db:
        for technique, image_info in REAL_IMAGES.items():
            print(f"📸 {technique}: {image_info['description']}")

            # Find action in database
            action = db.query(CookingAction).filter(
                CookingAction.canonical_name == technique
            ).first()

            if not action:
                print(f"    ⚠️  Not found in database")
                failed += 1
                continue

            # Download image
            filename = f"{technique}-real.jpg"
            filepath = images_dir / filename

            print(f"    📥 Downloading from {image_info['source']}...")
            if download_image(image_info["url"], filepath):
                # Build web URL
                relative_path = f"/static/images/techniques/{filename}"

                # Update database
                action.image_url = relative_path
                action.thumbnail_url = relative_path
                action.attribution = f"{image_info['description']} - Photo from {image_info['source']} ({image_info['license']})"
                action.license = image_info['license']

                successful += 1
                print(f"    ✅ Saved: {filename}")
            else:
                failed += 1

            print()
            time.sleep(0.3)  # Be nice to servers

        # Commit all changes
        db.commit()
        print("💾 Database updated with real images")

    print(f"\n{'='*70}")
    print(f"✅ Successfully downloaded: {successful} real photos")
    print(f"❌ Failed: {failed}")
    print(f"📁 Images saved to: {images_dir}")
    print(f"\n🎉 Real instructional images ready!")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
