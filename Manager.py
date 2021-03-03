from SLL import SLL
from PCB import PCB
from RCB import RCB


class Manager:
    _MAX_PCBs = 16
    _MAX_RCPs = 4
    _PRIORITY_LEVELS = 3

    def __init__(self):
        self._PCBs: list[PCB or None] = []
        self._RCBs: list[RCB or None] = []
        self._RL: list[SLL] = []
        self._running_process: int = 0
        self._number_of_processes = 0

    def _add_process_to_pcb_list(self, process: PCB) -> int:
        for i in range(self._MAX_PCBs):
            if not self._PCBs[i]:
                self._PCBs[i] = process
                return i

    def _add_to_ready_list(self, process_index: int) -> None:
        priority = self._get_process(process_index).priority
        self._RL[priority].push(process_index)

    def _pop_ready_list(self, process_index: int) -> any:
        priority = self._get_process(process_index).priority
        return self._RL[priority].pop()

    def _erase_process(self, process_index: int) -> None:
        for child in self._get_process(process_index).children:
            self._erase_process(child)

        self._remove_from_ready_list(process_index)
        self._release_recourses(process_index)
        self._remove_from_wait_list(process_index)
        self._remove_form_children(process_index)
        self._PCBs[process_index] = None

    def _remove_form_children(self, process_index: int) -> None:
        parent = self._get_process(process_index).parent
        self._get_process(parent).remove_child(process_index)

    def _remove_from_ready_list(self, process_index: int) -> None:
        for sll in self._RL:
            sll.remove(process_index)

    def _remove_from_wait_list(self, process_index: int) -> None:
        for rcp in self._RCBs:
            rcp.remove_from_wait_list(process_index)

    def _release_recourses(self, process_index: int) -> None:
        for recourse in self._get_process(process_index).recourses:
            self._release_recourse(process_index, recourse)

    def _release_recourse(self, process_index: int,
                          recourse_index: int, ) -> None:

        next_process_index = self._get_recourse(recourse_index).release()

        self._get_process(process_index).remove_recourse(recourse_index)

        if next_process_index is not None:
            self._get_process(next_process_index).add_recourse(recourse_index)
            self._add_to_ready_list(next_process_index)

    def _get_process_index(self, process: PCB) -> int:
        return self._PCBs.index(process)

    def _get_process(self, process_index: int) -> PCB:
        return self._PCBs[process_index]

    def _get_recourse(self, recourse_index):
        return self._RCBs[recourse_index]

    def _update_number_of_processes(self) -> None:
        self._number_of_processes = 0
        for x in self._PCBs:
            if x:
                self._number_of_processes += 1

    def create(self, priority: int) -> int:
        """ Creat and add a new process to the ready list. """

        try:
            if self._number_of_processes == Manager._MAX_PCBs:
                raise Exception(f"Not enough space for a new PCB.")

            if not -1 < priority < Manager._PRIORITY_LEVELS:
                raise ValueError(f"Priority level must be in range 0 to "
                                 f"{Manager._PRIORITY_LEVELS - 1}.\n"
                                 f"Priority level {priority} was given.")
        except Exception as arg:
            print(arg)
            return -1

        new_process = PCB(1, self._running_process, priority)
        process_index = self._add_process_to_pcb_list(new_process)
        self._get_process(self._running_process).add_child(process_index)
        self._add_to_ready_list(process_index)
        self._number_of_processes += 1
        print(f"Process {process_index} created.")
        return self.scheduler()

    def destroy(self, process_index: int) -> int:
        """ Destroys the running process or a child of the running process. """

        num_processes = self._number_of_processes

        if process_index == 0:
            print(f"{num_processes} processes destroyed.")
            self.init()
            return num_processes

        destroy_running_process: bool = process_index == self._running_process
        destroy_child: bool = process_index in self._get_process(
            self._running_process).children

        try:
            if not destroy_running_process and not destroy_child:
                raise Exception(f"Process {process_index} not found.")

        except Exception as arg:
            print(arg)
            return -1

        self._erase_process(process_index)
        self._update_number_of_processes()
        self.scheduler()
        processes_destroyed: int = num_processes - self._number_of_processes
        print(f"{processes_destroyed} processes destroyed.")
        return self.scheduler()

    def request(self, recourse_index: int) -> int:
        """ Request a recourse for the currently running process. """
        try:
            if self._get_process(self._running_process) == self._PCBs[0]:
                raise Exception("Process 0 not allowed to request recourses. ")

            if not -1 < recourse_index < Manager._MAX_RCPs:
                raise Exception(f"Recourse {recourse_index} does not exist.")

        except Exception as arg:
            print(arg)
            return -1

        got_recourse: int = self._get_recourse(recourse_index).request()
        self._get_process(self._running_process).state = got_recourse

        if got_recourse == 0:
            self._remove_from_ready_list(self._running_process)
            self._get_recourse(recourse_index).add_to_wait_list(
                self._running_process)
            print(f"Process {self._running_process} blocked.")
            return self.scheduler()

        self._get_process(self._running_process).add_recourse(recourse_index)
        print(f"Recourse {recourse_index} allocated to process"
              f"{self._running_process}.")
        return self.scheduler()

    def release(self, recourse_index: int) -> int:
        """ Release a recourse. """
        try:
            if not -1 < recourse_index < Manager._MAX_RCPs:
                raise ValueError(f"Recourse {recourse_index} does not exist.")

            if recourse_index not in self._get_process(
                    self._running_process).recourses:
                raise Exception(f"Process {self._running_process} is not "
                                f"holding recourse {recourse_index}.")

        except Exception as arg:
            print(arg)
            return -1

        self._release_recourse(self._running_process, recourse_index)

        print(f"Recourse {recourse_index} released.")
        return self.scheduler()

    def timeout(self):
        process_index = self._pop_ready_list(self._running_process)
        self._add_to_ready_list(process_index)
        return self.scheduler()

    def scheduler(self) -> int:
        for i in range(self._PRIORITY_LEVELS - 1, -1, -1):
            if not self._RL[i].is_empty():
                self._running_process = self._RL[i].get_head()
                break
        print(f"Process {self._running_process} running.")
        return self._running_process

    def init(self) -> int:
        print("\n")
        self._PCBs = [None for _ in range(Manager._MAX_PCBs)]
        self._RCBs = [RCB() for _ in range(Manager._MAX_RCPs)]
        self._RL = [SLL() for _ in range(Manager._PRIORITY_LEVELS)]
        self._running_process = 0
        self._number_of_processes = 1

        self._PCBs[0] = PCB()
        self._RL[0].push(0)

        return self.scheduler()


if __name__ == '__main__':
    test = Manager()
    test.init()
    test.create(1)
    test.create(2)
    test.create(2)
    test.create(2)
    test.request(1)
    test.timeout()
    test.request(2)
    test.request(1)
    test.request(1)
