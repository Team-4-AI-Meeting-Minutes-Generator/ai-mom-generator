import spacy
from typing import List, Dict

nlp = spacy.load("en_core_web_sm")

def get_entities(text: str) -> List[Dict]:
    """
    Extract responsible persons and deadlines linked to actions.
    Returns list of dictionaries:
    [
        {
            "owner": "...",
            "action": "...",
            "deadline": "..."
        }
    ]
    """

    doc = nlp(text)
    entities_output = []

    current_deadline = None

    # Step 1: Detect global deadline if mentioned
    for ent in doc.ents:
        if ent.label_ == "DATE":
            current_deadline = ent.text

    # Step 2: Process sentence by sentence
    for sent in doc.sents:
        sentence_text = sent.text.strip()
        sent_doc = nlp(sentence_text)

        owner = None
        deadline = None
        action_phrase = None

        # Extract named entities
        for ent in sent_doc.ents:
            if ent.label_ == "PERSON":
                owner = ent.text
            elif ent.label_ == "DATE":
                deadline = ent.text

        # If no deadline in sentence, use global deadline
        if not deadline:
            deadline = current_deadline

        # Detect action verb using dependency parsing
        for token in sent_doc:
            if token.pos_ == "VERB" and token.dep_ == "ROOT":
                subject = None
                obj = None

                for child in token.children:
                    if child.dep_ in ("nsubj", "nsubjpass"):
                        subject = child.text
                    if child.dep_ in ("dobj", "attr", "prep", "pobj"):
                        obj = child.text

                if subject:
                    owner = subject

                if obj:
                    action_phrase = token.text + " " + obj
                else:
                    action_phrase = token.text

                break

        # Add only if meaningful entity found
        if owner or deadline:
            entities_output.append({
                "owner": owner if owner else "Not specified",
                "action": action_phrase if action_phrase else sentence_text,
                "deadline": deadline if deadline else "Not specified"
            })

    return entities_output