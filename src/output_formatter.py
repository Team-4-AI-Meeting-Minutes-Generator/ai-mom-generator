# output_formatter.py

def format_key_points(key_points):
    """
    Formats key discussion points as professional bullet points
    """
    output = "==============================\n"
    output += "🧠 KEY DISCUSSION POINTS\n"
    output += "==============================\n"

    if not key_points:
        output += "• No key discussion points identified.\n\n"
        return output

    for point in key_points:
        output += f"• {point.strip()}\n"

    output += "\n"
    return output


def format_action_items(action_items):
    """
    Formats action items in a structured professional format
    """
    output = "==============================\n"
    output += "✅ ACTION ITEMS\n"
    output += "==============================\n"

    if not action_items:
        output += "• No action items identified.\n\n"
        return output

    for idx, item in enumerate(action_items, 1):

        action_text = item.get("action", "Task not specified")
        owner = item.get("owner")
        deadline = item.get("deadline")

        output += f"{idx}. {action_text}\n"

        if owner:
            output += f"   ↳ Owner    : {owner}\n"

        if deadline:
            output += f"   ↳ Deadline : {deadline}\n"

        output += "\n"

    return output


def format_output(data):
    """
    Main function called by main.py
    """
    result = ""
    result += format_key_points(data.get("key_points", []))
    result += format_action_items(data.get("action_items", []))
    return result