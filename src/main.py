from textnode import TextNode, TextType


def main():
    testNode = TextNode("Some Anchor Text", TextType.LINK, "pokemonshowdown.com")
    print(repr(testNode))


if __name__ == "__main__":
    main()
