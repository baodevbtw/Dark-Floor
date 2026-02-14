#!/usr/bin/env python3
"""
Dark Floor - A roguelike terminal game

Quick start: python main.py
"""

import curses
import time
from src.darkfloor import main

VERSION = "0.1.0-alpha.3"  # See docs/VERSION.md for version details

SEED = "dark-floor"

def setup_and_run():
    print("=" * 40)
    print("Dark Floor")
    print("=" * 40)
    print(f"Version: {VERSION}")
    print(f"Base Seed: {SEED}")
    print("Loading game...")
    time.sleep(1.5)
    run_id = 0
    try:
        while True:
            rng_seed = f"{SEED}-{run_id}"
            print(f"Run seed: {rng_seed}")
            result = curses.wrapper(main, rng_seed)

            if result == "quit":
                break
            run_id += 1

    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    setup_and_run()