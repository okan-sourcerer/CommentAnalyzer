import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_for_comments(imdb_url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get(imdb_url)
    comments_dict = {}

    try:
        did_load_all = False
        while True:
            # print("Reading comments!")
            # get the current page source and create a Beautiful Soup object
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            total_reviews = int(soup.select('div.header span:not(:empty,:has(div))')[0].text.split(' ')[0])
            comments_list = soup.select('div.lister-list')
            comments = []
            for single_comment in comments_list[0].contents:
                if single_comment != '\n':
                    comments.append(single_comment)

            for current_index in range(len(comments)):
                comment = comments[current_index]
                review_id = comment['data-review-id']

                comment_text = comment.findAll('div', class_='text')[0].text

                if review_id not in comments_dict:
                    comments_dict[review_id] = comment_text

            each_step = total_reviews / 50
            progress = int(len(comments_dict) / each_step)
            sys.stdout.write("\rLoading comments: " + str(len(comments_dict)) + f'/{total_reviews}' +
                             " [" + ("=" * progress) + (">" * ((50 - progress) > 0) + (" " * (49 - progress)) + "]"))

            if did_load_all:
                break

            try:
                # print("loading comments.. current comments length is ", len(comments_dict))
                load_more_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'load-more-data'))
                )
                load_more_button.click()
            except Exception as _:
                did_load_all = True
                continue
    finally:
        driver.quit()

    return comments_dict.values()
