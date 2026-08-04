import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    # Html Node tests
    def test_eq(self):
        node = HTMLNode(tag="a", value="This is a link", children=None, props={"href": "https://www.google.com"})
        node2 = HTMLNode(tag="a", value="This is a link", children=None, props={"href": "https://www.google.com"})
        self.assertEqual(node, node2)

    def test_props_none(self):
        node = HTMLNode(tag="a", value="This is a link", children=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html(self):
        node = HTMLNode(
            tag="a",
            value="This is a link",
            children=None,
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    # Leaf node tests
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    # Parent node tests

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
