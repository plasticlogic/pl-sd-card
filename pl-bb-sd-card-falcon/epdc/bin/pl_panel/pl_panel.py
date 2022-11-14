#!/usr/bin/python3

import sys
import os
import logging
import logging.handlers

import parse
import Panel
import OneWireSwitch
import PanelDisplay

def execute(args) -> None:
        logging.debug("Into execute")
        if args.init:
                PanelDisplay.start_epdc()
                PanelDisplay.set_temperature()
                OneWireSwitch.remove_one_wire_devices()
                OneWireSwitch.search_one_wire(32)
                return

        logging.debug("Create Panel object")
        pl_panel = Panel.Panel()
        logging.debug("Collecting displays")
        pl_panel.get_displays_by_switches()
        logging.debug("Got displays")

        if args.show_arrangement:
                pl_panel.clear()
                pl_panel.config_panel_update()
                return

        if args.clear:
                logging.debug("Calling clear update.")
                pl_panel.clear()
                return

        if args.update_all:
                logging.debug("Calling update")
                pl_panel.update(args.update_all)
                return

def setup_logger() -> None:
        rfh = logging.handlers.RotatingFileHandler(
                filename="/boot/uboot/epdc/bin/pl_panel/logging.out",
                mode='a',
                maxBytes=5*1024*1024,
                backupCount=2,
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
                logger.debug("args: {}".format(args))
                execute(args)
        except:
                logger.error("ERROR: execution failed.")

if __name__ == "__main__":
        main()
