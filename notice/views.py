import time
import requests
import hashlib
import json
import re
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

wxtoken = 'weixin'
my_wechat = 'JazzPiano_'
msgtype = 'text'
ROBOT_API = 'https://www.fedrobots.com/php/miji.php'

notice = '''<xml>  
             <ToUserName><![CDATA[%s]]></ToUserName>  
             <FromUserName><![CDATA[%s]]></FromUserName>  
             <CreateTime>%s</CreateTime>  
             <MsgType><![CDATA[%s]]></MsgType>  
             <Content><![CDATA[%s]]></Content>  
             </xml>'''


def wx_auth(request):
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    tmparr = [wxtoken, str(timestamp), str(nonce)]
    tmparr.sort()
    tmpstr = ''.join(tmparr)
    tmpstr = hashlib.sha1(tmpstr.encode('utf8')).hexdigest()

    return signature == tmpstr


def get_text(xml):
    ret = re.findall('<Content><!\[CDATA\[.+\]\]', xml)[0][18:-2]
    return ret


def get_robot(request):
    if request.method == 'GET':
        text = '讲笑话'
    else:
        text = get_text(str(request.body))
    if text:
        data = {'action': 'getSend', 'problem_send': text}
    else:
        data = {'action': 'getSend', 'problem_send': text}
    res = requests.post(ROBOT_API, data=data).text
    msg = json.loads(res)
    if msg.get('msg') == '获取成功':
        refer_msg = msg.get('json').get('text')
    else:
        refer_msg = '机器人出错 !'
    print(text)
    print(refer_msg)
    return refer_msg


@csrf_exempt
def piano(request):
    target_id = request.GET.get('openid')
    if wx_auth(request):
        # return HttpResponse(notice % (target_id, my_wechat, int(time.time()), msgtype, '说点啥呢。。。。'))
        ret = get_robot(request)
        return HttpResponse(notice % (target_id, my_wechat, int(time.time()), msgtype, ret))
    return render(request, 'index.html', {'msg': get_robot(request)})
    # return redirect('http://mp.weixin.qq.com/s/Z1uMbza4BMUMnWcG-KS5Og')
