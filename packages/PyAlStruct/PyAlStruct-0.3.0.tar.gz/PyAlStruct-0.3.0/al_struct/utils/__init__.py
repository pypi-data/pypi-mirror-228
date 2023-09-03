from .nodes import Node


def compare_nodes(node1: Node, node2: Node) -> bool:
    """
    Compare two Node instances.

    :param node1: The first Node instance.
    :param node2: The second Node instance.
    :return: True if the nodes are equal, False otherwise.
    """
    assert isinstance(node1, Node), "node1 should be a Node"
    assert isinstance(node2, Node), "node2 should be a Node"

    return node1.data == node2.data and node1.next == node2.next


__all__ = ["compare_nodes"]
