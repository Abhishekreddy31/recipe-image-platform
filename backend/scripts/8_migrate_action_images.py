"""
Migration Script - Link images to existing cooking actions
Fixes cooking actions that don't have image_url populated
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Change to backend directory
os.chdir(Path(__file__).parent.parent)

from app.database import get_db_context
from app.models import CookingAction


def migrate_action_images():
    """Link images to existing cooking actions"""
    print("=" * 60)
    print("Migration: Linking Images to Cooking Actions")
    print("=" * 60)

    actions_updated = 0
    images_dir = "static/images/techniques"

    with get_db_context() as db:
        # Get all cooking actions
        actions = db.query(CookingAction).all()
        print(f"\nFound {len(actions)} cooking actions in database\n")

        for action in actions:
            action_name = action.canonical_name
            image_path = None

            # Try different image file patterns (prefer curated > real > demo > pexels)
            for pattern in [f"{action_name}-curated.jpg", f"{action_name}-real.jpg", f"{action_name}-demo.jpg", f"{action_name}-pexels.jpg"]:
                full_path = os.path.join(images_dir, pattern)
                if os.path.exists(full_path):
                    image_path = f"/static/images/techniques/{pattern}"
                    break

            # Update action if image found
            if image_path:
                if action.image_url != image_path:
                    action.image_url = image_path
                    action.thumbnail_url = image_path
                    action.attribution = "Photo from Pexels"
                    action.license = "Pexels License"
                    actions_updated += 1
                    print(f"  ✅ {action_name}: {pattern}")
                else:
                    print(f"  ⏭️  {action_name}: already has image")
            else:
                if action.image_url:
                    print(f"  ⚠️  {action_name}: has image_url but file not found")
                else:
                    print(f"  ❌ {action_name}: no image file found")

        # Commit all changes
        db.commit()

    print("\n" + "=" * 60)
    print(f"✅ Migration complete!")
    print(f"   Actions updated: {actions_updated}")
    print("=" * 60)

    return actions_updated


def main():
    """Main entry point"""
    try:
        count = migrate_action_images()
        if count > 0:
            print(f"\n🎉 Successfully updated {count} cooking actions with images!")
        else:
            print("\n✨ All cooking actions already have images")
    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
