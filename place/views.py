from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from .models import Place, PlaceImage
from .forms import PlaceForm
from comments.models import Comment
from users.views import profile_valid
from constants import EXP_WRITE, EXP_IMG


@profile_valid
def home(request, category='None'):
    # contact filtering (url로 매개변수 받아옴 => 없다면 None)
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

    # search filtering
    search = request.GET.get('search', None)
    if search != None:
        places = places.filter(
            Q(name__icontains=search) |
            Q(content__icontains=search) |
            Q(user__nickname__exact=search) |  # 글쓴이(닉네임 정확히 일치해야함)
            Q(location__icontains=search)
        )

    # sort는 html에서 받아옴
    sort = request.GET.get('sort', 'None')
    if sort == "latest":
        places = places.order_by("-published_at")
    elif sort == "like":
        places = places.order_by("-likes")
    elif sort == "comment":
        places = places.annotate(comment_count=Count('comment'))
        places = places.order_by("-comment_count")
    else:
        places = places.order_by("-published_at")
    # 페이지네이터 적용
    paginator = Paginator(places, 6)
    page = request.GET.get('page', 1)
    places = paginator.get_page(page)

    pairs = []
    for place in places:
        images = PlaceImage.objects.filter(place=place)
        if images:
            image = images[0]
        else:
            image = None
        width = [0] * place.rating
        pair = [place, image, width]
        pairs.append(pair)

    context = {
        "pairs": pairs,
        "sort": sort,
        "search": search,
        "places": places,
        "user": request.user,
    }
    return render(request, template_name="place/home.html", context=context)


@login_required
@profile_valid
def write(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            place = form.save(commit=False)
            place.user = request.user
            place.save()

            user = place.user
            exp = user.exp
            if request.FILES.getlist('place_images'):
                exp += EXP_IMG
            for img in request.FILES.getlist('place_images'):
                photo = PlaceImage()
                photo.place = place
                photo.image = img
                photo.save()

            user.exp = exp + EXP_WRITE
            user.save()

            return redirect('/place')
        else:
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
    width = [0] * place.rating
    like_user = False
    flag_image = False
    if request.user in place.like_users.all():
        like_user = True
    for image in images:
        if image.place == place:
            flag_image = True
    context = {
        "place": place,
        "images": images,
        "comments": all_comments,
        "comments_len": comments_len,
        "edit_access": False,
        "width": width,
        "like_user": like_user,
        "flag_image": flag_image
    }
    if place.user == request.user:
        context['edit_access'] = True
    return render(request, template_name="place/detail.html", context=context)


@login_required
def update(request, id):
    place = Place.objects.get(id=id)

    if place.user != request.user:
        return redirect(f'/place/detail/{id}')
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

        imgs = request.FILES.getlist('place_images')
        if imgs:
            place.placeimage_set.clear()
            for img in imgs:
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
            "images": images,
        }
        return render(request, template_name='place/update.html', context=context)

@login_required
def delete(request, id):
    if request.method == "POST":
        place = Place.objects.get(id=id)

        if place.user != request.user:
            return redirect(f'/place/detail/{id}')
        place.delete()
        return redirect('/place')