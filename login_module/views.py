import datetime
import json
from hashlib import sha256

import pytz
import validators
from PIL import Image
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render

from login_module import models
from login_module.models import usr_info, ConfirmString
from takeaway_pj import settings
from takeaway_pj.settings import EMAIL_HOST_USER


def hash_code(s, salt='users_hash'):
    h = sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def get_response(resp_dict, content):
    if content is not None:
        resp_dict['content'] = content
    resp_bytes = json.dumps(resp_dict, ensure_ascii=False).encode(encoding='utf-8')
    return HttpResponse(resp_bytes, content_type='application/json')


def get_ok_response(reqeust_type, content=None):
    resp_dict = {
        'status': 'ok',
        'type': reqeust_type,
    }
    return get_response(resp_dict, content)


def get_error_response(reason, content=None):
    resp_dict = {
        'status': 'error',
        'type': reason,
    }
    return get_response(resp_dict, content)


def check_cookie_logout(request):
    if 'is_login' not in request.session:
        return 'Already logout.'
    if request.method != 'POST':
        return 'Request method is not POST.'
    return 'ok'


def check_cookie_login(request):
    if 'is_login' in request.session:
        return 'Already login.'
    if request.method != 'POST':
        return 'Request method is not POST.'
    return 'ok'


def log_in(request):
    global user
    reason = check_cookie_login(request)
    if reason != 'ok':
        return get_error_response(reason)
    request_data = request.POST
    usr, pwd = request_data['usr'], request_data['pwd']
    if validators.email(usr):
        try:
            user = usr_info.objects.get(usr_email=usr)
        except usr_info.DoesNotExist:
            print('Email not exist.')
            return get_error_response('Email not exist.')
    else:
        try:
            user = usr_info.objects.get(usr_id=usr)
        except usr_info.DoesNotExist:
            print('Username not exist.')
            return get_error_response('Username not exist.')
    if user.usr_pwd != hash_code(pwd):
        print('Wrong password.')
        return get_error_response('Wrong password.')
    request.session['is_login'] = True
    request.session['user_id'] = user.id
    request.session['user_name'] = user.usr_id
    print("ok")
    return get_ok_response('login', {'usr': user.usr_id})


def register(request):
    reason = check_cookie_login(request)
    if reason != 'ok':
        return get_error_response(reason)
    print(request.POST)
    # request_data = json.loads(request.body)
    request_data = request.POST
    usr, pwd, email = request_data['usr'], request_data['pwd'], request_data['email']
    if len(usr) >= 20:
        return get_error_response('Invalid Username.')

    same_name_user = usr_info.objects.filter(usr_id=usr)
    if same_name_user:
        return get_error_response('Username already exist.')
    user = usr_info(usr_id=usr, usr_email=email, usr_pwd=hash_code(pwd))
    user.save()
    return get_ok_response('register')


def make_confirm_string(email):
    global confirm
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    code = hash_code(email, now)
    now = datetime.datetime.now()
    now = now.replace(tzinfo=pytz.timezone('UTC'))
    try:
        confirm = ConfirmString.objects.get(usr_email=email)
        created_time = confirm.created_time
        cmp = created_time + datetime.timedelta(minutes=settings.CONFIRM_MINUTES, hours=settings.CONFIRM_UTC)
        if now > cmp:
            confirm.delete()
        else:
            return 'Validation Email not outdated.', False
    except:
        pass
    models.ConfirmString.objects.create(usr_email=email, code=code, )
    return code, True

