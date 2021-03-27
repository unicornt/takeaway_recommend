import json
import random
import datetime
from hashlib import sha256

import validators
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from login_module.models import usr_info
from login_module.utils.utils import generate_verification_code
from takeaway_pj.settings import EMAIL_HOST_USER



def hash_code(s, salt='users_hash'):
    h=sha256()
    s+=salt
    h.update(s.encode())
    return h.hexdigest()

def get_response(resp_dict, content):
    if content is not None:
        resp_dict['content']=content
    resp_bytes = json.dumps(resp_dict, ensure_ascii=False).encode(encoding='utf-8')
    return HttpResponse(resp_bytes, content_type='application/json')

def get_ok_response(reqeust_type, content=None):
    resp_dict={
        'status': 'ok',
        'type': reqeust_type,
    }
    return get_response(resp_dict, content)

def get_error_response(reason, content=None):
    resp_dict={
        'status':'error',
        'type':reason,
    }
    return  get_response(resp_dict, content)

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
    request_data = json.loads(request.body)
    usr, pwd = request_data['usr'], request_data['pwd']
    if usr.isdigit():
        try:
            user = usr_info.objects.get(usr_id=usr)
        except usr_info.DoesNotExist:
            return get_error_response('Username not exist.')
    elif validators.email('someone@example.com'):
        try:
            user = usr_info.objects.get(usr_email=usr)
        except usr_info.DoesNotExist:
            return get_error_response('Email not exist.')
    else:
        return get_error_response('Invalid Account Format.')
    if user.usr_pwd != hash_code(pwd):
        print(pwd)
        print(hash_code(pwd))
        print(user.usr_pwd)
        return get_error_response('Wrong password.')
    request.session['is_login'] = True
    request.session['user_id'] = user.id
    request.session['user_name'] = user.usr_id
    return get_ok_response('login', {'usr': user.usr_id})


def register(request):
    reason = check_cookie_login(request)
    if reason != 'ok':
        return get_error_response(reason)
    request_data = json.loads(request.body)
    usr, pwd, email = request_data['usr'], request_data['pwd'], request_data['email']
    if not usr.isdigit() :
        return get_error_response('Invalid Username')
    if not validators.email('someone@example.com') :
        return get_error_response('Invalid Email Address')

    same_name_user = usr_info.objects.filter(usr_id=usr)
    if same_name_user:
        return get_error_response('Username already exist')
    same_email_user = usr_info.objects.filter(usr_email=email)
    if same_email_user:
        return get_error_response('Email address has been used')
    user = usr_info(usr_id=usr, usr_email=email, usr_pwd=hash_code(pwd))
    user.save()
    return get_ok_response('register')


def email_validate(request):
    reason = check_cookie_login(request)
    if reason != 'ok':
        return get_error_response(reason)

    request_data = json.loads(request.body)
    email = request_data['email']
    if not validators.email('someone@example.com'):
        return get_error_response('Invalid Email Address')
    validate_code = generate_verification_code(False)
    email_subject = 'Validate Code for Take Away Recommend System'
    text_content = 'Here is the Validate Code for Take Away Recommend System.\n' \
                   'You should type the code \n{0} \ninto text box in the website in 10 minutes'.format(
        validate_code)

    send_mail(email_subject, text_content, EMAIL_HOST_USER, [email], fail_silently=False)
    return get_ok_response('email_validate', {'code': validate_code})

def log_out(request):
    if'is_login' not in request.session:
        return get_error_response('Already logout.')
    request.session.flush()
    return get_ok_response('log_out')

def get_current_user(request):
    if 'is_login' not in request.session:
        return get_error_response('Already logout.')
    return get_ok_response('ger_current_user', {'username':request.session['user_name']})



def change_pwd(request):
    reason =check_cookie_logout(request)
    if reason != 'ok':
        return get_error_response(reason)
    request_data = json.loads(request.body)
    usr=request.session['user_name']
    old_pwd, new_pwd = request_data['old_pwd'], request_data['new_pwd']
    if old_pwd == '' or new_pwd == '':
        return get_error_response('Invalid old/new password')
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
        return get_error_response('Invalid Email Address')

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
    global d
    data_error = {
        'Status Code': 404,
        'Reason': 'account error'
    }
    data_ok = {
        'Status Code': 200,
        'Reason': '200 OK'
    }
    if request.method == 'POST':
        try:
            usr = request.POST.get('usr')
            if usr.isdigit():
                try:
                    d = usr_info.objects.get(usr_id=usr)
                except usr_info.DoesNotExist:
                    return HttpResponse(json.dumps(data_error), content_type="application/json")

            pic_file = request.FILES['picture']
            d.usr_pic = pic_file
            d.save()
            return HttpResponse(json.dumps(data_ok), content_type='application/json')

        except ObjectDoesNotExist:
            data_error['Reason'] = 'format error'
            return HttpResponse(json.dumps(data_error), content_type='application/json')
    else:
        data_error['Reason'] = 'method error'
        return HttpResponse(json.dumps(data_error), content_type='application/json')
