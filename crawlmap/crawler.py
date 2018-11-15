from functools import reduce
from urllib.parse import urljoin

import grequests
import lxml.html
import lxml.etree


class Crawler:
    def __init__(self, store):
        self.store = store

    def add_roots(self, urls):
        self.store.roots(urls)

    def step(self, timeout):
        leaves = self.store.leaves()

        if len(leaves) == 0:
            return False, 0

        def page_links(page):
            try:
                root = lxml.html.fromstring(page.content)
                return [{'from': page.url, 'to': urljoin(page.url, l)} for l in root.xpath('//a/@href')]
            except lxml.etree.LxmlError:
                return []

        pages = grequests.map([grequests.get(u, timeout=timeout) for u in leaves])
        page_status = [{'url': page.url, 'status': page.status_code} for page in pages if page is not None]
        links = list(reduce(lambda l, r: l + r, [page_links(page) for page in pages if page is not None]))

        self.store.pages(map(lambda l: l['to'], links))
        self.store.links(links)
        self.store.page_status(page_status)

        return True, len(links), len(pages), sum(map(lambda x: 1, filter(lambda p: p is None, pages)))
