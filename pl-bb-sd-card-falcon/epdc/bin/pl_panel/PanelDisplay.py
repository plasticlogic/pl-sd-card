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
                try_call_epdc(["epdc-app", "-load_buffer", image_path, "7", "2", "0,0,1280,960"])

        def write_pre_buffer(self, buf_path: str) -> None:
                try_call_epdc(["epdc-app", "-override_post_buffer", buf_path, "1"])

        def clear(self) -> None:
                try_call_epdc(["epdc-app", "-fill", "GL15", "0"])

        def enable(self) -> None:
                self.__one_wire_switch.set_switch(SwitchState.ON)

        def disable(self) -> None:
                self.__one_wire_switch.set_switch(SwitchState.OFF)

def set_temperature(temp: int = 23) -> None:
        try_call_epdc(["epdc-app", "-set_temperature", str(temp)])

def start_epdc() -> None:
        subprocess.call(["epdc-app", "-start_epdc", "0", "0"], stdout=subprocess.DEVNULL)

def stop_epdc() -> None:
        subprocess.call(["epdc-app", "-stop_epdc"], stdout=subprocess.DEVNULL)

def try_call_epdc(args) -> None:
        timeout_counter = 0
        max_timeout = 10
        while True:
                if (timeout_counter >= max_timeout):
                        print("Error: Failed to call epdc-app!")
                        break
                timeout_counter += 1
                try:
                        subprocess.call(args, stdout=subprocess.DEVNULL)
                        break
                except:
                        start_epdc()