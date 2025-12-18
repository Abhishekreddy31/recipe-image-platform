"""Test NLP extraction"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.nlp import ActionExtractor, ActionMatcher
from app.nlp.action_matcher import load_taxonomy_for_matcher
from app.config import settings

# Load taxonomy
print("Loading taxonomy...")
taxonomy_actions = load_taxonomy_for_matcher(settings.TAXONOMY_PATH)
print(f"Loaded {len(taxonomy_actions)} actions")

# Create matcher and extractor
matcher = ActionMatcher(taxonomy_actions)
extractor = ActionExtractor(matcher, settings.SPACY_MODEL)

# Test extraction
test_texts = [
    "Peel the onions and slice them thinly",
    "Mince the garlic cloves finely",
    "Sauté the onions for 10-15 minutes",
    "Grate the Gruyère cheese",
    "Broil until golden brown"
]

print("\n" + "="*60)
print("Testing NLP Extraction")
print("="*60)

for text in test_texts:
    print(f"\nText: {text}")
    results = extractor.extract_actions(text)
    print(f"Extracted: {results}")
    if not results:
        print("  ⚠️  No actions extracted!")
