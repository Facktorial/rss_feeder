import cProfile
import pstats
import asyncio

import sys
import os
  
current = os.path.dirname(os.path.realpath(__file__))  # getting the name of the directory where is this file present.
parent = os.path.dirname(current)  # getting the parent directory name where the current directory is present.
sys.path.append(parent)  # adding the parent directory to the sys.path.
sys.path.append(f'{parent}/rss_feeder')
        
from rss_feeder.app import app


def main():
    with cProfile.Profile() as prof:
        # asyncio.run(app())
        app()

        stats = pstats.Stats(prof)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.print_stats()
        stats.dump_stats(filename='needs_profiling.prof')


if __name__ == "__main__":
    main()
