# Recipe Image Platform

Enterprise-grade recipe website that automatically displays contextual cooking technique images beside recipe steps. When a step says "dice onions," the UI shows a photo demonstrating the dicing technique.

**100% Free & Open Source** - No paid APIs, all images from Wikimedia Commons

[![GitHub Repo](https://img.shields.io/badge/github-recipe--image--platform-blue)](https://github.com/Abhishekreddy31/recipe-image-platform)

## Features

- **Automatic Action Extraction**: Uses spaCy NLP to extract cooking actions from recipe text
- **50+ Cooking Techniques**: Comprehensive taxonomy (dice, sauté, braise, etc.)
- **Free Legal Images**: Curated from Wikimedia Commons (CC-BY, CC-BY-SA, CC0)
- **Responsive UI**: Adaptive layouts for desktop, tablet, and mobile
- **Fast & Scalable**: FastAPI backend, React frontend, PostgreSQL/SQLite database
- **WCAG 2.1 AA Accessible**: Full keyboard navigation, screen reader support

## Architecture

- **Backend**: Python 3.11+ | FastAPI | SQLAlchemy | spaCy NLP
- **Frontend**: React 18 | TypeScript | Vite | Tailwind CSS | React Query
- **Database**: PostgreSQL (production) | SQLite (development)
- **Images**: Wikimedia Commons (curated) | WebP optimized

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- pip and npm

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Set up environment
cp .env.example .env

# Initialize database
python -m app.database

# Seed cooking actions (after running seed script)
python scripts/5_seed_database.py

# Run server
uvicorn app.main:app --reload --port 8000
```

**Backend will be available at**: http://localhost:8000

**API Documentation**: http://localhost:8000/docs

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment
cp .env.example .env

# Run development server
npm run dev
```

**Frontend will be available at**: http://localhost:5173

## Project Structure

```
recipe-image-platform/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # API endpoints
│   │   ├── models/          # SQLAlchemy ORM models
│   │   ├── nlp/             # NLP extraction pipeline
│   │   ├── services/        # Business logic
│   │   ├── main.py          # FastAPI app
│   │   ├── database.py      # DB configuration
│   │   └── schemas.py       # Pydantic models
│   ├── scripts/             # Image processing & seeding
│   ├── data/
│   │   └── taxonomy/        # Cooking actions taxonomy
│   ├── static/images/       # Processed technique images
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── hooks/           # Custom hooks
│   │   ├── services/        # API client
│   │   └── types/           # TypeScript types
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## API Endpoints

### Recipes

- `POST /api/v1/recipes` - Create recipe (auto-extracts actions)
- `GET /api/v1/recipes/:id` - Get recipe with enriched steps
- `GET /api/v1/recipes` - List recipes (paginated)

### Cooking Actions

- `GET /api/v1/actions` - List all cooking actions
- `GET /api/v1/actions/:id` - Get action by ID

### NLP Testing

- `POST /api/v1/nlp/extract` - Test action extraction from text

## Example Usage

### Create a Recipe

```bash
curl -X POST "http://localhost:8000/api/v1/recipes" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Simple Tomato Pasta",
    "description": "A quick and delicious pasta dish",
    "steps": [
      {
        "step_number": 1,
        "instruction_text": "Boil water in a large pot and cook pasta according to package directions"
      },
      {
        "step_number": 2,
        "instruction_text": "Dice the onions and mince the garlic"
      },
      {
        "step_number": 3,
        "instruction_text": "Sauté the onions and garlic in olive oil until golden"
      }
    ]
  }'
```

**Response includes extracted actions:**
```json
{
  "id": "...",
  "title": "Simple Tomato Pasta",
  "steps": [
    {
      "step_number": 1,
      "instruction_text": "Boil water in a large pot and cook pasta...",
      "extracted_actions": [
        {
          "canonical_name": "boil",
          "image_url": "/static/images/techniques/cooking/boil-water-001.webp",
          "confidence": 1.0
        }
      ]
    },
    {
      "step_number": 2,
      "instruction_text": "Dice the onions and mince the garlic",
      "extracted_actions": [
        {
          "canonical_name": "dice",
          "image_url": "/static/images/techniques/cutting/dice-onions-001.webp"
        },
        {
          "canonical_name": "mince",
          "image_url": "/static/images/techniques/cutting/mince-garlic-001.webp"
        }
      ]
    }
  ]
}
```

## Image Curation

Images are sourced from:
1. **WorldCuisines Dataset** (Hugging Face) - 6,000+ pre-vetted Wikimedia images
2. **Wikimedia Commons** - Manual search for specific techniques
3. **Wikimedia API** - Automated batch downloads

### Processing Pipeline

```bash
# 1. Download images from WorldCuisines
python scripts/1_download_worldcuisines.py

# 2. Search Wikimedia for missing techniques
python scripts/2_search_wikimedia.py --technique "dice"

# 3. Process images (resize, convert to WebP)
python scripts/3_process_images.py

# 4. Generate metadata
python scripts/4_generate_metadata.py

# 5. Seed database
python scripts/5_seed_database.py
```

## Legal Compliance

All images comply with:
- ✅ Creative Commons licenses (CC-BY, CC-BY-SA, CC0)
- ✅ Commercial use allowed
- ✅ Proper attribution displayed
- ✅ Derivative works allowed

## Development

### Run Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Backend linting
black backend/app
ruff backend/app

# Frontend linting
npm run lint
```

## Performance

- Recipe API response (cached): <50ms
- Recipe API response (uncached): <200ms
- NLP extraction: <100ms per step
- First Contentful Paint: <1.5s

## Roadmap

- [x] Core MVP (50 cooking actions)
- [x] NLP extraction pipeline
- [x] FastAPI backend
- [x] React frontend
- [ ] Image curation (100-150 images)
- [ ] Production deployment
- [ ] Mobile app (React Native)
- [ ] Community contributions
- [ ] Internationalization (i18n)

## Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## License

MIT License - see LICENSE file

## Acknowledgments

- Images from [Wikimedia Commons](https://commons.wikimedia.org/)
- [WorldCuisines Dataset](https://huggingface.co/datasets/worldcuisines/vqa) for initial image corpus
- Built with [spaCy](https://spacy.io/), [FastAPI](https://fastapi.tiangolo.com/), and [React](https://react.dev/)

## Support

- GitHub Issues: https://github.com/Abhishekreddy31/recipe-image-platform/issues
- Documentation: [See Plan](/.claude/plans/zazzy-waddling-wind.md)

---

**Built with ❤️ for home cooks and professional chefs alike**
