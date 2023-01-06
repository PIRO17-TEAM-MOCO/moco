from email import contentmanager
from inspect import TPFLAGS_IS_ABSTRACT
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
from users.views import profile_valid
import simplejson
from django.utils.html import strip_tags
from constants import EXP_CLOSE, EXP_WRITE

def update_exp(user, point):
    user.exp = user.exp + point
    user.save()

@profile_valid
def home(request, contact='None'):
    # contact filtering
    if contact == 'offline':
        posts = Post.objects.filter(contact='Off')
    elif contact == 'online':
        posts = Post.objects.filter(contact='On')
    elif contact == 'mix':
        posts = Post.objects.filter(contact='Mix')
    else:
        posts = Post.objects.all()

    # search filtering
    search = request.GET.get('search', None)
    if search != None:
        posts = posts.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search) |
            Q(user__nickname__exact=search) | 
            Q(location__icontains=search)
        )

    # tag filtering
    q=Q()
    tag = request.GET.get('tag', '')
    search_tag_list = []
    if tag != '':
        tags_list = simplejson.loads(tag)
        for tag_index in range(len(tags_list)):
            search_tag_list.append(tags_list[tag_index]["value"])
        for search_tag in search_tag_list:
            q.add(Q(tag__contains="'"+search_tag+"'"), q.OR)
        posts = posts.filter(q)

    # duration filtering
    duration = request.GET.get('duration', 'None')
    if (duration == "Regular") or (duration == "OneTime"):
        posts = posts.filter(duration=duration)

    # active filtering
    on_active = request.GET.get('onActive', 'None')
    if (on_active == "on"):
        posts = posts.filter(activation=True)
    elif (on_active == "off"):
        posts = posts.filter(activation=True or False)

    # sorting
    sort = request.GET.get('sort', 'None')
    if sort == "latest":
        posts = posts.order_by("-published_at")
    elif sort == "views":
        posts = posts.order_by("-views")
    elif sort == "comments":
        posts = posts.annotate(comment_count=Count(
            'comment')).order_by("-comment_count")
    elif sort == "likes":
        posts = posts.order_by("-likes")
    else:
        posts = posts.order_by("-published_at")

    # post 각각의 태그들 모음
    post_tags_dict = {}
    for post in posts:
        post_tags = post.tag
        post_tags = post_tags.replace(" ", "").replace("'", "")[1:len(post_tags)-1]
        post_tags = post_tags.split(",")
        post_tags_dict[post.id] = post_tags

    for post in posts:
        post.content = strip_tags(post.content)
    
    context = {
        "posts": posts,
        "sort": sort,
        "duration": duration,
        "onActive": on_active,
        "tags": post_tags_dict,
        "search": search,
        "tag_for_show": search_tag_list,
        "user": request.user,
    }

    return render(request, template_name="posts/main.html", context=context)


@ login_required
@ profile_valid
def write(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["number"] <= 1:
                messages.error(request, "인원 수는 2명 이상!")
                redirect(f"/post/write")
            tag = form.cleaned_data["tag"]
            tags = []
            tag_list = simplejson.loads(tag)
            for i in range(len(tag_list)):
                tags.append(tag_list[i]["value"])
            post = form.save(commit=False)
            post.tag = tags
            post.user = request.user
            post.save()
            update_exp(post.user, EXP_WRITE)
            return redirect(f"/post/detail/{post.id}")
        else:
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

    # review pagination
    all_reviews = post.review_set.all()
    paginator = Paginator(all_reviews, 5)
    page = request.GET.get('page', 1)
    reviews = paginator.get_page(page)

    all_comments = post.comment_set.all().filter(cmt_class=Comment.CMT_PARENT)

    # for cookie expire
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow = datetime.replace(tomorrow, hour=0, minute=0, second=0)
    expires = datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")

    reviews_len = len(post.review_set.all())
    comments_len = len(post.comment_set.all())
    cur_user = request.user

    # show tags
    tags = post.tag
    tags = tags.replace(" ", "")
    tags = tags.replace("'", "")
    tags_len = len(tags)
    tags = tags[1:tags_len-1]
    tags = tags.split(",")

    # 좋아요 누른 유저 체크
    like_user = False
    if request.user in post.like_users.all():
        like_user = True

    # 현재 로그인한 유저가 해당 모집글을 쓴 유저이면 can_revise가 True(수정, 삭제, 모집 완료 가능)
    if post.user == request.user:
        can_revise = True
    elif not cur_user.is_authenticated:
        can_revise = False
    else:
        can_revise = False
        context = {
            "post": post,
            'can_revise': can_revise,
            "reviews": reviews,
            "review_len": reviews_len,
            "comments": all_comments,
            "comments_len": comments_len,
            "tags": tags,
            "like_user": like_user,
        }

        # views(하루에 한번, 작성자 제외)
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
        "tags": tags,
        "like_user": like_user,
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
            post.contact = form.cleaned_data["contact"]
            if form.cleaned_data["number"] <= 1:
                messages.error(request, "인원 수는 2명 이상!")
                redirect(f"/post/update/{id}")
            post.number = form.cleaned_data["number"]
            tag = form.cleaned_data["tag"]
            if tag != None:
                tags = []
                tagList = simplejson.loads(tag)
                for i in range(len(tagList)):
                    tags.append(tagList[i]["value"])
                post.tag = tags
            post.content = form.cleaned_data["content"]
            post.apply_link = form.cleaned_data["apply_link"]
            post.duration = form.cleaned_data["duration"]
            post.save()

            return redirect(f"/post/detail/{id}")

    form = PostForm(instance=post)

    # 기존 tag show
    origin_tag = post.tag
    origin_tag_len = len(origin_tag)
    origin_tag = origin_tag[1:origin_tag_len-1]
    origin_tag = origin_tag.replace(' ', '')
    origin_tag = origin_tag.replace("'", '')
    origin_tag = origin_tag.split(',')

    context = {
        "form": form,
        "id": id,
        "post": post,
        'contacts': Post.CONTACT_CHOICE,
        'durations': Post.DURATION_CHOICE,
        'origin_tag': origin_tag
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
        update_exp(post.user, EXP_CLOSE)
        return redirect(f"/post/detail/{id}")


@ profile_valid
def review_home(request):
    all_reviews = Review.objects.all()
    paginator = Paginator(all_reviews, 5)
    page = request.GET.get('page', 1)
    reviews = paginator.get_page(page)
    context = {
        'reviews': reviews,
    }
    return render(request, template_name="reviews/review.html", context=context)


@ login_required
def review_write(request, id):
    if request.method == "POST":
        img = request.FILES.get('review_image')
        content = request.POST['review_content']
        user = request.user
        post = Post.objects.get(id=id)
        update_exp(user, EXP_WRITE)
        Review.objects.create(user=user, content=content, post=post, image=img)
        return redirect(f"/post/detail/{id}")


@ login_required
def review_revise(request, id):
    revised_review = Review.objects.get(id=id)
    if request.method == "POST":
        revised_review.user = request.user
        revised_review.content = request.POST['review_content']
        revised_review.post = Review.objects.get(id=id).post
        if request.FILES.get('review_image'):
            revised_review.image = request.FILES.get('review_image')
        revised_review.save()
        return redirect(f"/post/detail/{revised_review.post.id}")


@ csrf_exempt
def review_delete(request):
    req = json.loads(request.body)
    review_id = req['id']
    review = Review.objects.get(id=review_id)
    post = review.post
    Review.objects.filter(id=review_id).delete()
    length = len(post.review_set.all())
    data = {
        'id': review_id,
        'len': length
    }
    return JsonResponse(data)
