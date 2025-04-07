from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("Leaf node must have a value")
        
        if not self.tag:
            return self.value
        
        props = self.props_to_html()

        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
    
    

