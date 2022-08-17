from re import search
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .models import Place, PlaceImage
from .forms import PlaceForm
from comments.models import Comment


def home(request, category='None'):
    # url에서 매개변수로 카테고리 받아옴
    # url에서 매개변수를 안 주면 'None'처리
    if category == 'all':
        places = Place.objects.all()
    elif category == 'cafe':
        places = Place.objects.filter(category='Cafe')
    elif category == 'studyroom':
        places = Place.objects.filter(category='StudyRoom')
    elif category == 'etc':
        places = Place.objects.filter(category='Etc')
    else:
        places = Place.objects.all()
    places = places.annotate(comment_count=Count('comment'))
    # search했다면 필터링 실행
    search = request.Get.get('search', 'None')
    if search:
        places.filter(
            Q(title__icontains = search) | #제목
            Q(body__icontains = search) | #내용
            Q(writer__username__icontains = search) #글쓴이
            )
    # sort는 html에서 받아옴
    sort = request.GET.get('sort', 'None')
    if sort == "latest":
        places = places.order_by("-published_at")
    elif sort == "like":
        places = places.order_by("-likes")
    elif sort == "comment":
        places = places.order_by("-comment_count")
    # 플레이스와 해당 이미지를 묶어서 context로 보내줌
    pairs = []
    for place in places:
        images = PlaceImage.objects.filter(place=place)
        if images:
            image = images[0]
        else:
            image = None
        pair = [place, image]
        pairs.append(pair)

    context = {
        "pairs": pairs,
        "sort": sort,
    }
    return render(request, template_name="place/home.html", context=context)


@login_required
def write(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            place = form.save(commit=False)
            place.user = request.user
            place.save()
            for img in request.FILES.getlist('place_images'):
                photo = PlaceImage()
                photo.place = place
                photo.image = img
                photo.save()

            user = place.user
            exp = user.exp
            user.exp = exp + 25
            user.save()

            return redirect('/place')
        else:
            # print(form.is_valid())
            return redirect('place:write')
    else:
        form = PlaceForm()
        context = {
            'form': form,
        }
        return render(request, template_name="place/write.html", context=context)


def detail(request, id):
    place = Place.objects.get(id=id)
    images = PlaceImage.objects.filter(place=place)
    all_comments = place.comment_set.all().filter(cmt_class=Comment.CMT_PARENT)
    comments_len = len(place.comment_set.all())

    context = {
        "place": place,
        "images": images,
        "comments": all_comments,
        "comments_len": comments_len,
    }
    return render(request, template_name="place/detail.html", context=context)


@login_required
def update(request, id):
    place = Place.objects.get(id=id)
    if request.method == "POST":
        form = PlaceForm(request.POST)
        if form.is_valid():
            place.name = form.cleaned_data['name']
            place.location = form.cleaned_data['location']
            place.location_detail = form.cleaned_data['location_detail']
            place.category = form.cleaned_data['category']
            place.opening_time = form.cleaned_data['opening_time']
            place.closing_time = form.cleaned_data['closing_time']
            place.wifi = form.cleaned_data['wifi']
            place.power_socket = form.cleaned_data['power_socket']
            place.rating = form.cleaned_data['rating']
            place.content = form.cleaned_data['content']
            place.save()
        # 기존 이미지는 연결 해제하고 새로운 이미지 업로드
        place.placeimage_set.clear()
        for img in request.FILES.getlist('place_images'):
            photo = PlaceImage()
            photo.place = place
            photo.image = img
            photo.save()
        return redirect(f'/place/detail/{id}')
    else:
        form = PlaceForm(instance=place)
        images = PlaceImage.objects.filter(place=place)
        context = {
            "form": form,
            "id": id,
            "place": place,
            "images": images
        }
        return render(request, template_name='place/update.html', context=context)


@login_required
def delete(request, id):
    if request.method == "POST":
        place = Place.objects.get(id=id)
        place.delete()
        return redirect('/place')
