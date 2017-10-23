# -*- coding: utf-8 -*-
from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ('title', 'url', 'description')
		widgets = {
			'url': forms.HiddenInput,
		}

	def clean_url(self):
		url = self.cleaned_data['url']
		valid_extensions = ['jpg', 'jpeg', 'png', 'bmp']
		url_extensions = url.rsplit('.', 1)[1]
		if url_extensions not in valid_extensions:
			raise forms.ValidationError('Image wrong!')
		return url

	def save(self, force_insert=False, force_update=False, commit=True):
		image = super(ImageCreateForm, self).save(commit=False)
		#模型表单类的save生成模型对象，可选commit=False，只生成对象不向数据库保存
		image_url = self.cleaned_data['url']
		image_name = '{}.{}'.format(slugify(image.title),
			image_url.rsplit('.',1)[1].lower())
		response = request.urlopen(image_url)
		image.image.save(image_name,
			             ContentFile(response.read()),
			             save=False)
		#Model类的save=False与表单类的commit=False类似，只修改对象不向数据库保存
		if commit:
			image.save()
		return image