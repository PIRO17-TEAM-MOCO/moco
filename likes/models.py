from django.db import models
from users.models import User
from posts.models import Post
from place.models import Place

# Create your models here.


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, blank=True, null=True)
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, blank=True, null=True)
    # Like.TAG_POST
    # 아니면, 따로 태그 정보를 정의하는 상수를 만들자.
    # TAG_POST = 1
    # TAG_POST = 2
    tag = models.IntegerField()  # 1이면 post, 2면 place
