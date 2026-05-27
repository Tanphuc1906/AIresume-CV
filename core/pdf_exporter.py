def generate_markdown_file(markdown_text: str, output_path: str):
    """Lưu markdown ra file."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_text)
