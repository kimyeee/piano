from django.shortcuts import render
from django.db import models
import time
import requests
import threadpool
import bs4
import os
import random
import xlwt
import xlrd
from xlutils.copy import copy

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
s_time = time.time()


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
        # self.pool.wait()
        return

    def storage(self, file, filename, is_bytes=None):
        if is_bytes:
            storage_mode = 'wb'
        else:
            storage_mode = 'w'
        with open(os.path.join(SETTINGS.get('media_path', './'), filename), storage_mode) as file_device:
            file_device.write(file)
        return


class GetUniversitySpider(MyNetworkSpider):
    SCORES_TYPE = {
        '托福成绩: ': 'TOEFL_score',
        'SAT成绩: ': 'SAT_score',
        '雅思成绩: ': 'IELTS_score',
        'GMAT成绩: ': 'GMAT_score',
        '简介:': 'instructions',
    }

    def __init__(self, page_num, init_url, count=0):
        super().__init__(page_num, init_url)
        self.count = count

        self.book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        if os.path.isfile('test.xls'):
            count_book = xlrd.open_workbook('test.xls')
            count_sheet = count_book.sheet_by_index(0)
            self.count = count_sheet.nrows + 1
            self.row = count_sheet.nrows
            self.book = copy(count_book)
            self.sheet = self.book.get_sheet(0)
        else:
            self.sheet = self.book.add_sheet('test', cell_overwrite_ok=True)
            self.book_init()
            self.row = self.count

    def book_init(self):
        print(__name__)
        self.sheet.write(0, 0, '中文名')
        self.sheet.write(0, 1, '英文名')
        self.sheet.write(0, 2, '学校类型')
        self.sheet.write(0, 3, '学校地址')
        self.sheet.write(0, 4, '托福成绩')
        self.sheet.write(0, 5, '雅思成绩')
        self.sheet.write(0, 6, 'SAT成绩')
        self.sheet.write(0, 7, 'GMAT成绩')
        self.sheet.write(0, 8, '学校简介')
        self.sheet.write(0, 9, '学校校徽')
        self.sheet.write(0, 10, '详情链接')
        self.count = 1

    def decoder(self, html):
        soup = bs4.BeautifulSoup(html, self.parse_device)
        ret = soup.find_all('div', class_='block-g')
        university_list = []
        print(len(ret))
        for uni in ret:
            img = uni.find('img')['src']
            name = uni.find_all('a')[1].contents[0]
            try:
                e_name = uni.find_all('a')[1].contents[3]
            except:
                e_name = uni.find_all('a')[1].contents[2]
            school_type = uni.find('p', class_='p1').get_text().split('\n')[2]
            address = uni.find('p', class_='p2').get_text().split('\n')[2]
            # TOEFL_score, SAT_score, instructions = uni.find('div', class_='zklt').find_all('p')
            scores_list = uni.find('div', class_='zklt').find_all('p')
            scores_dict = {}
            for item in scores_list:
                key = item.find('b').get_text()
                text = item.find('span').get_text()
                scores_dict[key] = text

            university = {
                'c_name': str(name),
                'e_name': str(e_name),
                'school_type': school_type,
                'address': address,
                # 'TOEFL_score': TOEFL_score.find('span').get_text(),
                # 'SAT_score': SAT_score.find('span').get_text(),
                # 'instructions': instructions.find('span').get_text(),
                'badge_img_id': self.count,
                'badge_img_url': img,
            }
            university['scores_dict'] = scores_dict
            university_list.append(university)
            self.count += 1

        return university_list

    def get_init_url(self):
        request_list = []
        for page in range(1, self.page_num - 510):
            url = self.init_url % page
            request_list.append(url)
        return request_list

    def run(self, abc):
        wait_time = random.uniform(0, 9)
        # time.sleep(wait_time)
        html = open('page_4_1.html', 'rb')
        queryset = self.decoder(html)
        # for i in queryset:
        #     print('---------------')
        #     print(i, ':')

        self.storage(queryset, self.count)

    def storage(self, file, filename, is_bytes=None):

        for university in file:
            self.sheet.write(self.row, 0, university['c_name'])
            self.sheet.write(self.row, 1, university['e_name'])
            self.sheet.write(self.row, 2, university['school_type'])
            self.sheet.write(self.row, 3, university['address'])
            # self.sheet.write(self.row, 4, university['TOEFL_score'])
            # self.sheet.write(self.row, 5, university['SAT_score'])
            # self.sheet.write(self.row, 6, university['instructions'])
            self.sheet.write(self.row, 6, university['scores_dict'])
            self.sheet.write(self.row, 7, university['badge_img_id'])
            self.sheet.write(self.row, 8, university['badge_img_url'])
            self.row += 1
        print(self.count)


spider = GetUniversitySpider(515, INIT_URL)

url_list = spider.get_init_url()
queryset = spider.thread_pool(spider.run, url_list)

# for i in queryset[0]:
# print('---------------')
# print(i, ':', queryset[0][i])

spider.pool.wait()
spider.book.save('test.xls')
run_time = time.time() - s_time
print(run_time)
