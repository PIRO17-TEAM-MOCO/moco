from email import contentmanager
from django.shortcuts import redirect, render
from .models import Post, User
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@csrf_exempt
def home(request):
    posts = Post.objects.all()
    sort = request.GET.get('sort', 'None')
    if sort == "latest":
        posts = posts.order_by("-published_at")
    elif sort == "views":
        posts = posts.order_by("views")

    context = {
        "posts": posts,
    }
    return render(request, template_name="posts/main.html", context=context)


def write(request):
    if request.method == "POST":
        user = request.user
        title = request.POST["title"]
        location = request.POST["location"]
        contact = request.POST["contact"]
        number = request.POST["number"]
        if int(number) <= 1:     # 2명 미만인 경우
            return redirect("/post/write")
        tag = request.POST["tag"]
        if not tag:
            tag = "상관없음"
        content = request.POST["content"]
        apply_link = request.POST["apply_link"]
        duration = request.POST["duration"]

        Post.objects.create(user=user, title=title, location=location, contact=contact, number=number,
                            tag=tag, content=content, apply_link=apply_link, duration=duration)
        id = len(Post.objects.all())
        return redirect(f"/post/detail/{id}")

    context = {
        'contacts': Post.CONTACT_CHOICE,
        'durations': Post.DURATION_CHOICE
    }

    return render(request, template_name="posts/main_write.html", context=context)


def detail(request, id):
    post = Post.objects.get(id=id)

    context = {
        "post": post,
    }
    return render(request, template_name="posts/main_detail.html", context=context)


def update(request, id):
    if request.method == "POST":
        user = request.user
        title = request.POST["title"]
        location = request.POST["location"]
        contact = request.POST["contact"]
        number = request.POST["number"]
        if int(number) <= 1:
            return redirect(f"/post/update/{id}")
        tag = request.POST["tag"]
        if not tag:
            tag = "상관없음"
        content = request.POST["content"]
        apply_link = request.POST["apply_link"]
        duration = request.POST["duration"]

        Post.objects.filter(id=id).update(user=user, title=title, location=location, contact=contact, number=number,
                                          tag=tag, content=content, apply_link=apply_link, duration=duration)
        return redirect(f"/post/detail/{id}")

    post = Post.objects.get(id=id)
    context = {
        'post': post,
        'contacts': Post.CONTACT_CHOICE,
        'durations': Post.DURATION_CHOICE
    }

    return render(request, template_name="posts/main_update.html", context=context)


def delete(request, id):
    if request.method == "POST":
        Post.objects.filter(id=id).delete()
        return redirect("/post")
