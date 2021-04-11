# 前端接口文档

## 格式说明

#### html文件接口文档格式

引用的链接地址（如果大量引用类似的，可以自定一个符号统一标识）

触发事件（主要包括[1]需要说明发送请求的事件，以及附带数据的格式。 [2]网页跳转）

#### js文件接口文档格式：

请求地址（没有则填“无”）

接口信息（说明请求方式，是POST还是GET）

功能描述

接口参数信息（函数参数，请求附带的数据格式）

## static/js/upload_pic.js

### loadImg

#### 请求地址

无。

#### 接口信息

无。

#### 功能描述

加载图片，然后显示到指定html元素中。

#### 接口参数说明

**files：**input元素中包含的文件列表属性files

**imgbox：**图片显示的html元素

### upload_pic

#### 请求地址

参数url指定。

#### 接口信息

发送POST请求；

请求里包含**data**，**data**为json格式，里面主要包含**piclist**属性。

#### 功能描述

将指定div分支下的所有图片从前端发送到后端；

如果div下无图片，返回一个alert。

#### 接口参数说明

**调用参数：**{

​	**divname：**指定分支的id；

​	**url**：指定请求地址；

}

**data：**{

​	**piclist：**图片列表；在后端中，需要通过request.FILES.getlist('piclist')获取一个inMemoryUploadedFiles格式的文件列表；

}

## static/js/new_recommend.js

### upload_recommend

#### 请求地址

参数url指定。

#### 接口信息

发送POST请求；

请求里包含data，data为json格式，里面包含text属性。

#### 功能描述

将指定html元素下的文本内容从前端发送到后端；

#### 接口参数说明

**调用参数：**{

​	**textElement：**指定分支的id；

​	**url**：指定请求地址；

}

**data：**{

​	**text：**字符串，传输文本内容；在后端中，直接从request.POST.get('text')获取一个字符串。

}