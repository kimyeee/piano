import json
import random

import bs4
import requests
import threadpool
import time


class MyNetworkSpider:

    def __init__(self, page_num, init_url, thread_num=1, parse_device='html.parser'):
        self.page_num = page_num
        self.init_url = init_url
        self.pool = threadpool.ThreadPool(thread_num)
        self.parse_device = parse_device

    def decoder(self, html):
        soup = bs4.BeautifulSoup(html, self.parse_device)
        return soup

    def downloader(self, url):
        wait_time = random.uniform(0, 4)
        time.sleep(wait_time)
        file = requests.get(url)
        return file

    def geter(self, url):
        # print('get:', url)
        wait_time = random.uniform(0, 5)
        time.sleep(wait_time)
        page_html = requests.get(url)
        return page_html

    def poster(self, url, data):
        page_data = requests.post(url, data=data)
        return page_data

    def thread_pool(self, function, queryset):
        tasks = threadpool.makeRequests(function, queryset)
        for task in tasks:
            self.pool.putRequest(task)
        # self.pool.wait()
        return


class PianoSpider(MyNetworkSpider):

    def __init__(self, page_num, init_url, thread_num):
        super().__init__(page_num, init_url, thread_num)
        self.filename = 1

    def save(self, obj):
        photo = obj['photo']['path']
        filename = 'piano_%s.jpg' % self.filename
        self.filename += 1
        file = self.downloader(photo)
        open('D:\SOME\img\\' + filename, 'wb').write(file.content)
        print('********************已经下载图片%s********************' % filename)
        return

    def decoder(self, html):
        soup = json.loads(html)
        object_list = soup['data']['object_list']

        return object_list

    def run(self):
        for num in range(self.page_num):
            url = self.init_url.format(num*24)
            content = self.geter(url).content
            object_list = self.decoder(content)
            # object_list = self.decoder(open('piano.html', 'rb').read())
            if not object_list:
                print('***********************END************************')
                # break
            self.thread_pool(self.save, object_list)
        self.pool.wait()
        return


init_url = 'https://www.duitang.com/napi/blog/list/by_search/?kw=%E9%92%A2%E7%90%B4&type=feed&include_fields=' \
           'top_comments%2Cis_root%2Csource_link%2Citem%2Cbuyable%2Croot_id%2Cstatus%2Clike_count%2Csender%2Calbum&' \
           '_type=&start={0}&_=1522807168278'
piano = PianoSpider(151, init_url, 40)
piano.run()
# content = piano.geter(piano.init_url).content
# open('piano.html', 'wb').write(content)
