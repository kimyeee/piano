import time
import hashlib
from django.shortcuts import render, HttpResponse ,redirect
from django.views.decorators.csrf import csrf_exempt

wxtoken = 'weixin'
my_wechat = 'JazzPiano_'
msgtype = 'text'

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

@csrf_exempt
def piano(request):
    target_id = request.GET.get('openid')
    if wx_auth(request):
        return HttpResponse(notice % (target_id, my_wechat, int(time.time()), msgtype, '说点啥呢。。。。'))
    return redirect('http://mp.weixin.qq.com/s/Z1uMbza4BMUMnWcG-KS5Og')

