from django.shortcuts import redirect, render
from .models import Comment
from posts.models import Post

# Create your views here.


def write(request, id):
    if request.method == 'POST':
        content = request.POST["content"]
        user = request.user
        post = Post.objects.get(id=id)
        tag = 1
        cmt_class = 0
        Comment.objects.create(user=user, post=post,
                               cmt_class=cmt_class, tag=tag, content=content)
        return redirect(f"/post/detail/{id}")
