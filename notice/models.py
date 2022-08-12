from django.db import models
from users.models import User

# Create your models here.


class Notice(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
