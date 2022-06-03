#!/usr/bin/python3

import sys

import parse
import Panel
import OneWireSwitch
import PanelDisplay

def main() -> None:
        parser = parse.init_argparse()
        args = parser.parse_args()

        if args.init:
                OneWireSwitch.remove_one_wire_devices()
                OneWireSwitch.search_one_wire()
                PanelDisplay.start_epdc()
                return

        pl_panel = Panel.Panel()
        pl_panel.get_displays_by_switches()

        if args.clear:
                pl_panel.clear()

        

if __name__ == "__main__":
        main()