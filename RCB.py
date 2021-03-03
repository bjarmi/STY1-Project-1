from SLL import SLL


class RCB:
    """ Resource Control Block"""

    def __init__(self):
        self._state: int = 0  # 0 = free. 1 = allocated
        self._wait_list: SLL = SLL()

    @property
    def state(self) -> int:
        return self._state

    def release(self) -> int or None:
        """ Release recourse. """
        if self._wait_list.is_empty():
            self._state = 0
            return

        return self._wait_list.pop()

    def request(self) -> int:
        """ Request recourse. """
        if self._state:
            return 0

        self._state = 1
        return 1

    def add_to_wait_list(self, process_index: int) -> None:
        """ Adds process_index to wait_list. """

        self._wait_list.push(process_index)

    def remove_from_wait_list(self, process_index) -> None:
        """ Remove process_index from wait_list"""

        self._wait_list.remove(process_index)
