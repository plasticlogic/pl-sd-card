"""@package docstring
One wire switch control class module.
"""

from enum import Enum
import os
import re
from time import sleep
from typing import List

ONE_WIRE_DEVICES_FOLDER = "/sys/bus/w1/devices"
ONE_WIRE_MASTER_FOLDER = "/sys/bus/w1/devices/w1_bus_master1"

ONE_WIRE_TIMEOUT = 50

class FamilyCodes:
        DS2413 = "3a"

class SwitchState(Enum):
        """One wire switch state."""
        ON = 1
        OFF = 2

class OneWireSwitch:
        """One wire switch control class.
        """

        def __init__(self, switch_id: str):
                self.switch_id = switch_id
                self.dev_path = os.path.join(ONE_WIRE_DEVICES_FOLDER, switch_id)

        def set_switch(self, state: SwitchState) -> None:
                """Turn on/off switch.
                """
                out_file = os.path.join(self.dev_path, "output")

                timeout_counter = 0

                while True:
                        if (timeout_counter >= ONE_WIRE_TIMEOUT):
                                print("Error: Failed to write to 1w!")
                                break

                        timeout_counter += 1
                        try:
                                output_file = open(out_file, "wb")
                                with output_file:
                                        if (state == SwitchState.ON):
                                                #print(self.__on_state)
                                                output_file.write(self.__on_state)
                                                if (not self.__check_switch_state(SwitchState.ON)):
                                                        #print("ON TEST: ", self.__check_switch_state(SwitchState.ON))
                                                        continue
                                        else:
                                                output_file.write(self.__off_state)
                                                if (not self.__check_switch_state(SwitchState.OFF)):
                                                        #print("OFF TEST: ", self.__check_switch_state(SwitchState.OFF))
                                                        continue
                                break
                        except IOError:
                                pass #print("Failed to open file '", out_file, "'.")

        def __check_switch_state(self, state: SwitchState) -> bool:
                state_file_path = os.path.join(self.dev_path, "state")

                timeout_counter = 0

                while True:
                        if (timeout_counter >= ONE_WIRE_TIMEOUT):
                                print("Error: Failed to read 1w!")
                                break

                        timeout_counter += 1
                        try:
                                state_file = open(state_file_path, "rb")
                                with state_file:
                                        #print("CHECK: ", self.__off_state.to_bytes(1, "little"))
                                        #print("RESULT: ", state_file.read(1))
                                        if (state == SwitchState.ON):
                                                #print("STATE: ", state_file.read(1))
                                                return state_file.read(1) == self.__check_on_state
                                        else:
                                                return state_file.read(1) == self.__check_off_state
                        except:
                                pass

        __on_state = b"\xff" # GPIO A -> off; GPIO B -> on
        __off_state = b"\xfc"
        __check_on_state = b"\x0f"
        __check_off_state = b"\xf0"

def search_one_wire(count: int = 3) -> None:
        """Search for one wire switches.
        """
        #print("Search devices")
        search_file_path = os.path.join(ONE_WIRE_MASTER_FOLDER, "w1_master_search")
        
        try:
                search_file = open(search_file_path, mode="w")
                search_file.write(str(count))
        except IOError:
                print("File IO error.")
        search_file.close()

        try:
                search_file = open(search_file_path, mode="r")
                while search_file.read(1) != "0":
                        sleep(1)
                        search_file.seek(0, 0)
        except IOError:
                print("File IO Error")
        search_file.close()
        return

def remove_one_wire_devices() -> None:
        """Removes all one wire devices."""
        #print("Remove devices")
        dev_list = get_all_devices()
        #print("Dev list: ", dev_list)
        for dev in dev_list:
                #print(dev)
                with open(os.path.join(ONE_WIRE_MASTER_FOLDER, "w1_master_remove"), mode="w") as remove_file:
                        remove_file.write(dev)
        return

def get_all_devices() -> List[str]:
        """Get all one wire devices id strings."""
        devices = os.listdir(ONE_WIRE_DEVICES_FOLDER)
        dev_list = []

        for dev in devices:
                m = re.match("((.{2}-)+(.{12}))", dev)
                if m:
                        dev_list.append(dev)

        return dev_list
