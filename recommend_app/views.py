import datetime
import json
import os
from collections import defaultdict
from random import random

import pytz
from PIL import Image
from django.db.models import Q
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
    return 'ok'


def cookie_to_dict(string):
    liststr = string.replace("[", "").replace("]", "").replace("\"", "\\\"").replace("\'", "\"").split("{\"user\": ")
    ans = []
    length = len(liststr)
    for i in range(1, length):
        x = "{\"user\": " + liststr[i].strip(' ').strip(']').strip(',')
        ans.append(json.loads(x))
    return ans


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
    print(request.POST)
    key = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
    title = request.POST["title"]
    text = request.POST["text"]
    piclist = request.FILES.getlist("picture")
    '''新增'''
    timeRange = request.POST["timeRange"]
    catalog = request.POST["catalog"]
    pic_num = len(piclist)
    newdict = {}
    print(piclist, pic_num)
    for i in range(pic_num):
        pic_file = piclist[i]
        print(pic_file)
        type = pic_file.name.split('.').pop()
        print(key, i, type)
        pic_file.name = '{0}-{1}.{2}'.format(key, i + 1, type)
        newdict[str(i+1)] = pic_file.name
        print(pic_file.name)
        recommend_pic.objects.create(picture_id=pic_file.name, picture_key=key, picture=pic_file)
    # request.session['recommend_piclist'][str(num)] = pic_file.name
    recommend_info.objects.create(recommend_key=key, recommend_title=title,
                                  recommend_user=request.session['user_name'],
                                  recommend_picnum=pic_num,
                                  recommend_time=timeRange, recommend_catalog=catalog,
                                  recommend_text=text, recommend_piclist=json.dumps(newdict), recommend_flag=False)
    return get_ok_response('create_recommend', {'key': str(key)})


def input_recommend(request):  # 创建原始推荐数据库
    reason = check_cookie_logout(request)
    if reason != 'ok':
        return get_error_response(reason)
    print(request.POST)
    key = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
    title = request.POST["title"]
    text = request.POST["text"]
    timeRange = request.POST["timeRange"]
    catalog = request.POST["catalog"]
    like = int(request.POST["like"])
    clicks = int(request.POST["clicks"])
    flag = int(request.POST["testflag"])
    pic_dict = request.FILES
    print(len(pic_dict))
    newdict = {}
    for pickey, value in pic_dict.items():
        type = value.name.split('.').pop()
        print(key, pickey, type)
        value.name = '{0}-{1}.{2}'.format(key, pickey, type)
        newdict[str(pickey)] = value.name
        print(value.name)
        recommend_pic.objects.create(picture_id=value.name, picture_key=key, picture=value)
        # request.session['recommend_piclist'][str(num)] = pic_file.name
    recommend_info.objects.create(recommend_key=key, recommend_title=title,
                                  recommend_user=request.session['user_name'],
                                  recommend_picnum=len(pic_dict),
                                  recommend_time=timeRange, recommend_catalog=catalog,
                                  recommend_like=like, recommend_clicks=clicks,
                                  recommend_text=text, recommend_piclist=json.dumps(newdict), recommend_flag=False)
    if flag == 1:
        for i in range(like):
            recommend_like.objects.create(like_id=key, like_user=request.session['user_name'],
                                          like_time=timeRange, like_catalog=catalog)
        for i in range(clicks):
            recommend_click.objects.create(click_id=key, click_user=request.session['user_name'],
                                           click_time=timeRange, click_catalog=catalog)
    return get_ok_response('input_recommend', {'key': str(key)})


# def edit_index(request):  # 编辑推荐
#     reason = check_cookie_logout(request)
#     if reason != 'ok':
#         return get_error_response(reason)
#     request_data = request.GET
#     key = request_data['key']
#     try:
#         recommend_atom = recommend_info.objects.get(recommend_key=key)
#     except recommend_info.DoesNotExist:
#         print('recommend_info not exist.')
#         return get_error_response('recommend_info not exist.')
#     if (recommend_atom.recommend_user != request.session['user_name']):
#         return get_error_response('Invalid Operation!')
#
#     '''新增'''
#     render_dict = {
#         "title": recommend_atom.recommend_title,
#         "text": recommend_atom.recommend_text,
#         "piclist": json.loads(recommend_atom.recommend_piclist),
#         "timeRange": recommend_atom.recommend_time,
#         "catalog": recommend_atom.recommend_catalog,
#     }
#     return render(request, 'edit.html', render_dict)


