"""
Pymem module.
"""

from modules.process import Process
from modules.process import process_from_name
from modules.memory import Memory
from modules.module import Module
from contrib.decorators import is_init


class Pymem(object):
    """Provides class instance methods for general process and memory
manipulations.
    """

    def __init__(self):
        """
        Initialize pymem objects
        """

        self.process = None
        self.memory = None
        self.module = None
        self.pid = None  # refractor
        self.process32 = None  # refractor
        self.process_handle = None

    def _init_process(self):
        """
        Initialize process class when it's needed by pymem.
        """

        self.process = Process()

    def _init_memory(self):
        """
        Initialize memory class when it's needed by pymem.
        """

        self.memory = Memory()

    def _init_module(self):
        """
        Initialize module class when it's needed by pymem.
        """

        self.module = Module()

    @is_init('process')
    def open_process(self, process_id, debug=True):
        """
        Opens a process for interaction.
        """

        if debug:
            if self.process.open_debug(process_id):
                self.process_handle = self.process.h_process
                self.pid = process_id
                self.process32 = self.process.process32
                return True
            return False
        return self.process.open(process_id)

    @is_init('process')
    def open_process_from_name(self, process_name, debug=True, number=0):
        """
        Opens a process from its name for interaction.
        """

        processes = process_from_name(process_name)
        if processes is not None:
            if len(processes) - 1 == number:
                process = processes[len(processes) - 1]
                return self.open_process(process.th32ProcessID, debug)
        return False

    @is_init('memory')
    def read_offset(self, address, selected_type):
        """
        Read memory from a process.
        If the type <T> is supported, this method will provide the required
        call in order to read, from the process. If either the type <T> is not
        supported or process is not Open, the method will raise an Exception.

        Supported types : float, int, uint, long, ulong, int64, uint64, byte
        """

        if self.process.is_process_open:
            if self.memory.is_process_set == False:
                self.memory.set_process(self.process.h_process)
            return self.memory.read_offset(address, selected_type)
        return False

    @is_init('module')
    def list_module32(self):
        """
        Return module (MODULEENTRY32) loaded by current process.
        """

        if self.process32 is not None:
            if self.module.is_process_set == False:
                self.module.set_process32(self.process32)
            return self.module.list_module32()
        return []

    @is_init('module')
    def has_module32(self, module):
        """
        Return True if current process has loaded given module (dll)
        """

        if self.process32 is not None:
            if self.module.is_process_set == False:
                self.module.set_process32(self.process32)
            return self.module.has_module32(module)
        return False
