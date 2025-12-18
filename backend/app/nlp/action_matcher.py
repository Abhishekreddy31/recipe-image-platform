"""
Action Matcher - Maps extracted verbs to cooking actions using taxonomy
"""
from typing import Dict, List, Optional, Set
from uuid import UUID
import json
from pathlib import Path

class ActionMatcher:
    """Maps lemmatized verbs to cooking actions using synonym matching"""

    def __init__(self, cooking_actions: List[Dict]):
        """
        Initialize action matcher with cooking actions from database

        Args:
            cooking_actions: List of cooking action dicts with id, canonical_name, synonyms
        """
        self.action_map: Dict[str, UUID] = {}
        self.generic_verbs: Set[str] = {
            "put", "place", "let", "allow", "make", "get", "take",
            "add", "remove", "set", "use", "prepare", "cook"  # Too generic
        }

        self._build_action_map(cooking_actions)

    def _build_action_map(self, cooking_actions: List[Dict]):
        """
        Build lookup map from canonical names and synonyms to action IDs

        Args:
            cooking_actions: List of action dicts from database
        """
        for action in cooking_actions:
            action_id = action["id"]

            # Map canonical name
            canonical = action["canonical_name"].lower()
            self.action_map[canonical] = action_id

            # Map all synonyms
            for synonym in action.get("synonyms", []):
                synonym_lower = synonym.lower()
                # Store first matching action (priority given to first in taxonomy)
                if synonym_lower not in self.action_map:
                    self.action_map[synonym_lower] = action_id

    def match(self, lemma: str) -> Optional[UUID]:
        """
        Match a lemmatized verb to a cooking action ID

        Args:
            lemma: Lemmatized verb from spaCy

        Returns:
            Action UUID if matched, None otherwise
        """
        lemma_lower = lemma.lower()

        # Filter out generic verbs
        if lemma_lower in self.generic_verbs:
            return None

        # Direct match
        if lemma_lower in self.action_map:
            return self.action_map[lemma_lower]

        # Handle multi-word actions (e.g., "bring to boil")
        # This would require phrase matching - simplified for MVP
        return None

    def match_phrase(self, phrase: str) -> Optional[UUID]:
        """
        Match a multi-word phrase to a cooking action

        Args:
            phrase: Multi-word phrase (e.g., "bring to a boil")

        Returns:
            Action UUID if matched, None otherwise
        """
        phrase_lower = phrase.lower()

        # Normalize common variations
        normalized = phrase_lower.replace(" a ", " ").replace(" the ", " ").strip()

        # Try exact match first
        if normalized in self.action_map:
            return self.action_map[normalized]

        # Try individual words
        words = normalized.split()
        for word in words:
            if word in self.action_map:
                return self.action_map[word]

        return None

    def is_cooking_action(self, lemma: str) -> bool:
        """
        Check if a lemma is a known cooking action

        Args:
            lemma: Lemmatized verb

        Returns:
            True if it's a cooking action, False otherwise
        """
        return lemma.lower() in self.action_map

    def get_all_actions(self) -> List[str]:
        """Get list of all known action names"""
        return list(self.action_map.keys())


def load_taxonomy_for_matcher(taxonomy_path: str) -> List[Dict]:
    """
    Load cooking actions taxonomy and format for ActionMatcher

    Args:
        taxonomy_path: Path to cooking_actions_taxonomy.json

    Returns:
        List of action dicts suitable for ActionMatcher
    """
    with open(taxonomy_path, 'r') as f:
        taxonomy = json.load(f)

    actions = []
    for category in taxonomy["categories"]:
        for action in category["actions"]:
            actions.append({
                "id": action["id"],
                "canonical_name": action["canonical_name"],
                "synonyms": action.get("synonyms", []),
                "category": action.get("category"),
                "priority": action.get("priority", 1)
            })

    return actions
