from django.shortcuts import render, redirect
from django.db.models.query_utils import Q
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from datetime import datetime
from .models import User
from .forms import ProfileForm, SignupForm, FindidForm, ResetpwForm
from posts.models import Post
from place.models import Place

# tag 정의
TAG_POST=1
TAG_PLACE=2


# main은 기능확인용입니다.
# def main(request):
#     users = User.objects.all()
#     context = {
#         'users': users
#     }
#     if request.user:
#         context['me'] = request.user
#         print(context)
#     return render(request, template_name='users/main.html', context=context)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('posts:home')
        else:
            return redirect('users:signup')
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
            return redirect('posts:home')
        else:
            return redirect('user:signout')
    else:
        return render(request, template_name='users/signout.html')


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        next = request.POST.get("next")
        if form.is_valid():
            auth.login(request, form.get_user())
            if next == 'None':
                return redirect('posts:home')
            else:
                return redirect(next)
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
    context = {
        'next': next,
    }
    if next == 'None':
        return redirect('posts:home')
    else:
        return redirect(next)


def find_id(request):
    if request.method == 'POST':
        form = FindidForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            birth = form.cleaned_data['birth']
            users = User.objects.filter(name=name, birth=birth) # 모든 user 반환
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
            messages.success(request, 'Password successfully changed')
            redirect('users:change_pw')
        else:
            messages.error(request, 'Password not changed')
            redirect('users:change_pw')
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
                        'domain': '127.0.0.1:8000',
                        'site_name': 'MOCO',
                        # MTE4
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        # Return a token that can be used once to do a password reset for the given user.
                        'token': default_token_generator.make_token(user),
                        # local: http, prod: https // settings.PROTOCOL 후에 사용
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'mocoofficial180@gmail.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect('users:reset_pw_done')
    else:
        form = ResetpwForm()
        context={
            'form': form,
            }
        return render(request, template_name='users/reset_pw.html',context=context)


def profile_view(request, id):
    user = User.objects.get(id=id)
    birth = user.birth
    today = datetime.now().date()
    age = today.year - birth.year + 1 # 나이 구하기
    context = {
    'user': user,
    'age': age,
    'edit_access': False,
    }
    if request.user == user:
        context['edit_access'] = True   
    return render(request, template_name='users/profile_view.html', context=context)


@login_required
def profile_edit(request, id):
    # 다른 사람이 프로필 수정하는 것 방지
    if id != request.user.id:
        return redirect(f'/account/profile/{id}')
    user = User.objects.get(id=id)
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.name = form.cleaned_data['name']
            user.nickname = form.cleaned_data['nickname']
            user.profile_img = form.cleaned_data['profile_img']
            user.gender = form.cleaned_data['gender']
            user.birth = form.cleaned_data['birth']
            user.job = form.cleaned_data['job']
            user.desc = form.cleaned_data['desc']
            user.email = form.cleaned_data['email']
            user.save()
            return redirect(f'/account/profile/{id}')
        else:
            return redirect('users:profile_view')
    else:
        form = ProfileForm(instance=user)
        context = {
            "form": form,
            "id": id,
        }
        return render(request, template_name='users/profile_edit.html', context=context)


@login_required
def like(request, id, tag):
    if request.method == 'POST':
        user = request.user
        if tag == TAG_POST:
            post = Post.objects.get(id=id)
            post.like_users.add(user)
            post.likes += 1
            post.save()
            return redirect(f'/post/detail/{id}')
        elif tag == TAG_PLACE:
            place = Place.objects.get(id=id)
            place.like_users.add(user)
            place.likes += 1
            place.save()
            print('like 성공')
            for like_place in user.like_places.all():
                print(like_place)
            return redirect(f'/place/detail/{id}')
        else:
            return redirect('/post')
    else:
        return redirect('/post')


@login_required
def unlike(request, id, tag):
    if request.method == 'POST':
        user = request.user
        if tag == TAG_POST:
            post = Post.objects.get(id=id)
            post.like_users.remove(user)
            post.likes -= 1
            post.save()
            return redirect(f'/post/detail/{id}')
        elif tag == TAG_PLACE:
            place = Place.objects.get(id=id)
            place.like_users.remove(user)
            place.likes -= 1
            place.save()
            print('unlike 성공')
            for like_place in user.like_places.all():
                print(like_place)
            return redirect(f'/place/detail/{id}')
        else:
            return redirect('/post')
    else:
        return redirect('/post')