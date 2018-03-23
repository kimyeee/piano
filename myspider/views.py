from django.shortcuts import render
import requests
import threadpool
import bs4
import os

INIT_URL = 'http://bjmx.xdf.cn/guowaidaxue/_%s____'

SETTINGS = {
    'media_path': ''
}


class MyNetworkSpider:

    def __init__(self, page_num, init_url, thread_num=50, parse_device='html.parser'):
        self.page = page_num
        self.init_url = init_url
        self.pool = threadpool.ThreadPool(thread_num)
        self.parse = parse_device
        # requests = threadpool.makeRequests(get_page, )

    def decoder(self, html, parse_device):
        soup = bs4.BeautifulSoup(html, parse_device)
        return

    def downloader(self, url):
        page_html = requests.get(url)
        return page_html

    def geter(self):
        re

    def poster(self, url, data):
        page_data = requests.post(url, data=data)
        return page_data

    def thread_pool(self):
        return

    def storage(self, file, filename, is_bytes=None):
        if is_bytes:
            storage_mode = 'wb'
        else:
            storage_mode = 'w'
        with open(os.path.join(SETTINGS['media_path'], filename), storage_mode) as file_device:
            file_device.write(file)
        return

    def start(self):
        return

    def run(self):
        self.downloader(INIT_URL)


if __name__ == '__main__':
    spider = MyNetworkSpider(515, INIT_URL)
    spider.start()
