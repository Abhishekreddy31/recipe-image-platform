#!/usr/bin/env python3
"""
Recipe Creation Script
Run this locally to create the 5 example recipes via API
Usage: python create_recipes.py
"""
import requests
import json

# API endpoint
API_URL = "https://recipe-image-platform.onrender.com/api/v1/recipes"

# Example recipes
RECIPES = [
    {
        "title": "Pan-Seared Salmon with Roasted Vegetables and Garlic Herb Butter",
        "description": "A restaurant-quality dish featuring perfectly seared salmon with a crispy skin, accompanied by caramelized roasted vegetables and finished with a rich garlic herb butter sauce.",
        "steps": [
            {"step_number": 1, "instruction_text": "Dice the onions into small cubes and mince the garlic cloves finely using a sharp knife."},
            {"step_number": 2, "instruction_text": "Slice the bell peppers into strips and julienne the carrots into thin matchsticks."},
            {"step_number": 3, "instruction_text": "Chop the fresh herbs including parsley, thyme, and dill, then grate the lemon zest into a small bowl."},
            {"step_number": 4, "instruction_text": "Whisk together olive oil, lemon juice, salt, and pepper in a mixing bowl to create the marinade."},
            {"step_number": 5, "instruction_text": "Toss the vegetables in the marinade and roast them in a preheated oven at 400°F for 25 minutes until caramelized."},
            {"step_number": 6, "instruction_text": "Season the salmon fillets with salt and pepper, then sear them skin-side down in a hot skillet until the skin is crispy."},
            {"step_number": 7, "instruction_text": "Flip the salmon and baste it with butter, continuing to cook until it reaches medium doneness."},
            {"step_number": 8, "instruction_text": "In a separate pan, sauté the minced garlic in butter until fragrant, then stir in the chopped herbs."},
            {"step_number": 9, "instruction_text": "Simmer the garlic butter sauce gently while whisking to emulsify the butter with the pan juices."},
            {"step_number": 10, "instruction_text": "Plate the roasted vegetables, top with the seared salmon, and drizzle the garlic herb butter over everything. Garnish with fresh dill and lemon wedges."}
        ]
    },
    {
        "title": "Classic Italian Bolognese with Fresh Pasta",
        "description": "A traditional slow-cooked meat sauce with aromatic vegetables, served over homemade pasta. This authentic recipe requires patience but delivers incredible depth of flavor.",
        "steps": [
            {"step_number": 1, "instruction_text": "Dice the onions, carrots, and celery into small uniform cubes for the soffritto base."},
            {"step_number": 2, "instruction_text": "Mince the garlic cloves and chop fresh basil and oregano finely."},
            {"step_number": 3, "instruction_text": "In a large pot, sauté the diced vegetables in olive oil over medium heat until they soften and caramelize."},
            {"step_number": 4, "instruction_text": "Add ground beef and pork, breaking it up with a wooden spoon, and sear until browned on all sides."},
            {"step_number": 5, "instruction_text": "Pour in red wine and simmer until the alcohol evaporates and the liquid reduces by half."},
            {"step_number": 6, "instruction_text": "Stir in crushed tomatoes, tomato paste, and beef stock, then season with salt, pepper, and Italian herbs."},
            {"step_number": 7, "instruction_text": "Reduce heat to low and braise the sauce uncovered for 2-3 hours, stirring occasionally to prevent sticking."},
            {"step_number": 8, "instruction_text": "While the sauce simmers, knead pasta dough on a floured surface until smooth and elastic."},
            {"step_number": 9, "instruction_text": "Roll out the pasta dough thinly using a pasta machine or rolling pin, then slice into fettuccine ribbons."},
            {"step_number": 10, "instruction_text": "Boil the fresh pasta in salted water for 2-3 minutes until al dente, then drain and toss with the Bolognese sauce."},
            {"step_number": 11, "instruction_text": "Plate the pasta, garnish with fresh basil and grated Parmesan cheese, and drizzle with extra virgin olive oil."}
        ]
    },
    {
        "title": "Thai Green Curry with Jasmine Rice",
        "description": "An aromatic and spicy Thai curry featuring tender chicken, vegetables, and fragrant herbs in a creamy coconut milk base. Perfectly balanced with sweet, spicy, and savory notes.",
        "steps": [
            {"step_number": 1, "instruction_text": "Slice the chicken breast into bite-sized strips and season with salt and pepper."},
            {"step_number": 2, "instruction_text": "Dice the bell peppers and onions, then julienne the Thai basil leaves."},
            {"step_number": 3, "instruction_text": "Mince the garlic, ginger, and lemongrass stalks finely for the curry paste."},
            {"step_number": 4, "instruction_text": "Chop the green chilies and cilantro, keeping the stems separate from the leaves."},
            {"step_number": 5, "instruction_text": "In a wok, sauté the curry paste in coconut oil until fragrant and the oil separates."},
            {"step_number": 6, "instruction_text": "Add the sliced chicken and stir-fry until the pieces are seared and lightly browned."},
            {"step_number": 7, "instruction_text": "Pour in coconut milk and simmer gently, allowing the flavors to infuse."},
            {"step_number": 8, "instruction_text": "Toss in the diced vegetables and simmer until they're tender but still crisp."},
            {"step_number": 9, "instruction_text": "Stir in fish sauce, palm sugar, and lime juice to balance the flavors."},
            {"step_number": 10, "instruction_text": "Meanwhile, rinse jasmine rice and steam it in a rice cooker until fluffy and tender."},
            {"step_number": 11, "instruction_text": "Plate the steamed rice, ladle the green curry over it, and garnish with Thai basil and sliced red chilies."}
        ]
    },
    {
        "title": "Braised Short Ribs with Creamy Mashed Potatoes",
        "description": "Fall-off-the-bone tender beef short ribs slow-braised in red wine with aromatic vegetables, served alongside velvety mashed potatoes. Perfect comfort food for special occasions.",
        "steps": [
            {"step_number": 1, "instruction_text": "Season the short ribs generously with salt, pepper, and fresh thyme."},
            {"step_number": 2, "instruction_text": "Sear the ribs in a hot Dutch oven until deeply browned on all sides, then set aside."},
            {"step_number": 3, "instruction_text": "Dice the onions, carrots, and celery into large chunks for the braising base."},
            {"step_number": 4, "instruction_text": "Mince the garlic cloves and chop fresh rosemary and thyme."},
            {"step_number": 5, "instruction_text": "In the same pot, sauté the diced vegetables until caramelized and fragrant."},
            {"step_number": 6, "instruction_text": "Deglaze the pot with red wine, scraping up the browned bits from the bottom."},
            {"step_number": 7, "instruction_text": "Add beef stock, tomato paste, and the seared short ribs back to the pot."},
            {"step_number": 8, "instruction_text": "Cover and braise in a 325°F oven for 3-4 hours until the meat is fork-tender."},
            {"step_number": 9, "instruction_text": "While the ribs braise, peel and dice the potatoes into uniform chunks."},
            {"step_number": 10, "instruction_text": "Boil the potatoes in salted water until tender, then drain thoroughly."},
            {"step_number": 11, "instruction_text": "Mash the potatoes with butter, cream, and roasted garlic until smooth and creamy."},
            {"step_number": 12, "instruction_text": "Whip the mashed potatoes with a mixer to make them extra fluffy."},
            {"step_number": 13, "instruction_text": "Remove the short ribs from the braising liquid and strain the sauce through a fine sieve."},
            {"step_number": 14, "instruction_text": "Reduce the braising liquid on the stovetop until it thickens into a rich glaze."},
            {"step_number": 15, "instruction_text": "Plate the creamy mashed potatoes, top with the braised short ribs, and drizzle the reduced sauce over everything. Garnish with fresh thyme."}
        ]
    },
    {
        "title": "Grilled Mediterranean Vegetable Platter",
        "description": "A vibrant array of grilled seasonal vegetables with herb-infused olive oil and tangy balsamic glaze. Healthy, colorful, and bursting with smoky charred flavors.",
        "steps": [
            {"step_number": 1, "instruction_text": "Slice the eggplant, zucchini, and yellow squash into 1/2-inch thick rounds."},
            {"step_number": 2, "instruction_text": "Dice the red bell peppers and red onions into large chunks suitable for grilling."},
            {"step_number": 3, "instruction_text": "Halve the cherry tomatoes and slice the mushrooms thickly."},
            {"step_number": 4, "instruction_text": "Chop fresh basil, oregano, and parsley, then mince the garlic."},
            {"step_number": 5, "instruction_text": "Whisk together olive oil, balsamic vinegar, minced garlic, and chopped herbs to make a marinade."},
            {"step_number": 6, "instruction_text": "Toss all the sliced vegetables in the marinade and let them rest for 15 minutes."},
            {"step_number": 7, "instruction_text": "Preheat the grill to medium-high heat and oil the grates to prevent sticking."},
            {"step_number": 8, "instruction_text": "Grill the marinated vegetables in batches, turning them to achieve nice char marks on both sides."},
            {"step_number": 9, "instruction_text": "Roast the bell pepper chunks until the skin blisters and chars."},
            {"step_number": 10, "instruction_text": "Transfer the grilled vegetables to a large serving platter as they finish cooking."},
            {"step_number": 11, "instruction_text": "Drizzle extra balsamic glaze over the warm vegetables and garnish with fresh herbs and crumbled feta cheese."}
        ]
    }
]


