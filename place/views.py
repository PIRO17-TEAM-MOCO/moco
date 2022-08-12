from django.shortcuts import render, redirect
from .models import Place, PlaceImage
from .forms import PlaceForm
from django.contrib.auth.decorators import login_required

def home(request):
    places = Place.objects.all()
    images = PlaceImage.objects.all()
    sort = request.GET.get('sort', 'None')
    if sort == "latest":
        places = places.order_by("-published_at")
        
    context = {
        "places": places,
        "sort": sort,
        "images": images,
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
    images = PlaceImage.objects.all()
    place = Place.objects.get(id=id)
    # len_likes = len(place.like_set.all())
    # all_comments = place.comment_set.all()
    context = {
        "place": place,
        "images": images,
        # "len_likes": len_likes,
        # "comments": all_comments
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

            # if request.FILES.get("place_images"):
            #     revised_images.image = request.FILES.get("place_images")
            # else:
            #     revised_images.image = revised_images.image
            # revised_images.save()
            return redirect(f'/place/detail/{id}')
        
    else:
        form = PlaceForm(instance=place)
        # place = revised_images.place
        # all_images = place.image_set.all()
        context = {
            "form": form,
            "id": id,
            "place": place,
            # "all_images": all_images
        }
        return render(request, template_name='place/update.html', context=context)

@login_required
def delete(request, id):
    if request.method == "POST":
        place = Place.objects.get(id=id)
        place.delete()
        return redirect('/place')