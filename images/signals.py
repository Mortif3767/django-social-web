# -*- coding: utf-8 -*-
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image


@receiver(m2m_changed, sender=Image.user_like.through)
def user_like_changed(sender, instance, **kwargs):
	instance.total_likes = instance.user_like.count()
	instance.save()
	#这个receiver函数与m2m_changed信号绑定，当Image.user_like.through被执行的时候调用
	#注册这个信号，可以通过自定义应用配置类，把这个信号导入到信号的ready()方法中