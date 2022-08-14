from django.db import models
from users.models import User
from posts.models import Post
from place.models import Place
from notice.models import Notice

# Create your models here.


class Comment(models.Model):
    TAG_POST = 1
    TAG_PLACE = 2
    TAG_NOTICE = 3
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, blank=True, null=True)
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, blank=True, null=True)
    notice = models.ForeignKey(
        Notice, on_delete=models.CASCADE, blank=True, null=True)
    tag = models.IntegerField()
    content = models.TextField()
    cmt_class = models.IntegerField(default=0)
    pnt_comment = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)
