# Recipe Image Platform - Usage Guide

## System Overview

The Recipe Image Platform automatically extracts cooking techniques from recipe instructions using NLP and displays instructional images alongside each step.

## Running the Application

### Backend (Already Running)
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Frontend (Already Running)
```bash
cd frontend
npm run dev
```
- Application: http://localhost:5173

## Creating Recipes

### Method 1: Using the API Directly

Create a JSON file with your recipe:

```json
{
  "title": "Your Recipe Title",
  "description": "Brief description of the recipe",
  "recipe_metadata": {
    "servings": 4,
    "prep_time_minutes": 20,
    "cook_time_minutes": 30,
    "difficulty": "medium"
  },
  "steps": [
    {
      "step_number": 1,
      "instruction_text": "Dice the onions and mince the garlic."
    },
    {
      "step_number": 2,
      "instruction_text": "Sauté the vegetables in olive oil for 5 minutes."
    }
  ]
}
```

Then send a POST request:

```bash
curl -X POST http://localhost:8000/api/v1/recipes/ \
  -H "Content-Type: application/json" \
  -d @your_recipe.json
```

### Method 2: Using the Interactive API Documentation

1. Open http://localhost:8000/docs
2. Click on "POST /api/v1/recipes/"
3. Click "Try it out"
4. Paste your JSON in the request body
5. Click "Execute"

### Method 3: Using the Frontend (Future)

Visit http://localhost:5173 and use the recipe creation form (to be implemented).

## Example Recipe

A complete French Onion Soup example is available at:
`/Users/user/Documents/GitHub/pp/recipe-image/recipe-image-platform/example_recipe.json`

**Detected Techniques:**
- Step 1: peel, slice
- Step 2: mince, chop
- Step 3: toss, slice
- Step 4: stir
- Step 5: caramelize, stir, reduce
- Step 10: slice, toast
- Step 11: grate

## Currently Supported Cooking Actions (50 Total)

### Cutting & Preparation (15)
- dice, mince, chop, slice, julienne, brunoise, chiffonade
- peel, zest, grate, shred, debone, fillet, score, tenderize

### Mixing & Combining (8)
- whisk, stir, fold, beat, cream, knead, toss, emulsify

### Dry Heat Cooking (10)
- sauté, stir-fry, deep-fry, roast, bake, grill, broil, sear, toast, caramelize

### Moist Heat Cooking (10)
- boil, simmer, poach, steam, blanch, parboil, braise, stew, sous-vide, pressure-cook

### Finishing & Presentation (7)
- glaze, garnish, plate, drizzle, dust, rest, reduce

## How the NLP Extraction Works

1. **Lemmatization**: "chopped" → "chop", "dicing" → "dice"
2. **Synonym Matching**: "cube" → "dice", "pan-fry" → "sauté"
3. **Confidence Scoring**: >0.5 threshold for inclusion
4. **Generic Verb Filtering**: Removes "put", "let", "make", etc.

## API Endpoints

### Create Recipe
```bash
POST /api/v1/recipes/
Content-Type: application/json

{
  "title": "Recipe Name",
  "description": "Description",
  "steps": [...]
}
```

**Response**: Recipe with extracted actions and UUIDs

### Get Recipe
```bash
GET /api/v1/recipes/{recipe_id}
```

**Response**: Recipe with enriched action details

### List Recipes
```bash
GET /api/v1/recipes/?skip=0&limit=10
```

**Response**: Paginated list of recipes

### Get All Cooking Actions
```bash
GET /api/v1/actions/
```

**Response**: List of all 50 cooking actions with metadata

## Response Format

Each recipe step includes extracted actions with full details:

```json
{
  "id": "uuid",
  "step_number": 1,
  "instruction_text": "Dice the onions and sauté in oil",
  "extracted_actions": [
    {
      "id": "action-uuid",
      "canonical_name": "dice",
      "description": "Cut into small, uniform cubes",
      "category": "cutting-prep",
      "confidence": 1.0,
      "image_url": null,
      "thumbnail_url": null
    },
    {
      "id": "action-uuid",
      "canonical_name": "sauté",
      "description": "Cook quickly in a small amount of fat",
      "category": "dry-heat-cooking",
      "confidence": 1.0,
      "image_url": null,
      "thumbnail_url": null
    }
  ]
}
```

## Testing NLP Extraction

Test the NLP extractor directly:

```bash
cd backend
source venv/bin/activate
python test_nlp.py
```

This will show you which actions are detected in sample recipe steps.

## Adding Images (Future Step)

Images are currently `null` because they haven't been curated yet. To add images:

1. Run the image curation scripts in `backend/scripts/`:
   - `1_download_worldcuisines.py` - Download from Hugging Face
   - `2_search_wikimedia.py` - Search Wikimedia Commons
   - `3_process_images.py` - Resize and optimize
   - `4_generate_metadata.py` - Create attribution metadata

2. Update the database:
   ```sql
   UPDATE cooking_actions
   SET image_url = '/static/images/techniques/cutting/dice-001.webp'
   WHERE canonical_name = 'dice';
   ```

## Known Limitations (MVP)

1. **Accent Sensitivity**: "Sauté" with accent (é) may not match "saute" in taxonomy
2. **Multi-word Actions**: "bring to a boil" detected as "boil" only
3. **Context Awareness**: Cannot distinguish "slice bread" from "slice onions"
4. **No Images Yet**: Image curation from Wikimedia Commons is pending

## Database Location

SQLite database file: `backend/recipe_platform.db`

View data directly:
```bash
sqlite3 backend/recipe_platform.db
.tables
SELECT * FROM cooking_actions LIMIT 5;
```

## Logs and Debugging

- Backend logs: Check console where uvicorn is running
- Frontend logs: Check browser console (F12)
- API errors: Returned in JSON response with status codes

## Next Steps

1. **Frontend Development**: Complete React UI for recipe browsing
2. **Image Curation**: Download and process 100-150 images
3. **Search Feature**: Add recipe search by ingredients or techniques
4. **User Authentication**: Add user accounts and saved recipes
5. **Mobile App**: React Native version

## Performance Metrics

- Recipe creation with NLP: ~500ms for 15-step recipe
- Action extraction accuracy: ~80-90% for common techniques
- Database size: ~50KB with 50 actions, <1MB with 100 recipes

## Support

- API Documentation: http://localhost:8000/docs
- GitHub Issues: (Add your repo URL)
- Email: (Add your email)

---

**Last Updated**: December 18, 2025
**Version**: 1.0.0 (MVP)
