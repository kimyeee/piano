import re


s = ['支付宝支付','微信支付','银行']
for string in s:
    if re.search('支付宝|微信',string):
        print('匹配成功--search')
    if re.findall('支付宝|微信',string):
        print('匹配成功--findall')
