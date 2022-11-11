#!/usr/bin/python3

import sys
import os

import parse
import Panel
import OneWireSwitch
import PanelDisplay

def execute(args) -> None:
        if args.init:
                PanelDisplay.start_epdc()
                PanelDisplay.set_temperature()
                OneWireSwitch.remove_one_wire_devices()
                OneWireSwitch.search_one_wire(32)
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
                parser = parse.init_argparse()
                args = parser.parse_args()
                sys.stdout.flush()
                execute(args)
        except:
                print("ERROR: execution failed.")

if __name__ == "__main__":
        main()
