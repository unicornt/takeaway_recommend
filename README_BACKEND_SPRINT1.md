# 数据库文档

Sprint1阶段实现多个数据类。

## login_module.usr_info

```
	usr_id = models.CharField('用户id',max_length=20, unique=True)
    usr_email = models.EmailField('用户邮箱', null=True,unique=True)
    usr_pwd = models.CharField('用户密码', max_length=256)
    usr_nkname = models.CharField('用户昵称',max_length=40, null=True)
    usr_pic = models.ImageField('照片', upload_to = user_directory_path, blank = True, null = True)
```

其中user_directory_path为传入图片自动设置保存地址，用户密码保存为加密后的16进制密码字符串。

## login_module.ConfirmString

```
	code = models.CharField(max_length=256, verbose_name='confirm code')
    usr_email = models.EmailField('用户邮箱', null=True,unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
```

其中code表示验证码。验证码在10分钟之内有效，后端验证函数保证该功能的实现。

## recommend_app.recommend_info

```
	recommend_key = models.CharField('推荐对应id', max_length=20, unique=True, null=False)
    recommend_user = models.CharField('推荐用户',max_length=20,unique=True,null=False)
    recommend_title = models.TextField('推荐标题', max_length=200, null=False)
    recommend_text = models.TextField('推荐文本', max_length=10000, null=False)
    recommend_piclist = models.CharField('存储图片列表',max_length=1000)
    recommend_flag=models.BooleanField('信息是否上传',default=False)
    recommend_picnum =models.IntegerField('图片数量')
    recommend_like=models.IntegerField('喜欢数量',default=0)
```

其中recommend_piclist仅保存图片名.图片格式，图片保存于recommend_pic数据表中。

## recommend_app.recommend_pic

```
	picture_id = models.CharField('图片编号(UTC时间)表示存储名', max_length=20, unique=True, null=False)
    picture_key = models.CharField('图片对应推荐编号', max_length=20, unique=True, null=False)
    picture = models.ImageField('推荐图片', upload_to=recommend_path, blank=True, null=True)
```

其中recommend_path为传入图片自动设置保存地址。

# 接口文档

此文件为Takeaway_recommend项目后端代码的接口文档。

## 请求地址

Sprint1阶段请求后端支持的访问地址为http://localhost:8000。

## 前后端交互数据类型

后端实现用render跳转页面，增删查改数据库信息等功能。前端与后端通过约定格式的http/json信息交互，传递包括用户名、密码、图片、文字等信息。

后端实现cookie保存访问状态信息，记录包括用户登录状态、登录名、是否正在编辑推荐、上传的图片名等信息。

## 各接口信息描述

### 四类特殊返回值

为了防止重复描述，现介绍四种特殊类型返回情况，在对应接口的对应情况中出现：

**用户已登录：**`reason='Already login.'`

**接口不为POST请求：**`reason='Request method is not POST.'`

**未登录或已注销：**`reason='Already logout.'`

**未创建空推荐表：**`reason='Not recommended.'`

### login/log_in

#### 接口信息

接口为POST请求，要求用户尚未登录或已经注销账号（即cookie中无登录信息）。

#### 功能描述

实现前端界面登录功能，验证输入的用户名/邮箱与密码是否匹配。

#### 接口参数说明

**usr：**用户输入的用户名/邮箱，字符格式。

**pwd：**用户输入的密码，字符格式。

#### 返回值说明

##### 状态正常

```
HTTP Response:
{
    'status': 'ok',
    'type': 'login', {'usr': user.usr_id},
}

cookie:
request.session['is_login'] = True
request.session['user_id'] = user.id
request.session['user_name'] = user.usr_id
```

##### 状态不正常

```
HTTP Response:
{
    'status': 'error',
    'type': reason,
}
```

**邮箱不存在：**`reason='Email not exist.'`

**用户不存在：**`reason='Username not exist.'`

**密码错误：**`reason='Wrong password.'`

### login/log_out

#### 接口信息

接口为POST请求，要求用户已登录（即cookie中有登录信息）。

#### 功能描述

实现前端界面注销登录功能。

#### 接口参数说明

