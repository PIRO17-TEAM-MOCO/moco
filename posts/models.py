from email.mime import image
from django.db import models
from users.models import User

# Create your models here.


class Post(models.Model):
    CONTACT_CHOICE = [
        ('On', '온라인'),
        ('Off', '오프라인'),
        ('Mix', '혼합'),
    ]
    DURATION_CHOICE = [
        ('Regular', '정기'),
        ('One-Time', '번개')
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)  # 유저가 삭제되면 작성한 글도 삭제됨
    title = models.CharField(max_length=50)
    published_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=20)  # XX시 XX구
    contact = models.CharField(max_length=10, choices=CONTACT_CHOICE)
    number = models.IntegerField(default=2)  # 최소2명
    # Python, Django, 알고리즘
    tag = models.CharField(max_length=50, default="상관없음")
    content = models.TextField()
    apply_link = models.CharField(max_length=100)  # 구글폼 링크가 더 길면 수정
    views = models.IntegerField(default=0)
    duration = models.CharField(max_length=10, choices=DURATION_CHOICE)
    activation = models.BooleanField(default=True)  # True : 모집중, False : 모집완료
