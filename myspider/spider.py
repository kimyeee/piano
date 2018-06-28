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

    def geter(self, url, data=None,headers = None):
        print('get:', url)
        page_html = requests.get(url, params=data,headers = headers)
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


he = {
'Accept':'application/json, text/plain, */*',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection':'keep-alive',
'Cookie':'bid=Ldy_XL9ixwQ; gr_user_id=a064c137-5fb2-42fe-a870-cfbdea1b7c0d; _vwo_uuid_v2=DDC1D1E547EE9EAE3EE017DDF5D848967|20137eb0dd167c0a7678733f6249345b; viewed="5317954_6519779_25746627"; ll="118254"; __utmz=30149280.1522719040.23.22.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmz=223695111.1522719040.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1522749226%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DuQ3F7SRXEg_6sEiMfVuM6tiEGCYqsXvTdpC6sYREd7pKy1yZpIBwxgdNhsiQQeBb%26wd%3D%26eqid%3Dc4af5042000177c8000000055ac2d93d%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.147774725.1515462837.1522719040.1522749226.24; __utmb=30149280.0.10.1522749226; __utmc=30149280; __utma=223695111.1903552006.1518501289.1522719040.1522749226.3; __utmb=223695111.0.10.1522749226; __utmc=223695111; _pk_id.100001.4cf6=85fe09edbd81d696.1518501289.3.1522749295.1522719048.; ap=1',
'Host':'movie.douban.com',
'Referer':'https://movie.douban.com/tag/',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}

# init_url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=0'
# sp = MyNetworkSpider(1, init_url)
# hh = sp.geter(sp.init_url,headers=he)
# headers = hh.headers
# cookies = hh.cookies
# print(headers,cookies)
# hh = requests.get(
#     'https://list.tmall.com/search_product.htm?q=%B5%E7%B8%D6%C7%D9&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&from=mallfp..pc_1_searchbutton',
#     headers=headers,
#     cookies=cookies)
# sp.storage(hh.text, '111.html', )

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