from django.shortcuts import render, redirect
from django.db.models.query_utils import Q
from django.core.mail import send_mail, BadHeaderError
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.http import HttpResponse
from posts.models import Post
from place.models import Place, PlaceImage
from .models import User
from .forms import ProfileForm, SignupForm, FindidForm, ResetpwForm
from constants import *
from datetime import datetime
import json


# 프로필 유효성 검사 데코레이터
def profile_valid(func):
    def wrapper(request, **kargs):
        user = request.user
        if user.is_authenticated:
            if user.birth is None: # 소셜로그인 후 프로필을 입력하지 않았다면
                return redirect(f'/account/profile/add/{user.id}')
            else:
                return func(request, **kargs)
        else:
            return func(request, **kargs)
    return wrapper


@profile_valid
def main(request):
    return render(request, template_name='users/main.html')


def signup_error(request):
    form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, template_name='users/signup_error.html', context=context)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                print('이미 존재하는 이메일입니다.')
                messages.error(request, '이미 존재하는 이메일입니다.')
                return redirect('users:signup_error')
            if User.objects.filter(nickname=form.cleaned_data['nickname']).exists():
                print('이미 존재하는 닉네임입니다.')
                messages.error(request, '이미 존재하는 닉네임입니다.')
                return redirect('users:signup_error')
            user = form.save()
            auth.login(request, user,
                       backend='django.contrib.auth.backends.ModelBackend')      
            if request.FILES.get('profile_img'):
                user.profile_img = request.FILES.get('profile_img')
            user.save()
            return redirect('posts:home')
        else:
            print(form.errors)
            return redirect('users:signup_error')
    else:
        form = SignupForm()
        context = {
            'form': form,
        }
        return render(request, template_name='users/signup.html', context=context)


@login_required
def signout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            request.user.delete()
            auth.logout(request)
            # '그동안 저희 서비스를 이용해주셔서 감사합니다' 페이지 만들어서 바꾸기
            return redirect('posts:home')
        else:
            return redirect('users:login')
    else:
        return render(request, template_name='users/signout.html')


def login(request):
    if request.user.is_authenticated:
            return redirect('posts:home')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        next = request.POST.get("next")
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            try:
                return redirect(next)
            except:
                return redirect('posts:home')
        else:
            context = {
                'form': form,
                'next': next,
            }
            return render(request, template_name='users/login.html', context=context)
    else:
        form = AuthenticationForm()
        next = request.GET.get('next')
        context = {
            'form': form,
            'next': next,
        }
        return render(request, template_name='users/login.html', context=context)


@login_required
def logout(request):
    auth.logout(request)
    next = request.GET.get('next')
    try:
        return redirect(next)
    except:
        return redirect('posts:home')


def find_id(request):
    if request.method == 'POST':
        form = FindidForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            birth = form.cleaned_data['birth']
            email = form.cleaned_data['email']
            users = User.objects.filter(name=name, birth=birth, email=email)  # 모든 user 반환
            context = {
                'users': users,
            }
            return render(request, template_name='users/find_id.html', context=context)
        else:
            return redirect('users:find_id')
    else:
        form = FindidForm()
        context = {
            'form': form,
        }
        return render(request, template_name='users/find_id.html', context=context)


@login_required
def change_pw(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        context = {
            'form': form,
        }
        if form.is_valid():
            user = form.save()
            auth.update_session_auth_hash(request, user)
            # 비밀번호 변경 성공 페이지로 이동
            return redirect('posts:home')
        else:
            return redirect('users:change_pw')
    else:
        form = PasswordChangeForm(request.user)
        context = {
            'form': form,
        }
    return render(request, template_name='users/change_pw.html', context=context)


class CustomConfirmView(PasswordResetConfirmView):
    success_url = '/account/reset-pw/complete/'


def reset_pw(request):
    if request.method == "POST":
        form = ResetpwForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            users = get_user_model().objects.filter(Q(email=email) & Q(username=username))
            if users.exists():
                for user in users:
                    subject = '[MOCO] 비밀번호 재설정'
                    email_template_name = "users/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        # local: '127.0.0.1:8000', prod: '?' // settings.HOSTNAME 후에 사용
                        'domain': 'moco-coding.com',
                        'site_name': 'MOCO',
                        # MTE4
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        # Return a token that can be used once to do a password reset for the given user.
                        'token': default_token_generator.make_token(user),
                        # local: http, prod: https // settings.PROTOCOL 후에 사용
                        'protocol': 'https',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'mocoofficial180@gmail.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect('users:reset_pw_done')
    else:
        form = ResetpwForm()
        context = {
            'form': form,
        }
        return render(request, template_name='users/reset_pw.html', context=context)


@profile_valid
def profile_view(request, id):
    user = User.objects.get(id=id)
    birth = user.birth
    today = datetime.now().date()
    age = today.year - birth.year + 1 # 나이 구하기
    pairs_my = []
    for place in user.place_set.all() :
        width = [0] * place.rating
        images = PlaceImage.objects.filter(place=place)
        if images:
            image = images[0]
        else:
            image = None
        pair = [place, image, width]
        pairs_my.append(pair)
    pairs_like = []
    for place in user.like_places.all() :
        width = [0] * place.rating
        images = PlaceImage.objects.filter(place=place)
        if images:
            image = images[0]
        else:
            image = None
        pair = [place, image, width]
        pairs_like.append(pair)

    context = {
    'user': user,
    'age': age,
    'edit_access': False,
    'pairs_my': pairs_my,
    'pairs_like': pairs_like
    }
    if request.user == user:
        context['edit_access'] = True
    return render(request, template_name='users/profile_view.html', context=context)


@login_required
@profile_valid
def profile_edit(request, id):
    # 다른 사람이 프로필 수정하는 것 방지
    if id != request.user.id:
        return redirect(f'/account/profile/{id}')
    user = User.objects.get(id=id)
    if request.method == "POST":
        form = ProfileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exclude(username=user.username).exists():
                print('다른 유저의 이메일과 중복됩니다. 다른 이메일을 입력해주세요.')
                messages.error(request, '다른 유저의 이메일과 중복됩니다. 다른 이메일을 입력해주세요.')
                return redirect(f'/account/profile/edit/error/{id}')
            if User.objects.filter(nickname=form.cleaned_data['nickname']).exclude(username=user.username).exists():
                print('이미 존재하는 닉네임입니다.')
                messages.error(request, '이미 존재하는 닉네임입니다.')
                return redirect(f'/account/profile/edit/error/{id}')
            user.name = form.cleaned_data['name']
            user.nickname = form.cleaned_data['nickname']
            if form.cleaned_data['profile_img']:
                user.profile_img = form.cleaned_data['profile_img']
            user.gender = form.cleaned_data['gender']
            user.birth = form.cleaned_data['birth']
            user.job = form.cleaned_data['job']
            user.desc = form.cleaned_data['desc']
            user.email = form.cleaned_data['email']
            if request.FILES.get('profile_img'):
                user.profile_img = request.FILES.get('profile_img')
            user.save()
            return redirect(f'/account/profile/{id}')
        else:
            print(form.errors)
            return redirect(f'/account/profile/edit/{id}')
    else:
        form = ProfileForm(instance=user)
        context = {
            "form": form,
            "id": id,
        }
        return render(request, template_name='users/profile_edit.html', context=context)


def signup_error(request):
    form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, template_name='users/signup_error.html', context=context)


