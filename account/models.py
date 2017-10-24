# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)    #扩展User的一对一关系
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username) #注意.user.username，先调用对应User，再取出username


class Contact(models.Model):
    follower = models.ForeignKey(User, related_name='followed_set') #followed
    followed = models.ForeignKey(User, related_name='followers_set') #followers
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.follower, self.followed)


User.add_to_class('followers',
                  models.ManyToManyField('self',
                                         through=Contact,
                                         related_name='followed',
                                         symmetrical=False))
