# output_formatter.py

def format_key_points(key_points):
    """
    Formats key discussion points as professional bullet points
    """
    output = "### 🧠 Key Discussion Points\n"

    if not key_points:
        output += "• No key discussion points identified.\n\n"
        return output

    for point in key_points:
        output += f"• {point}\n"

    output += "\n"
    return output


def format_action_items(action_items):
    """
    Formats action items as professional bullet statements
    """
    output = "### ✅ Action Items\n"

    if not action_items:
        output += "• No action items identified.\n\n"
        return output

    for item in action_items:
        task = item.get("task", "Task not specified")
        owner = item.get("owner", "Owner not specified")
        deadline = item.get("deadline", "Deadline not specified")

        output += f"• **{owner}** will {task.lower()} by **{deadline}**\n"

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
