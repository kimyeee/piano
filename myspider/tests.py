from django.test import TestCase

# Create your tests here.
import requests

ret = requests.get('http://bjmx.xdf.cn/guowaidaxue/_1_caababc8f15c44f28daa4d6c733e64ad___')
open('page_4_1.html','wb').write(ret.content)