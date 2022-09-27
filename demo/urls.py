#encoding:utf-8
# from django.conf.urls.defaults import *
from django.urls import path, re_path, include

from django.contrib import admin

admin.autodiscover()

# urlpatterns = patterns('',
#     (r'^accounts/',include('accounts.urls')),
# )

urlpatterns = [
    path('accounts/', include('accounts.urls')),  # 首页
]