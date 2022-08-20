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
        ('OneTime', '번개')
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)  # 유저가 삭제되면 작성한 글도 삭제됨
    title = models.CharField(max_length=50)  # 제목
    published_at = models.DateTimeField(auto_now_add=True)  # 게시일자
    location = models.CharField(max_length=20)  # 지역 -> XX시 XX구
    contact = models.CharField(max_length=10, choices=CONTACT_CHOICE)  # 온, 오프
    number = models.IntegerField(default=2)  # 인원 -> 최소2명
    tag = models.CharField(max_length=50, default="상관없음")  # 파이썬, 알고리즘
    content = models.TextField()  # 내용
    apply_link = models.CharField(max_length=100)  # 구글폼 링크가 더 길면 수정
    views = models.IntegerField(default=0)  # 조회수
    duration = models.CharField(
        max_length=10, choices=DURATION_CHOICE)  # 정기, 번개
    activation = models.BooleanField(default=True)  # True : 모집중, False : 모집완료
    likes = models.IntegerField(default=0)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    # 후기 작성 유저
    post = models.ForeignKey(Post, on_delete=models.CASCADE)    # 후기를 다는 Post
    image = models.ImageField(blank=True, null=True,
                              upload_to='post/reviews/%Y%m%d')    # 모임 인증 이미지
    content = models.TextField()    # 내용
    write_at = models.DateTimeField(auto_now_add=True)
