class SLL:
    """ Singly linked list implemented as a queue. """

    class SLLNode:
        """ Singly linked node. """

        def __init__(self, value: any, next_node=None):
            self.value: any = value
            self.next_node: SLL.SLLNode = next_node

        def __str__(self) -> str:
            return f"{self.value}"

    def __init__(self):
        self._root: SLL.SLLNode = SLL.SLLNode("root")
        self._end: SLL.SLLNode = self._root

    def push(self, value: any) -> None:
        """ Adds node with a given value to the end of the SLL. """

        self._end.next_node = SLL.SLLNode(value)
        self._end = self._end.next_node

    def pop(self) -> any:
        """ Removes and returns the head node from the SLL. """

        popped_value = self._root.next_node.value

        if self._root.next_node == self._end:
            self._end = self._root
        self._root.next_node = self._root.next_node.next_node

        return popped_value

    def remove(self, value: any, node=None) -> bool:
        """ Finds a given value and removes to from the SLL. """

        if not node:
            return self.remove(value, self._root)

        if not node.next_node:
            return False

        if value == node.next_node.value:
            node.next_node = node.next_node.next_node
            if not node.next_node:
                self._end = node
            return True

        return self.remove(value, node.next_node)

    def get_head(self) -> any:
        """ Returns the first node in the SLL"""

        return self._root.next_node.value

    def is_empty(self):
        return not self._root.next_node

    def __iter__(self):
        self.n = self._root.next_node
        return self

    def __next__(self):
        if self.n:
            value = self.n.value
            self.n = self.n.next_node
            return value
        else:
            raise StopIteration

    def __get_nodes(self, node) -> str:
        """ Get values of all nodes as a string. """

        if node:
            return f"{node} -> {self.__get_nodes(node.next_node)}"

        return "None"

    def __str__(self) -> str:
        return self.__get_nodes(self._root)


if __name__ == '__main__':
    test = SLL()
    test.push(1)
    test.push(2)
    test.push(3)
    test.push(4)
    print(test)
    print(test.pop())
    print(test)
    test.push(5)
    test.push(6)
    test.push(7)
    print(test)
    test.remove(4)
    print(test)
    for node_value in test:
        print(node_value)

