"""
Download Real Cooking Technique Images from Pexels API
Free, high-quality stock photos showing actual cooking techniques
"""
import os
import sys
import json
import requests
from pathlib import Path
import time
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

from app.database import get_db_context
from app.models import CookingAction

# Get API key from environment
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY', '')

if not PEXELS_API_KEY:
    print("⚠️  Please set PEXELS_API_KEY environment variable")
    print("Get your free API key from: https://www.pexels.com/api/")
    print()
    print("Steps:")
    print("1. Go to https://www.pexels.com/api/")
    print("2. Click 'Get Started'")
    print("3. Sign up (free)")
    print("4. Copy your API key")
    print("5. Set environment variable:")
    print("   export PEXELS_API_KEY='your-api-key-here'")
    print()
    sys.exit(1)

# Highly specific search queries for each cooking technique
# Focus on close-ups showing clear demonstration of the technique
SEARCH_QUERIES = {
    # Cutting & Preparation
    "dice": "close up hands dicing onion into cubes knife cutting board",
    "chop": "close up hands chopping vegetables chef knife cutting",
    "slice": "close up hands slicing cucumber tomato knife blade",
    "mince": "close up hands mincing garlic fine knife chopping",
    "grate": "close up hands grating cheese grater kitchen",
    "peel": "close up hands peeling potato carrot peeler vegetable",
    "julienne": "close up hands cutting carrot julienne matchstick strips knife",
    "brunoise": "close up hands dicing vegetables tiny cubes precise knife",
    "chiffonade": "close up hands cutting basil herbs ribbons chiffonade knife",
    "zest": "close up hands zesting lemon orange zester grater",
    "shred": "close up hands shredding cabbage lettuce knife",
    "debone": "close up hands deboning chicken fish knife meat",
    "fillet": "close up hands filleting fish knife removing bones",
    "score": "close up hands scoring meat knife cuts crosshatch",
    "tenderize": "close up hands tenderizing meat mallet pounding hammer",

    # Mixing & Combining
    "whisk": "close up hands whisking eggs bowl wire whisk beating",
    "stir": "close up hands stirring pot wooden spoon cooking sauce",
    "fold": "close up hands folding batter spatula bowl gentle mixing",
    "beat": "close up hands beating eggs whisk mixer bowl",
    "cream": "close up hands creaming butter sugar mixer bowl",
    "knead": "close up hands kneading dough bread flour working",
    "toss": "close up hands tossing salad bowl mixing vegetables",
    "emulsify": "close up hands whisking vinaigrette dressing bowl emulsion",

    # Dry Heat Cooking
    "sauté": "close up hands sauteing vegetables pan skillet stove cooking",
    "stir-fry": "close up hands stir frying wok vegetables spatula tossing",
    "deep-fry": "close up deep frying food oil hot bubbling fryer",
    "roast": "close up roasting vegetables oven tray golden brown",
    "bake": "close up baking bread oven golden crust",
    "grill": "close up grilling meat steak barbecue grill marks flames",
    "broil": "close up broiling food oven top heat browning",
    "sear": "close up searing steak pan hot crust browning",
    "toast": "close up toasting bread golden brown toaster",
    "caramelize": "close up caramelizing onions pan golden brown sweet",

    # Moist Heat Cooking
    "boil": "close up boiling water pot bubbles rolling steam",
    "simmer": "close up simmering soup sauce pot gentle bubbles low",
    "poach": "close up poaching eggs water gentle cooking",
    "steam": "close up steaming vegetables steamer basket vapor rising",
    "blanch": "close up blanching vegetables boiling water briefly",
    "parboil": "close up boiling vegetables pot water partially cooking",
    "braise": "close up braising meat pot dutch oven liquid cooking",
    "stew": "close up stewing meat vegetables pot slow cooking",
    "sous-vide": "close up sous vide cooking vacuum sealed bag water bath",
    "pressure-cook": "close up pressure cooker pot steam valve cooking",

    # Finishing & Presentation
    "glaze": "close up glazing food brush sauce coating basting",
    "garnish": "close up hands garnishing plate food herbs decorating",
    "plate": "close up hands plating food arranging presentation chef",
    "drizzle": "close up drizzling olive oil sauce food pouring",
    "dust": "close up dusting powdered sugar dessert sifting sprinkling",
    "rest": "close up resting meat steak cutting board after cooking",
    "reduce": "close up reducing sauce pot simmering thickening concentrated"
}


def search_pexels(query, per_page=15):
    """Search Pexels for images"""
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query,
        "per_page": per_page,
        "orientation": "landscape"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"    ❌ Search failed: {e}")
        return None


def download_image(url, save_path):
    """Download image from Pexels"""
    try:
        response = requests.get(url, timeout=15, stream=True)
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
    print("Pexels Cooking Technique Image Downloader")
    print("="*70)
    print()

    # Create directories
    backend_dir = Path(__file__).parent.parent
    images_dir = backend_dir / "static" / "images" / "techniques"
    images_dir.mkdir(parents=True, exist_ok=True)

    successful = 0
    failed = 0
    metadata = {}

    with get_db_context() as db:
        # Get all actions from database
        actions = db.query(CookingAction).all()

        print(f"Processing {len(actions)} cooking actions...")
        print()

        for action in actions:
            technique = action.canonical_name

            # Skip if no search query defined
            if technique not in SEARCH_QUERIES:
                print(f"⏭️  Skipping '{technique}' - no search query defined")
                continue

            print(f"📸 {technique}: {SEARCH_QUERIES[technique]}")

            # Search Pexels
            results = search_pexels(SEARCH_QUERIES[technique], per_page=15)

            if not results or not results.get('photos'):
                print(f"    ⚠️  No results found")
                failed += 1
                print()
                continue

            # Get the best image (first result is usually most relevant)
            photo = results['photos'][0]

            # Use 'large' size (good balance of quality and file size)
            image_url = photo['src']['large']
            photographer = photo['photographer']
            photo_url = photo['url']

            # Download image
            filename = f"{technique}-pexels.jpg"
            filepath = images_dir / filename

            print(f"    📥 Downloading from Pexels...")
            print(f"    👤 Photo by: {photographer}")

            if download_image(image_url, filepath):
                # Build web URL
                relative_path = f"/static/images/techniques/{filename}"

                # Create attribution
                attribution = f"Photo by {photographer} from Pexels"

                # Update database
                action.image_url = relative_path
                action.thumbnail_url = relative_path
                action.attribution = attribution
                action.license = "Pexels License (Free to use)"
                action.wikimedia_file_id = photo_url

                metadata[technique] = {
                    "image_url": relative_path,
                    "photographer": photographer,
                    "pexels_url": photo_url,
                    "attribution": attribution
                }

                successful += 1
                print(f"    ✅ Saved: {filename}")
            else:
                failed += 1

            print()
            time.sleep(0.5)  # Be respectful to API (200 requests/hour limit)

        # Commit all changes
        db.commit()
        print("💾 Database updated with Pexels images")

    # Save metadata
    metadata_file = backend_dir / "data" / "metadata" / "pexels_metadata.json"
    metadata_file.parent.mkdir(parents=True, exist_ok=True)

    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"\n{'='*70}")
    print(f"✅ Successfully downloaded: {successful} images")
    print(f"❌ Failed/skipped: {failed}")
    print(f"📁 Images saved to: {images_dir}")
    print(f"📄 Metadata: {metadata_file}")
    print(f"\n🎉 Real cooking technique images ready!")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