无。

#### 返回值说明

##### 状态正常

```
HTTP Response:
{
    'status': 'ok',
    'type': 'log_out',
}

cookie:
request.session 清空
```

##### 状态不正常

```
HTTP Response:
{
    'status': 'error',
    'type': reason,
}
```

### login/register

#### 接口信息

接口为POST请求，要求用户尚未登录或已经注销账号（即cookie中无登录信息）。

#### 功能描述

实现前端界面注册功能，验证输入的用户名/邮箱与密码是否匹配。

保存用户信息到usr_info数据表。

#### 接口参数说明

**usr：**用户输入的用户名，字符格式，长度小于20字符，且不与其他用户名重复。

**pwd：**用户输入的密码，字符格式。

**email：**用户输入的邮箱，字符格式，且不与已经注册邮箱重复。

#### 返回值说明

##### 状态正常

```
HTTP Response:
{
    'status': 'ok',
    'type': 'register',
}
```

##### 状态不正常

```
HTTP Response:
{
    'status': 'error',
    'type': reason,
}
```

**邮箱名格式错误：**`reason='Invalid Email Address.'`

**邮箱已存在：**`reason='Email not exist.'`

**用户名过长：**`reason='Invalid Username.'`

**用户名已存在：**`reason='Username already exist.'`

### login/log_email_validate

#### 接口信息

接口为POST请求，要求用户尚未登录或已经注销账号（即cookie中无登录信息）。

#### 功能描述

实现前端界面邮箱验证功能，发送包含验证连接的邮件。

保存验证码信息到ConfirmString数据表。

<img src="README_BACKEND_SPRINT1_resources\fig_email_validate.png" style="zoom:80%;" />

#### 接口参数说明

**email：**用户输入的邮箱，字符格式。

#### 返回值说明

##### 状态正常

```
HTTP Response:
{
    'status': 'ok',
    'type': 'email_validate', {'code': confirm_code},
}
```

##### 状态不正常

```
HTTP Response:
{
    'status': 'error',
    'type': reason,
}
```

**邮箱名格式错误：**`reason='Invalid Email Address.'`

### login/change_pwd

#### 接口信息

接口为POST请求，要求用户已登录（即cookie中有登录信息）。

#### 功能描述

实现前端界面修改密码功能，验证输入旧密码是否正确，新密码与旧密码是否不同。

#### 接口参数说明

**old_pwd：**用户输入的旧密码，字符格式。

**new_pwd：**用户输入的新密码，字符格式。

#### 返回值说明

##### 状态正常

```
HTTP Response:
{
    'status': 'ok',
    'type': 'change_pwd',
}
```

##### 状态不正常

```
HTTP Response:
{
    'status': 'error',
    'type': reason,
}
```

**新/旧密码为空：**`reason='Invalid old/new password.'`

**旧密码输入错误：**`reason='Wrong old password.'`

**新密码与旧密码相同：**`reason='New password cannot be the same with old password.'`

### login/reset_pwd

#### 接口信息

接口为POST请求，要求用户尚未登录或已经注销账号（即cookie中无登录信息）。

#### 功能描述

实现前端界面重设密码功能，验证输入用户名与邮箱是否配对，发送系统随机生成的密码字符串到邮箱。

usr_info数据表中密码修改为新的密码。

#### 接口参数说明

**usr：**用户输入的用户名，字符格式。

**email：**用户输入的密码，字符格式。

<img src="README_BACKEND_SPRINT1_resources\fig_email_resetpwd.png" alt=" " style="zoom:80%;" />

#### 返回值说明

##### 状态正常

```
HTTP Response:
{
    'status': 'ok',
    'type': 'reset_pwd',
}
```

##### 状态不正常

```
HTTP Response:
{
    'status': 'error',
    'type': reason,
}
```

**用户不存在：**`reason='Username not exist.'`

**邮箱与用户名不匹配：**`reason='Invalid Email Address.'`

### login/upload_pic

#### 接口信息

接口为POST请求，要求用户已登录（即cookie中有登录信息）。

#### 功能描述

实现前端界面上传头像功能。

保存图像到cookie对应的用户头像。