def email_validate(request):
    reason = check_cookie_login(request)
    if reason != 'ok':
        return get_error_response(reason)

    print(request.POST)
    request_data = request.POST
    email = request_data['email']

    if not validators.email(email):
        print('Invalid Email Address.')
        return get_error_response('Invalid Email Address.')
    try:
        _ = usr_info.objects.get(usr_email=email)
        print('Email Address exists.')
        return get_error_response('Email Address exists.')
    except:
        pass

    email_subject = 'Validate Code for Take Away Recommend System'
    text_content = 'This is a registration confirmation.'
    url_part = 'localhost:8000'
    confirm_code, status = make_confirm_string(email)
    if status == False:
        print(confirm_code)
        return get_error_response(confirm_code)
    url = f'http://{url_part}/login/confirm?code={confirm_code}'
    html_content = f'<p>Click <a href="{url}" target="blank">this</a> to accomplish the confirmation.</p>'
    message = EmailMultiAlternatives(email_subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
    message.attach_alternative(html_content, 'text/html')
    message.send()
    return get_ok_response('email_validate', {'code': confirm_code})


def user_confirm(request):
    confirm_code = request.GET.get('code', None)
    try:
        confirm = ConfirmString.objects.get(code=confirm_code)
    except:
        message = 'Invalid confirm request.'
        print(message)
        return render(request, 'invalid_confirm_request.html', locals())
    created_time = confirm.created_time
    now = datetime.datetime.now()
    now = now.replace(tzinfo=pytz.timezone('UTC'))
    cmp = created_time + datetime.timedelta(minutes=settings.CONFIRM_MINUTES, hours=settings.CONFIRM_UTC)
    #cmp = created_time + datetime.timedelta(seconds=5, hours=settings.CONFIRM_UTC)
    print(now, cmp)
    confirm.delete()
    if now > cmp:
        message = 'Your email expired. Please register again.'
        print(message)
        return render(request, 'email_expired.html', locals())
    message = 'Successfully confirmed.'
    print(message)
    return render(request, 'Successfully_confirmed.html', {"email": confirm.usr_email})


def log_out(request):
    if 'is_login' not in request.session:
        return get_error_response('Already logout.')
    request.session.flush()
    return get_ok_response('log_out')


def get_current_user(request):
    if 'is_login' not in request.session:
        return get_error_response('Already logout.')
    return get_ok_response('ger_current_user', {'username': request.session['user_name']})


def change_pwd(request):
    reason = check_cookie_logout(request)
    if reason != 'ok':
        return get_error_response(reason)
    request_data = json.loads(request.body)
    usr = request.session['user_name']
    old_pwd, new_pwd = request_data['old_pwd'], request_data['new_pwd']
    if old_pwd == '' or new_pwd == '':
        return get_error_response('Invalid old/new password.')
    user = usr_info.objects.get(usr_id=usr)
    if user.usr_pwd != hash_code(old_pwd):
        return get_error_response('Wrong old password.')
    if new_pwd == old_pwd:
        return get_error_response('New password cannot be the same with old password.')
    user.usr_pwd = hash_code(new_pwd)
    user.save()
    return get_ok_response('change_pwd')


def reset_pwd(request):
    reason = check_cookie_login(request)
    if reason != 'ok':
        return get_error_response(reason)
    request_data = json.loads(request.body)
    usr, email = request_data['usr'], request_data['email']
    try:
        user = usr_info.objects.get(usr_id=usr)
    except:
        return get_error_response('Username not exist.')
    if user.usr_email != email:
        return get_error_response('Invalid Email Address.')

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_pwd = hash_code(usr, now)[:16]
    email_subject = 'New Password for Take Away Recommend System Account'
    text_content = 'Here is your New Password for Take Away Recommend System.\n' \
                   'It is formed in random and you should remember the password {0} carefully' \
        .format(new_pwd)
    print(new_pwd)
    print(hash_code(new_pwd))
    send_mail(email_subject, text_content, EMAIL_HOST_USER, [email], fail_silently=False)
    user.usr_pwd = hash_code(new_pwd)
    user.save()
    return get_ok_response('reset_pwd')


def upload_pic(request):
    reason = check_cookie_logout(request)
    if reason != 'ok':
        # return get_error_response(reason)
        usr = '1111111'
    else:
        usr = request.session['user_name']
    #pic_file = request.FILES['picture']

    pic_list = request.FILES.getlist('piclist')
    print(pic_list)

    d = usr_info.objects.get(usr_id=usr)
    for pic_file in pic_list:
        d.usr_pic = pic_file
    d.save()

    return get_ok_response('upload_pic')


def download_pic(request):
    global response
    reason = check_cookie_logout(request)
    if reason != 'ok':
        # return get_error_response(reason)
        usr = '1111111'
    else:
        usr = request.session['user_name']
    d = usr_info.objects.get(usr_id=usr)
    im = Image.open(d.usr_pic)
    type = d.usr_pic.name.split('.').pop()
    # print(im)
    # plt.imshow(im)
    # return get_ok_response('download_pic')
    if type in ['jpeg', 'jpg', 'jpe']:
        response = HttpResponse(content_type='image/jpg')
        im.save(response, "JPEG")
    elif type == 'png':
        response = HttpResponse(content_type='image/jpg')
        im.save(response, "PNG")
    elif type in ['mpeg', 'mpg', 'mpe']:
        response = HttpResponse(content_type='image/jpg')
        im.save(response, "PNG")
    return response

def upload_text(request):
    global response
    print(request.POST)
    print(request.POST['text'])
    return get_ok_response('upload_text')
