from django.shortcuts import render, redirect
from .models import Like
from posts.models import Post
from users.models import User
from place.models import Place

# Create your views here.


def add(request, id, tag):
    if request.method == 'POST':
        user = request.user
        # tag == 1 이런 식이면 맥락 파악이 어렵다. 각주가 있어야만 이해 가능하지만
        # 나중에 수정하다가 각주 수정 안하면 혼란 발생한다.
        # if tag == TAG_PLACE나,
        # if is_tag_place(tag) 함수를 정의해서 사용하도록 하자.
        if tag == 1:
            post = Post.objects.get(id=id)
            Like.objects.create(user=user, post=post, tag=tag)
            return redirect(f"/post/detail/{id}")
        elif tag == 2:
            place = Place.objects.get(id=id)
            Like.objects.create(user=user, place=place, tag=tag)


def delete(request, id, tag):
    if request.method == 'POST':
        user = request.user
        if tag == 1:  # Post
            post = Post.objects.get(id=id)
            deleted_like = Like.objects.get(user=user, post=post, tag=tag)
            deleted_like.delete()
            return redirect(f"/post/detail/{id}")
        elif tag == 2:  # Place
            place = Place.objects.get(id=id)
            deleted_like = Like.objects.get(user=user, place=place, tag=tag)
            deleted_like.delete()
