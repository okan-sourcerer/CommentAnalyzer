import cProfile
import pstats
import time

import webScraper

if __name__ == "__main__":
    tic = time.perf_counter()
    imdb_url = "https://www.imdb.com/title/tt0460649/reviews"

    profiler = cProfile.Profile()
    profiler.enable()
    comments = webScraper.scrape_for_comments(imdb_url)
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats(pstats.SortKey.CUMULATIVE)
    stats.print_stats(30)
    tac = time.perf_counter()

    for comment in comments:
        print(comment)
        print(30 * "*")
    toc = time.perf_counter()
    print(f"Printed data in {toc - tac:0.4f} seconds")
