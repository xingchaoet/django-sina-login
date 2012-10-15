#encoding:utf-8
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    """
    用户资料
    """
    user = models.ForeignKey(User,unique=True)
    screen_name = models.CharField('昵称',max_length=10,blank=False,null=False,help_text='长度为1~10个字符')
    city = models.CharField('城市',max_length=15,default='北京')
    introduction = models.CharField('介绍',max_length=200,blank=True,help_text='个人介绍最大长度为200字符')

    def __unicode__(self):
        return self.screen_name

