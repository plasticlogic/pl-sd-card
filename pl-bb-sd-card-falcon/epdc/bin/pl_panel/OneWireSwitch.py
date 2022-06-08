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

                while True:
                        try:
                                output_file = open(out_file, "wb")
                                with output_file:
                                        if (state == SwitchState.ON):
                                                output_file.write(self.__on_state.to_bytes(1, 'little'))
                                        else:
                                                output_file.write(self.__off_state.to_bytes(1, 'little'))
                                break
                        except IOError:
                                print("Failed to open file '", out_file, "'.")

        __on_state = 0xFF
        __off_state = 0xFE

def search_one_wire(count: int = 3) -> None:
        """Search for one wire switches.
        """
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

def remove_one_wire_devices() -> None:
        """Removes all one wire devices."""
        with open(ONE_WIRE_MASTER_FOLDER + "/w1_master_remove", mode="w") as remove_file:
                dev_list = get_all_devices()
                for dev in dev_list:
                        remove_file.write(dev)

def get_all_devices() -> List[str]:
        """Get all one wire devices id strings."""
        devices = os.listdir(ONE_WIRE_DEVICES_FOLDER)
        dev_list = []

        for dev in devices:
                m = re.match("((.{2}-)+(.{12}))", dev)
                if m:
                        dev_list.append(dev)

        return dev_list
