# Recipe Image Platform - API Examples

## Complete API Usage Guide with Real Examples

---

## 1. Create a Recipe (POST)

### Simple Example: Garlic Pasta

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/recipes/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Simple Garlic Pasta",
    "description": "Quick and easy pasta with garlic and oil",
    "recipe_metadata": {
      "servings": 2,
      "prep_time_minutes": 5,
      "cook_time_minutes": 15,
      "difficulty": "easy"
    },
    "steps": [
      {
        "step_number": 1,
        "instruction_text": "Bring a large pot of salted water to a boil."
      },
      {
        "step_number": 2,
        "instruction_text": "Peel and mince 4 cloves of garlic finely."
      },
      {
        "step_number": 3,
        "instruction_text": "Grate the parmesan cheese and set aside."
      },
      {
        "step_number": 4,
        "instruction_text": "Sauté the minced garlic in olive oil until fragrant."
      },
      {
        "step_number": 5,
        "instruction_text": "Toss the cooked pasta with garlic oil and fold in parmesan."
      }
    ]
  }'
```

**Response (Excerpt):**
```json
{
  "id": "abc123-uuid",
  "title": "Simple Garlic Pasta",
  "steps": [
    {
      "step_number": 2,
      "instruction_text": "Peel and mince 4 cloves of garlic finely.",
      "extracted_actions": [
        {
          "canonical_name": "peel",
          "description": "Remove the outer skin or rind",
          "category": "cutting-prep",
          "confidence": 1.0
        },
        {
          "canonical_name": "mince",
          "description": "Cut into very small, fine pieces",
          "category": "cutting-prep",
          "confidence": 1.0
        }
      ]
    },
    {
      "step_number": 3,
      "instruction_text": "Grate the parmesan cheese and set aside.",
      "extracted_actions": [
        {
          "canonical_name": "grate",
          "confidence": 1.0
        }
      ]
    },
    {
      "step_number": 5,
      "instruction_text": "Toss the cooked pasta with garlic oil and fold in parmesan.",
      "extracted_actions": [
        {
          "canonical_name": "toss",
          "confidence": 1.0
        },
        {
          "canonical_name": "fold",
          "confidence": 1.0
        }
      ]
    }
  ]
}
```

**Detected Actions:** peel, mince, grate, toss, fold

---

## 2. Using Example Files

### Example 1: French Onion Soup (Complex Recipe)

```bash
# Located at: example_recipe.json
curl -X POST http://localhost:8000/api/v1/recipes/ \
  -H "Content-Type: application/json" \
  -d @example_recipe.json
```

**Actions Detected:**
- Cutting: peel, slice, chop, mince, grate
- Cooking: sauté, caramelize, simmer, toast
- Finishing: reduce, garnish, plate

**Total Steps:** 15
**Actions Extracted:** 21 occurrences across steps

---

### Example 2: Simple Pasta (Basic Recipe)

```bash
# Located at: examples/simple_pasta.json
curl -X POST http://localhost:8000/api/v1/recipes/ \
  -H "Content-Type: application/json" \
  -d @examples/simple_pasta.json
```

**Actions Detected:** mince, grate, stir, toss, fold
**Total Steps:** 9
**Actions Extracted:** 5 occurrences

---

### Example 3: Advanced Steak (Expert Recipe)

```bash
# Located at: examples/advanced_steak.json
curl -X POST http://localhost:8000/api/v1/recipes/ \
  -H "Content-Type: application/json" \
  -d @examples/advanced_steak.json
