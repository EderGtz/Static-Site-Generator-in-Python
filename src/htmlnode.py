
class HTMLNode:

    def __init__(self,tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    #This method is supossed to be overrided
    def to_html(self):
        raise NotImplementedError
    
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