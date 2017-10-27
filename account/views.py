# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from actions.utils import create_action
from actions.models import Action
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            #authenticate方法返回一个用户对象
            if user is not None:
                if user.is_active:
                    login(request, user) #login方法将用户设置到session中
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    followed_ids = request.user.followed.values_list('id', flat=True)
    if followed_ids:
        actions = actions.filter(user_id__in=followed_ids)\
            .select_related('user', 'user__profile')\
            .prefetch_related('target')
    actions = actions[:10]
    return render(request, 'account/dashboard.html',
                  {'section': 'dashboard',
                   'actions': actions})
                  #section用来追踪用户在站点中正在查看的页面


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            create_action(new_user, 'has create an account')
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user,
                                      data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                            data=request.POST,
                                            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated!')
            return HttpResponseRedirect('/account/')
        else:
            messages.error(request, 'Error updating profile!')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 
                  'account/user/list.html',
                  {'section': 'people',
                   'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, 
                             username=username,
                             is_active=True)
    return render(request, 
                  'account/user/detail.html',
                  {'section': 'people',
                  'user': user})


@login_required
def follow(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    if request.user in user.followers.all():
        messages.warning(request, 'You have been followed this user!')
    else:
        Contact.objects.get_or_create(follower=request.user, followed=user)  #必须用get_or_create,如果用CREATE那么会造成重复关注
        create_action(request.user, 'is following', user) #这句算是对create_action最好的解释了
        messages.success(request, 'follow success!')
    return redirect(user.get_absolute_url())


@login_required
def unfollow(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    if request.user not in user.followers.all():
        messages.warning(request, 'invalid operate!')  
    else:
        Contact.objects.filter(follower=request.user, followed=user).delete()
        messages.success(request, 'unfollow done!')
    return redirect(user.get_absolute_url())