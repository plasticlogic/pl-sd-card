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
                print("SET NEW IMAGE")
                try_call_epdc(["epdc-app", "-load_buffer", image_path, "7", "2", "0,0,1280,960"])

        def write_pre_buffer(self, buf_path: str) -> None:
                print("SET OLD IMAGE")
                try_call_epdc(["epdc-app", "-override_post_buffer", buf_path, "1"])

        def clear(self) -> None:
                print("CLEAR UPDATE")
                try_call_epdc(["epdc-app", "-fill", "GL15", "0"])

        def enable(self) -> None:
                print("ENABLE DISPLAY {}".format(self.__display_idx))
                self.__one_wire_switch.set_switch(SwitchState.ON)

        def disable(self) -> None:
                print("DISABLE DISPLAY {}".format(self.__display_idx))
                self.__one_wire_switch.set_switch(SwitchState.OFF)

def set_temperature(temp: int = 23) -> None:
        print("SET TEMPERATURE TO {}".format(temp))
        try_call_epdc(["epdc-app", "-set_temperature", str(temp)])

def start_epdc() -> None:
        print("START EPDC:")
        subprocess.call(["epdc-app", "-start_epdc", "0", "0"], stdout=subprocess.DEVNULL)

def stop_epdc() -> None:
        print("STOP EPDC:")
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
                        p = subprocess.run(args, shell=True, stdout=subprocess.PIPE)

                        if p.returncode != 0:
                                proc_res = p.stdout.decode()
                                print("EPDC ERROR (Error Code {}):\n{}".format(p.returncode, proc_res))
                                p.check_returncode() # raise CalledProcessError
                        break
                except:
                        print("TRY TO RECOVER EPDC (Try {} of {})".format(timeout_counter, max_timeout))
                        start_epdc()