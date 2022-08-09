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
    tag = models.IntegerField()  # 1이면 post, 2면 place
    content = models.TextField()
    cmt_class = models.IntegerField(default=0)
    cmt_parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
