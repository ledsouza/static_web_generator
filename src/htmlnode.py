class HTMLNode:
    """
    Represents a basic HTML node. Can be either a parent node or a leaf node.

    Args:
        tag (str, optional): The HTML tag name (e.g., "div", "p", "span"). Defaults to None.
        value (str, optional): Text content of the node. Defaults to None.
        children (object, optional): A list of child HTMLNode objects. Defaults to None.
        **props: Additional attributes for the HTML node, provided as key-value pairs.
    """

    def __init__(
        self, tag: str = None, value: str = None, children: object = None, **props
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        """Abstract method to generate the HTML representation of the node.

        Raises:
            NotImplementedError: This method must be implemented in derived classes.
        """
        raise NotImplementedError
    
    def props_to_html(self):
        """
        Converts the node's properties (props) into a string of HTML attributes.

        Returns:
            str: A string containing HTML attributes, or an empty string if no properties are defined.
        """
        if not self.props:
            return ""
        return " " + " ".join([f'{key}="{value}"' for key, value in self.props.items()])
    
    def __eq__(self, other_object: object) -> bool:
        """
        Determines if two HTMLNode objects are considered equal.

        Args:
            other_object (object): The other HTMLNode object to compare with.

        Returns:
            bool: True if the nodes have the same tag, value, children, and properties. False otherwise.
        """
        return (
            self.tag == other_object.tag and
            self.value == other_object.value and
            self.children == other_object.children and
            self.props == other_object.props
        )
    
    def __repr__(self) -> str:
        """
        Creates a string representation of the HTMLNode object.

        Returns:
            str: A string containing the class name and its attributes.
        """
        return f"{self.__class__.__name__}({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    """
    Represents a leaf HTML node (an HTML node without children).

    Args:
        tag (str): The HTML tag name.
        value (str): The text content of the leaf node.
        **props: Additional HTML attributes for the node.
    """

    def __init__(self, tag: str, value: str, **props) -> None:
        super().__init__(tag, value, None, **props)

    def to_html(self):
        """
        Generates the HTML representation of the LeafNode.

        Returns:
            str: The HTML representation of the leaf node.

        Raises:
            ValueError: If the 'value' is None or the 'tag' is None.
        """
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    """
    Represents a parent HTML node (an HTML node with child nodes).

    Args:
        tag (str):  The HTML tag name.
        children (object): A list of child HTMLNode objects. 
        **props: Additional HTML attributes for the node.
    """
    def __init__(self, tag: str, children: list[object], **props) -> None:
        super().__init__(tag, None, children, **props)

    def to_html(self):
        """
        Generates the HTML representation of the ParentNode and its children.

        Returns:
            str: The HTML representation of the parent node.

        Raises:
            ValueError: If the 'tag' is None or the 'children' list is None.
        """
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        return f"<{self.tag}{self.props_to_html()}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"
    
    def __repr__(self) -> str:
        """
        Creates a string representation of the ParentNode object.

        Returns:
            str: A string containing the class name and its attributes.
        """
        return f"{self.__class__.__name__}({self.tag}, {self.value}, {self.children}, {self.props})"