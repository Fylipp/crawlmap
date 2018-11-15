import itertools
import sys

from crawlmap.cfg import Config
from crawlmap.crawler import Crawler
from crawlmap.store import Store

print('Loading configuration ...')
config = Config.load('crawlmap.ini')

print('Connecting to database ...')
with Store(config.db_uri, config.db_user, config.db_password) as store:
    if config.db_autoclear:
        print('Clearing database since autoclear is enabled ...')
        store.clear()

    crawl = Crawler(store)
    crawl.add_roots(sys.argv[1:])

    print('Crawling ...')
    print()

    for i in itertools.count():
        has_next, found, page_count, page_error_count = crawl.step(config.web_timeout)
        print(f'--- Iteration {i} ---')
        print(f'Links followed: {page_count - page_error_count}')
        print(f'Errors: {page_error_count} request(s) / {round(page_error_count / page_count * 100)} %')
        print(f'New links found: {found}')

        if not has_next:
            break

    print('Crawling complete')
