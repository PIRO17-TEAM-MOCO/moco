from django.shortcuts import redirect, render
from .models import Comment
from posts.models import Post
from place.models import Place
from notice.models import Notice
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from constants import EXP_CMT, POST_NAME, PLACE_NAME



def update_exp(user, exp):
    user.exp = exp + EXP_CMT
    user.save()
    
@login_required
def write_post(request, id):
    if request.method == 'POST':
        content = request.POST["content"]
        post = Post.objects.get(id=id)
        tag = Comment.TAG_POST
        update_exp(request.user, request.user.exp)
        Comment.objects.create(user=request.user, post=post,
                               tag=tag, content=content)
        return redirect(f"/post/detail/{id}")

@login_required
def write_place(request, id):
    if request.method == 'POST':
        content = request.POST["content"]
        place = Place.objects.get(id=id)
        tag = Comment.TAG_PLACE
        update_exp(request.user, request.user.exp)
        Comment.objects.create(user=request.user, place=place,
                               tag=tag, content=content)
        return redirect(f"/place/detail/{id}")

@csrf_exempt
@login_required
def revise(request):
    req = json.loads(request.body)
    comment_id = req['id']
    comment_content = req['content']
    Comment.objects.filter(id=comment_id).update(content=comment_content)
    data = {
        'id': comment_id,
        'content':comment_content
    }
    return JsonResponse(data)


@csrf_exempt
@login_required
def delete(request):
    req = json.loads(request.body)
    comment_id = req['id']
    comment = Comment.objects.get(id=comment_id)
    if comment.tag == Comment.TAG_POST:
        temp = comment.post
    elif comment.tag == Comment.TAG_PLACE:
        temp = comment.place
    Comment.objects.get(id=comment_id).delete()
    length = len(temp.comment_set.all())
    temp.save()
    data = {
        'id': comment_id,
        'len': length
    }
    return JsonResponse(data)


@login_required
def recomment(request, id):
    if request.method == 'POST':
        pnt_id = id
        content = request.POST["content"]
        user = request.user
        pnt_comment = Comment.objects.get(id=pnt_id)
        tag = pnt_comment.tag
        cmt_class = Comment.CMT_CHILD
        if pnt_comment.tag == Comment.TAG_POST:
            temp = pnt_comment.post
            temp_name = POST_NAME
            Comment.objects.create(
                user=user, pnt_comment=pnt_comment, content=content, tag=tag, cmt_class=cmt_class, post=temp)
        elif pnt_comment.tag == Comment.TAG_PLACE:
            temp = pnt_comment.place
            temp_name = PLACE_NAME
            Comment.objects.create(
                user=user, pnt_comment=pnt_comment, content=content, tag=tag, cmt_class=cmt_class, place=temp)
        return redirect(f"/{temp_name}/detail/{temp.id}")

