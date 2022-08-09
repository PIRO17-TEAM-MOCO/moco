from email import contentmanager
from django.shortcuts import redirect, render
from .models import Post, Review
from comments.models import Comment
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.db.models import Q, Count

# Create your views here.


def home(request):
    query = request.GET.get('query', None)
    dur = request.GET.get('duration', None)
    ctt = request.GET.get('contact', None)

    q = Q()
    if dur == "regular":
        q.add(Q(duration="정기"), q.AND)

    elif dur == "one-time":
        q.add(Q(duration="번개"), q.AND)

    if ctt == "on":
        q.add(Q(contact="온라인"), q.AND)
    elif ctt == "off":
        q.add(Q(contact="오프라인"), q.AND)
    elif ctt == "mix":
        q.add(Q(contact="혼합"), q.AND)

    if query:
        q.add(Q(title__contains=query), q.OR)
        q.add(Q(tag__contains=query), q.OR)
        q.add(Q(content__contains=query), q.OR)
        q.add(Q(location__contains=query), q.OR)
        q.add(Q(user__nickname__contains=query), q.OR)

    posts = Post.objects.filter(q)

    sort = request.GET.get('sort', 'None')
    if sort == "latest":
        posts = posts.order_by("-published_at")
    elif sort == "views":
        posts = posts.order_by("-views")
    elif sort == "comments":
        posts = posts.annotate(comment_count=Count(
            'comment')).order_by("-comment_count")

    context = {
        "posts": posts,
        "sort": sort,
        "duration": dur,
        "contact": ctt
    }
    return render(request, template_name="posts/main.html", context=context)


def write(request):
    if request.method == "POST":
        
        print(request.POST)
        user = request.user
        title = request.POST["title"]
        location = request.POST["location"]
        contact = request.POST["contact"]
        number = request.POST["number"]
        print("number:", number)
        number = float(number.strip())

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

    all_comments = post.comment_set.all()

    len_likes = len(post.like_set.all())

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
            "reviews": all_reviews,
            "comments": all_comments,
            "len_likes": len_likes,
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
        "reviews": all_reviews,
        "comments": all_comments,
        "len_likes": len_likes,
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

    if post.user.id != request.user.id:
        return redirect(f'/post/detail/{id}')
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
        print(img)
        content = request.POST['review_content']
        user = request.user
        post = Post.objects.get(id=id)
        Review.objects.create(user=user, content=content, post=post, image=img)
        return redirect(f"/post/detail/{id}")


def review_revise(request, id):
    revised_review = Review.objects.get(id=id)
    if request.method == "POST":
        revised_review.user = request.user
        revised_review.content = request.POST['review_content']
        revised_review.post = Review.objects.get(id=id).post
        if request.FILES.get("review_image"):
            revised_review.image = request.FILES.get("review_image")
        else:
            revised_review.image = revised_review.image
        revised_review.save()
        return redirect(f"/post/detail/{revised_review.post.id}")

    post = revised_review.post
    all_reviews = post.review_set.all()
    all_comments = post.comment_set.all()

    context = {
        'reviews': all_reviews,
        'revised_review': revised_review,
        'comments': all_comments,
        'post': post
    }
    return render(request, template_name="reviews/review_revise.html", context=context)


def review_delete(request, id):
    if request.method == "POST":
        review = Review.objects.get(id=id)
        post_id = review.post.id
        Review.objects.filter(id=id).delete()
        return redirect(f"/post/detail/{post_id}")
