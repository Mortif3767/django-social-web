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