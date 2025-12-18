"""Seed database with example recipes"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import get_db_context
from app.models import Recipe, RecipeStep, CookingAction
from app.nlp import ActionExtractor, ActionMatcher
from app.nlp.action_matcher import load_taxonomy_for_matcher
from app.config import settings

# Example comprehensive recipes
EXAMPLE_RECIPES = [
    {
        "title": "Pan-Seared Salmon with Roasted Vegetables and Garlic Herb Butter",
        "description": "A restaurant-quality dish featuring perfectly seared salmon with a crispy skin, accompanied by caramelized roasted vegetables and finished with a rich garlic herb butter sauce.",
        "steps": [
            "Dice the onions into small cubes and mince the garlic cloves finely using a sharp knife.",
            "Slice the bell peppers into strips and julienne the carrots into thin matchsticks.",
            "Chop the fresh herbs including parsley, thyme, and dill, then grate the lemon zest into a small bowl.",
            "Whisk together olive oil, lemon juice, salt, and pepper in a mixing bowl to create the marinade.",
            "Toss the vegetables in the marinade and roast them in a preheated oven at 400°F for 25 minutes until caramelized.",
            "Season the salmon fillets with salt and pepper, then sear them skin-side down in a hot skillet until the skin is crispy.",
            "Flip the salmon and baste it with butter, continuing to cook until it reaches medium doneness.",
            "In a separate pan, sauté the minced garlic in butter until fragrant, then stir in the chopped herbs.",
            "Simmer the garlic butter sauce gently while whisking to emulsify the butter with the pan juices.",
            "Plate the roasted vegetables, top with the seared salmon, and drizzle the garlic herb butter over everything. Garnish with fresh dill and lemon wedges."
        ]
    },
    {
        "title": "Classic Italian Bolognese with Fresh Pasta",
        "description": "A traditional slow-cooked meat sauce with aromatic vegetables, served over homemade pasta. This authentic recipe requires patience but delivers incredible depth of flavor.",
        "steps": [
            "Dice the onions, carrots, and celery into small uniform cubes for the soffritto base.",
            "Mince the garlic cloves and chop fresh basil and oregano finely.",
            "In a large pot, sauté the diced vegetables in olive oil over medium heat until they soften and caramelize.",
            "Add ground beef and pork, breaking it up with a wooden spoon, and sear until browned on all sides.",
            "Pour in red wine and simmer until the alcohol evaporates and the liquid reduces by half.",
            "Stir in crushed tomatoes, tomato paste, and beef stock, then season with salt, pepper, and Italian herbs.",
            "Reduce heat to low and braise the sauce uncovered for 2-3 hours, stirring occasionally to prevent sticking.",
            "While the sauce simmers, knead pasta dough on a floured surface until smooth and elastic.",
            "Roll out the pasta dough thinly using a pasta machine or rolling pin, then slice into fettuccine ribbons.",
            "Boil the fresh pasta in salted water for 2-3 minutes until al dente, then drain and toss with the Bolognese sauce.",
            "Plate the pasta, garnish with fresh basil and grated Parmesan cheese, and drizzle with extra virgin olive oil."
        ]
    },
    {
        "title": "Thai Green Curry with Jasmine Rice",
        "description": "An aromatic and spicy Thai curry featuring tender chicken, vegetables, and fragrant herbs in a creamy coconut milk base. Perfectly balanced with sweet, spicy, and savory notes.",
        "steps": [
            "Slice the chicken breast into bite-sized strips and season with salt and pepper.",
            "Dice the bell peppers and onions, then julienne the Thai basil leaves.",
            "Mince the garlic, ginger, and lemongrass stalks finely for the curry paste.",
            "Chop the green chilies and cilantro, keeping the stems separate from the leaves.",
            "In a wok, sauté the curry paste in coconut oil until fragrant and the oil separates.",
            "Add the sliced chicken and stir-fry until the pieces are seared and lightly browned.",
            "Pour in coconut milk and simmer gently, allowing the flavors to infuse.",
            "Toss in the diced vegetables and simmer until they're tender but still crisp.",
            "Stir in fish sauce, palm sugar, and lime juice to balance the flavors.",
            "Meanwhile, rinse jasmine rice and steam it in a rice cooker until fluffy and tender.",
            "Plate the steamed rice, ladle the green curry over it, and garnish with Thai basil and sliced red chilies."
        ]
    },
    {
        "title": "Braised Short Ribs with Creamy Mashed Potatoes",
        "description": "Fall-off-the-bone tender beef short ribs slow-braised in red wine with aromatic vegetables, served alongside velvety mashed potatoes. Perfect comfort food for special occasions.",
        "steps": [
            "Season the short ribs generously with salt, pepper, and fresh thyme.",
            "Sear the ribs in a hot Dutch oven until deeply browned on all sides, then set aside.",
            "Dice the onions, carrots, and celery into large chunks for the braising base.",
            "Mince the garlic cloves and chop fresh rosemary and thyme.",
            "In the same pot, sauté the diced vegetables until caramelized and fragrant.",
            "Deglaze the pot with red wine, scraping up the browned bits from the bottom.",
            "Add beef stock, tomato paste, and the seared short ribs back to the pot.",
            "Cover and braise in a 325°F oven for 3-4 hours until the meat is fork-tender.",
            "While the ribs braise, peel and dice the potatoes into uniform chunks.",
            "Boil the potatoes in salted water until tender, then drain thoroughly.",
            "Mash the potatoes with butter, cream, and roasted garlic until smooth and creamy.",
            "Whip the mashed potatoes with a mixer to make them extra fluffy.",
            "Remove the short ribs from the braising liquid and strain the sauce through a fine sieve.",
            "Reduce the braising liquid on the stovetop until it thickens into a rich glaze.",
            "Plate the creamy mashed potatoes, top with the braised short ribs, and drizzle the reduced sauce over everything. Garnish with fresh thyme."
        ]
    },
    {
        "title": "Grilled Mediterranean Vegetable Platter",
        "description": "A vibrant array of grilled seasonal vegetables with herb-infused olive oil and tangy balsamic glaze. Healthy, colorful, and bursting with smoky charred flavors.",
        "steps": [
            "Slice the eggplant, zucchini, and yellow squash into 1/2-inch thick rounds.",
            "Dice the red bell peppers and red onions into large chunks suitable for grilling.",
            "Halve the cherry tomatoes and slice the mushrooms thickly.",
            "Chop fresh basil, oregano, and parsley, then mince the garlic.",
            "Whisk together olive oil, balsamic vinegar, minced garlic, and chopped herbs to make a marinade.",
            "Toss all the sliced vegetables in the marinade and let them rest for 15 minutes.",
            "Preheat the grill to medium-high heat and oil the grates to prevent sticking.",
            "Grill the marinated vegetables in batches, turning them to achieve nice char marks on both sides.",
            "Roast the bell pepper chunks until the skin blisters and chars.",
            "Transfer the grilled vegetables to a large serving platter as they finish cooking.",
            "Drizzle extra balsamic glaze over the warm vegetables and garnish with fresh herbs and crumbled feta cheese."
        ]
    }
]


def seed_recipes():
    """Seed example recipes into the database"""
    print("=" * 60)
    print("Seeding Example Recipes")
    print("=" * 60)

    # Initialize NLP components
    taxonomy_actions = load_taxonomy_for_matcher(settings.TAXONOMY_PATH)
    matcher = ActionMatcher(taxonomy_actions)
    extractor = ActionExtractor(matcher, settings.SPACY_MODEL)

    recipes_added = 0

    with get_db_context() as db:
        for recipe_data in EXAMPLE_RECIPES:
            # Check if recipe already exists
            existing = db.query(Recipe).filter(
                Recipe.title == recipe_data["title"]
            ).first()

            if existing:
                print(f"\n⏭️  Skipping '{recipe_data['title']}' (already exists)")
                continue

            # Create recipe
            recipe = Recipe(
                title=recipe_data["title"],
                description=recipe_data["description"]
            )
            db.add(recipe)
            db.flush()  # Get the recipe ID

            # Add steps with NLP extraction
            print(f"\n📝 Processing '{recipe_data['title']}':")
            for idx, step_text in enumerate(recipe_data["steps"], 1):
                step = RecipeStep(
                    recipe_id=recipe.id,
                    step_number=idx,
                    instruction_text=step_text
                )
                db.add(step)
                db.flush()  # Get the step ID

                # Extract cooking actions using NLP
                try:
                    extracted = extractor.extract_actions(step_text)

                    if extracted:
                        # Get action IDs from extraction results
                        action_ids = [action["action_id"] for action in extracted]

                        # Find cooking actions in database by ID
                        actions = db.query(CookingAction).filter(
                            CookingAction.id.in_(action_ids)
                        ).all()

                        # Link actions to step
                        step.extracted_actions = actions
                        action_names = [a.canonical_name for a in actions]
                        print(f"  Step {idx}: {', '.join(action_names)}")
                    else:
                        print(f"  Step {idx}: (no techniques detected)")

                except Exception as e:
                    print(f"  Step {idx}: Error extracting actions - {e}")

            recipes_added += 1
            print(f"✅ Added '{recipe_data['title']}' with {len(recipe_data['steps'])} steps")

        db.commit()

    print("\n" + "=" * 60)
    print(f"✅ Seeding complete! Added {recipes_added} recipes")
    print("=" * 60)
    return recipes_added


def main():
    """Main entry point"""
    try:
        count = seed_recipes()
        if count > 0:
            print(f"\n🎉 Successfully seeded {count} example recipes!")
        else:
            print("\n✨ All recipes already exist in database")
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
