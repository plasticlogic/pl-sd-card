#!/usr/bin/python3

import sys
import os
import logging

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

def setup_logger() -> None:
        rfh = logging.handlers.RotatingFileHandler(
                filename="logging.out",
                mode='a',
                maxBytes=5*1024*1024,
                backupCount=2
                encoding="utf-8",
                delay=0
        )

        logging.basicConfig(
                level=logging.DEBUG,
                format="%(asctime)s %(name)-25s %(levelname)-8s %(message)s",
                datefmt="%y-%m-%d %H:%M:%S",
                handlers=[ rfh ]
        )

def main() -> None:
        setup_logger()
        logger = logging.getLogger('main')
        try:
                logger.debug("Start parsing")
                parser = parse.init_argparse()
                args = parser.parse_args()
                sys.stdout.flush()
                logger.debug("Start process")
                execute(args)
        except:
                logger.error("ERROR: execution failed.")

if __name__ == "__main__":
        main()
