"""
Migration Script - Re-extract cooking actions for existing recipes
Fixes recipes that were created before NLP extraction was working correctly
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Change to backend directory
os.chdir(Path(__file__).parent.parent)

from app.database import get_db_context
from app.models import Recipe, RecipeStep, CookingAction
from app.nlp import ActionExtractor, ActionMatcher
from app.nlp.action_matcher import load_taxonomy_for_matcher
from app.config import settings


def migrate_extract_actions():
    """Re-extract cooking actions for all existing recipes"""
    print("=" * 60)
    print("Migration: Re-extracting Cooking Actions")
    print("=" * 60)

    # Initialize NLP components
    print("\nInitializing NLP components...")
    taxonomy_actions = load_taxonomy_for_matcher(settings.TAXONOMY_PATH)
    matcher = ActionMatcher(taxonomy_actions)
    extractor = ActionExtractor(matcher, settings.SPACY_MODEL)

    recipes_updated = 0
    steps_updated = 0

    with get_db_context() as db:
        # Get all recipes
        recipes = db.query(Recipe).all()
        print(f"\nFound {len(recipes)} recipes in database")

        for recipe in recipes:
            print(f"\n📝 Processing '{recipe.title}':")
            recipe_has_updates = False

            # Get all steps for this recipe
            steps = db.query(RecipeStep).filter(
                RecipeStep.recipe_id == recipe.id
            ).order_by(RecipeStep.step_number).all()

            for step in steps:
                # Extract cooking actions using NLP
                try:
                    extracted = extractor.extract_actions(step.instruction_text)

                    if extracted:
                        # Get action IDs from extraction results
                        action_ids = [action["action_id"] for action in extracted]

                        # Find cooking actions in database by ID
                        actions = db.query(CookingAction).filter(
                            CookingAction.id.in_(action_ids)
                        ).all()

                        # Check if this step needs updating
                        existing_action_ids = {a.id for a in step.extracted_actions}
                        new_action_ids = {a.id for a in actions}

                        if existing_action_ids != new_action_ids:
                            # Update the step's extracted actions
                            step.extracted_actions = actions
                            action_names = [a.canonical_name for a in actions]
                            print(f"  ✅ Step {step.step_number}: {', '.join(action_names)}")
                            steps_updated += 1
                            recipe_has_updates = True
                        else:
                            action_names = [a.canonical_name for a in actions]
                            print(f"  ⏭️  Step {step.step_number}: {', '.join(action_names)} (no change)")
                    else:
                        if step.extracted_actions:
                            # Had actions before, now has none
                            step.extracted_actions = []
                            print(f"  🔄 Step {step.step_number}: Cleared actions (none detected)")
                            steps_updated += 1
                            recipe_has_updates = True
                        else:
                            print(f"  ⏭️  Step {step.step_number}: (no techniques detected)")

                except Exception as e:
                    print(f"  ❌ Step {step.step_number}: Error extracting actions - {e}")

            if recipe_has_updates:
                recipes_updated += 1

        # Commit all changes
        db.commit()

    print("\n" + "=" * 60)
    print(f"✅ Migration complete!")
    print(f"   Recipes updated: {recipes_updated}")
    print(f"   Steps updated: {steps_updated}")
    print("=" * 60)

    return recipes_updated, steps_updated


def main():
    """Main entry point"""
    try:
        recipe_count, step_count = migrate_extract_actions()
        if recipe_count > 0 or step_count > 0:
            print(f"\n🎉 Successfully updated {recipe_count} recipes ({step_count} steps)!")
        else:
            print("\n✨ All recipes are already up to date")
    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
