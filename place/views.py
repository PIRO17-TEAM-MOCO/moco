from django.shortcuts import render, redirect
from .models import Place, PlaceImage
from .forms import PlaceForm
from django.contrib.auth.decorators import login_required

def home(request):
    pairs = []
    places = Place.objects.all()
    # 플레이스와 첫번째 이미지를 묶어서 보내줌
    for place in places:
        images = PlaceImage.objects.filter(place=place)
        if images:
            image = images[0]
        else:
            image = None
        pair = [place, image]
        pairs.append(pair) 
 
    sort = request.GET.get('sort', 'None')
    if sort == "latest":
        places = places.order_by("-published_at")
        
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
            return redirect('/place')
        else:
            print(form.is_valid())
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
    context = {
        "place": place,
        "images": images,
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
            place.category = form.cleaned_data['category']
            place.opening_time = form.cleaned_data['opening_time']
            place.closing_time = form.cleaned_data['closing_time']
            place.wifi = form.cleaned_data['wifi']
            place.power_socket = form.cleaned_data['power_socket']
            place.rating = form.cleaned_data['rating']
            place.content = form.cleaned_data['content']
            place.save()

            return redirect(f'/place/detail/{id}')
        
    else:
        form = PlaceForm(instance=place)
        context = {
            "form": form,
            "id": id,
            "place": place,
        }
        return render(request, template_name='place/update.html', context=context)

@login_required
def delete(request, id):
    if request.method == "POST":
        place = Place.objects.get(id=id)
        place.delete()
        return redirect('/place')