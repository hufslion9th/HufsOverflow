from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import (AbstractUser)

# Create your models here.
medium_len = 100
long_len = 255


class StackoverflowUser(AbstractUser):
    email = models.EmailField(verbose_name='email address', max_length=long_len, unique=True)
    name = models.CharField(max_length=long_len)
    reputation_score = models.IntegerField(default=0)
    about_me = models.TextField(default='안녕하세요~')
    ques_asked = models.ManyToManyField('main.Questions', blank=True)
    ans_given = models.ManyToManyField('main.Answer', blank=True)
    profile_pic = models.ImageField(upload_to='user_profile_pic', default='default_image.png', blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
