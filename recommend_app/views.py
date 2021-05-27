import json
import os
from datetime import datetime

from PIL import Image
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from recommend_app.models import recommend_info, recommend_pic, recommend_like, recommend_click


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
    # if request.method != 'POST':
    # return 'Request method is not POST.'
    return 'ok'


def check_cookie_recommend(request):
    if 'new_recommend' not in request.session:
        return 'Not recommended.'
    if request.method != 'POST':
        return 'Request method is not POST.'
    return 'ok'


def create_recommend(request):  # 创建推荐
    reason = check_cookie_logout(request)
    if reason != 'ok':
        return get_error_response(reason)
    key = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    title = request.POST["title"]
    text = request.POST["text"]
    piclist = request.FILES.getlist("picture")
    '''新增'''
    timeRange = request.POST["timeRange"]
    catalog = request.POST["catalog"]
    pic_num = len(piclist)
    dict = {}
    for i in range(pic_num):
        pic_file = piclist[i]
        type = pic_file.name.split('.').pop()
        pic_file.name = '{0}-{1}.{2}'.format(key, i, type)
        dict[str(i)] = pic_file.name
        recommend_pic.objects.create(picture_id=pic_file.name, picture_key=key, picture=pic_file)
    # request.session['recommend_piclist'][str(num)] = pic_file.name
    recommend_info.objects.create(recommend_key=key, recommend_title=title,
                                  recommend_user=request.session['user_name'],
                                  recommend_picnum=pic_num, recommend_time=timeRange, recommend_catalog=catalog,
                                  recommend_text=text, recommend_piclist=json.dumps(dict), recommend_flag=False)
    return get_ok_response('create_recommend', {'key': str(key)})


def edit_index(request):  # 编辑推荐
    reason = check_cookie_logout(request)
    if reason != 'ok':
        return get_error_response(reason)
    request_data = request.GET
    key = request_data['key']
    try:
        recommend_atom = recommend_info.objects.get(recommend_key=key)
    except recommend_info.DoesNotExist:
        print('recommend_info not exist.')
        return get_error_response('recommend_info not exist.')
    if (recommend_atom.recommend_user != request.session['user_name']):
        return get_error_response('Invalid Operation!')

    title = recommend_atom.recommend_title
    text = recommend_atom.recommend_text
    piclist = json.loads(recommend_atom.recommend_piclist)
    '''新增'''
    timeRange = recommend_atom.recommend_time
    catalog = recommend_atom.recommend_catalog
    render_dict = {
        "title": title,
        "text": text,
        "piclist": piclist,
        "timeRange": timeRange,
        "catalog": catalog,
    }
    print(piclist)
    return render(request, 'edit.html', render_dict)


def update_recommend(request):  # 完全的更新推荐，先删除原推荐的全部信息，再覆盖
    reason = check_cookie_logout(request)
    if reason != 'ok':
        return get_error_response(reason)
    request_data = request.POST
    key = request_data['key']
    try:
        recommend_atom = recommend_info.objects.get(recommend_key=key)
    except recommend_info.DoesNotExist:
        print('recommend_info not exist.')
        return get_error_response('recommend_info not exist.')
    if recommend_atom.recommend_user != request.session['user_name']:
        return get_error_response('Invalid Operation!')
    num = recommend_atom.recommend_picnum
    dicts = json.loads(recommend_atom.recommend_piclist)
    for x in range(num):
        pic_name = dicts[str(x)]
        print(pic_name)
        path = os.path.join('upload', 'recommend', pic_name)
        if os.path.isfile(path):
            os.remove(path)
        recommend_pic.objects.get(picture_id=pic_name).delete()

    title = request.POST["title"]
    text = request.POST["text"]
    piclist = request.FILES.getlist("picture")
    '''新增'''
    timeRange = request.POST["timeRange"]
    catalog = request.POST["catalog"]
    pic_num = len(piclist)
    dict = {}
    recommend_atom.recommend_title = title
    recommend_atom.recommend_text = text
    recommend_atom.recommend_picnum = pic_num
    recommend_atom.recommend_time = timeRange
    recommend_atom.recommend_catalog = catalog
    recommend_atom.recommend_piclist = json.dumps(dict)

    for i in range(pic_num):
        pic_file = piclist[i]
        type = pic_file.name.split('.').pop()
        pic_file.name = '{0}-{1}.{2}'.format(key, i, type)
        dict[str(i)] = pic_file.name
        recommend_pic.objects.create(picture_id=pic_file.name, picture_key=key, picture=pic_file)
    return get_ok_response('create_recommend', {'key': str(key)})


