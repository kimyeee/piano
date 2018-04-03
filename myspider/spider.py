import bs4
import os
import requests
import threadpool

INIT_URL = 'http://bjmx.xdf.cn/guowaidaxue/_%s_%s_%s__'
SETTINGS = {
    'media_path': r'C:\www\piano\notice'
}


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

    def geter(self, url, data=None):
        print('get:', url)
        page_html = requests.get(url, params=data)
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
        with open(filename, storage_mode) as file_device:
            file_device.write(file)
        return




url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1&start='
sp = MyNetworkSpider(1, url)
hh = sp.geter(sp.init_url)
# headers = hh.headers
# cookies = hh.cookies
# print(headers,cookies)
# hh = requests.get(
#     'https://list.tmall.com/search_product.htm?q=%B5%E7%B8%D6%C7%D9&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&from=mallfp..pc_1_searchbutton',
#     headers=headers,
#     cookies=cookies)
sp.storage(hh.text, '111.html', )

# url = 'https://list.tmall.com/search_product.htm?spm=875.7931836/B.subpannel2016040.3.6b5f4265tSJPzG&q=%F7%C8%D7%E5&pos=3&from=.list.pc_1_searchbutton&acm=2016030713.1003.2.709043&type=p&scm=1003.2.2016030713.OTHER_1462805399393_709043'
# from selenium import webdriver
# browser = webdriver.Chrome()
# browser.get(url)
# browser.maximize_window()
# cont = browser.page_source
# browser.close()
# print(type(cont))
# open('11.html','wb').write(cont.encode('utf-8'))

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
#
# chrome_options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
# # chrome_options.binary_location = '/opt/google/chrome/chrome'
#
# opener = webdriver.Chrome(chrome_options=chrome_options)
# opener.get(url)
# opener.maximize_window()
# content = opener.page_source
# opener.close()
# open('head.html','wb').write(content.encode('utf-8'))