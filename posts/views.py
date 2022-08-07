from email import contentmanager
from django.shortcuts import redirect, render
from .models import Post, User, Review
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta

# Create your views here.


def home(request):
    posts = Post.objects.all()
    sort = request.GET.get('sort', 'None')
    if sort == "latest":
        posts = posts.order_by("-published_at")
    elif sort == "views":
        posts = posts.order_by("-views")

    context = {
        "posts": posts,
        "sort": sort,
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
        id = Post.objects.last().id
        return redirect(f"/post/detail/{id}")

    context = {
        'contacts': Post.CONTACT_CHOICE,
        'durations': Post.DURATION_CHOICE
    }

    return render(request, template_name="posts/main_write.html", context=context)


def detail(request, id):
    post = Post.objects.get(id=id)

    all_reviews = post.review_set.all()

    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow = datetime.replace(tomorrow, hour=0, minute=0, second=0)
    expires = datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")

    if post.user == request.user:  # 현재 로그인한 유저가 해당 모집글을 쓴 유저이면 can_revise가 True
        can_revise = True
    else:
        can_revise = False
        context = {
            "post": post,
            'can_revise': can_revise,   # can_revise가 True면 수정, 삭제, 모집 완료로 전환 가능
            "reviews": all_reviews
        }

        session_cookie = id
        cookie_name = F'post_views:{session_cookie}'
        response = render(
            request, template_name="posts/main_detail.html", context=context)
        if request.COOKIES.get(cookie_name) is not None:
            cookies = request.COOKIES.get(cookie_name)
            cookies_list = cookies.split('|')
            if str(request.user.id) not in cookies_list:
                response.set_cookie(cookie_name, cookies +
                                    f'|{request.user.id}', expires=expires)
                post.views += 1
                post.save()
                return response
        else:
            response.set_cookie(cookie_name, request.user.id, expires=expires)
            post.views += 1
            post.save()
            return response

    context = {
        "post": post,
        'can_revise': can_revise,
        "reviews": all_reviews
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
        'durations': Post.DURATION_CHOICE,
    }

    return render(request, template_name="posts/main_revise.html", context=context)


def delete(request, id):
    if request.method == "POST":
        Post.objects.filter(id=id).delete()
        return redirect("/post")


def close(request, id):
    if request.method == "POST":
        Post.objects.filter(id=id).update(activation=False)
        return redirect(f"/post/detail/{id}")


def review_home(request):
    reviews = Review.objects.all()
    context = {
        'reviews': reviews,
    }
    return render(request, template_name="reviews/review.html", context=context)


def review_write(request, id):
    if request.method == "POST":
        img = request.FILES.get('review_image')
        content = request.POST['review_content']
        user = request.user
        post = Post.objects.get(id=id)
        Review.objects.create(user=user, content=content, post=post, image=img)
        return redirect(f"/post/detail/{id}")


def review_revise(request, id):
    if request.method == "POST":
        img = request.FILES.get('review_image')
        content = request.POST['review_content']
        user = request.user
        post = Review.objects.get(id=id).post
        Review.objects.filter(id=id).update(
            user=user, content=content, post=post, image=img)
        return redirect(f"/post/detail/{post.id}")
    revised_review = Review.objects.get(id=id)
    post = revised_review.post
    all_reviews = post.review_set.all()

    context = {
        'reviews': all_reviews,
        'revised_review': revised_review,
        'post': post
    }
    return render(request, template_name="reviews/review_revise.html", context=context)


def review_delete(request, id):
    if request.method == "POST":
        review = Review.objects.get(id=id)
        post_id = review.post.id
        Review.objects.filter(id=id).delete()
        return redirect(f"/post/detail/{post_id}")
