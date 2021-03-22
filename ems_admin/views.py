import hashlib
import random
import string

from captcha.image import ImageCaptcha
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from ems_admin.getsalt import get_salt
from ems_admin.models import User


# Create your views here.

# 转发登录视图为login.html
def login(request):
    # 设置前端弹出提示信息
    info = None
    if request.session.get('info'):
        # 获取前端提示信息到info
        info = request.session.get('info')
        # 删除session提示信息，只用一次用后清空
        del request.session['info']
    # 获取COOKIE
    if request.COOKIES.get('username'):
        # 设置登录成功重定向的URL
        response = redirect('/emplist/')
        # 获取本地的COOKIES数据
        username = request.COOKIES.get('username')
        password = request.COOKIES.get('password')
        try:
            # 对数据库进行查询
            # if '@' in username:
            #     user = User.objects.get(email=username, password=password)
            # else:
            #     user = User.objects.get(phone=username, password=password)
            user = User.objects.get(Q(email=username, password=password) | Q(phone=username, password=password))
            # 登录成功后语句
            if user:
                request.session['name'] = user.name
                request.session['check_login'] = True
                # request.session['info'] = '登录成功！'
                return response
            # 登录失败后回到本页
        except Exception as e:
            print(e)
            request.session['info'] = '登录失败！'
            return redirect('/')
    if request.session.get('check_login'):
        return redirect('/emplist/')
    return render(request, 'login.html', {'info': info})


# 登录检查
def check(request):
    response = redirect('/emplist/')
    username = request.POST.get('username')
    password = request.POST.get('password')
    # print(password.hexdigest())
    # captcha = request.POST.get('number')
    # 验证码比对
    # if request.session.get('code').lower() != captcha.lower():
    #     request.session['info'] = '验证码输入错误!'
    #     return redirect('/')
    # else:
    #     del request.session['code']
    try:
        salt = User.objects.get(Q(email=username) | Q(phone=username)).salt
        # print(salt, type(salt))
        password = hashlib.md5(password.encode() + salt.encode())
        # if '@' in username:
        #     user = User.objects.get(email=username, password=password.hexdigest())
        # else:
        #     user = User.objects.get(phone=username, password=password.hexdigest())
        user = User.objects.get(
            Q(email=username, password=password.hexdigest()) | Q(phone=username, password=password.hexdigest()))
        # print(user)
        if user:
            request.session['name'] = user.name
            # 登录状态获取
            request.session['check_login'] = True
            # request.session['info'] = '登录成功！'
            if request.POST.get('check_login'):
                # 选择免登录后存储账号密码到COOKIE
                response.set_cookie("username", username, max_age=3600 * 24 * 7)
                response.set_cookie("password", password.hexdigest(), max_age=3600 * 24 * 7)
            return response
    except Exception as e:
        print(e)
        request.session['info'] = '登录失败！'
        return redirect('/')


# 注册
def register(request):
    info = None
    if request.session.get('info'):
        info = request.session.get('info')
        del request.session['info']

    if request.session.get('check_login'):
        return redirect('/emplist/')
    return render(request, 'regist.html', {'info': info})


# 注册插入
def insert(request):
    if request.session.get('info'):
        del request.session['info']
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    password = request.POST.get('password')
    salt = get_salt()
    password = hashlib.md5(password.encode() + salt.encode())
    # print(password.hexdigest())
    name = request.POST.get('name')
    sex = request.POST.get('sex')
    # captcha = request.POST.get('number')
    # 验证码比对
    # if request.session.get('code').lower() != captcha.lower():
    #     request.session['info'] = '验证码输入错误!'
    #     return redirect('/register/')
    # else:
    #     del request.session['code']
    try:
        with transaction.atomic():
            try:
                id = User.objects.values('id').last()['id']
            except:
                id = 0
            user = User.objects.create(id=id + 1, email=email, phone=phone, password=password.hexdigest(), name=name,
                                       sex=sex, salt=salt)
            if user:
                del request.session['sendCodeTime']
                request.session['info'] = '注册成功，您可以进行登录了!'
                return redirect('/login/')
    except Exception as e:
        print(e)
        # if (str(e).find('username')):
        #     request.session['info'] = '用户名已存在!'
        # else:
        #     request.session['info'] = '注册失败!'
        request.session['info'] = '注册失败!'
        return redirect('/register/')


# 验证码视图
def get_captcha(request):
    # 声明一个图片验证码对象
    image = ImageCaptcha()
    # 生成随机的4位验证码
    code = random.sample(string.ascii_letters + string.digits, 4)
    code = ''.join(code)
    print(code)
    request.session['code'] = code
    # 将验证码写入图片中
    data = image.generate(code)
    return HttpResponse(data, 'image/png')


# 退出登录
def exit(request):
    # 清空登录状态的SESSION
    request.session.flush()
    # 检查COOKIES无法退出
    if request.COOKIES.get('username'):
        request.session['info'] = '七天免登录已开启，无法退出登录!'
        return redirect('/emplist/')
    return redirect('/')
