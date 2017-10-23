from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.conf import settings
from .forms import ImageCreateForm
from .models import Image


@login_required
def image_create(request):
	if request.method == "POST":
		form = ImageCreateForm(data=request.POST)
		if form.is_valid():
			new_image = form.save(commit=False)
			new_image.user = request.user
			new_image.save()
			messages.success(request, 'New image added!')
			return redirect(new_image.get_absolute_url())
	else:
		form = ImageCreateForm()
	return render(request, 'images/image/create.html',
		          {'section': 'images', 'form': form})


def image_detail(request, id, slug):
	image = get_object_or_404(Image, id=id, slug=slug)
	image_dir = settings.BASE_DIR + image.image.url
	return render(request, 'images/image/detail.html',
		          {'section': 'images', 'image': image, 'image_dir': image_dir})


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

