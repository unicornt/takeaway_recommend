import json
import os
from datetime import datetime

from PIL import Image
from django.http import HttpResponse

# Create your views here.
from recommend_app.models import recommend_info, recommend_pic


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


def check_cookie_recommend(request):
    if 'new_recommend' not in request.session:
        return 'Not recommended.'
    if request.method != 'POST':
        return 'Request method is not POST.'
    return 'ok'


def create_recommend(request):
    reason = check_cookie_logout(request)
    print(reason)
    if reason != 'ok':
        return get_error_response(reason)
    key = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    print(key)
    print(request.POST)
    title = request.POST["title"]
    text = request.POST["text"]
    piclist = request.FILES.getlist("picture")
    pic_num = len(piclist)
    dict = {}
    for i in range(pic_num):
        pic_file = piclist[i]
        type = pic_file.name.split('.').pop()
        # now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        pic_file.name = '{0}-{1}.{2}'.format(key, i, type)
        dict[str(i)] = pic_file.name
        recommend_pic.objects.create(picture_id=pic_file.name, picture_key=key, picture=pic_file)
    # request.session['recommend_piclist'][str(num)] = pic_file.name
    recommend_info.objects.create(recommend_key=key, recommend_title=title,
                                  recommend_user=request.session['user_name'],
                                  recommend_picnum=pic_num,
                                  recommend_text=text, recommend_piclist=json.dumps(dict), recommend_flag=False)
    return get_ok_response('create_recommend', {'key': str(key)})


def get_recommend_for_range_and_order(request):
    POST_INFO = request.POST
    # POST_INFO = json.loads(request.body)
    type_id = POST_INFO['type']  # TYPE=0: LIKES, TYPE=1: UPLOAD TIME, TYPE=2: CLICKS
    user = POST_INFO['user']
    if user == 'admin' and 'is_login' in request.session:
        user = request.session['user_name']
    upbound = int(POST_INFO['upbound']) + 1
    downbound = int(POST_INFO['downbound'])
    order = POST_INFO['order']
    ordertext = ''
    if POST_INFO['order'] == '-':
        ordertext += '-'
    if type_id == '0':
        ordertext += 'recommend_like'
    if type_id == '1':
        ordertext += 'recommend_key'
    if type_id == '2':
        ordertext += 'recommend_clicks'
    try:
        recommend = recommend_info.objects.filter(recommend_user=user).order_by(ordertext)
    except recommend_info.DoesNotExist:
        print('recommend not exist.')
        return get_error_response('recommend not exist.')
    no, ret_dict = 0, {}
    for recommend_item in recommend:
        print(recommend_item.recommend_clicks)
    for recommend_item in recommend[downbound:upbound]:
        user = recommend_item.recommend_user
        title = recommend_item.recommend_title
        text = recommend_item.recommend_text
        like = recommend_item.recommend_like
        clicks = recommend_item.recommend_clicks
        picnum = recommend_item.recommend_picnum
        picdict = json.loads(recommend_item.recommend_piclist)
        print(picdict)
        piclist = []
        for value in picdict.values():
            piclist.append(value)
        print(piclist)
        recommend_dict = {'user': user,
                          'title': title,
                          'text': text,
                          'like': like,
                          'clicks': clicks,
                          'picnum': picnum,
                          'piclist': piclist,
                          }
        ret_dict[no] = recommend_dict
        no += 1
    print(ret_dict)
    return get_ok_response('get_recommend', ret_dict)


def get_recommend_in_range_and_order(request):
    POST_INFO = request.POST
    type = POST_INFO["type"]  # TYPE=0: LIKES, TYPE=1:
    print(id)
    try:
        recommend = recommend_info.objects.get(recommend_key=id)
    except recommend_info.DoesNotExist:
        print('recommend not exist.')
        return get_error_response('recommend not exist.')

    title = recommend.recommend_title
    text = recommend.recommend_text
    piclist = recommend.recommend_piclist
    user = recommend.recommend_user
    like = recommend.recommend_like
    picnum = recommend.recommend_picnum

    # pic_url = []
    if (recommend.recommend_picnum > 0):
        pl = recommend_pic.objects.filter(picture_key=id)
        for pic in pl:
            # pic_url.append(pic.photo_url())
            print(pic.photo_url())
    # ret_dict = {'text':text, 'title':title, 'pic_url':pic_url}

    ret_dict = {'text': text,
                'title': title,
                'piclist': piclist,
                'picnum': picnum,
                'user': user,
                'like': like,
                }
    return get_ok_response('get_recommend', ret_dict)


