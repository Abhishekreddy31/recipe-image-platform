"""
Database Seeding Script - Populate cooking actions from taxonomy
"""
import json
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Change to backend directory
os.chdir(Path(__file__).parent.parent)

from app.database import get_db_context
from app.models import CookingAction
from app.config import settings


def load_taxonomy(path: str) -> dict:
    """Load cooking actions taxonomy from JSON"""
    # If path is relative, make it absolute from backend directory
    if not os.path.isabs(path):
        backend_dir = Path(__file__).parent.parent
        path = os.path.join(backend_dir, path)

    print(f"Loading taxonomy from: {path}")
    with open(path, 'r') as f:
        return json.load(f)


def seed_cooking_actions():
    """Seed database with cooking actions from taxonomy"""
    print("Loading taxonomy...")
    taxonomy = load_taxonomy(settings.TAXONOMY_PATH)

    print(f"Found {len(taxonomy['categories'])} categories")

    actions_added = 0

    with get_db_context() as db:
        # Clear existing actions (optional - comment out if you want to preserve)
        # db.query(CookingAction).delete()
        # print("Cleared existing cooking actions")

        for category in taxonomy["categories"]:
            category_id = category["id"]
            category_name = category["name"]
            print(f"\nProcessing category: {category_name}")

            for action_data in category["actions"]:
                # Check if action already exists
                existing = db.query(CookingAction).filter(
                    CookingAction.canonical_name == action_data["canonical_name"]
                ).first()

                if existing:
                    print(f"  ⏭️  Skipping '{action_data['canonical_name']}' (already exists)")
                    continue

                # Auto-detect image file for this action
                action_name = action_data["canonical_name"]
                image_path = None

                # Try different image file patterns (prefer curated > real > demo > pexels)
                import os
                # We're already in backend/ directory after os.chdir() above
                images_dir = "static/images/techniques"
                for pattern in [f"{action_name}-curated.jpg", f"{action_name}-real.jpg", f"{action_name}-demo.jpg", f"{action_name}-pexels.jpg"]:
                    full_path = os.path.join(images_dir, pattern)
                    if os.path.exists(full_path):
                        image_path = f"/static/images/techniques/{pattern}"
                        print(f"    Found image: {pattern}")
                        break

                # Create new cooking action
                action = CookingAction(
                    canonical_name=action_data["canonical_name"],
                    synonyms=action_data.get("synonyms", []),
                    description=action_data.get("description"),
                    category=category_id,
                    priority=action_data.get("priority", 1),
                    difficulty=action_data.get("difficulty", "easy"),
                    image_url=image_path,
                    thumbnail_url=image_path,  # Use same image for thumbnail
                    attribution="Photo from Pexels",
                    license="Pexels License"
                )

                db.add(action)
                actions_added += 1
                print(f"  ✅ Added '{action_data['canonical_name']}'")

        db.commit()

    print(f"\n✨ Successfully seeded {actions_added} cooking actions!")
    return actions_added


def main():
    """Main entry point"""
    print("="* 60)
    print("Database Seeding Script - Cooking Actions")
    print("="* 60)

    try:
        count = seed_cooking_actions()

        print("\n" + "="* 60)
        print(f"✅ Database seeding complete!")
        print(f"   Total actions: {count}")
        print("="* 60)

    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