def get_recommend_for_range_and_order(request):  # 获得排序的推荐
    POST_INFO = request.POST
    # POST_INFO = json.loads(request.body)
    type_id = POST_INFO['type']  # TYPE=0: LIKES, TYPE=1: UPLOAD TIME, TYPE=2: CLICKS
    is_all = POST_INFO['is_all']
    user = POST_INFO['user']
    if user == 'admin' and 'is_login' in request.session:
        user = request.session['user_name']
    downbound = 0
    upbound = recommend_info.objects.filter(recommend_user=user).count()
    if (is_all == '0'):
        upbound = int(POST_INFO['upbound']) + 1
        downbound = int(POST_INFO['downbound'])
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
    for recommend_atom in recommend[downbound:upbound]:
        user = recommend_atom.recommend_user
        title = recommend_atom.recommend_title
        text = recommend_atom.recommend_text
        like = recommend_atom.recommend_like
        clicks = recommend_atom.recommend_clicks
        picnum = recommend_atom.recommend_picnum
        piclist = recommend_atom.recommend_piclist
        '''新增'''
        timeRange = recommend_atom.recommend_time
        catalog = recommend_atom.recommend_catalog
        recommend_dict = {'user': user,
                          'title': title,
                          'text': text,
                          'like': like,
                          'clicks': clicks,
                          'picnum': picnum,
                          'piclist': piclist,
                          "timeRange": timeRange,
                          "catalog": catalog,
                          }
        ret_dict[no] = recommend_dict
        no += 1
    print(ret_dict)
    return get_ok_response('get_recommend', ret_dict)


def delete_recommend(request):  # 删除推荐
    print("program: delete_recommend")
    reason = check_cookie_logout(request)
    if reason != 'ok':
        return get_error_response(reason)
    request_data = request.GET
    key = request_data['key']
    try:
        recommend_atom = recommend_info.objects.get(recommend_key=key)
    except recommend_info.DoesNotExist:
        print('recommend_info not exist.')
        return get_error_response('recommend_info not exist.')
    if recommend_atom.recommend_user != request.session['user_name']:
        return get_error_response('Invalid Operation!')
    num = recommend_atom.recommend_picnum
    dicts = json.loads(recommend_atom.recommend_piclist)
    for x in range(num):
        pic_name = dicts[str(x)]
        print(pic_name)
        path = os.path.join('upload', 'recommend', pic_name)
        if os.path.isfile(path):
            os.remove(path)
        recommend_pic.objects.get(picture_id=pic_name).delete()
    recommend_atom.delete()
    return get_ok_response('delete_recommend')


def download_pic(request):  # 下载图片
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


def get_recommend(request):  # 根据推荐的id获得单条推荐详细信息
    id = request.GET.get('id')
    try:
        recommend_atom = recommend_info.objects.get(recommend_key=id)
    except recommend_info.DoesNotExist:
        print('recommend not exist.')
        return get_error_response('recommend not exist.')
    title = recommend_atom.recommend_title
    text = recommend_atom.recommend_text
    piclist = recommend_atom.recommend_piclist
    user = recommend_atom.recommend_user
    like = recommend_atom.recommend_like
    picnum = recommend_atom.recommend_picnum
    '''新增'''
    timeRange = recommend_atom.recommend_time
    catalog = recommend_atom.recommend_catalog
    # if (recommend_atom.recommend_picnum > 0):
    #     pl = recommend_pic.objects.filter(picture_key=id)
    #     for pic in pl:
    #         print(pic.photo_url())
    ret_dict = {'text': text,
                'title': title,
                'piclist': piclist,
                'picnum': picnum,
                'user': user,
                'like': like,
                'rid': id,
                "timeRange": timeRange,
                "catalog": catalog,
                }
    return get_ok_response('get_recommend', ret_dict)


