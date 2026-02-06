def get_key_points(text):
    """
    This function extracts important discussion points
    from a meeting transcript.
    """
    sentences = text.split(".")

    keywords = [
        "discussed",
        "decided",
        "agreed",
        "plan",
        "meeting",
        "conclude"
    ]

    key_points = []

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        for word in keywords:
            if word in sentence.lower():
                if sentence not in key_points:
                    key_points.append(sentence)
                break

    return key_points
