from django.shortcuts import render

import requests
import threadpool

ALL_PAGE = 515
INIT_URL = 'http://bjmx.xdf.cn/guowaidaxue/_%s____'


class MySpider:
    ALL_PAGE = 515
    INIT_URL = 'http://bjmx.xdf.cn/guowaidaxue/_%s____'

    def __init__(self,thread_num):
        self.pool = threadpool.ThreadPool(thread_num)
        # requests = threadpool.makeRequests(get_page, )

    def get_info(self):
        return

    def get_page(self, url):
        page_html = requests.get(url)
        return page_html

    def thread_pool(self):
        return

    def start(self):
        return

    def run(self):
        self.get_page(INIT_URL)


if __name__ == '__main__':
    spider = MySpider(50)
    spider.start()
