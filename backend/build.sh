#!/usr/bin/env bash
# Build script for Render deployment

set -e  # Exit on error

echo "==> Upgrading pip..."
pip install --upgrade pip

echo "==> Installing dependencies..."
pip install -r requirements.txt

echo "==> Installing spaCy language model..."
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl

echo "==> Creating database tables..."
python -c "from app.database import init_db; init_db()"

echo "==> Seeding cooking actions..."
python scripts/5_seed_database.py

echo "==> Linking images to cooking actions..."
python scripts/8_migrate_action_images.py

echo "==> Seeding example recipes..."
python scripts/6_seed_recipes.py

echo "==> Migrating existing recipes (re-extract actions)..."
python scripts/7_migrate_extract_actions.py

echo "==> Build completed successfully!"
