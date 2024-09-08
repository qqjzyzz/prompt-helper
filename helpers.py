def calculate_height(text, line_height=24):
    lines = text.count('\n') + 1
    return min(800, max(200, lines * line_height))