def delete_recommend(request):
    reason = check_cookie_logout(request)
    # print(reason)
    if reason != 'ok':
        return get_error_response(reason)
    request_data = request.POST
    print(request_data)
    key = request_data['key']
    try:
        recommend_atom = recommend_info.objects.get(recommend_key=key)
    except recommend_info.DoesNotExist:
        print('recommend_info not exist.')
        return get_error_response('recommend_info not exist.')
    num = recommend_atom.recommend_picnum
    dicts = json.loads(recommend_atom.recommend_piclist)
    for x in range(num):
        pic_name = dicts[str(x)]
        path = os.path.join('upload', 'recommend', pic_name)
        if os.path.isfile(path):
            os.remove(path)
    recommend_atom.delete()
    return get_ok_response('delete_recommend')


def download_pic(request):
    global response
    reason = check_cookie_logout(request)

    if reason != 'ok':
        pic_path = '1111111.jpg'
    else:
        request_data = request.POST
        pic_path = request_data['path']

    pic = recommend_pic.objects.get(picture_id=pic_path)
    im = Image.open(pic.picture)
    type = pic.picture.name.split('.').pop()
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


def get_recommend(request):
    id = request.GET.get('id')
    print(id)
    try:
        recommend = recommend_info.objects.get(recommend_key=id)
    except recommend_info.DoesNotExist:
        print('recommend not exist.')
        return get_error_response('recommend not exist.')

    title = recommend.recommend_title
    text = recommend.recommend_text
    piclist = recommend.recommend_piclist
    user = recommend.recommend_user
    like = recommend.recommend_like
    picnum = recommend.recommend_picnum

    # pic_url = []
    if (recommend.recommend_picnum > 0):
        pl = recommend_pic.objects.filter(picture_key=id)
        for pic in pl:
            # pic_url.append(pic.photo_url())
            print(pic.photo_url())
    # ret_dict = {'text':text, 'title':title, 'pic_url':pic_url}

    ret_dict = {'text': text,
                'title': title,
                'piclist': piclist,
                'picnum': picnum,
                'user': user,
                'like': like,
                }
    return get_ok_response('get_recommend', ret_dict)


def user_recommend(request):
    '''
    reason = check_cookie_logout(request)
    # print(reason)
    if reason != 'ok':
        return get_error_response(reason)
    usr = request.session['user_name']

    try:
        recommend_atom = recommend_info.objects.filter(recommend_user=usr).order_by('-recommend_like')
    except recommend_info.DoesNotExist:
        print('recommends not exist.')
        return get_error_response('recommends not exist.')
    '''
    usr = request.POST.get('username')
    print(usr)
    try:
        recommend_atom = recommend_info.objects.filter(recommend_user=usr).order_by('-recommend_like')
    except recommend_info.DoesNotExist:
        print('recommends not exist.')
        return get_error_response('recommends not exist.')
    ret_dict = {}
    for filt in recommend_atom:
        now_dict = {}
        key = filt.recommend_key
        now_dict['user'] = filt.recommend_user
        now_dict['title'] = filt.recommend_title
        now_dict['text'] = filt.recommend_text
        now_dict['piclist'] = filt.recommend_piclist
        now_dict['like'] = filt.recommend_like
        ret_dict[key] = now_dict

    return get_ok_response('user_recommend', ret_dict)


def all_recommend(request):
    reason = check_cookie_logout(request)
    # print(reason)
    try:
        recommend_atom = recommend_info.objects.all().order_by('-recommend_like')
    except recommend_info.DoesNotExist:
        print('recommends not exist.')
        return get_error_response('recommends not exist.')
    ret_dict = {}
    for filt in recommend_atom:
        now_dict = {}
        key = filt.recommend_key
        now_dict['user'] = filt.recommend_user
        now_dict['title'] = filt.recommend_title
        now_dict['text'] = filt.recommend_text
        now_dict['piclist'] = filt.recommend_piclist
        now_dict['like'] = filt.recommend_like
        ret_dict[key] = now_dict

    return get_ok_response('user_recommend', ret_dict)

