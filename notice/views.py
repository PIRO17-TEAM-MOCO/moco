from configparser import NoOptionError
from django.shortcuts import render, redirect
from .models import Notice

# Create your views here.


def home(request):
    notices = Notice.objects.all()
    context = {
        "notices": notices
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
    return render(request, template="notice/write.html")


def detail(request, id):
    notice = Notice.objects.get(id=id)
    context = {
        'notice': notice,
    }
    return render(request, template_name="notice/detail.html", context=context)


def update(request, id):
    if request.method == 'POST':
        user = request.user
        title = request.POST["title"]
        content = request.POST["content"]
        Notice.objects.filter(id=id).update(title=title, content=content)
        return redirect(f"/notice/detail/{id}")
    notice = Notice.objects.get(id=id)
    context = {
        'notice': notice,
    }
    if notice.user.id != request.user.id:
        return redirect(f'/notice/detail/{id}')
    return render(request, template_name="notice/revise.html", context=context)


def delete(request, id):
    if request.method == 'POST':
        Notice.objects.filter(id=id).delete()
        return redirect("/notice")
