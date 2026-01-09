"""The classes created here helps to identify the nodes that will be created using the mdNodes"""
class HTMLNode:
    #all set to None because the natural properties of html nodes
    def __init__(self,tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    #This method is supossed to be overrided
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    def properties_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        props_str = ""
        for key in self.props:
            props_str += f' {key}="{self.props[key]}"'
        return props_str 
    def __eq__(self, other):
        return (
            other.tag == self.tag and
            other.value == self.value and
            other.children == self.children and
            other.props == self.props
        )
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.properties_to_html()})"  
#A leaf represents a single HTML tag with no children
class LeafNode(HTMLNode):
    def __init__(self,tag, value, props = None):
        super().__init__(tag=tag, value=value, props=props)
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value #returned as raw text
        return f"<{self.tag}{self.properties_to_html()}>{self.value}</{self.tag}>"
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.properties_to_html()})"  
"""This class handle the nesting of HTML nodes inside of one another. These
kind of nodes have children, and are any HTML node that is not a LeafNode"""
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag=tag, children=children,props=props)
    def to_html(self):
        if not self.tag:
            raise ValueError("Tag argument requiered")
        if not self.children:
            raise ValueError("Children argument required")
        #Recursively converts the node and its children to HTML
        #Since to_html form LeafNode does not call .to_html, it is the case
        #base. This is a DFS because it has to go to the last child
        #until go back and enclose all between the self.tag
        final_html = ""
        for child in self.children:
            final_html += child.to_html()
        return f"<{self.tag}{self.properties_to_html()}>{final_html}</{self.tag}>"
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