# def create_recommend_old(request):
#     reason = check_cookie_logout(request)
#     print(reason)
#     if reason != 'ok':
#         return get_error_response(reason)
#     key = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     dict = {}
#     recommend_info.objects.create(recommend_key=key, recommend_title="no title",
#                                   recommend_user=request.session['user_name'],
#                                   recommend_picnum=0,
#                                   recommend_text="no text", recommend_piclist=json.dumps(dict), recommend_flag=False)
#     request.session['new_recommend'] = key
#     request.session['recommend_piclist'] = []
#     request.session['pic_num'] = 0
#     print("create_recommend ok")
#     return get_ok_response('create_recommend', {'key': key})
#
#
# def recommend_addpic(request):
#     reason = check_cookie_logout(request)
#     if reason != 'ok':
#         return get_error_response(reason)
#     reason = check_cookie_recommend(request)
#     print(reason)
#     if reason != 'ok':
#         return get_error_response(reason)
#     if 'recommend_piclist' not in request.session:
#         request.session['recommend_piclist'] = {}
#         request.session['pic_num'] = 0
#     # 获取推荐的编号，HTTP传来的图片
#     key = request.session['new_recommend']
#     pic_file = request.FILES['picture']
#     print(key)
#     print(pic_file)
#     # 图片重命名
#     type = pic_file.name.split('.').pop()
#     now = datetime.now().strftime('%Y-%m-%d %H%M%S')
#     pic_file.name = '{0}.{1}'.format(now, type)
#     # 更新cookie
#     num = request.session['pic_num'] + 1
#     request.session['recommend_piclist'][str(num)] = pic_file.name
#     request.session['pic_num'] = num
#     #更新数据库
#     recommend_atom = recommend_info.objects.get(recommend_key=key)
#     recommend_atom.recommend_picnum = num
#     recommend_atom.save()
#
#     # 保存图片对象
#     recommend_pic.objects.create(picture_id=pic_file.name, picture_key=key, picture=pic_file)
#     print("recommend_addpic ok")
#     return get_ok_response('recommend_addpic', {'key': now})
#
#
# def recommend_delpic(request):
#     reason = check_cookie_logout(request)
#     if reason != 'ok':
#         return get_error_response(reason)
#     reason = check_cookie_recommend(request)
#     if reason != 'ok':
#         return get_error_response(reason)
#     if 'recommend_piclist' not in request.session:
#         print("Not picture now.")
#         return get_error_response("Not picture now.")
#
#     request_data = request.POST
#     pic_id = request_data['pic_id']
#     pic_name = request.session['recommend_piclist'][str(pic_id)]
#     path = os.path.join('upload', 'recommend', pic_name)
#     if os.path.isfile(path):
#         os.remove(path)
#     recommend_pic.objects.get(picture_id=pic_name).delete()
#     request.session['recommend_piclist'][str(pic_id)] = request.session['recommend_piclist'][
#         str(request.session['pic_num'])]
#     request.session['pic_num'] = request.session['pic_num'] - 1
#     return get_ok_response('recommend_delpic')
#
#
# def upload_recommend(request):
#     reason = check_cookie_logout(request)
#     # print(reason)
#     if reason != 'ok':
#         return get_error_response(reason)
#     reason = check_cookie_recommend(request)
#     # print(reason)
#     if reason != 'ok':
#         return get_error_response(reason)
#     request_data = request.POST
#     print(request_data)
#     title, text = request_data['title'], request_data['text']
#     key = request.session['new_recommend']
#     try:
#         recommend_atom = recommend_info.objects.get(recommend_key=key)
#     except recommend_info.DoesNotExist:
#         print('recommend_info not exist.')
#         return get_error_response('recommend_info not exist.')
#
#     if title != "":
#         recommend_atom.recommend_title = title
#     if text != "":
#         recommend_atom.recommend_text = text
#
#     recommend_atom.recommend_piclist = json.dumps(request.session['recommend_piclist'])
#     recommend_atom.recommend_flag = True
#     recommend_atom.recommend_picnum = request.session['pic_num']
#     recommend_atom.save()
#     del request.session['new_recommend']
#     del request.session['recommend_piclist']
#     del request.session['pic_num']
#     return get_ok_response('upload_recommend')
