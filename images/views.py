# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.conf import settings
from actions.utils import create_action
from .forms import ImageCreateForm
from .models import Image
import redis
from django.conf import settings

r = redis.StrictRedis(host=settings.REDIS_HOST,
	                  port=settings.REDIS_PORT,
	                  db=settings.REDIS_DB)


@login_required
def image_create(request):
	if request.method == "POST":
		form = ImageCreateForm(data=request.POST)
		if form.is_valid():
			new_image = form.save(commit=False)
			new_image.user = request.user
			new_image.save()
			create_action(request.user, 'bookmarked image', new_image)
			messages.success(request, 'New image added!')
			return redirect(new_image.get_absolute_url())
	else:
		form = ImageCreateForm()
	return render(request, 'images/image/create.html',
		          {'section': 'images', 'form': form})


def image_detail(request, id, slug):
	image = get_object_or_404(Image, id=id, slug=slug)
	total_views = r.incr('image:{}:views'.format(image.id)) #INCR key-name——将键存储的值加上1
	r.zincrby('image_ranking', image.id, 1)    #ZINCRBY key-name increment member：将member成员的分值加上increment
	return render(request, 'images/image/detail.html',
		          {'section': 'images', 'image': image, 
		           'total_views': total_views})


def image_list(request):
	images_list = Image.objects.all()
	paginator = Paginator(images_list, 10)
	page = request.GET.get('page')
	try:
		images = paginator.page(page)
	except PageNotAnInteger:
		images = paginator.page(1)
	except EmptyPage:
		images = paginator.page(paginator.num_pages)
	return render(request, 'images/image/list.html',
		          {'section': 'images', 'images': images})


@login_required
def image_ranking(request):
	image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
	#ZRANGE key-name start stop [WITHSCORES]——返回有序集合中排名介于start和stop之间的成员
	#如果给定了可选的WITHSCORES选项，那么命令会将成员的分值也一并返回
	image_ranking_ids = [int(id) for id in image_ranking]
	most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
	#list()在这里很重要，因为filter返回的还是查询集，不能用在sort()上，需要强制转换成列表
	#同理以前取回单个对象后面加[:1]也是这个原因
	most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
	return render(request, 'images/image/ranking.html',
		          {'section': 'images',
		           'most_viewed': most_viewed})
