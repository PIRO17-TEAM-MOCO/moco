from django.shortcuts import render, redirect
from django.contrib import auth
from .models import User
from .forms import SignupForm

# url은 임시입니다
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
    return render(request, 'signup.html', {'form' : form})

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(request, username=username, password=password)
    if user is not None:
      auth.login(request, user)
      return redirect('users:main')
    else:
      return render(request, 'login.html')
  else:
    return render(request, 'login.html')

def logout(request):
  auth.logout(request)
  return redirect("users:main")