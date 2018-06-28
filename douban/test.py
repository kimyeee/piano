import requests

url = 'https://movie.douban.com/top250?start=%s&filter='
url2 = 'https://movie.douban.com/subject/1292281/'
res = requests.get(url2)

open('c.html', 'wb').write(res.content)
