"""
Download Cooking Technique Images from Wikimedia Commons
Searches for and downloads free images for cooking techniques
"""
import os
import sys
import json
import requests
from pathlib import Path
from urllib.parse import quote
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import get_db_context
from app.models import CookingAction

# Wikimedia Commons API endpoint
COMMONS_API = "https://commons.wikimedia.org/w/api.php"

# Priority techniques to fetch images for (most common in recipes)
PRIORITY_TECHNIQUES = [
    "dice", "chop", "slice", "mince", "grate",
    "whisk", "stir", "fold",
    "sauté", "roast", "bake", "grill", "sear",
    "boil", "simmer", "steam"
]

def search_wikimedia_images(search_term, limit=5):
    """
    Search Wikimedia Commons for images

    Args:
        search_term: Cooking technique to search for
        limit: Maximum number of results

    Returns:
        List of image info dicts
    """
    print(f"  Searching for '{search_term}'...")

    # Build search query - focus on cooking/food related images
    query = f"{search_term} cooking technique food preparation"

    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {query}",
        "gsrlimit": limit,
        "prop": "imageinfo|categories",
        "iiprop": "url|size|mime|extmetadata",
        "iiurlwidth": 800,  # Request 800px width thumbnail
    }

    # Add proper headers to avoid 403
    headers = {
        "User-Agent": "RecipeImagePlatform/1.0 (Educational/Non-commercial project; mailto:noreply@example.com)"
    }

    try:
        response = requests.get(COMMONS_API, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "query" not in data or "pages" not in data["query"]:
            print(f"    ⚠️  No results found")
            return []

        images = []
        for page in data["query"]["pages"].values():
            if "imageinfo" not in page:
                continue

            info = page["imageinfo"][0]
            metadata = info.get("extmetadata", {})

            # Extract license info
            license_short = metadata.get("LicenseShortName", {}).get("value", "Unknown")
            license_url = metadata.get("LicenseUrl", {}).get("value", "")

            # Filter for acceptable licenses (CC0, CC-BY, CC-BY-SA)
            acceptable_licenses = ["CC0", "CC-BY", "CC-BY-SA", "Public domain"]
            if not any(lic in license_short for lic in acceptable_licenses):
                print(f"    ❌ Skipping {page['title']} - Non-commercial or restrictive license: {license_short}")
                continue

            # Extract attribution info
            artist = metadata.get("Artist", {}).get("value", "Unknown")
            # Clean HTML from artist field
            if artist and "<" in artist:
                import re
                artist = re.sub('<[^<]+?>', '', artist)

            images.append({
                "title": page["title"],
                "url": info.get("thumburl") or info["url"],
                "original_url": info["url"],
                "width": info.get("thumbwidth", info.get("width")),
                "height": info.get("thumbheight", info.get("height")),
                "size": info.get("size", 0),
                "mime": info.get("mime", "image/jpeg"),
                "description_url": info.get("descriptionurl", ""),
                "license": license_short,
                "license_url": license_url,
                "artist": artist,
                "page_id": page["pageid"]
            })

        print(f"    ✅ Found {len(images)} usable images")
        return images

    except Exception as e:
        print(f"    ❌ Error searching: {e}")
        return []


def download_image(image_info, save_dir, filename):
    """
    Download an image from URL

    Args:
        image_info: Image info dict from search
        save_dir: Directory to save image
        filename: Filename to save as

    Returns:
        Path to saved image or None
    """
    try:
        url = image_info["url"]
        response = requests.get(url, timeout=15, stream=True)
        response.raise_for_status()

        # Determine file extension from mime type
        mime = image_info["mime"]
        if "jpeg" in mime or "jpg" in mime:
            ext = "jpg"
        elif "png" in mime:
            ext = "png"
        elif "webp" in mime:
            ext = "webp"
        else:
            ext = "jpg"  # Default

        filepath = save_dir / f"{filename}.{ext}"

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return filepath

    except Exception as e:
        print(f"      ❌ Download failed: {e}")
        return None


def main():
    """Main execution"""
    print("="*70)
    print("Wikimedia Commons Image Downloader for Cooking Techniques")
    print("="*70)
    print()

    # Create image directories
    backend_dir = Path(__file__).parent.parent
    static_dir = backend_dir / "static"
    images_dir = static_dir / "images" / "techniques"

    print(f"Creating directories at: {images_dir}")
    images_dir.mkdir(parents=True, exist_ok=True)

    # Load existing cooking actions from database
    actions_with_images = {}
    successful_downloads = 0
    failed_downloads = 0

    with get_db_context() as db:
        # Get priority actions from database
        actions = db.query(CookingAction).filter(
            CookingAction.canonical_name.in_(PRIORITY_TECHNIQUES)
        ).all()

        if not actions:
            print("❌ No cooking actions found in database!")
            return

        print(f"Found {len(actions)} priority techniques to fetch images for\n")

        # Process each action
        for action in actions:
            print(f"📸 Processing: {action.canonical_name}")

            # Search for images
            search_results = search_wikimedia_images(action.canonical_name, limit=3)

            if not search_results:
                failed_downloads += 1
                print(f"    ⏭️  Skipping (no suitable images found)\n")
                continue

            # Take the first suitable image
            best_image = search_results[0]

            # Download image
            print(f"    📥 Downloading: {best_image['title']}")
            filename = f"{action.canonical_name}-001"
            filepath = download_image(best_image, images_dir, filename)

            if filepath:
                # Build web-accessible URL
                relative_path = f"/static/images/techniques/{filepath.name}"

                # Prepare attribution text
                attribution = f"Image: {best_image['artist']}, {best_image['license']}, via Wikimedia Commons"

                # Update database
                action.image_url = relative_path
                action.thumbnail_url = relative_path
                action.attribution = attribution
                action.license = best_image['license']
                action.wikimedia_file_id = best_image['title']

                actions_with_images[action.canonical_name] = {
                    "image_url": relative_path,
                    "attribution": attribution,
                    "license": best_image['license'],
                    "original_url": best_image['description_url']
                }

                successful_downloads += 1
                print(f"    ✅ Saved: {filepath.name}")
                print(f"    📄 License: {best_image['license']}")
                print(f"    👤 Artist: {best_image['artist'][:50]}...")
            else:
                failed_downloads += 1

            print()

            # Be nice to Wikimedia servers
            time.sleep(1)

        # Commit all changes
        db.commit()
        print("💾 Database updated with image URLs and attribution")

    # Save metadata to JSON
    metadata_file = backend_dir / "data" / "metadata" / "image_metadata.json"
    metadata_file.parent.mkdir(parents=True, exist_ok=True)

    with open(metadata_file, 'w') as f:
        json.dump(actions_with_images, f, indent=2)

    print(f"\n{'='*70}")
    print("📊 Summary")
    print(f"{'='*70}")
    print(f"✅ Successful downloads: {successful_downloads}")
    print(f"❌ Failed/skipped: {failed_downloads}")
    print(f"📁 Images saved to: {images_dir}")
    print(f"📄 Metadata saved to: {metadata_file}")
    print(f"\n🎉 Image download complete!")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
