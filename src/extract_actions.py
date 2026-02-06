import spacy
from typing import List, Dict

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


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


def get_actions(text: str) -> List[Dict]:
    """
    Extract structured action items from transcript.
    """

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