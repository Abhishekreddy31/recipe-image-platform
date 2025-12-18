"""NLP Testing API endpoints"""
from fastapi import APIRouter

from ...schemas import NLPExtractRequest, NLPExtractResponse
from ...nlp import ActionExtractor, ActionMatcher
from ...nlp.action_matcher import load_taxonomy_for_matcher
from ...config import settings

router = APIRouter()

# Initialize NLP components
_extractor = None

def get_extractor():
    """Lazy load NLP extractor"""
    global _extractor
    if _extractor is None:
        taxonomy_actions = load_taxonomy_for_matcher(settings.TAXONOMY_PATH)
        matcher = ActionMatcher(taxonomy_actions)
        _extractor = ActionExtractor(matcher, settings.SPACY_MODEL)
    return _extractor


@router.post("/extract", response_model=NLPExtractResponse)
async def extract_actions(request: NLPExtractRequest):
    """
    Test endpoint: Extract cooking actions from text

    This endpoint is for testing NLP extraction without creating a recipe.
    """
    extractor = get_extractor()
    extracted = extractor.extract_actions(request.text)

    return {
        "text": request.text,
        "extracted_actions": extracted
    }
