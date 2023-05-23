import sys
import time
import requests
from bs4 import BeautifulSoup

time_find_specific = 0
time_find_all_next = 0
time_extract_comment_text = 0
time_find_review_count = 0
time_get_source = 0
time_init_soups = 0
comments_dict = {}


def parse_comments(comment_soup, main_url):
    global time_find_specific
    global time_find_all_next
    global time_extract_comment_text

    comments = []
    start_find_specific = time.perf_counter()
    specific_element = comment_soup.select_one('div.lister-list')
    time_find_specific += time.perf_counter() - start_find_specific

    start_find_all_next = time.perf_counter()
    following_elements = specific_element.find_all_next(lambda tag: tag.has_attr('data-review-id'))
    time_find_all_next += time.perf_counter() - start_find_all_next

    comments.extend(following_elements)

    for comment in comments:
        review_id = comment['data-review-id']

        start_extract_comment = time.perf_counter()
        comment_text = comment.find('div', class_='text').text
        comments_dict[review_id] = comment_text
        time_extract_comment_text += time.perf_counter() - start_extract_comment

    pagination_key = comment_soup.find('div', class_="load-more-data")
    if pagination_key is not None:
        next_url = f"{main_url}/_ajax?ref_=undefined&paginationKey=" \
              f"{pagination_key['data-key']}"
    else:
        next_url = ""

    return next_url


def scrape_for_comments(url):
    global time_find_specific
    global time_find_all_next
    global time_extract_comment_text
    global time_find_review_count
    global time_get_source
    global time_init_soups

    tic = time.perf_counter()
    main_url = url

    request_session = requests.Session()

    start_page_source = time.perf_counter()
    response = request_session.get(url)
    time_get_source += time.perf_counter() - start_page_source
    start_init_soup = time.perf_counter()
    soup = BeautifulSoup(response.text, 'lxml')
    time_init_soups += time.perf_counter() - start_init_soup

    start_review_count = time.perf_counter()
    total_reviews = int(soup.select('div.header span:not(:empty,:has(div))')[0].text.split(' ')[0])
    time_find_review_count += time.perf_counter() - start_review_count

    url = parse_comments(soup, main_url)

    while url != "":
        start_page_source = time.perf_counter()
        response = request_session.get(url)
        time_get_source += time.perf_counter() - start_page_source
        # Check the response status code
        if response.status_code == requests.codes.ok:
            # Successful request
            start_init_soup = time.perf_counter()
            soup = BeautifulSoup(response.text, 'lxml')
            time_init_soups += time.perf_counter() - start_init_soup

            url = parse_comments(soup, main_url)

            each_step = total_reviews / 50
            progress = int(len(comments_dict) / each_step)
            sys.stdout.write("\rLoading comments: " + str(len(comments_dict)) + f'/{total_reviews}' +
                             " [" + ("=" * progress) + (">" * ((50 - progress) > 0) + (" " * (49 - progress)) + "]"))
        else:
            # Request failed
            print("Request failed with status code:", response.status_code)
            url = ""

    print(f"\nAll comments {len(comments_dict)}")
    print(f"\nfind specific {time_find_specific}"
          f"\n, find all next {time_find_all_next}"
          f"\n, extract text {time_extract_comment_text}"
          f"\n, find review count {time_find_review_count}"
          f"\n, init soups {time_init_soups}"
          f"\n, load page source {time_get_source}")

    toc = time.perf_counter()

    print(f"Total time: {toc - tic}")
    return comments_dict.values()