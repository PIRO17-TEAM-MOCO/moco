from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from .forms import SignupForm


# url은 임시입니다
# main은 기능확인용입니다.
def main(request):
    if request.user:
      context = {
        'user': request.user,
      }
    return render(request, template_name='users/main.html', context=context)

def signup(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      user = form.save()
      auth.login(request, user)
      return redirect('users:main')
    return redirect('users:signup')
  else:
    form = SignupForm()
    context = {
      'form': form,
    }
    return render(request, template_name='users/signup.html', context=context)

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

def logout(request):
  auth.logout(request)
  return redirect("users:main")