# def update_recommend(request):  # 完全的更新推荐，先删除原推荐的全部信息，再覆盖
#     reason = check_cookie_logout(request)
#     if reason != 'ok':
#         return get_error_response(reason)
#     request_data = request.POST
#     key = request_data['key']
#     try:
#         recommend_atom = recommend_info.objects.get(recommend_key=key)
#     except recommend_info.DoesNotExist:
#         print('recommend_info not exist.')
#         return get_error_response('recommend_info not exist.')
#     if recommend_atom.recommend_user != request.session['user_name']:
#         return get_error_response('Invalid Operation!')
#     num = recommend_atom.recommend_picnum
#     dicts = json.loads(recommend_atom.recommend_piclist)
#     for x in range(num):
#         pic_name = dicts[str(x)]
#         print(pic_name)
#         path = os.path.join('upload', 'recommend', pic_name)
#         if os.path.isfile(path):
#             os.remove(path)
#         recommend_pic.objects.get(picture_id=pic_name).delete()
#
#     '''新增'''
#     piclist = request.FILES.getlist("picture")
#     pic_num = len(piclist)
#     dict = {}
#     recommend_atom.recommend_title = request.POST["title"]
#     recommend_atom.recommend_text = request.POST["text"]
#     recommend_atom.recommend_picnum = pic_num
#     recommend_atom.recommend_time = request.POST["timeRange"]
#     recommend_atom.recommend_catalog = request.POST["catalog"]
#     recommend_atom.recommend_piclist = json.dumps(dict)
#
#     for i in range(pic_num):
#         pic_file = piclist[i]
#         type = pic_file.name.split('.').pop()
#         pic_file.name = '{0}-{1}.{2}'.format(key, i, type)
#         dict[str(i)] = pic_file.name
#         recommend_pic.objects.create(picture_id=pic_file.name, picture_key=key, picture=pic_file)
#     return get_ok_response('create_recommend', {'key': str(key)})


order_choose = ['recommend_like', 'recommend_key', 'recommend_clicks']


# def get_recommend_for_range_and_order(request):  # 获得排序的推荐
#     POST_INFO = request.POST
#     # POST_INFO = json.loads(request.body)
#     type_id = POST_INFO['type']  # TYPE=0: LIKES, TYPE=1: UPLOAD TIME, TYPE=2: CLICKS
#     is_all = POST_INFO['is_all']
#     user = POST_INFO['user']
#     if user == 'admin' and 'is_login' in request.session:
#         user = request.session['user_name']
#     downbound = 0
#     upbound = recommend_info.objects.filter(recommend_user=user).count()
#     if is_all == '0':
#         upbound = int(POST_INFO['upbound']) + 1
#         downbound = int(POST_INFO['downbound'])
#     ordertext = ''
#     if POST_INFO['order'] == '-':
#         ordertext += '-'
#     ordertext += order_choose[int(type_id)]
#     try:
#         recommend = recommend_info.objects.filter(recommend_user=user).order_by(ordertext)
#     except recommend_info.DoesNotExist:
#         print('recommend not exist.')
#         return get_error_response('recommend not exist.')
#     ret_dict = {}
#     for i, recommend_atom in enumerate(recommend[downbound:upbound]):
#         '''新增'''
#         recommend_dict = {'user': recommend_atom.recommend_user,
#                           'title': recommend_atom.recommend_title,
#                           'text': recommend_atom.recommend_text,
#                           'like': recommend_atom.recommend_like,
#                           'clicks': recommend_atom.recommend_clicks,
#                           'picnum': recommend_atom.recommend_picnum,
#                           'piclist': recommend_atom.recommend_piclist,
#                           "timeRange": recommend_atom.recommend_time,
#                           "catalog": recommend_atom.recommend_catalog,
#                           }
#         ret_dict[i] = recommend_dict
#     print(ret_dict)
#     return get_ok_response('get_recommend', ret_dict)


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
    for x in range(1,1+num):
        pic_name = dicts[str(x)]
        path = os.path.join('upload', 'recommend', pic_name)
        if os.path.isfile(path):
            os.remove(path)
        recommend_pic.objects.get(picture_id=pic_name).delete()
    recommend_atom.delete()
    return get_ok_response('delete_recommend')


