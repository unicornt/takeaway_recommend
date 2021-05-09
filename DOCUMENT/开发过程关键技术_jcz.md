1. 数据库生成

   在django项目下每个新的app内的models.py文件中定义模型的各个属性和属性的类别，再通过

   ```
   python manage.py makemigrations # 创建迁移文件
   python manage.py migrate # 将迁移文件写入数据库
   ```

   来保证数据库文件可以正常被调用

2. 获取前端数据：

   ```
   request.POST["key_name"]
   ```

3. 对数据库进行增删查改：

   ```
   MODEL.objects.create(key=key_value) # 添加条目
   MODEL.objects.get/filter(key=key_value).delete() # 删除条目
   MODEL.objects.get/filter(key=key_value).order_by('key') # 查找信息
   MODEL.objects.get/filter(key=key_value).key = new_value # 更改信息
   ```

4. 发送验证邮件：

   ```
   EmailMultiAlternatives(email_subject, text_content, settings.DEFAULT_FROM_EMAIL, [email]) # 定义邮件主题、内容、发送方，接收方等信息，完成邮件发送
   ```

5. 确认验证邮件是否超时：

   ```
   created_time = confirm.created_time
   now = datetime.datetime.now()
   now = now.replace(tzinfo=pytz.timezone('UTC'))
   cmp = created_time + datetime.timedelta(minutes=settings.CONFIRM_MINUTES, hours=settings.CONFIRM_UTC)
   if now > cmp:
   	# code
   # 判断邮件生成时间与当前时间之间时间差少于设定时间差
   ```

6. 获取图片：

   ```
   piclist = request.FILES.getlist("picture") # 获得所有传送图片文件
   pic_num = len(piclist)
   for i in range(pic_num):
   	pic_file = piclist[i]
   	# code
   # 获取列表中每个图片信息
   ```

7. 保存图片：

   ```
   def recommend_path(instance, filename):
       ext = filename.split('.').pop()
       # filename = 'recommend_{0}_picture_{1}.{2}'.format(instance.picture_key, instance.picture_id, ext)
       filename = instance.picture_id # 重命名图片
       return os.path.join('recommend', filename)  # 设置保存地址
       
   class recommend_pic(models.Model):
   	# code
       picture = models.ImageField('推荐图片', upload_to=recommend_path, blank=True, null=True)  # 调用设置函数
   ```

   