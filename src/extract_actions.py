from typing import List, Dict

try:
    import spacy
    # Load spaCy model
    nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True
except Exception:
    SPACY_AVAILABLE = False
    print("Warning: spaCy not found or model missing. Using regex fallback.")


ACTION_VERBS = {
    "complete", "prepare", "submit", "deliver", "review",
    "schedule", "plan", "update", "finish", "assign",
    "organize", "follow", "call", "send", "create",
    "develop", "implement", "design", "fix", "analyze"
}

MODAL_WORDS = {"will", "should", "must", "need", "needs", "have", "has"}


def is_action_sentence(sentence):
    """
    Detect whether sentence contains action-related structure.
    """
    doc = nlp(sentence)

    for token in doc:
        # Check modal verbs (will, should, must)
        if token.lemma_.lower() in MODAL_WORDS:
            return True

        # Check strong action verbs
        if token.lemma_.lower() in ACTION_VERBS and token.pos_ == "VERB":
            return True

    return False


def extract_owner(doc):
    """
    Extract person responsible (NER based).
    """
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None


def extract_deadline(doc):
    """
    Extract deadline using DATE entity.
    """
    for ent in doc.ents:
        if ent.label_ == "DATE":
            return ent.text
    return None


def get_actions_regex(text: str) -> List[Dict]:
    """
    Fallback regex-based action extraction.
    """
    import re
    actions = []
    
    # Simple sentence splitting
    sentences = re.split(r'[.!?]', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        lower_sent = sentence.lower()
        
        # Check for modals or action verbs
        has_modal = any(w in lower_sent.split() for w in MODAL_WORDS)
        has_verb = any(w in lower_sent.split() for w in ACTION_VERBS)
        
        if has_modal or has_verb:
            # Attempt to extract owner (simple heuristic: word before modal/verb)
            owner = "Unknown"
            
            # Look for explicit subject patterns like "John will", "I need to", "She must"
            # Pattern: (Subject) (Modal)
            # Match Names (Capitalized) or Pronouns (case-insensitive)
            match = re.search(r'\b([A-Z][a-z]+|I|i|We|we|He|he|She|she|They|they)\b\s+(?:will|must|should|can|could)', sentence)
            if match:
                owner = match.group(1).title() # Normalize to Title Case (e.g. "i" -> "I")
            
            # Attempt to extract deadline
            # Pattern: by (Day/Time), on (Date)
            deadline = None
            date_match = re.search(r'\b(?:by|on|at|before)\s+((?:[0-9]{1,2}(?:st|nd|rd|th)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*)|(?:Monday|Tuesday|Wednesday|Thursday|Friday)|(?:tomorrow|next week))', sentence, re.IGNORECASE)
            if date_match:
                deadline = date_match.group(1)

            actions.append({
                "action": sentence,
                "owner": owner,
                "deadline": deadline
            })
            
    return actions


def get_actions(text: str) -> List[Dict]:
    """
    Extract structured action items from transcript.
    """
    if not SPACY_AVAILABLE:
        return get_actions_regex(text)

    doc = nlp(text)
    actions = []

    for sentence in doc.sents:
        sent_text = sentence.text.strip()

        if is_action_sentence(sent_text):

            sent_doc = nlp(sent_text)

            action_item = {
                "action": sent_text,
                "owner": extract_owner(sent_doc),
                "deadline": extract_deadline(sent_doc)
            }

            actions.append(action_item)

    return actions