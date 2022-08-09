from django.shortcuts import render, redirect
from .models import Place, PlaceImage
from .forms import PlaceForm
from django.contrib.auth.decorators import login_required

def home(request):
    places = Place.objects.all()
    sort = request.GET.get('sort', 'None')
    if sort == "latest":
        places = places.order_by("-published_at")
        
    context = {
        "places": places,
        "sort": sort
    }
    return render(request, template_name="place/home.html", context=context)

@login_required
def write(request):
    categories = Place.CATEGORY_CHOICE
    wifis = Place.WIFI_CHOICE
    power_sockets = Place.SOCKET_CHOICE

    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            place = form.save(commit=False)
            place.user = request.user
            place.save()
            return redirect(f'/place/detail/{id}')
            
    else:
        form = PlaceForm()
        context = {
            'form': form,
            'categories': categories,
            "wifis": wifis,
            "power_sockets": power_sockets
            }
        return render(request, template_name="place/write.html", context=context)

def detail(request, id):
    place = Place.objects.get(id=id)
    context = {
        "place": place,
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
        }
        return render(request, template_name='place/update.html', context=context)

@login_required
def delete(request, id):
    if request.method == "POST":
        place = Place.objects.get(id=id)
        place.delete()
        return redirect('/place')