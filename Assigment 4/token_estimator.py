def estimate_tokens(text):
    """
    Estimate tokens in a text.
    Assumes 1 token ≈ 4 characters.
    """
    return len(text) // 4 + (1 if len(text) % 4 != 0 else 0)

file_path = input("Enter the path of the file: ")

try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
except FileNotFoundError:
    print("File not found. Please check the path!")
    exit()

words = content.split()
print(f"Word count: {len(words)}")

tokens = estimate_tokens(content)
print(f"Estimated tokens: {tokens}")

if len(content) > 4000:
    print("Warning: File contains more than 4000 characters!")
