import time

import webScraper

if __name__ == "__main__":
    tic = time.perf_counter()
    comments = webScraper.scrape_for_comments("https://www.imdb.com/title/tt0460649/reviews/?ref_=ttrt_ql_2")

    toc = time.perf_counter()
    print(f"Scraped data in {toc - tic:0.4f} seconds")
    print("printing comments ", len(comments))
    for comment in comments:
        print(comment)
        print('*' * 30)

    tac = time.perf_counter()
    print(f"Printed data in {tac - toc:0.4f} seconds")
