# -*- coding: utf-8 -*-
from django.apps import AppConfig


class ImagesConfig(AppConfig):
	name = 'images'        #python应用路径
	verbose_name = 'Image bookmarks' #设置该应用可读名字
	def ready(self):
		import images.signals