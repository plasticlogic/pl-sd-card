"""@package docstring
Panel display class module.
"""

import subprocess

from OneWireSwitch import OneWireSwitch, SwitchState

class PanelDisplay:
        def __init__(self, one_wire_id: str, display_idx: int):
                self.__one_wire_switch = OneWireSwitch(one_wire_id)
                self.disable()
                self.__display_idx = display_idx

        def update(self, image_path: str) -> None:
                subprocess.call(["epdc-app", "-load_buffer", image_path, "7", "2", "0,0,1280,960"],
                stdout=subprocess.DEVNULL)

        def write_pre_buffer(self, buf_path: str) -> None:
                subprocess.call(["epdc-app", "-override_post_buffer", buf_path, "1"],
                stdout=subprocess.DEVNULL)

        def clear(self) -> None:
                subprocess.call(["epdc-app", "-fill", "GL15", "0"],
                stdout=subprocess.DEVNULL)

        def enable(self) -> None:
                self.__one_wire_switch.set_switch(SwitchState.ON)

        def disable(self) -> None:
                self.__one_wire_switch.set_switch(SwitchState.OFF)

def start_epdc() -> None:
        subprocess.call(["epdc-app", "-start_epdc", "0", "0"], stdout=subprocess.DEVNULL)

def stop_epdc() -> None:
        subprocess.call(["epdc-app", "-stop_epdc"], stdout=subprocess.DEVNULL)
        