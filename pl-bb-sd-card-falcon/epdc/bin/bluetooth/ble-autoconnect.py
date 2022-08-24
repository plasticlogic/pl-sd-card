#!/usr/bin/python3

import asyncio
import subprocess
import signal
import argparse, configparser
import logging
from bleak import BleakScanner
from bleak.backends.device import BLEDevice

async def run_tool(conf_section: dict):
        await scanner.stop()

        params = [conf_section["executable"]]
        for key, val in conf_section.items():
                if key != "executable":
                        params.append(f"--{key}")
                        if val:
                                params.append(val)
        logging.info(params)

        proc = subprocess.run(params)
        logging.debug(f"-> target exit code: {proc.returncode}")

        await scanner.start()

def detection_callback(device: BLEDevice, advertisement_data):
        logging.info(f"{device.address} = {device.name} (RSSI: {device.rssi})")

        if device.address in config:
                section = config[device.address]
                logging.info(f"Found {device.address} in config!")
                loop.create_task(run_tool(section))
        else:
                logging.debug(f"{device.address} -> Unknown device")

def stop(signal, stackframe=None):
        logging.warning(f"signal {signal} received. Stopping scan!")
        loop.create_task(scanner.stop())
        loop.stop()

async def start_scan():
        scanner.register_detection_callback(detection_callback)
        await scanner.start()

        signal.signal(signal.SIGINT, stop)
        signal.signal(signal.SIGTERM, stop)

if __name__ == "__main__":
        parser = argparse.ArgumentParser(
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                description="BLE Device auto connection.")
        parser.add_argument("-c", "--config", default="autoconnect.ini", 
                required=False, help="Path to a INI file with device configs")
        parser.add_argument("-v", "--verbose", dest="verbose", action="store_true",
                help="Increase log level from info to debug")
        args = parser.parse_args()

        logging.basicConfig(format="[%(levelname)s] %(message)s",
                level=logging.DEBUG if args.verbose else logging.INFO)
        
        config = configparser.ConfigParser(allow_no_value=True)
        with open(args.config, 'r') as f:
                config.read_file(f)
        
        scanner = BleakScanner()

        loop = asyncio.get_event_loop()
        loop.create_task(start_scan())
        loop.run_forever()
