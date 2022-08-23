from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # 유저네임, 비밀번호 상속
    GENDER_CHOICE = [
        ('Male', '남자'),
        ('Female', '여자'),
    ]
    JOB_CHOICE = [
        ('Student', '학생'),
        ('JobSeeker', '취준생'),
        ('Worker', '직장인'),
        ('Etc', '기타')
    ]
    # AbstractUser가 제공하는 이름은 없애고 name 새로 생성
    first_name = None
    last_name = None
    name = models.CharField(max_length=10, null=True)
    email = models.EmailField(null=True) # 이메일을 필수 컬럼으로 재선언
    nickname = models.CharField(max_length=20, null=True)
    birth = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, null=True)
    exp = models.IntegerField(default=0)
    profile_img = models.ImageField(upload_to='profile_img/%Y%m%d', blank=True, null=True)
    job = models.CharField(max_length=10, choices=JOB_CHOICE, null=True)
    desc = models.TextField(max_length=100, blank=True, null=True)
    like_posts = models.ManyToManyField('posts.Post', related_name='like_users')
    like_places = models.ManyToManyField('place.Place', related_name='like_users')