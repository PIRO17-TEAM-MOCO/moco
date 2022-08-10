from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import User
from .forms import ProfileForm, SignupForm, FindidForm


# main은 기능확인용입니다.
def main(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    if request.user:
        context['me'] = request.user
        print(context)
    return render(request, template_name='users/main.html', context=context)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('users:main')
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
            return redirect('users:main')
        else:
            return redirect('user:main')
    else:
        return render(request, template_name='users/signout.html')


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return redirect('users:main')
        else:
            context = {
                'form': form,
            }
            return render(request, template_name='users/login.html', context=context)
    else:
        form = AuthenticationForm()
        context = {
            'form': form,
        }
        return render(request, template_name='users/login.html', context=context)


@login_required
def logout(request):
    auth.logout(request)
    return redirect('users:main')


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


def profile_view(request, id):
    user = User.objects.get(id=id)
    birth = user.birth
    today = datetime.now().date()
    age = today.year - birth.year + 1 # 나이 구하기
    context = {
    'user': user,
    'age': age,
    'tag': 0,
    }
    if request.user and request.user == user:
        context['tag'] = 1
    return render(request, template_name='users/profile_view.html', context=context)


@login_required
def profile_edit(request, id):
    # Minor Issue
    # 유저 쿼리 by id -> 이후 request.user와 id 비교
    # 보다 먼저 request.user와 id를 비교하는 것이 효율적입니다.
    user = User.objects.get(id=id)
    # 다른 사람이 프로필 수정하는 것 방지
    if user.id != request.user.id:
        return redirect(f'/account/profile/{id}')
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.nickname = form.cleaned_data['nickname']
            user.profile_img = form.cleaned_data['profile_img']
            user.gender = form.cleaned_data['gender']
            user.birth = form.cleaned_data['birth']
            user.job = form.cleaned_data['job']
            user.desc = form.cleaned_data['desc']
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
