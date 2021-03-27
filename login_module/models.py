import os

from django.db import models

def user_directory_path(instance, filename):
    ext = filename.split('.').pop()
    filename = '{0}_picture.{1}'.format(instance.usr_id, ext)
    return os.path.join(instance.usr_nkname, filename) # 系统路径分隔符差异，增强代码重用性

# Create your models here.
class usr_info(models.Model):
    usr_id = models.CharField('用户id',max_length=20, unique=True)
    usr_email = models.EmailField('用户邮箱', null=True,unique=True)
    usr_pwd = models.CharField('用户密码', max_length=256)
    usr_nkname = models.CharField('用户昵称',max_length=40, null=True)
    usr_pic = models.ImageField('照片', upload_to = user_directory_path, blank = True, null = True)
    # upload_to 参数接收一个回调函数 user_directory_path，该函数返回具体的路径字符串，图片会自动上传到指定路径下，即 MEDIA_ROOT + upload_to
    # user_directory_path 函数必须接收 instace 和 filename 两个参数。
    # 参数 instace 代表一个定义了 ImageField 的模型的实例，说白了就是当前数据记录；filename 是原本的文件名
    # null 是针对数据库而言，如果 null = True, 表示数据库的该字段可以为空；blank 是针对表单的，如果 blank = True，表示你的表单填写该字段的时候可以不填，但是对数据库来说，没有任何影响

    # 这里定义一个方法，作用是当用户注册时没有上传照片，模板中调用 [ModelName].[ImageFieldName].url 时赋予一个默认路径
    def photo_url(self):
        if self.usr_pic and hasattr(self.usr_pic, 'url'):
            return self.usr_pic.url
        else:
            return '/media/default/user.jpg'