```

**Actions Detected:**
- Knife Skills: score, chop, slice
- Cooking: sear, reduce, cream
- Finishing: rest, drizzle, plate

**Total Steps:** 17
**Actions Extracted:** 12 occurrences

---

## 3. Get Recipe by ID

**Request:**
```bash
# Replace {recipe_id} with actual UUID from create response
curl http://localhost:8000/api/v1/recipes/446cf496-a797-4a41-9bfa-2a9d3781cafd
```

**Response:**
```json
{
  "id": "446cf496-a797-4a41-9bfa-2a9d3781cafd",
  "title": "Classic French Onion Soup",
  "description": "A rich, hearty soup...",
  "steps": [
    {
      "id": "step-uuid",
      "step_number": 1,
      "instruction_text": "Peel the onions and slice them thinly...",
      "extracted_actions": [
        {
          "id": "action-uuid",
          "canonical_name": "peel",
          "description": "Remove the outer skin or rind",
          "category": "cutting-prep",
          "image_url": null,
          "confidence": 1.0
        },
        {
          "id": "action-uuid",
          "canonical_name": "slice",
          "description": "Cut into thin, flat pieces",
          "category": "cutting-prep",
          "image_url": null,
          "confidence": 1.0
        }
      ]
    }
  ],
  "created_at": "2025-12-18T09:42:44.766087"
}
```

---

## 4. List All Recipes

**Request:**
```bash
# Get first 10 recipes
curl http://localhost:8000/api/v1/recipes/?skip=0&limit=10

# Get next 10 recipes (pagination)
curl http://localhost:8000/api/v1/recipes/?skip=10&limit=10
```

**Response:**
```json
[
  {
    "id": "recipe-1-uuid",
    "title": "Classic French Onion Soup",
    "description": "...",
    "steps": [...],
    "created_at": "2025-12-18T09:42:44"
  },
  {
    "id": "recipe-2-uuid",
    "title": "Simple Garlic Pasta",
    "description": "...",
    "steps": [...],
    "created_at": "2025-12-18T09:45:12"
  }
]
```

---

## 5. Get All Cooking Actions

**Request:**
```bash
curl http://localhost:8000/api/v1/actions/
```

**Response:**
```json
[
  {
    "id": "action-uuid",
    "canonical_name": "dice",
    "synonyms": ["cube", "cut into cubes", "dicing", "diced"],
    "description": "Cut food into small, uniform cubes (typically 0.5-1 cm)",
    "category": "cutting-prep",
    "priority": 1,
    "difficulty": "easy",
    "image_url": null,
    "thumbnail_url": null
  },
  {
    "id": "action-uuid",
    "canonical_name": "sauté",
    "synonyms": ["pan-fry", "fry lightly", "sauteing", "sauteed"],
    "description": "Cook food quickly in a small amount of fat over high heat",
    "category": "dry-heat-cooking",
    "priority": 1,
    "difficulty": "medium",
    "image_url": null,
    "thumbnail_url": null
  }
]
```

**Total Actions:** 50

---

## 6. Get Single Cooking Action

**Request:**
```bash
# Replace {action_id} with actual UUID
curl http://localhost:8000/api/v1/actions/{action_id}
```

---

## 7. Testing NLP Extraction

### Direct Text Testing

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/nlp/extract \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Dice the onions and sauté them in butter until golden brown"
  }'
```

**Response:**
```json
{
  "text": "Dice the onions and sauté them in butter until golden brown",
  "extracted_actions": [
    {
      "action_id": "uuid",
      "canonical_name": "dice",
      "matched_text": "dice",
      "confidence": 1.0,
      "position": {"start": 0, "end": 4}
    }
  ]
}
```

---

## 8. Advanced Usage: Batch Recipe Creation

### Creating Multiple Recipes

```bash
# Create recipes from multiple files
for file in examples/*.json; do
  echo "Creating recipe from $file"
  curl -X POST http://localhost:8000/api/v1/recipes/ \
    -H "Content-Type: application/json" \
    -d @"$file" -s | jq '.title'
  sleep 1
done
```

---

## 9. Pretty Output with jq

### Get Recipe with Formatted Output

```bash
curl -s http://localhost:8000/api/v1/recipes/{recipe_id} | jq '
{
  title: .title,
  total_steps: (.steps | length),
  actions: [.steps[].extracted_actions[].canonical_name] | unique
}'
```

**Output:**
```json
{
  "title": "Classic French Onion Soup",
  "total_steps": 15,
  "actions": [
    "caramelize",
    "chop",
    "grate",
    "mince",
    "peel",
    "plate",
    "reduce",
    "simmer",
    "slice",
    "stir",
    "toast",
    "toss"
  ]
}
```

---

## 10. Python Example

