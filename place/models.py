from django.db import models
from users.models import User

class Place(models.Model):
    CATEGORY_CHOICE = [
        ('Cafe', '카페'),
        ('StudyRoom', '스터디룸'),
        ('Etc', '기타'),
    ]
    SOCKET_CHOICE = [
        ('Many', '많음'),
        ('Average', '보통'),
        ('Less', '적음'),
        ('No', '없음'),
    ]
    WIFI_CHOICE = [
        ('Fast', '빠름'),
        ('Slow', '느림'),
        ('No', '없음'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    location = models.CharField(max_length=25)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICE)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    wifi = models.CharField(max_length=5, choices=WIFI_CHOICE)
    power_socket = models.CharField(max_length=5, choices=SOCKET_CHOICE)
    rating = models.FloatField()
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

class PlaceImage(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    image = models.ImageField()