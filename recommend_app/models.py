import os

from django.db import models


# Create your models here.

def recommend_path(instance, filename):
    ext = filename.split('.').pop()
    #filename = 'recommend_{0}_picture_{1}.{2}'.format(instance.picture_key, instance.picture_id, ext)
    filename = instance.picture_id
    return os.path.join('recommend', filename)  # 系统路径分隔符差异，增强代码重用性


class recommend_pic(models.Model):
    picture_id = models.CharField('图片编号(UTC时间)表示存储名', max_length=20, unique=True, null=False)
    picture_key = models.CharField('图片对应推荐编号', max_length=20, null=False)
    picture = models.ImageField('推荐图片', upload_to=recommend_path, blank=True, null=True)

    def photo_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url
        else:
            return '/media/default/user.jpg'


class recommend_info(models.Model):
    recommend_key = models.CharField('推荐对应id', max_length=20, unique=True, null=False)
    recommend_user = models.CharField('推荐用户',max_length=20, null=False)
    recommend_title = models.TextField('推荐标题', max_length=200, null=False)
    recommend_text = models.TextField('推荐文本', max_length=10000, null=False)
    recommend_piclist = models.CharField('存储图片列表',max_length=1000)
    recommend_flag=models.BooleanField('信息是否上传',default=False)
    recommend_picnum =models.IntegerField('图片数量')
    recommend_like=models.IntegerField('喜欢数量',default=0)
    recommend_clicks = models.IntegerField('点击数', default=1)

class recommend_like(models.Model):
    like_id = models.CharField('点赞推荐编号', max_length=20, null=False)
    like_user = models.CharField('点赞的用户名', max_length=20, null=False)
