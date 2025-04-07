from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict = None):
        super().__init__(tag, None, children, props)
        self.children = children if children is not None else []

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node must have a tag")

        if not self.children:
            raise ValueError("Parent node must have children")

        props = self.props_to_html()
        children_html = "".join(child.to_html() for child in self.children)

        return f"<{self.tag}{props}>{children_html}</{self.tag}>"
    
    