def create_recipes():
    """Create all recipes via API"""
    print("=" * 70)
    print("Recipe Creation Script")
    print("=" * 70)
    print(f"\nAPI Endpoint: {API_URL}")
    print(f"Creating {len(RECIPES)} recipes...\n")

    created_recipes = []

    for i, recipe_data in enumerate(RECIPES, 1):
        print(f"{i}. Creating: {recipe_data['title'][:60]}...")

        try:
            response = requests.post(API_URL, json=recipe_data, timeout=30)

            if response.status_code == 201:
                recipe = response.json()
                created_recipes.append(recipe)

                # Count techniques
                total_techniques = sum(len(step['extracted_actions']) for step in recipe['steps'])
                techniques_with_images = sum(
                    sum(1 for action in step['extracted_actions'] if action.get('image_url'))
                    for step in recipe['steps']
                )

                print(f"   ✅ Success! ID: {recipe['id']}")
                print(f"   📊 {total_techniques} techniques extracted | {techniques_with_images} with images")
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                print(f"   Error: {response.text[:200]}")

        except requests.exceptions.RequestException as e:
            print(f"   ❌ Network error: {e}")

        print()

    # Summary
    print("=" * 70)
    print(f"✅ Successfully created {len(created_recipes)}/{len(RECIPES)} recipes")
    print("=" * 70)

    if created_recipes:
        print("\n📋 Recipe URLs:")
        frontend_base = "https://recipe-image-platformv2-j7dryrqtz-abhishekreddy31s-projects.vercel.app"
        for recipe in created_recipes:
            print(f"\n• {recipe['title']}")
            print(f"  🔗 {frontend_base}/recipes/{recipe['id']}")

        print(f"\n🎉 All done! View your recipes at: {frontend_base}")
    else:
        print("\n❌ No recipes were created. Check your API endpoint and try again.")


if __name__ == "__main__":
    create_recipes()
