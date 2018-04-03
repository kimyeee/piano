import json
import time
import requests
import threadpool
import bs4
import os
import random
import xlwt
import xlrd
import functools
from tornado import concurrent
from xlutils.copy import copy

# INIT_URL = 'http://bjmx.xdf.cn/guowaidaxue/_%s____'
INIT_URL = 'http://bjmx.xdf.cn/guowaidaxue/_%s_%s_%s__'
SETTINGS = {
    'media_path': r'C:\www\piano\notice'
}
s_time = time.time()
executor_pool = concurrent.futures.ThreadPoolExecutor()


def run_on_executor(fn):
    """
    Decorator to run a synchronous method asynchronously
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        future = executor_pool.submit(fn, *args, **kwargs)
        return future

    return wrapper


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
        print('get:',url)
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
    country_dict = {
        '63b33eae6be44997afb2141ace68c154': '美国',
        '5f913b6ba60c44029be4d2c9046ea914': '加拿大',
        '9c8dcf808b8f4cc6b3c6c3799f25ab4e': '英国',
        'cb752b8ff0da45e0beaa511709a7f3d3': '澳大利亚',
        'e20e0d86f3d1419aa9fb9211f28c564b': '亚洲',
        '57991135ab4d408e9a744a268575ffff': '其他',
    }
    country_list = ['63b33eae6be44997afb2141ace68c154', '5f913b6ba60c44029be4d2c9046ea914',
                    '9c8dcf808b8f4cc6b3c6c3799f25ab4e',
                    'cb752b8ff0da45e0beaa511709a7f3d3', 'e20e0d86f3d1419aa9fb9211f28c564b',
                    '57991135ab4d408e9a744a268575ffff']
    level_dict = {
        '3c6085168429449ca95abc83e4159b4c': '高中',
        '73a78dde4eb24854b8bc8375ce1eee92': '本科',
        'caababc8f15c44f28daa4d6c733e64ad': '研究生',
        '18d04cf7cf974abf852bde554578d60d': '高中',
    }
    level_list = [
        '3c6085168429449ca95abc83e4159b4c', '73a78dde4eb24854b8bc8375ce1eee92', 'caababc8f15c44f28daa4d6c733e64ad',
        '18d04cf7cf974abf852bde554578d60d'
    ]

    def __init__(self, page_num, init_url, count=1):
        super().__init__(page_num, init_url)
        self.count = count
        self.level_index = 0
        self.country_index = 0

        self.book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        if os.path.isfile('university.xls'):
            count_book = xlrd.open_workbook('university.xls')
            count_sheet = count_book.sheet_by_index(0)
            self.count = count_sheet.nrows + 1
            self.row = count_sheet.nrows
            self.book = copy(count_book)
            self.sheet = self.book.get_sheet(0)
        else:
            self.sheet = self.book.add_sheet('国外学校', cell_overwrite_ok=True)
            self.book_init()
            self.row = self.count

    def book_init(self):
        print(__name__)
        self.country = '63b33eae6be44997afb2141ace68c154'
        self.level = '3c6085168429449ca95abc83e4159b4c'
        self.sheet.write(0, 0, '中文名')
        self.sheet.write(0, 1, '英文名')
        self.sheet.write(0, 2, '学校校徽ID')
        self.sheet.write(0, 3, '国家')
        self.sheet.write(0, 4, '学历')
        self.sheet.write(0, 5, '学校类型')
        self.sheet.write(0, 6, '学校地址')
        self.sheet.write(0, 7, '托福成绩')
        self.sheet.write(0, 8, '雅思成绩')
        self.sheet.write(0, 9, 'SAT成绩')
        self.sheet.write(0, 10, 'GMAT成绩')
        self.sheet.write(0, 11, '学校简介')
        self.sheet.write(0, 12, '详情链接')
        self.count = 1

    def decoder(self, html):
        soup = bs4.BeautifulSoup(html, self.parse_device)
        ret = soup.find_all('div', class_='block-g')
        if not ret:
            if self.country_index < 5:
                self.country_index += 1
            else:
                self.country_index = 0
                self.level_index += 1
            print('page error !')
            return
        university_list = []
        print(len(ret), self.country_index, self.level_index)
        for uni in ret:
            img = uni.find('img')['src']
            name = uni.find_all('a')[1].contents[0]
            try:
                e_name = uni.find_all('a')[1].contents[3]
            except:
                try:
                    e_name = uni.find_all('a')[1].contents[2]
                except:
                    e_name = uni.find_all('a')[1].get_text()
                    name = ''
            school_type = uni.find('p', class_='p1').get_text().split('\n')[2]
            address = uni.find('p', class_='p2').get_text().split('\n')[2]
            detail_url = uni.find('div', class_='col-md-2 list').find('a')['href']
            scores_list = uni.find('div', class_='zklt').find_all('p')
            scores_dict = {}
            for item in scores_list:
                key = item.find('b').get_text()
                text = item.find('span').get_text()
                scores_dict[key] = text
            self.count += 1
            university = {
                'c_name': str(name),
                'e_name': str(e_name),
                'school_type': school_type,
                'address': address,
                'TOEFL_score': scores_dict.get('托福成绩：', '-'),
                'IELTS_score': scores_dict.get('雅思成绩：', '-'),
                'SAT_score': scores_dict.get('SAT成绩：', '-'),
                'GMAT_score': scores_dict.get('GMAT成绩：', '-'),
                'instructions': scores_dict.get('简介：', '-'),
                'badge_img_id': self.count,
                'badge_img_url': img,
                'detail_url': detail_url,
            }
            university_list.append(university)

            self.book.save('university.xls')

        return university_list

    def get_init_url(self):
        if self.level_index == 4:
            return
        self.country = self.country_list[self.country_index]
        self.level = self.level_list[self.level_index]
        request_list = []
        print(self.country, self.level)
        for page in range(1, self.page_num):
            url = self.init_url % (page, self.level, self.country)
            request_list.append(url)
        return request_list

    def run(self, url_list):
        wait_time = random.uniform(0, 3)
        for url in url_list:
            print('---------------')
            # time.sleep(wait_time)
            # print(url)
            html = self.geter(url)
            queryset = self.decoder(html.content)
            if queryset:
                self.storage(queryset, self.count)
                self.book.save('university.xls')
            if not queryset:
                print(1)
                url_list = spider.get_init_url()
                if not url_list:
                    exit()
                spider.run(url_list)

    def storage(self, queryset, filename, is_bytes=None):
        if not queryset: return
        country = self.country_dict.get(self.country)
        level = self.level_dict.get(self.level)
        for university in queryset:
            self.sheet.write(self.row, 0, university['c_name'])
            self.sheet.write(self.row, 1, university['e_name'])
            self.sheet.write(self.row, 2, university['badge_img_id'])
            self.sheet.write(self.row, 3, country)
            self.sheet.write(self.row, 4, level)
            self.sheet.write(self.row, 5, university['school_type'])
            self.sheet.write(self.row, 6, university['address'])
            self.sheet.write(self.row, 7, university['TOEFL_score'])
            self.sheet.write(self.row, 8, university['IELTS_score'])
            self.sheet.write(self.row, 9, university['GMAT_score'])
            self.sheet.write(self.row, 10, university['SAT_score'])
            self.sheet.write(self.row, 11, university['instructions'])
            self.sheet.write(self.row, 12, university['detail_url'])
            self.row += 1
            # self.download_img(university['badge_img_url'], self.row)
        print(self.count)

    @run_on_executor
    def download_img(self, url, img_id):
        wait_time = random.uniform(0, 3)
        time.sleep(wait_time)
        image = requests.get(url)
        open(os.path.join(r'E:\大学LOGO', str(img_id) + '.jpg'), 'wb').write(image.content)


spider = GetUniversitySpider(352, INIT_URL)

url_list = spider.get_init_url()
spider.run(url_list)
spider.pool.wait()
spider.book.save('university.xls')
run_time = time.time() - s_time
print(run_time)
