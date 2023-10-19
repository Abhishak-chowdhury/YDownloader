from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class DownloadedVideos(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_download')
    video_title=models.CharField(max_length=200)
    video_url=models.CharField(max_length=500)
    video_thumbnali=models.CharField(max_length=500)
    download_date=models.DateTimeField(auto_now_add=True)