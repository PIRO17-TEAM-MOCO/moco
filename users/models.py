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
        ('Job_Seeker', '취준생'),
        ('Worker', '직장인'),
        ('Etc', '기타')
    ]
    # AbstractUser가 제공하는 이름은 없애고 name 새로 생성
    first_name = None
    last_name = None
    name = models.CharField(max_length=10)
    email = models.EmailField() # 이메일을 필수 컬럼으로 재선언
    nickname = models.CharField(max_length=20)
    birth = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE)
    exp = models.IntegerField(default=0)
    profile_img = models.ImageField(blank=True, null=True)
    job = models.CharField(max_length=10, choices=JOB_CHOICE)
    desc = models.CharField(max_length=100, blank=True, null=True)