from django.shortcuts import render
from django.db import models
import time
import requests
import threadpool
import bs4
import os

# from notice.models import University

# import functools
# from tornado import concurrent
#
# executor_pool = concurrent.futures.ThreadPoolExecutor()
#
#
# def run_on_executor(fn):
#     @functools.wraps(fn)
#     def wrapper(*args, **kwargs):
#         future = executor_pool.submit(fn, *args, **kwargs)
#         return future
#
#     return wrapper


INIT_URL = 'http://bjmx.xdf.cn/guowaidaxue/_%s____'

SETTINGS = {
    'media_path': r'C:\www\piano\notice'
}


class MyNetworkSpider:

    def __init__(self, page_num, init_url, thread_num=100, parse_device='html.parser'):
        self.page = page_num
        self.init_url = init_url
        self.pool = threadpool.ThreadPool(thread_num)
        self.parse_device = parse_device

    def decoder(self, html):
        soup = bs4.BeautifulSoup(html, self.parse_device)
        return soup

    def downloader(self, url):
        file = requests.get(url)
        return file

    def geter(self, url):
        page_html = requests.get(url)
        return page_html

    def poster(self, url, data):
        page_data = requests.post(url, data=data)
        return page_data

    def thread_pool(self, function, queryset):
        tasks = threadpool.makeRequests(function, queryset)
        for task in tasks:
            self.pool.putRequest(task)
        return

    def storage(self, file, filename, is_bytes=None):
        if is_bytes:
            storage_mode = 'wb'
        else:
            storage_mode = 'w'
        with open(os.path.join(SETTINGS.get('media_path', './'), filename), storage_mode) as file_device:
            file_device.write(file)
        return

    # def start(self):
    #     self.test()
    #     return


#     def test(self):
#         for i in range(1, 11):
#             print(i, '========================')
#             self.thread_pool(aaa, [i * j for j in range(1, 11)])
#         self.pool.wait()
#         return
#
#     def run(self):
#         self.downloader(INIT_URL)
#
#
# def aaa(a):
#     time.sleep(1)
#     print(a)
#
#
# if __name__ == '__main__':
#     spider = MyNetworkSpider(515, INIT_URL)
#     spider.start()

class GetUniversitySpider(MyNetworkSpider):

    def decoder(self, html):
        soup = bs4.BeautifulSoup(html, self.parse_device)
        ret = soup.find_all('div', class_='block-g')
        university_dict = []
        for uni in ret:
            img = uni.find('img')['src']
            name = uni.find_all('a')[1].contents[0]
            e_name = uni.find_all('a')[1].contents[3]
            school_type = uni.find('p', class_='p1').get_text().split('\n')[2]
            address = uni.find('p', class_='p2').get_text().split('\n')[2]
            TOEFL_score, SAT_score, instructions = uni.find('div', class_='zklt').find_all('p')
            university_dict.append({
                'c_name': name,
                'e_name': e_name,
                'school_type': school_type,
                'address': address,
                'TOEFL_score': TOEFL_score.find('span').get_text(),
                'SAT_score': SAT_score.find('span').get_text(),
                'instructions': instructions.find('span').get_text(),
                'img':img
            })

        return university_dict


sss = GetUniversitySpider(515, INIT_URL, 10)
html = open('page_1.html', 'rb')
queyset = sss.decoder(html)
for i in queyset:
    print('---------------')
    print(i)