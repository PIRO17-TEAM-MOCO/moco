from configparser import NoOptionError
from django.shortcuts import render, redirect
from .models import Notice, User
from users.views import profile_valid

@profile_valid
def home(request):
    notices = Notice.objects.all()
    admin = User.objects.filter(is_superuser=True)
    user = request.user
    count = len(notices)
    context = {
        "notices": notices,
        "admin": admin,
        "user": user,
        "count": count
    }
    return render(request, template_name="notice/main.html", context=context)


def write(request):
    if request.method == 'POST':
        user = request.user
        title = request.POST["title"]
        content = request.POST["content"]
        Notice.objects.create(user=user, title=title, content=content)
        id = Notice.objects.last().id
        return redirect(f"/notice/detail/{id}")
    return render(request, template_name="notice/write.html")


def detail(request, id):
    notice = Notice.objects.get(id=id)
    admin = User.objects.filter(is_superuser=True)
    user = request.user
    context = {
        'notice': notice,
        'admin': admin,
        'user': user
    }
    return render(request, template_name="notice/detail.html", context=context)


def update(request, id):
    if request.method == 'POST':
        title = request.POST["title"]
        content = request.POST["content"]
        Notice.objects.filter(id=id).update(title=title, content=content)
        return redirect(f"/notice/detail/{id}")
    notice = Notice.objects.get(id=id)
    context = {
        'notice': notice,
    }
    return render(request, template_name="notice/revise.html", context=context)


def delete(request, id):
    if request.method == 'POST':
        Notice.objects.filter(id=id).delete()
        return redirect("/notice")