#### 接口参数说明

**piclist：**用户输入图像，InMemoryUploadedFile格式。

#### 返回值说明

##### 状态正常

```
HTTP Response:
{
    'status': 'ok',
    'type': 'upload_pic',
}
```

##### 状态不正常

```
HTTP Response:
{
    'status': 'error',
    'type': reason,
}
```

### login/download_pic

#### 接口信息

接口为POST请求，要求用户已登录（即cookie中有登录信息）。

#### 功能描述

实现前端界面下载头像功能。

#### 接口参数说明

无

#### 返回值说明

##### 状态正常

```
HTTP Response：
包含返回图片，以及格式信息。
```

##### 状态不正常

```
HTTP Response:
{
    'status': 'error',
    'type': reason,
}
```

### login/confirm

#### 接口信息

接口为GET请求，要求用户点击邮箱中的验证链接。

#### 功能描述

实现前端界面邮箱验证功能，用户点击邮件中的链接，确认。

#### 接口参数说明

无。

#### 返回值说明

页面跳转，无返回值。

### get/user

#### 接口信息

要求用户已登录（即cookie中有登录信息）。

#### 功能描述

输出当前用户名。

#### 接口参数说明

无。

#### 返回值说明

##### 状态正常

```
HTTP Response:
{
    'status': 'ok',
    'type': 'ger_current_user', {'username': request.session['user_name']},
}
```

##### 状态不正常

```
HTTP Response:
{
    'status': 'error',
    'type': reason,
}
```

### recommend/new_recommend

#### 接口信息

接口为POST请求，要求用户已登录（即cookie中有登录信息）。

#### 功能描述

实现前端界面创建新推荐。

```
recommend_info.objects.create(recommend_key=key, 
							  recommend_title="no title",
							  recommend_user=request.session['user_name'],
                              recommend_text="no text", 
                              recommend_piclist=json.dumps(dict), 
                              recommend_flag=False )
```

数据表recommend_info中创建新条目，key为当前时间，dict为空字典。

#### 接口参数说明

**usr：**用户输入的用户名/邮箱，字符格式。

**pwd：**用户输入的密码，字符格式。

#### 返回值说明

##### 状态正常

```
HTTP Response:
{
    'status': 'ok',
    'type': 'create_recommend', {'key': key},
}

cookie:
request.session['new_recommend'] = key
```

##### 状态不正常

```
HTTP Response:
{
    'status': 'ok',
    'type': reason,
}
```

### recommend/recommend_addpic

#### 接口信息

接口为POST请求，要求用户已登录（即cookie中有登录信息）。

#### 功能描述

实现前端界面添加推荐图片功能。

```
recommend_pic.objects.create(picture_id= pic_file.name, 
							 picture_key=key, 
							 picture=pic_file)
```

数据表recommend_pic中添加新条目，其中key为当前时间。

添加图片文件名更新为当前时间。

图片保存在本地默认地址，cookie中保存图片名以及该推荐的图片总数。

#### 接口参数说明

**picture：**用户输入图像，InMemoryUploadedFile格式。

#### 返回值说明

##### 状态正常

```
HTTP Response:
{
    'status': 'ok',
    'type': 'recommend_addpic', {'key': now},
}

cookie:
request.session['pic_num'] + 1
request.session['recommend_piclist'][str(num)] = pic_file.name
```

##### 状态不正常

```
HTTP Response:
{
    'status': 'error',
    'type': reason,
}
```

### recommend/recommend_delpic

#### 接口信息

接口为POST请求，要求用户已登录（即cookie中有登录信息）。

#### 功能描述

实现前端界面删除图片功能。

删除数据库中保存的图片条目，删除cookie中保存的图片名和位置信息，删除本地保存的图片，更新该推荐图片数量。

#### 接口参数说明

**usr：**用户输入的用户名/邮箱，字符格式。

**pwd：**用户输入的密码，字符格式。

#### 返回值说明

##### 状态正常

```
HTTP Response:
{
    'status': 'ok',
    'type': 'recommend_delpic',
}
```

##### 状态不正常