# def download_pic(request):  # 下载图片
#     global response
#     reason = check_cookie_logout(request)
#
#     if reason != 'ok':
#         pic_path = '1111111.jpg'
#     else:
#         request_data = request.POST
#         pic_path = request_data['path']
#
#     pic = recommend_pic.objects.get(picture_id=pic_path)
#     im = Image.open(pic.picture)
#     type = pic.picture.name.split('.').pop()
#     if type in ['jpeg', 'jpg', 'jpe']:
#         response = HttpResponse(content_type='image/jpg')
#         im.save(response, "JPEG")
#     elif type == 'png':
#         response = HttpResponse(content_type='image/jpg')
#         im.save(response, "PNG")
#     elif type in ['mpeg', 'mpg', 'mpe']:
#         response = HttpResponse(content_type='image/jpg')
#         im.save(response, "PNG")
#     return response


def get_recommend(request):  # 根据推荐的id获得单条推荐详细信息
    id = request.GET.get('id')
    try:
        recommend_atom = recommend_info.objects.get(recommend_key=id)
    except recommend_info.DoesNotExist:
        print('recommend not exist.')
        return get_error_response('recommend not exist.')
    '''新增'''
    # if (recommend_atom.recommend_picnum > 0):
    #     pl = recommend_pic.objects.filter(picture_key=id)
    #     for pic in pl:
    #         print(pic.photo_url())
    ret_dict = {'text': recommend_atom.recommend_text,
                'title': recommend_atom.recommend_title,
                'piclist': recommend_atom.recommend_piclist,
                'picnum': recommend_atom.recommend_picnum,
                'user': recommend_atom.recommend_user,
                'like': recommend_atom.recommend_like,
                'rid': id,
                "timeRange": recommend_atom.recommend_time,
                "catalog": recommend_atom.recommend_catalog,
                }
    return get_ok_response('get_recommend', ret_dict)


def user_recommend(request):  # 获得某个用户的所有推荐
    usr = request.POST.get('username')
    print(usr)
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
    print(ret_dict)
    return get_ok_response('user_recommend', ret_dict)


def like_recommend(request):
    user = request.session['user_name']
    like_atom = recommend_like.objects.filter(like_user=user)
    ret_dict = {}
    for recommend in like_atom:
        now_dict = {}
        rid = recommend.like_id
        recommend_atom = recommend_info.objects.get(recommend_key=rid)
        now_dict['user'] = recommend_atom.recommend_user
        now_dict['title'] = recommend_atom.recommend_title
        now_dict['text'] = recommend_atom.recommend_text
        now_dict['piclist'] = recommend_atom.recommend_piclist
        now_dict['like'] = recommend_atom.recommend_like
        now_dict['picnum'] = recommend_atom.recommend_picnum
        now_dict['rid'] = rid
        '''新增'''
        now_dict['timeRange'] = recommend_atom.recommend_time
        now_dict['catalog'] = recommend_atom.recommend_catalog
        ret_dict[rid] = now_dict
    return get_ok_response('like_recommend', ret_dict)


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
    return get_ok_response('all_recommend', ret_dict)


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


def check_like(request):
    user = request.session['user_name']
    print(user)
    rid = request.GET['rid']
    print(rid)
    like_atom = recommend_like.objects.filter(like_id=rid, like_user=user)
    ret_dict = {}
    if like_atom.count() > 0:
        ret_dict['result'] = 'YES'
    else:
        ret_dict['result'] = 'NO'
    return get_ok_response('like', ret_dict)


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


