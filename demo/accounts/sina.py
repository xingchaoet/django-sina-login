#encoding:utf-8
# Data:11-6-29 下午9:59
# Author: T-y(master@t-y.me)
# File:sina
import sys
sys.path.insert(0,'/var/www/pythoner')
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth.models import User
from models import UserProfile
from weibo import APIClient

APP_KEY = u'your app key'
APP_SECRET = u'your app secret key'

# callback url需与新浪的设置保持一致，本地测试时，修改hosts
CALLBACK_URL = u'your call back url'

def index(request):
    """
    跳转到验证页面
    """
    client = APIClient(app_key=APP_KEY,app_secret=APP_SECRET,redirect_uri=CALLBACK_URL)
    auth_url = client.get_authorize_url()
    return HttpResponseRedirect(auth_url)

def callback(request):
    """
    用户授权后的回调
    """
    code = request.GET.get(u'code')
    client = APIClient(app_key=APP_KEY,app_secret=APP_SECRET,redirect_uri=CALLBACK_URL)
    res = client.request_access_token(code)
    access_token = res['access_token']
    expires_in = res['expires_in']
    request.session['access_token'] = access_token
    request.session['expires_in'] = expires_in
    client.set_access_token(access_token,expires_in)
    uid = client.get.account__get_uid()['uid']
    username = str(uid)+'@weibo'
    email = str(uid) + '@weibo.com'

    # 判断用户是否已经注册过
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:

        # 注册一个微博用户
        new_user = User.objects.create_user(username=username,email=email,password='*******')
        new_user.is_active = True
        try:
            new_user.save()
        except Exception,e:
            return HttpResponse('连接新浪账号时出错:%s'%e)
        
        # 获取用户的新浪信息
        sina_profile = client.users__show(uid)

        # 增加用户档案
        new_prfile = UserProfile(user = new_user)
        new_prfile.screen_name = sina_profile['screen_name'] # 截取前10个字符
        new_prfile.city = '北京'
        new_prfile.introduction = sina_profile['description']

        try:
            new_prfile.save()
        except Exception,e:
            return HttpResponse('注册账号时服务器出现错误：%s' %str(e))
        else:
            pass


    # 登录当前的用户
    login_user = authenticate(username=username,password='*******')
    auth_login(request,login_user)
    return HttpResponse('欢迎你，%s'%request.user.get_profile().screen_name )
