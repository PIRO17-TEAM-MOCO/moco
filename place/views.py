from django.shortcuts import render, redirect
from .models import Place, PlaceImage

def home(request):
    places = Place.objects.all()
    sort = request.GET.get('sort', 'None')
    if sort == "latest":
        posts = posts.order_by("-published_at")

    context = {
        "places": places,
    }
    return render(request, template_name="place/home.html", context=context)

def write(request):
    if request.method == "POST":
        user = request.user
        name = request.POST["name"]
        location = request.POST["location"]
        category = request.POST["category"]
        opening_time = request.POST["opening_time"]
        closing_time = request.POST["closing_time"]
        wifi = request.POST["wifi"]
        power_socket = request.POST["power_socket"]
        rating = request.POST["rating"]
        content = request.POST["content"]
        Place.objects.create(user=user, name=name, location=location, category=category, opening_time=opening_time,
                            closing_time=closing_time, wifi=wifi, power_socket=power_socket, rating=rating, content=content)

        image = request.FILES["image"]
        id = Place.objects.latest('id')
        PlaceImage.objects.create(place=id, image=image)
        return redirect(f"place/detail/{id}")

    context = {
        'categorys': Place.CATEGORY_CHOICE,
        'sockets': Place.SOCKET_CHOICE,
        'wifis': Place.WIFI_CHOICE
    }

    return render(request, template_name="place/write.html", context=context)