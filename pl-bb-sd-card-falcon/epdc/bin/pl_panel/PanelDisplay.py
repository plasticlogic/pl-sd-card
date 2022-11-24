"""@package docstring
Panel display class module.
"""

import subprocess
import logging

from OneWireSwitch import OneWireSwitch, SwitchState

class PanelDisplay:
        def __init__(self, one_wire_id: str, display_idx: int):
                self.__one_wire_switch = OneWireSwitch(one_wire_id)
                self.disable()
                self.__display_idx = display_idx
                self.logger = logging.getLogger("Display")

        def update(self, image_path: str) -> None:
                self.logger.debug("Set new image")
                try_call_epdc("epdc-app -load_buffer {} 7 2 0,0,1280,960".format(image_path))

        def write_pre_buffer(self, buf_path: str) -> None:
                self.logger.debug("Set old image")
                try_call_epdc("epdc-app -override_post_buffer {} 1".format(buf_path))

        def clear(self) -> None:
                self.logger.debug("Trigger clear update")
                try_call_epdc("epdc-app -fill GL15 0")

        def enable(self) -> None:
                self.logger.debug("Enable display")
                self.__one_wire_switch.set_switch(SwitchState.ON)

        def disable(self) -> None:
                self.logger.debug("Disable display")
                self.__one_wire_switch.set_switch(SwitchState.OFF)

def set_temperature(temp: int = 23) -> None:
        logging.info("Set temperature to {}".format(temp))
        try_call_epdc("epdc-app -set_temperature {}".format(temp))

def start_epdc() -> None:
        logging.debug("Start EPDC")
        try_call_epdc("epdc-app -start_epdc 0 0")

def stop_epdc() -> None:
        logging.debug("Stop EPDC:")
        try_call_epdc("epdc-app -stop_epdc")

def try_call_epdc(args) -> None:
        timeout_counter = 0
        max_timeout = 10
        while True:
                if (timeout_counter >= max_timeout):
                        logging.error("Failed to call epdc-app.")
                        break
                timeout_counter += 1
                try:
                        p = subprocess.run(args, shell=True, stdout=subprocess.PIPE)

                        if p.returncode != 0:
                                proc_res = p.stdout.decode()
                                logging.warning("EPDC error (Error Code {}):\n{}".format(p.returncode, proc_res))
                                p.check_returncode() # raise CalledProcessError
                        break
                except:
                        logging.info("Try to restart EPDC (Try {} of {})".format(timeout_counter, max_timeout))
                        start_epdc()