```
HTTP Response:
{
    'status': 'error',
    'type': reason,
}
```

**图片已经删完：**`reason='Not picture now.'`

### recommend/upload_recommend

#### 接口信息

接口为POST请求，要求用户已登录（即cookie中有登录信息）。

#### 功能描述

实现前端界面上传推荐功能，保存推荐的标题、内容、图片列表、图片数量等信息到recommend_info，清楚cookie中关于此次推荐的信息。

#### 接口参数说明

**title：**用户输入的推荐标题。

**text：**用户输入的推荐正文。

#### 返回值说明

##### 状态正常

```
HTTP Response:
{
    'status': 'ok',
    'type': 'upload_recommend',
}
cookie：
del request.session['new_recommend']
del request.session['recommend_piclist']
del request.session['pic_num']
```

##### 状态不正常

```
HTTP Response:
{
    'status': 'error',
    'type': reason,
}
```

**cookie中推荐key存放错误：**`reason='recommend_info not exist.'`

### recommend/delete_recommend

#### 接口信息

接口为POST请求，要求用户已登录（即cookie中有登录信息）。

#### 功能描述

实现前端界面删除推荐功能。

删除推荐对应图片以及recommend_info中的条目。

#### 接口参数说明

**key：**推荐对应的索引。

#### 返回值说明

##### 状态正常

```
HTTP Response:
{
    'status': 'ok',
    'type': 'delete_recommend',
}
```

##### 状态不正常

```
HTTP Response:
{
    'status': 'error',
    'type': reason,
}
```

**推荐key错误：**`reason='recommend_info not exist.'`

### recommend/download_pic

#### 接口信息

接口为POST请求，要求用户已登录（即cookie中有登录信息）。

#### 功能描述

实现前端界面获取推荐图片功能。

#### 接口参数说明

**path：**用户输入的需求图片。

#### 返回值说明

##### 状态正常

```
HTTP Response：
包含返回图片，以及格式信息。
```

##### 状态不正常

```
HTTP Response:
{
    'status': 'error',
    'type': reason,
}
```

### recommend/user_recommend

#### 接口信息

接口为POST请求，要求用户已登录（即cookie中有登录信息）。

#### 功能描述

实现前端界面获取当前用户所有推荐信息。

#### 接口参数说明

**usr：**用户输入的用户名/邮箱，字符格式。

**pwd：**用户输入的密码，字符格式。

#### 返回值说明

##### 状态正常

```
HTTP Response:
{
    'status': 'ok',
    'type': 'user_recommend', ret_dict,
}

其中：
		key = filt.recommend_key
        now_dict['user'] = filt.recommend_user
        now_dict['title'] = filt.recommend_title
        now_dict['text'] = filt.recommend_text
        now_dict['piclist'] = filt.recommend_piclist
        now_dict['like'] = filt.recommend_like
        ret_dict[key] = now_dict
```

##### 状态不正常

```
HTTP Response:
{
    'status': 'error',
    'type': reason,
}
```

**用户无上传的推荐：**`reason='recommends not exist.'`

### recommend/all_recommend

#### 接口信息

接口为POST请求，要求用户已登录（即cookie中有登录信息）。

#### 功能描述

实现前端界面获取所有用户所有推荐信息。

#### 接口参数说明

**usr：**用户输入的用户名/邮箱，字符格式。

**pwd：**用户输入的密码，字符格式。

#### 返回值说明

##### 状态正常

```
HTTP Response:
{
    'status': 'ok',
    'type': 'user_recommend', ret_dict,
}

其中：
		key = filt.recommend_key
        now_dict['user'] = filt.recommend_user
        now_dict['title'] = filt.recommend_title
        now_dict['text'] = filt.recommend_text
        now_dict['piclist'] = filt.recommend_piclist
        now_dict['like'] = filt.recommend_like
        ret_dict[key] = now_dict
```

##### 状态不正常

```
HTTP Response:
{
    'status': 'error',
    'type': reason,
}
```

**用户无上传的推荐：**`reason='recommends not exist.'`

# 文档版本

本文档为软件工程项目Sprint1阶段后端需求报告1.0版本，编写于2021年4月10日。