@login_required
@profile_valid
def profile_edit_error(request, id):
    form = ProfileForm()
    context = {
        'form': form,
    }
    return render(request, template_name='users/profile_edit_error.html', context=context)


@login_required
def profile_add(request, id):
    # 다른 사람이 프로필 추가하는 것 방지
    if id != request.user.id:
        return redirect(f'/account/profile/{id}')
    user = User.objects.get(id=id)
    if request.method == "POST":
        form = ProfileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exclude(username=user.username).exists():
                print('다른 유저의 이메일과 중복됩니다. 다른 이메일을 입력해주세요.')
                messages.error(request, '다른 유저의 이메일과 중복됩니다. 다른 이메일을 입력해주세요.')
                return redirect(f'/account/profile/add/error/{id}')
            if User.objects.filter(nickname=form.cleaned_data['nickname']).exclude(username=user.username).exists():
                print('이미 존재하는 닉네임입니다.')
                messages.error(request, '이미 존재하는 닉네임입니다.')
                return redirect(f'/account/profile/add/error/{id}')
            user.name = form.cleaned_data['name']
            user.nickname = form.cleaned_data['nickname']
            user.profile_img = form.cleaned_data['profile_img']
            user.gender = form.cleaned_data['gender']
            user.birth = form.cleaned_data['birth']
            user.job = form.cleaned_data['job']
            user.desc = form.cleaned_data['desc']
            user.email = form.cleaned_data['email']
            if request.FILES.get('profile_img'):
                user.profile_img = request.FILES.get('profile_img')
            user.save()
            return redirect('posts:home')
        else:
            return redirect(f'/account/profile/add/{id}')
    else:
        form = ProfileForm(instance=user)
        context = {
            "form": form,
            "id": id,
        }
        return render(request, template_name='users/profile_add.html', context=context)


@login_required
def profile_add_error(request, id):
    form = ProfileForm()
    context = {
        'form': form,
    }
    return render(request, template_name='users/profile_add_error.html', context=context)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def likes(request, tag):
    if is_ajax(request):
        error = False
        # 로그인 안 했으면 로그인 창으로 이동
        if not request.user.is_authenticated:
            error = True
            context = {
                'error': error,
            }
            return HttpResponse(json.dumps(context), content_type='application/json')

        id = request.GET['id']
    if tag == TAG_POST:
        post = Post.objects.get(id=id)
        user = request.user
        if user in post.like_users.all():
            post.like_users.remove(user)
            post.likes -= 1
            post.save()
        else:
            post.like_users.add(user)
            post.likes += 1
            post.save()
        context = {
            'like_count': post.likes,
            'error': error,
        }
        return HttpResponse(json.dumps(context), content_type='application/json')
    elif tag == TAG_PLACE:
        place = Place.objects.get(id=id)
        user = request.user

        if user in place.like_users.all():
            place.like_users.remove(user)
            place.likes -= 1
            place.save()
        else:
            place.like_users.add(user)
            place.likes += 1
            place.save()  
        context = {
            'like_count': place.likes,
            'error': error,
        }
        return HttpResponse(json.dumps(context), content_type='application/json')


def social_error(request):
    return render(request, template_name='users/social_error.html')


@profile_valid
def social_check(request):
    return redirect('posts:home')