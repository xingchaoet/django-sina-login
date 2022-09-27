# encoding:utf-8
from Scripts.priforgepng import patterns
from django.conf.urls.defaults import *

urlpatterns = patterns('accounts',
                       ('^login/sina/$', 'sina.index'),
                       (r'login/sina/callback/$', 'sina.callback'),
                       )
