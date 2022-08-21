from email import contentmanager
from django.shortcuts import redirect, render
from .models import Post, Review
from comments.models import Comment
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.db.models import Q, Count
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from users.views import profile_valid, user_check
import simplejson


@profile_valid
def home(request, contact='None'):
    # url에서 매개변수로 컨택트 받아옴
    # url에서 매개변수를 안 주면 'None'처리
    if contact == 'offline':
        posts = Post.objects.filter(contact='Off')
    elif contact == 'online':
        posts = Post.objects.filter(contact='On')
    elif contact == 'mix':
        posts = Post.objects.filter(contact='Mix')
    else:
        posts = Post.objects.all()
    # search했다면 필터링 실행
    search = request.GET.get('search', 'None')
    if search != 'None':
        posts = posts.filter(
            Q(title__icontains=search) |  # 제목
            Q(content__icontains=search) |  # 내용
            Q(user__nickname__exact=search) |  # 글쓴이(닉네임 정확히 일치해야함)
            Q(location__icontains=search)  # 위치
        )
    # 기간별 필터링 실행
    duration = request.GET.get('duration', 'None')
    if (duration == "Regular") or (duration == "OneTime"):
        posts = posts.filter(duration=duration)

    # 모집중 분류
    # onActive = request.GEt.get('onActive', 'None')
    # if (onActive == 'Yes'):
    #     posts = posts.filter(activation=True)
    # elif (onActive == 'No'):
    #     posts = posts.filter(activation=False)

    # 정렬 실행
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
        "duration": duration,
    }
    return render(request, template_name="posts/main.html", context=context)


@login_required
@profile_valid
def write(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["number"] <= 1:
                messages.error(request, "인원 수는 2명 이상!")
                redirect(f"/post/write")
            tag = form.cleaned_data["tag"]
            tags = []
            tagList = simplejson.loads(tag)
            print(tagList[0]["value"])
            for i in range(len(tagList)):
                tags.append(tagList[i]["value"])
            post = form.save(commit=False)
            post.tag = tags
            post.user = request.user
            post.save()
            exp = post.user.exp
            user = post.user
            user.exp = exp + 25
            user.save()
            return redirect(f"/post/detail/{post.id}")
        else:
            print(form.errors)
            print(form.non_field_errors())
            return redirect("/post/write")

    form = PostForm()
    context = {
        'form': form,
        'contacts': Post.CONTACT_CHOICE,
        'durations': Post.DURATION_CHOICE
    }

    return render(request, template_name="posts/main_write.html", context=context)


def detail(request, id):
    post = Post.objects.get(id=id)

    all_reviews = post.review_set.all()
    paginator = Paginator(all_reviews, 5)
    page = request.GET.get('page', 1)
    reviews = paginator.get_page(page)

    all_comments = post.comment_set.all().filter(cmt_class=Comment.CMT_PARENT)

    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow = datetime.replace(tomorrow, hour=0, minute=0, second=0)
    expires = datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")

    reviews_len = len(post.review_set.all())
    comments_len = len(post.comment_set.all())
    cur_user = request.user

    tags = post.tag
    tags = tags.replace("'", "")
    tags_len = len(tags)
    tags = tags[1:tags_len-1]
    tags = tags.split(",")
    print("tags : ", tags)

    if post.user == request.user:  # 현재 로그인한 유저가 해당 모집글을 쓴 유저이면 can_revise가 True
        can_revise = True
    elif not cur_user.is_authenticated:
        can_revise = False
    else:
        can_revise = False
        context = {
            "post": post,
            'can_revise': can_revise,   # can_revise가 True면 수정, 삭제, 모집 완료로 전환 가능
            "reviews": reviews,
            "review_len": reviews_len,
            "comments": all_comments,
            "comments_len": comments_len,
            "tags": tags
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
        "reviews": reviews,
        "review_len": reviews_len,
        "comments": all_comments,
        "comments_len": comments_len,
    }

    return render(request, template_name="posts/main_detail.html", context=context)


@login_required
def update(request, id):
    post = Post.objects.get(id=id)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data["title"]
            post.location = form.cleaned_data["location"]
            post.contact = form.cleaned_data["contacts"]
            if form.cleaned_data["number"] <= 1:
                messages.error(request, "인원 수는 2명 이상!")
                redirect(f"/post/update/{id}")
            post.number = form.cleaned_data["number"]
            post.tag = form.cleaned_data["tag"]
            post.content = form.cleaned_data["content"]
            post.apply_link = form.cleaned_data["apply_link"]
            post.duration = form.cleaned_data["durations"]
            post.save()

            return redirect(f"/post/detail/{id}")

    form = PostForm(instance=post)
    context = {
        "form": form,
        "id": id,
        "post": post,
    }

    return render(request, template_name="posts/main_revise.html", context=context)


def delete(request, id):
    if request.method == "POST":
        Post.objects.filter(id=id).delete()
        return redirect("/post")


def close(request, id):
    if request.method == "POST":
        Post.objects.filter(id=id).update(activation=False)
        post = Post.objects.get(id=id)
        user = post.user
        exp = user.exp
        user.exp = exp + 50
        user.save()
        return redirect(f"/post/detail/{id}")


@profile_valid
def review_home(request):
    all_reviews = Review.objects.all()
    paginator = Paginator(all_reviews, 5)
    page = request.GET.get('page', 1)
    reviews = paginator.get_page(page)
    context = {
        'reviews': reviews,
    }

    return render(request, template_name="reviews/review.html", context=context)


@login_required
def review_write(request, id):
    if request.method == "POST":
        print("file : ", request.FILES)
        img = request.FILES.get('review_image')
        content = request.POST['review_content']
        user = request.user
        post = Post.objects.get(id=id)
        exp = user.exp
        user.exp = exp + 25
        user.save()
        Review.objects.create(user=user, content=content, post=post, image=img)
        return redirect(f"/post/detail/{id}")


@login_required
def review_revise(request, id):
    revised_review = Review.objects.get(id=id)
    if request.method == "POST":
        print("file_update : ", request.FILES)
        revised_review.user = request.user
        revised_review.content = request.POST['review_content']
        revised_review.post = Review.objects.get(id=id).post
        if request.FILES.get('review_image'):
            revised_review.image = request.FILES.get('review_image')
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


@csrf_exempt
def review_delete(request):
    req = json.loads(request.body)
    review_id = req['id']
    Review.objects.filter(id=review_id).delete()
    data = {
        'id': review_id,
    }
    return JsonResponse(data)
