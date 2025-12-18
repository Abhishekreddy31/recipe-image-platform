"""
Action Extractor - Extract cooking actions from recipe text using spaCy + rules
"""
import spacy
from typing import List, Dict, Optional
from uuid import UUID
from .action_matcher import ActionMatcher

class ActionExtractor:
    """Extract cooking actions from recipe step text using hybrid spaCy + rule-based approach"""

    def __init__(self, action_matcher: ActionMatcher, model_name: str = "en_core_web_sm"):
        """
        Initialize the action extractor

        Args:
            action_matcher: ActionMatcher instance with loaded taxonomy
            model_name: spaCy model to use (default: en_core_web_sm)
        """
        self.action_matcher = action_matcher
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            raise RuntimeError(
                f"spaCy model '{model_name}' not found. "
                f"Please install it with: python -m spacy download {model_name}"
            )

        # Context words that indicate cooking (boosts confidence)
        self.cooking_context_words = {
            "ingredient", "food", "mixture", "pan", "bowl", "pot", "oven",
            "heat", "oil", "water", "sauce", "until", "minutes", "seconds",
            "hot", "cold", "warm", "golden", "brown", "tender", "soft"
        }

    def extract_actions(self, text: str) -> List[Dict]:
        """
        Extract cooking actions from recipe step text

        Args:
            text: Recipe step instruction text

        Returns:
            List of extracted actions with metadata:
            [
                {
                    "action_id": UUID,
                    "matched_text": str,
                    "confidence": float,
                    "position": {"start": int, "end": int}
                }
            ]
        """
        # Preprocess text
        text = self._preprocess(text)

        # Process with spaCy
        doc = self.nlp(text)

        # Extract verbs
        verbs = [token for token in doc if token.pos_ == "VERB"]

        matched_actions = []

        for verb in verbs:
            # Get lemmatized form
            lemma = verb.lemma_.lower()

            # Try to match single verb
            action_id = self.action_matcher.match(lemma)

            if action_id:
                confidence = self._calculate_confidence(verb, doc)

                # Only include if confidence above threshold
                if confidence > 0.5:
                    matched_actions.append({
                        "action_id": str(action_id),
                        "matched_text": lemma,
                        "confidence": confidence,
                        "position": {
                            "start": verb.idx,
                            "end": verb.idx + len(verb.text)
                        }
                    })

        # Deduplicate and sort by confidence
        deduplicated = self._deduplicate(matched_actions)

        return deduplicated

    def _preprocess(self, text: str) -> str:
        """
        Clean and normalize text

        Args:
            text: Raw recipe step text

        Returns:
            Cleaned text
        """
        # Basic cleaning
        text = text.strip()

        # Remove extra whitespace
        text = " ".join(text.split())

        return text

    def _calculate_confidence(self, verb_token, doc) -> float:
        """
        Calculate confidence score based on context

        Args:
            verb_token: spaCy token for the verb
            doc: spaCy doc object

        Returns:
            Confidence score (0.0 to 1.0)
        """
        score = 1.0

        # Boost confidence if cooking context words nearby
        sentence_words = {token.text.lower() for token in verb_token.sent}
        if sentence_words & self.cooking_context_words:
            score *= 1.2

        # Check if verb has direct object (common in cooking instructions)
        has_dobj = any(child.dep_ == "dobj" for child in verb_token.children)
        if has_dobj:
            score *= 1.1

        # Cap at 1.0
        return min(score, 1.0)

    def _deduplicate(self, actions: List[Dict]) -> List[Dict]:
        """
        Remove duplicate actions, keeping highest confidence

        Args:
            actions: List of extracted actions

        Returns:
            Deduplicated list, sorted by confidence descending
        """
        seen = {}

        for action in actions:
            action_id = action["action_id"]

            if action_id not in seen or action["confidence"] > seen[action_id]["confidence"]:
                seen[action_id] = action

        # Sort by confidence (highest first)
        result = list(seen.values())
        result.sort(key=lambda x: x["confidence"], reverse=True)

        return result

    def extract_with_phrases(self, text: str) -> List[Dict]:
        """
        Extract actions including multi-word phrases (e.g., "bring to a boil")

        Args:
            text: Recipe step instruction text

        Returns:
            List of extracted actions with metadata
        """
        # Start with single-word extraction
        actions = self.extract_actions(text)

        # TODO: Add multi-word phrase detection
        # This would involve looking for patterns like:
        # - "bring to a boil" -> "boil"
        # - "fold in" -> "fold"
        # - "cut into cubes" -> "dice"

        return actions


class ActionExtractionError(Exception):
    """Raised when action extraction fails"""
    pass
