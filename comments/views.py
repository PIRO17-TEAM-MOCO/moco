from django.shortcuts import redirect, render
from .models import Comment
from posts.models import Post
from place.models import Place

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


def revise(request, id):
    if request.method == 'POST':
        content = request.POST["content"]
        Comment.objects.filter(id=id).update(content=content)
        post_id = Comment.objects.get(id=id).post.id
        return redirect(f"/post/detail/{post_id}")
    revised_comment = Comment.objects.get(id=id)
    post = revised_comment.post
    all_reviews = post.review_set.all()
    all_comments = post.comment_set.all()
    context = {
        'post': post,
        'revised_comment': revised_comment,
        'reviews': all_reviews,
        'comments': all_comments
    }
    return render(request, 'comments/comment_revise.html', context=context)


def delete(request, id):
    if request.method == "POST":
        comment = Comment.objects.get(id=id)
        post_id = comment.post.id
        Comment.objects.filter(id=id).delete()
        return redirect(f"/post/detail/{post_id}")


def recomment(request, id):
    re_comment = Comment.objects.get(id=id)
    post = re_comment.post
    all_reviews = post.review_set.all()
    all_comments = post.comment_set.all()
    context = {
        'post': post,
        're_comment': re_comment,
        'reviews': all_reviews,
        'comments': all_comments
    }
    return render(request, 'comments/comment_recomment.html', context=context)
