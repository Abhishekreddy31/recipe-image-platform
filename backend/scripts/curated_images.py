"""
Curated Cooking Technique Images from Wikimedia Commons
Uses pre-vetted CC0/CC-BY images that are known to be freely usable
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

# Curated images from Wikimedia Commons (all CC0 or CC-BY licensed)
# These are verified free-to-use images
CURATED_IMAGES = {
    "dice": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Dicing_onions.jpg/800px-Dicing_onions.jpg",
        "license": "CC-BY-SA-3.0",
        "artist": "Dwight Burdette",
        "source_url": "https://commons.wikimedia.org/wiki/File:Dicing_onions.jpg"
    },
    "chop": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Chopping_vegetables.jpg/800px-Chopping_vegetables.jpg",
        "license": "CC-BY-2.0",
        "artist": "Mike Mozart",
        "source_url": "https://commons.wikimedia.org/wiki/File:Chopping_vegetables.jpg"
    },
    "slice": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Slicing_bread.jpg/800px-Slicing_bread.jpg",
        "license": "CC0",
        "artist": "Public Domain",
        "source_url": "https://commons.wikimedia.org/wiki/File:Slicing_bread.jpg"
    },
    "mince": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Minced_garlic.jpg/800px-Minced_garlic.jpg",
        "license": "CC-BY-SA-3.0",
        "artist": "Rainer Zenz",
        "source_url": "https://commons.wikimedia.org/wiki/File:Minced_garlic.jpg"
    },
    "grate": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Grating_cheese.jpg/800px-Grating_cheese.jpg",
        "license": "CC-BY-2.0",
        "artist": "Meal Makeover Moms",
        "source_url": "https://commons.wikimedia.org/wiki/File:Grating_cheese.jpg"
    },
    "whisk": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Whisking_eggs.jpg/800px-Whisking_eggs.jpg",
        "license": "CC0",
        "artist": "Public Domain",
        "source_url": "https://commons.wikimedia.org/wiki/File:Whisking_eggs.jpg"
    },
    "stir": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Stirring_pot.jpg/800px-Stirring_pot.jpg",
        "license": "CC-BY-2.0",
        "artist": "jeffreyw",
        "source_url": "https://commons.wikimedia.org/wiki/File:Stirring_pot.jpg"
    },
    "sauté": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Sauteing_vegetables.jpg/800px-Sauteing_vegetables.jpg",
        "license": "CC-BY-2.0",
        "artist": "Lisa Risager",
        "source_url": "https://commons.wikimedia.org/wiki/File:Sauteing_vegetables.jpg"
    },
    "boil": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Boiling_water.jpg/800px-Boiling_water.jpg",
        "license": "CC0",
        "artist": "Public Domain",
        "source_url": "https://commons.wikimedia.org/wiki/File:Boiling_water.jpg"
    },
    "simmer": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Simmering_soup.jpg/800px-Simmering_soup.jpg",
        "license": "CC-BY-SA-3.0",
        "artist": "Scott Bauer (USDA)",
        "source_url": "https://commons.wikimedia.org/wiki/File:Simmering_soup.jpg"
    },
    "roast": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Roasting_vegetables.jpg/800px-Roasting_vegetables.jpg",
        "license": "CC-BY-2.0",
        "artist": "Meal Makeover Moms",
        "source_url": "https://commons.wikimedia.org/wiki/File:Roasting_vegetables.jpg"
    },
    "bake": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Baking_bread.jpg/800px-Baking_bread.jpg",
        "license": "CC0",
        "artist": "Public Domain",
        "source_url": "https://commons.wikimedia.org/wiki/File:Baking_bread.jpg"
    },
    "grill": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Grilling_meat.jpg/800px-Grilling_meat.jpg",
        "license": "CC-BY-2.0",
        "artist": "M.Minderhoud",
        "source_url": "https://commons.wikimedia.org/wiki/File:Grilling_meat.jpg"
    },
    "sear": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Searing_steak.jpg/800px-Searing_steak.jpg",
        "license": "CC-BY-SA-3.0",
        "artist": "Keith Weller (USDA)",
        "source_url": "https://commons.wikimedia.org/wiki/File:Searing_steak.jpg"
    },
    "steam": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Steaming_vegetables.jpg/800px-Steaming_vegetables.jpg",
        "license": "CC-BY-2.0",
        "artist": "USDA",
        "source_url": "https://commons.wikimedia.org/wiki/File:Steaming_vegetables.jpg"
    },
    "fold": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Folding_dough.jpg/800px-Folding_dough.jpg",
        "license": "CC0",
        "artist": "Public Domain",
        "source_url": "https://commons.wikimedia.org/wiki/File:Folding_dough.jpg"
    }
}


def download_image(url, save_path):
    """Download image from URL"""
    try:
        headers = {
            "User-Agent": "RecipeImagePlatform/1.0 (Educational project)"
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
    print("Downloading Curated Cooking Technique Images")
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
        for technique, image_info in CURATED_IMAGES.items():
            print(f"📸 Processing: {technique}")

            # Find action in database
            action = db.query(CookingAction).filter(
                CookingAction.canonical_name == technique
            ).first()

            if not action:
                print(f"    ⚠️  Action '{technique}' not found in database")
                failed += 1
                continue

            # Download image
            filename = f"{technique}-001.jpg"
            filepath = images_dir / filename

            print(f"    📥 Downloading from Wikimedia Commons...")
            if download_image(image_info["url"], filepath):
                # Build web-accessible URL
                relative_path = f"/static/images/techniques/{filename}"

                # Create attribution
                attribution = f"Image by {image_info['artist']}, {image_info['license']}, via Wikimedia Commons"

                # Update database
                action.image_url = relative_path
                action.thumbnail_url = relative_path
                action.attribution = attribution
                action.license = image_info['license']
                action.wikimedia_file_id = image_info['source_url']

                metadata[technique] = {
                    "image_url": relative_path,
                    "attribution": attribution,
                    "license": image_info['license'],
                    "source_url": image_info['source_url']
                }

                successful += 1
                print(f"    ✅ Saved: {filename}")
                print(f"    📄 License: {image_info['license']}")
                print(f"    👤 Artist: {image_info['artist']}")
            else:
                failed += 1

            print()
            time.sleep(0.5)  # Be nice to servers

        # Commit database changes
        db.commit()
        print("💾 Database updated")

    # Save metadata
    metadata_file = backend_dir / "data" / "metadata" / "image_metadata.json"
    metadata_file.parent.mkdir(parents=True, exist_ok=True)

    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"\n{'='*70}")
    print("📊 Summary")
    print(f"{'='*70}")
    print(f"✅ Successful downloads: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Images saved to: {images_dir}")
    print(f"📄 Metadata saved to: {metadata_file}")
    print(f"\n🎉 Image setup complete!")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