def user_recommend(request):  # 获得某个用户的所有推荐
    usr = request.POST.get('username')
    try:
        recommend = recommend_info.objects.filter(recommend_user=usr).order_by('-recommend_like')
    except recommend_info.DoesNotExist:
        print('recommends not exist.')
        return get_error_response('recommends not exist.')
    ret_dict = {}
    for recommend_atom in recommend:
        now_dict = {}
        key = recommend_atom.recommend_key
        now_dict['user'] = recommend_atom.recommend_user
        now_dict['title'] = recommend_atom.recommend_title
        now_dict['text'] = recommend_atom.recommend_text
        now_dict['piclist'] = recommend_atom.recommend_piclist
        now_dict['like'] = recommend_atom.recommend_like
        now_dict['picnum'] = recommend_atom.recommend_picnum
        now_dict['rid'] = key
        '''新增'''
        now_dict['timeRange'] = recommend_atom.recommend_time
        now_dict['catalog'] = recommend_atom.recommend_catalog
        ret_dict[key] = now_dict
    return get_ok_response('user_recommend', ret_dict)


def all_recommend(request):  # 获得所有用户的推荐
    try:
        recommend = recommend_info.objects.all().order_by('-recommend_like')
    except recommend_info.DoesNotExist:
        print('recommends not exist.')
        return get_error_response('recommends not exist.')
    ret_dict = {}
    for recommend_atom in recommend:
        now_dict = {}
        key = recommend_atom.recommend_key
        now_dict['user'] = recommend_atom.recommend_user
        now_dict['title'] = recommend_atom.recommend_title
        now_dict['text'] = recommend_atom.recommend_text
        now_dict['piclist'] = recommend_atom.recommend_piclist
        now_dict['like'] = recommend_atom.recommend_like
        now_dict['picnum'] = recommend_atom.recommend_picnum
        now_dict['rid'] = key
        '''新增'''
        now_dict['timeRange'] = recommend_atom.recommend_time
        now_dict['catalog'] = recommend_atom.recommend_catalog
        ret_dict[key] = now_dict
    return get_ok_response('user_recommend', ret_dict)


def like(request):  # 记录点赞
    reason = check_cookie_logout(request)
    if reason != 'ok':
        return get_error_response(reason)
    user = request.session['user_name']
    request_data = request.GET
    recommend_id = request_data['rid']
    otype = request_data['otype']
    like_atom = recommend_like.objects.filter(like_id=recommend_id, like_user=user)
    recommend_atom = recommend_info.objects.get(recommend_key=recommend_id)
    cur_like = recommend_atom.recommend_like
    if otype == 'like':
        if like_atom.count() == 0:
            '''新增'''
            recommend_like.objects.create(like_id=recommend_id, like_user=user,
                                          like_time=recommend_atom.recommend_time,
                                          like_catalog=recommend_atom.recommend_catalog)
            recommend_atom.recommend_like = cur_like + 1
            recommend_atom.save()
    elif like_atom.count() > 0:
        like_atom.delete()
        recommend_atom.recommend_like = cur_like - 1
        recommend_atom.save()
    return get_ok_response('like', {})


def click(request):
    '''新增'''
    reason = check_cookie_logout(request)
    if reason != 'ok':
        user = "admin"
    else:
        user = request.session['user_name']
    request_data = request.GET
    recommend_id = request_data['rid']
    recommend_atom = recommend_info.objects.get(recommend_key=recommend_id)
    cur_clicks = recommend_atom.recommend_clicks
    recommend_atom.recommend_clicks = cur_clicks + 1
    recommend_atom.save()
    recommend_click.objects.create(click_id=recommend_id, click_user=user,
                                   click_time=recommend_atom.recommend_time,
                                   click_catalog=recommend_atom.recommend_catalog)
    return get_ok_response('click', {})