```python
import requests
import json

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

# Create a recipe
recipe_data = {
    "title": "Quick Omelette",
    "description": "Fast and easy breakfast",
    "steps": [
        {
            "step_number": 1,
            "instruction_text": "Whisk eggs with salt and pepper in a bowl."
        },
        {
            "step_number": 2,
            "instruction_text": "Dice vegetables and grate cheese."
        },
        {
            "step_number": 3,
            "instruction_text": "Pour eggs into pan and fold when set."
        }
    ]
}

# Send POST request
response = requests.post(f"{BASE_URL}/recipes/", json=recipe_data)
recipe = response.json()

# Print results
print(f"Created: {recipe['title']}")
print(f"ID: {recipe['id']}")

for step in recipe['steps']:
    actions = [a['canonical_name'] for a in step['extracted_actions']]
    if actions:
        print(f"Step {step['step_number']}: {', '.join(actions)}")
```

**Output:**
```
Created: Quick Omelette
ID: xyz789-uuid
Step 1: whisk
Step 2: dice, grate
Step 3: fold
```

---

## 11. JavaScript/Node.js Example

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000/api/v1';

async function createRecipe() {
  const recipe = {
    title: 'Grilled Cheese',
    description: 'Classic comfort food',
    steps: [
      {
        step_number: 1,
        instruction_text: 'Slice bread and grate cheese.'
      },
      {
        step_number: 2,
        instruction_text: 'Butter the bread slices on one side.'
      },
      {
        step_number: 3,
        instruction_text: 'Grill sandwich until golden and cheese melts.'
      }
    ]
  };

  const response = await axios.post(`${BASE_URL}/recipes/`, recipe);
  console.log('Created:', response.data.title);

  response.data.steps.forEach(step => {
    const actions = step.extracted_actions.map(a => a.canonical_name);
    if (actions.length > 0) {
      console.log(`Step ${step.step_number}: ${actions.join(', ')}`);
    }
  });
}

createRecipe();
```

---

## 12. Error Handling

### Invalid Request

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/recipes/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Recipe without steps"
  }'
```

**Response (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "loc": ["body", "steps"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Recipe Not Found

**Request:**
```bash
curl http://localhost:8000/api/v1/recipes/nonexistent-uuid
```

**Response (404 Not Found):**
```json
{
  "detail": "Recipe not found"
}
```

---

## 13. Performance Tips

### Efficient Recipe Creation
- Group related steps logically
- Use clear, descriptive action verbs
- Avoid overly generic instructions ("prepare the food")

### NLP Extraction Optimization
- Each recipe creation takes ~500ms for 15 steps
- Extractor initializes once and caches
- Database queries are optimized with indexes

---

## 14. Testing the Complete Flow

```bash
# 1. Check health
curl http://localhost:8000/health

# 2. Get all actions
curl http://localhost:8000/api/v1/actions/ | jq 'length'

# 3. Create a recipe
RECIPE_ID=$(curl -X POST http://localhost:8000/api/v1/recipes/ \
  -H "Content-Type: application/json" \
  -d @example_recipe.json -s | jq -r '.id')

# 4. Retrieve the recipe
curl http://localhost:8000/api/v1/recipes/$RECIPE_ID | jq '.title'

# 5. List all recipes
curl http://localhost:8000/api/v1/recipes/ | jq 'length'
```

---

## Summary of API Endpoints

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| GET | `/health` | Health check | `{"status": "healthy"}` |
| POST | `/api/v1/recipes/` | Create recipe with NLP | Recipe with actions |
| GET | `/api/v1/recipes/{id}` | Get single recipe | Full recipe details |
| GET | `/api/v1/recipes/` | List recipes (paginated) | Array of recipes |
| GET | `/api/v1/actions/` | List all cooking actions | Array of 50 actions |
| GET | `/api/v1/actions/{id}` | Get single action | Action details |
| POST | `/api/v1/nlp/extract` | Test NLP extraction | Extracted actions |

**Base URL:** `http://localhost:8000`
**Documentation:** `http://localhost:8000/docs`
**OpenAPI Schema:** `http://localhost:8000/openapi.json`

---

**Last Updated:** December 18, 2025
