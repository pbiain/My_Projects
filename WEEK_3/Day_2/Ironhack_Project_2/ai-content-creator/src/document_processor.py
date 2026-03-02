# src/document_processor.py

# This function loads a markdown file and returns its full content as a string.
# It does NOT process the content — it just reads it.
def load_markdown(file_path):
    # Open the file in read mode ("r")
    # encoding="utf-8" ensures special characters are handled correctly
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# This function extracts a section of text between two markers.
# Example:
# extract_section(content, "## 1. Brand Voice", "## 2.")
def extract_section(content, start_marker, end_marker=None):

    try:
        # Split the full content at the start marker
        # The text after the marker will be at index [1]
        section = content.split(start_marker)[1]

        # If we define an end marker, stop extraction at that point
        if end_marker:
            section = section.split(end_marker)[0]

        # Remove extra whitespace and return clean text
        return section.strip()

    # If the markers are not found, prevent the program from crashing
    except IndexError:
        return ""