'''新增'''
time_list = ["早餐", "中餐", "下午茶", "晚餐", "夜宵"]
catalog_list = ["包子粥", "炒菜饭", "西式餐饮", "甜点奶茶", "火锅", "烧烤"]


def getCatalog(recommend, rank):
    now_dict = {}
    for id, recommend_atom in enumerate(recommend):
        now_dict[id] = {'user': recommend_atom.recommend_user,
                        'rid': recommend_atom.recommend_key,
                        'title': recommend_atom.recommend_title,
                        'text': recommend_atom.recommend_text,
                        'like': recommend_atom.recommend_like,
                        'clicks': recommend_atom.recommend_clicks,
                        'picnum': recommend_atom.recommend_picnum,
                        'piclist': recommend_atom.recommend_piclist,
                        "timeRange": recommend_atom.recommend_time,
                        "catalog": recommend_atom.recommend_catalog,
                        }
    lists = [[], [], []]
    for _, recommend_atom in now_dict.items():
        if recommend_atom["catalog"] == rank[0]:
            lists[0].append(recommend_atom)
        elif recommend_atom["catalog"] == rank[1]:
            lists[1].append(recommend_atom)
        else:
            lists[2].append(recommend_atom)
    return lists, [len(lists[0]), len(lists[1]), len(lists[2])]


def getRecommend(user, clock, type):
    # 设置权重，判断偏好
    print(user, clock, type)
    time_dict, catalog_dict = defaultdict(int), defaultdict(int)
    for item in time_list:
        time_dict[item]=0
    for item in catalog_list:
        catalog_dict[item]=0
    like_recommend = recommend_like.objects.filter(like_user=user)
    click_recommend = recommend_click.objects.filter(click_user=user)
    #print(len(like_recommend),len(click_recommend))
    for like_item in like_recommend:  # 检索用户点赞数据（与点击数据重复，相当于加权）
        time_dict[like_item.like_time] += 1
        catalog_dict[like_item.like_catalog] += 1
    now = datetime.datetime.now()
    now = now.replace(tzinfo=pytz.timezone('UTC'))
    for click_item in click_recommend:  # 检索十五天内数据点击
        cmp = click_item.click_date + datetime.timedelta(days=15)
        if now < cmp:
            time_dict[click_item.click_time] += 1
            catalog_dict[click_item.click_catalog] += 1
    time_dict = sorted(time_dict.items(), key=lambda x: (x[1], x[0]), reverse=True)
    catalog_dict = sorted(catalog_dict.items(), key=lambda x: (x[1], x[0]), reverse=True)
    print(time_dict)
    print(catalog_dict)
    # 根据 时间4:1-种类3:1:1 或种类4:1-时间3:1:1
    # catalog_key = list(catalog_dict.keys())[0:1]
    catalog_key = [catalog_dict[0][0], catalog_dict[1][0]]
    time_key = [clock, time_dict[0][0] if clock != time_dict[0][0] else time_dict[1][0]]
    if type == "timeRange":
        recommend_notnow = recommend_info.objects.filter(~Q(recommend_time=clock)).order_by("-recommend_like")
        recommend_now = recommend_info.objects.filter(recommend_time=clock).order_by("-recommend_like")
        rank = catalog_key
    else:
        recommend_notnow = recommend_info.objects.filter(~Q(recommend_catalog=catalog_dict[0].key())).order_by(
            "-recommend_catalog")
        recommend_now = recommend_info.objects.filter(recommend_catalog=catalog_dict[0].key()).order_by(
            "-recommend_catalog")
        rank = time_key
    # 规整数据为列表，并按照比例随机排序
    # print(len(recommend_now), len(recommend_notnow))
    list0, len0 = getCatalog(recommend_now, rank)
    list1, len1 = getCatalog(recommend_notnow, rank)
    rawlist, lenlist, anslist = list0 + list1, len0 + len1, []
    length0, lenght1 = len0[0] + len0[1] + len0[2], len1[0] + len1[1] + len1[2]
    index, indexi, indexij = 0, 0, [0, 0, 0, 0, 0, 0]
    for ii in range(length0 + lenght1):
        x, y = random(), random()
        index = 0 if x < 0.8 else 1
        if y < 0.6:
            indexi = index * 3
        elif y < 0.8:
            indexi = index * 3 + 1
        else:
            indexi = index * 3 + 2
        while indexi < 6 and indexij[indexi] >= lenlist[indexi]:
            indexi += 1

        if indexi < 6:
            anslist.append(rawlist[indexi][indexij[indexi]])
            # print(index, indexi, indexij[indexi])
            # print(ii,rawlist[indexi][indexij[indexi]])
        indexij[indexi] += 1
        # print(indexij)
    # 返回排序后的值
    return anslist


