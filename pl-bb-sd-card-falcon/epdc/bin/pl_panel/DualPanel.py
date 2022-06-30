#!/usr/bin/python3

import argparse
import subprocess
import sys
import os

import PanelDisplay

LOCK_FILE_PATH = "/tmp/.lock_script"
TMP_IMG_PATH1 = "/tmp/tmp_img1.raw"
TMP_IMG_PATH2 = "/tmp/tmp_img2.raw"
FINAL_IMG_PATH = "/tmp/final.raw"

def init_argparse() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
                usage="%(prog)s [OPTION]...",
                description="Handle a multi-display panel."
        )

        parser.add_argument(
                "-v", "--version", action="version",
                version = '%(proc)s version 1.0.0'
        )

        parser.add_argument(
                "-i", "--init", action="store_true",
                help="Initializes the panel."
        )

        parser.add_argument(
                "-c", "--clear", action="store_true",
                help="Clear all panel displays."
        )

        parser.add_argument(
                "-u", "--update_all", nargs=2, type=str,
                help="Updates the two displays with 2 png params."
        )
        
        return parser

#print(init_argparse().parse_args("-u test1 test2".split()))

def execute(args) -> None:
        if args.init:
                PanelDisplay.start_epdc()
                return

        if args.clear:
                PanelDisplay.try_call_epdc(["epdc-app", "-fill", "GL15", "0"])

        if args.update_all:
                subprocess.call(["png2cfa", "-i", args.update_all[0], "-o", TMP_IMG_PATH1, "-c", "grbw"])
                subprocess.call(["png2cfa", "-i", args.update_all[1], "-o", TMP_IMG_PATH2, "-c", "bwgr"])
                with open(FINAL_IMG_PATH, "wb") as final_img:
                        width = 1280
                        with open(TMP_IMG_PATH1, "rb") as img1:
                                with open(TMP_IMG_PATH2, "rb") as img2:
                                        for row in range(960):
                                                final_img.write(img1.read(width))
                                                final_img.write(img2.read(width))
                PanelDisplay.try_call_epdc(["epdc-app", "-load_buffer", FINAL_IMG_PATH, "2", "2", "0,0,2560,960"])

def main() -> None:
        try:

                parser = init_argparse()
                args = parser.parse_args()
                execute(args)

        except:
                pass

if __name__ == "__main__":
        main()