from al_struct.exceptions import NodeNotFoundException, EmptyListException
from al_struct.utils.nodes import Node


class SinglyLinkedList:
    """A singly linked list data structure."""

    def __init__(self):
        """Initialize an empty singly linked list."""
        self._head = None

    def __str__(self):
        values = []
        tmp = self._head
        while tmp:
            values.append(str(tmp.data))
            tmp = tmp.next
        del tmp
        return " -> ".join(values)

    def __repr__(self):
        return f"SinglyLinkedList({str(self)})"

    def __len__(self):
        """Return len(self)"""
        size = 0
        tmp = self._head
        while tmp:
            size += 1
            tmp = tmp.next
        return size

    def __iter__(self):
        """Initialize an iterator over the linked list."""
        self._current = self._head
        return self

    def __next__(self):
        """Get the next element in the iteration."""
        if self._current:
            current = self._current
            self._current = self._current.next
            return current.data
        else:
            raise StopIteration

    def is_empty(self) -> bool:
        """
        Check if the linked list is empty.
        :returns: bool -- True if the linked list is empty, otherwise False.
        """
        return self._head is None

    def prepend(self, data) -> None:
        """
        Add a new node with data to the beginning of the list.
        :param data: The data to be added to the list.
        """
        node = Node(data)
        node.next = self._head
        self._head = node

    def append(self, data) -> None:
        """
        Add a new node with data to the end of the list.
        :param data: The data to be added to the list.
        """
        node = Node(data)
        if not self._head:
            self._head = node
            return
        tmp = self._head
        while tmp.next:
            tmp = tmp.next
        tmp.next = node

    def get_head(self):
        """
        Get data of the first node in the list.
        :return: The data of the first node in the list.
        """
        if not self._head:
            raise EmptyListException()
        return self._head.data

    def get_tail(self):
        """
        Get data of the last node in the list.
        :return: The data of the last node in the list.
        """
        if not self._head:
            raise EmptyListException()
        temp = self._head
        while temp.next:
            temp = temp.next
        return temp.data

    def get(self, data):
        """
        Return the node that contains data if exist in the list.
        :param data: The data to search for.
        :return: Node -- The node that contains data if exists, otherwise None.
        """
        temp = self._head
        while temp:
            if temp.data == data:
                return temp
            temp = temp.next
        return None

    def search(self, data) -> bool:
        """
        Return boolean value if data exists in the list.
        :param data: The data to search for.
        :return: bool -- True if data exists, otherwise False.
        """
        temp = self._head
        while temp:
            if temp.data == data:
                return True
            temp = temp.next
        return False

    def index(self, data) -> int:
        """
        Find the index of the first occurrence of data in the linked list.
        :param data: The data to search for in the list.
        :returns: int -- The index of the first occurrence of the data.
        :raises NodeNotFoundException: If the data is not found in the linked list.
        """
        index = 0
        temp = self._head
        while temp:
            if temp.data == data:
                return index
            temp = temp.next
            index += 1
        raise NodeNotFoundException(data)

    def delete(self, data) -> None:
        """
        Delete the first occurrence of data in the linked list.
        :param data: The data to be deleted
        """
        if not self._head:
            raise EmptyListException()
        if self._head.data == data:
            temp = self._head
            self._head = self._head.next
            del temp
            return
        current = self._head
        while current.next:
            if current.next.data == data:
                temp = current.next
                current.next = current.next.next
                del temp
                return
            current = current.next
        raise NodeNotFoundException(data)
