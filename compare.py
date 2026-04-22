import difflib

def compare_texts(text1, text2):
    # Split texts into lines for better comparison
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()

    # Generate the differences
    differences = difflib.ndiff(lines1, lines2)

    # Print the legend to understand the output
    print("=== COMPARISON RESULT ===")
    print(" Legend:")
    print(" [ ] (space) = Line is identical in both.")
    print(" [-]         = Line was REMOVED (in text 1, but not in 2).")
    print(" [+]         = Line was ADDED (in text 2, but not in 1).")
    print(" [?]         = Points exactly to the word or letter that changed.")
    print("=" * 35 + "\n")

    # Print the comparison line by line
    for line in differences:
        print(line)

# --- PROGRAM TEST ---

original_text = """Hello, world.
This is a small program.
It is used to compare texts."""

modified_text = """Hello, dear world.
This is a small and awesome program.
It is used to compare texts."""

# Call the function
compare_texts(original_text, modified_text)