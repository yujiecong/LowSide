from typing import *

from Source import Globs
from Source.Common.Logger import ls_print
from Source.Custom.LSCommand import LSCommand


class LSUndoStack:
    def __init__(self):
        self.stack:List[LSCommand] = []

    def push(self, command:LSCommand):
        """
        只有在 undo_flag 为 False 时才能push
        :param command:
        :return:
        """
        if Globs.is_record_command is True:
            self.stack.append(command)
            ls_print(f"push {command}")


    def undo(self):
        if self.stack:
            command=self.stack.pop()
            ls_print(f"undo {command}")
            command.undo()

