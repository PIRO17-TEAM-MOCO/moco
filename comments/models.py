from django.db import models
from users.models import User
from posts.models import Post
from place.models import Place

# Create your models here.


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, blank=True, null=True)
    # tag 숫자에 대한 의미를 정의하는 변수 필요하다.
    # TAG_POST = 1
    # TAG_PLACE = 2
    tag = models.IntegerField()  # 1이면 post, 2면 place
    content = models.TextField()
    cmt_class = models.IntegerField(default=0)
    cmt_parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
