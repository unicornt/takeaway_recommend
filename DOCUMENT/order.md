前置条件存在于cookie；

输入存在于POST.body，为json.loads下的字典格式；输出为json.dumps下的字符串格式

输出字典第一个的key均为status，第二个的key为content

未登录状态下错误信息{“Already logout.”}为已经登出，已登录状态下错误信息{“Already login.”}为已经登录

#### register

url：/login/register

前置条件：未登录状态

输入：用户名(usr)，密码(pwd)，邮箱(email)

输出：{status：register}    #此后输出字典第一个的key均为status，第二个的key为content

错误信息：

- {“Invalid Username”}用户名不为纯数字
- {"Invalid Email Address"}邮箱格式错误
- {“Username already exist”}用户名已经存在
- {“Email address has been used”}邮箱已经注册



#### login

url:/login/log_in

前置条件：未登录状态

输入：用户名/邮箱(usr)，密码(pwd)

输出：{'login', {'usr': user.usr_id}}

错误信息：

- {“Username not exist.”}用户名不存在
- {"Email not exist."}注册邮箱不存在
- {“Invalid Account Format.”}输入用户名/邮箱不合形式
- {“Wrong password.”}密码错误



#### logout

url:/login/log_out

前置条件：登录状态

输入：null

输出：{logout}

错误信息：\*



#### email_validate 表示邮箱验证码

url:/login/email_validate

前置条件：未登录状态

输入：邮箱（email）

输出：{'email_validate', {'code': validate_code}}

错误信息：

- {“Invalid Email Address”}邮箱不合法



#### change_pwd

url:/login/change_pwd

前置条件：登录状态

输入：旧的密码(old_pwd)，新的密码(new_pwd)

输出：{change_pwd}

错误信息：

- {“Invalid old/new password”}旧密码或者新密码为空
- {"Wrong old password."}旧密码出错
- {“New password cannot be the same with old password.”}旧密码与新密码相同



#### reset_pwd

url:/login/reset_pwd

前置条件：未登录状态

输入：用户名(usr)，邮箱(email)

输出：{'reset_pwd'}

错误信息：

- {“Username not exist.”}用户名不存在
- {"Invalid Email Address"}注册邮箱与输入不同



#### 需要信息：

1.输入图片的encode格式

2.输入推荐的各式，如标题，内容，图片的长度/数量，数据库内标注等

3.需要的接口，如保存新建推荐，输出某人的推荐，删除某人的推荐，显示所有推荐，显示热门推荐等