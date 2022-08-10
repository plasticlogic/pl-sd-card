#!/usr/bin/python3

import sys
import os

import parse
import Panel
import OneWireSwitch
import PanelDisplay

LOCK_FILE_PATH = "/tmp/.lock_script"

def lock_mutex():
        if os.path.exists(LOCK_FILE_PATH):
                print("Error: script was already activated.")
                sys.exit(-1)
        else:
                file = open(LOCK_FILE_PATH, "w")

def unlock_mutex():
        assert(os.path.exists(LOCK_FILE_PATH))
        os.remove(LOCK_FILE_PATH)

def execute(args) -> None:
        if args.init:
                PanelDisplay.start_epdc()
                PanelDisplay.set_temperature()
                OneWireSwitch.remove_one_wire_devices()
                OneWireSwitch.search_one_wire()
                return

        pl_panel = Panel.Panel()
        pl_panel.get_displays_by_switches()

        if args.show_arrangement:
                pl_panel.clear()
                pl_panel.config_panel_update()
                return

        if args.clear:
                pl_panel.clear()

        if args.update_all:
                pl_panel.update(args.update_all)

def main() -> None:
        try:
                #lock_mutex()

                parser = parse.init_argparse()
                args = parser.parse_args()
                execute(args)

                #unlock_mutex()
        except:
                pass
                #unlock_mutex()

if __name__ == "__main__":
        main()
