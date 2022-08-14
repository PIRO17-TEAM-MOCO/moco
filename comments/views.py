from django.shortcuts import redirect, render
from .models import Comment
from posts.models import Post
from place.models import Place
from notice.models import Notice
import json
from django.http import JsonResponse


# Create your views here.


def write_post(request, id):
    if request.method == 'POST':
        content = request.POST["content"]
        user = request.user
        post = Post.objects.get(id=id)
        tag = 1
        Comment.objects.create(user=user, post=post,
                               tag=tag, content=content)
        return redirect(f"/post/detail/{id}")


def write_place(request, id):
    if request.method == 'POST':
        content = request.POST["content"]
        user = request.user
        place = Place.objects.get(id=id)
        tag = Comment.TAG_PLACE
        Comment.objects.create(user=user, place=place,
                               tag=tag, content=content)
        return redirect(f"/place/detail/{id}")


def write_notice(request, id):
    if request.method == 'POST':
        content = request.POST["content"]
        user = request.user
        notice = Notice.objects.get(id=id)
        tag = Comment.TAG_NOTICE
        Comment.objects.create(user=user, notice=notice,
                               tag=tag, content=content)
        return redirect(f"/notice/detail/{id}")


def revise(request):
    req = json.loads(request.body)
    content = req['content']
    comment_id = req['id']
    comment = Comment.objects.get(id=comment_id)
    comment.update(content=content)
    data = {
        'content': content,
    }
    if comment.tag == Comment.TAG_POST:
        post = comment.post
        post.save()
    elif comment.tag == Comment.TAG_PLACE:
        place = comment.place
        place.save()
    elif comment.tag == Comment.TAG_NOTICE:
        notice = comment.notice
        notice.save()

    print(data)
    return JsonResponse(data)


def delete(request):
    req = json.loads(request.body)
    comment_id = req['id']
    comment = Comment.objects.get(id=comment_id)
    if comment.tag == Comment.TAG_POST:
        post = comment.post
        Comment.objects.get(id=comment_id).delete()
        post_id = post.id
        post.save()
        return redirect(f"/post/detail/{post_id}")
    elif comment.tag == Comment.TAG_PLACE:
        place = comment.place
        Comment.objects.get(id=comment_id).delete()
        place_id = place.id
        place.save()
        return redirect(f"/place/detail/{place_id}")
    elif comment.tag == Comment.TAG_NOTICE:
        notice = comment.notice
        Comment.objects.get(id=comment_id).delete()
        notice_id = notice.id
        notice.save()
        return redirect(f"/notice/detail/{notice_id}")


def recomment(request):
    req = json.loads(request.body)
    pnt_id = req['id']
    content = req['content']
    user = request.user
    pnt_comment = Comment.objects.get(id=pnt_id)
    tag = pnt_comment.tag
    recomment = Comment.objects.create(
        user=user, pnt_comment=pnt_comment, content=content, tag=tag)
    recomment.save()
    data = {
        "content": recomment.content,
        "user": recomment.user,
        "published_at": recomment.published_at
    }
    print(data)
    return JsonResponse(data)
