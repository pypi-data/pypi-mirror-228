from swmonkey.util.util import get_out_dir
import os
import time
from swmonkey.data_structure.gui_action import GUIAction


class ReplayController:
    def __init__(self):
        self.acions = []

    def run(self, actions_json_file_path):
        # check path
        if not os.path.exists(actions_json_file_path):
            raise Exception("File not found: {}".format(
                actions_json_file_path))
        with open(actions_json_file_path, 'r') as f:
            self.actions = f.read()

        self.actions = eval(self.actions)
        self.replay()

    def replay(self):
        for action in self.actions:
            action = GUIAction(**action)
            action.execute()
