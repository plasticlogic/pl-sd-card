
import argparse

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
                "-a", "--update_all", nargs=1,
                help="Updates all panel displays with content of given folder."
        )
        
        return parser