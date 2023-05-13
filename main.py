import webScraper

if __name__ == "__main__":
    comments = webScraper.scrape_for_comments("https://www.imdb.com/title/tt0460649/reviews/?ref_=ttrt_ql_2")

    print("printing comments ", len(comments))
    for comment in comments:
        print(comment)
        print('*' * 30)
