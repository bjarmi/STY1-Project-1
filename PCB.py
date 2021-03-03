from SLL import SLL


class PCB:
    """ Process Control Block. """

    def __init__(self, state=1, parent=0, priority=0):
        self._state: int = state  # 0 = Blocked. 1 = Ready
        self._parent: int = parent
        self._priority: int = priority
        self._children: SLL = SLL()
        self._resources: SLL = SLL()

    @property
    def state(self) -> int:
        return self._state

    @property
    def parent(self) -> int:
        return self._parent

    @property
    def priority(self) -> int:
        return self._priority

    @property
    def children(self):
        return self._children

    @property
    def recourses(self):
        return self._resources

    @state.setter
    def state(self, state: int) -> None:
        self._state = state

    def add_child(self, child_index: int) -> None:
        self._children.push(child_index)

    def add_recourse(self, recourse: int) -> None:
        self._resources.push(recourse)

    def remove_child(self, child_index: int) -> None:
        self._children.remove(child_index)

    def remove_recourse(self, recourse_int: int) -> bool:
        return self._resources.remove(recourse_int)

    def __str__(self):
        return f"State: {self._state}\n" \
               f"Parent: {self._parent}\n" \
               f"Children: {self._children}\n" \
               f"Recourses: {self._resources}"



