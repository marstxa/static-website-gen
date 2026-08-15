def extract_title(markdown):
    lines = markdown.splitlines()

    for line in lines:
        if line.startswith("# "):
            return line.strip("#").strip()

    raise Exception("There is no title in this markdown file")
