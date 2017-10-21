# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneFields(settings.AUTH_USER_MODEL)    #扩展User的一对一关系
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username) #注意.user.username，先调用对应User，再取出username