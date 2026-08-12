from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    lines = block.splitlines()

    # HEADING
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    # CODE: First and last line must be exactly ``` (ignoring indentation spaces)
    if len(lines) > 1 and lines[0].strip() == "```" and lines[-1].strip() == "```":
        return BlockType.CODE

    # QUOTE
    if block.startswith(">"):
        for line in lines:
            if not line.lstrip().startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    # UNORDERED LIST
    if block.startswith("- ") or block.startswith("* "):
        for line in lines:
            if not (line.lstrip().startswith("- ") or line.lstrip().startswith("* ")):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    # ORDERED LIST
    if block.startswith("1. "):
        expected_number = 1
        for line in lines:
            if not line.lstrip().startswith(f"{expected_number}. "):
                return BlockType.PARAGRAPH
            expected_number += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
