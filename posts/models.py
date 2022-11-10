from email.mime import image
from django.db import models
from users.models import User

class Post(models.Model):
    CONTACT_CHOICE = [
        ('On', '온라인'),
        ('Off', '오프라인'),
        ('Mix', '혼합'),
    ]
    DURATION_CHOICE = [
        ('Regular', '정기'),
        ('OneTime', '번개')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    title = models.CharField(max_length=50) 
    published_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=20)
    contact = models.CharField(max_length=10, choices=CONTACT_CHOICE)
    number = models.IntegerField()
    tag = models.CharField(max_length=250, blank=True, null=True) 
    content = models.TextField()
    apply_link = models.CharField(max_length=100) 
    views = models.IntegerField(default=0)
    duration = models.CharField(max_length=10, choices=DURATION_CHOICE) 
    activation = models.BooleanField(default=True)
    likes = models.IntegerField(default=0)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE) 
    image = models.ImageField(blank=True, null=True, upload_to='post/reviews/%Y%m%d')  
    content = models.TextField() 
    write_at = models.DateTimeField(auto_now_add=True)