def get_recommend_for_type(request):  # 获得排序的推荐
    print("programme: get_recommend_for_type")
    POST_INFO = request.POST
    type = POST_INFO['type']  # 时间范围或者种类
    clock = POST_INFO['time']  # 当前时间
    downbound, upbound = int(POST_INFO['downbound']), int(POST_INFO['upbound']) + 1
    reason = check_cookie_logout(request)
    if reason != 'ok':
        recommends = recommend_info.objects.filter(recommend_time=clock).order_by("-recommend_like")
        ret_dict = {}
        for i, recommend_atom in enumerate(recommends[downbound:upbound]):
            now_dict = {}
            now_dict['user'] = recommend_atom.recommend_user
            now_dict['title'] = recommend_atom.recommend_title
            now_dict['text'] = recommend_atom.recommend_text
            now_dict['piclist'] = recommend_atom.recommend_piclist
            now_dict['like'] = recommend_atom.recommend_like
            now_dict['picnum'] = recommend_atom.recommend_picnum
            now_dict['rid'] = recommend_atom.recommend_key
            '''新增'''
            now_dict['timeRange'] = recommend_atom.recommend_time
            now_dict['catalog'] = recommend_atom.recommend_catalog
            ret_dict[str(i+1)] = now_dict
        return get_ok_response('get_recommend', ret_dict)

    user = request.session['user_name']  # 用户名
    # 未筛选过/ 筛选另一种类/ 刷新
    if 'typeRange' not in request.session or type != request.session["rangeType"] or POST_INFO['refresh'] == '1':
        request.session['typeRange'] = str(getRecommend(user, clock, type))
        request.session["rangeType"] = type
    # 读取cookie中保存的之前排好序的推荐
    recommend = cookie_to_dict(request.session['typeRange'])
    if int(POST_INFO['downbound']) >= len(recommend):
        reason = "out of index"
        print(reason)
        return get_error_response(reason)

    downbound, upbound = int(POST_INFO['downbound']), min(len(recommend), int(POST_INFO['upbound']) + 1)
    
    # 返回合法的上下界之间的所有推荐
    ret_dict = {}
    for i, recommend_atom in enumerate(recommend[downbound:upbound]):
        now_dict = recommend_atom
        ret_dict[str(i+1)] = now_dict
        # print(now_dict)

    return get_ok_response('get_recommend', ret_dict)

def get_liked_recommend(request):
    reason = check_cookie_logout(request)
    if (reason != 'ok'):
        return get_error_response(reason)
    user = request.session['user_name']
    liked_recommends = recommend_like.objects.filter(like_user=user)
    ret_dict = {}
    for i,lr in enumerate(liked_recommends):
        rid = lr.like_id
        recommends = recommend_info.objects.filter(recommend_key=rid)
        for recommend_atom in recommends:
            now_dict = {}
            now_dict['user'] = recommend_atom.recommend_user
            now_dict['title'] = recommend_atom.recommend_title
            now_dict['text'] = recommend_atom.recommend_text
            now_dict['piclist'] = recommend_atom.recommend_piclist
            now_dict['like'] = recommend_atom.recommend_like
            now_dict['picnum'] = recommend_atom.recommend_picnum
            now_dict['rid'] = recommend_atom.recommend_key
            '''新增'''
            now_dict['timeRange'] = recommend_atom.recommend_time
            now_dict['catalog'] = recommend_atom.recommend_catalog
            ret_dict[str(i+1)] = now_dict
    return get_ok_response('get_recommend', ret_dict)

