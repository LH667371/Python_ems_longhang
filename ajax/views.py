import os
import random
import string
import time

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect
from redis import Redis

from ems_admin.views import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ems_proj.settings')

redis = Redis(host="192.168.106.134", port=7000)


# Create your views here.
def check_email(request):
    email = request.POST.get('email')
    if email == '':
        return HttpResponse("<span style='color:green; font-size:12px;'></span>")
    if User.objects.filter(email=email):
        return HttpResponse("<span style='color:red; font-size:12px;'>该邮箱已注册！</span>")
    else:
        return HttpResponse("<span style='color:green; font-size:12px;'>邮箱可用!</span>")


def check_phone(request):
    phone = request.POST.get('phone')
    if phone == '':
        return HttpResponse("<span style='color:green; font-size:12px;'></span>")
    if User.objects.filter(phone=phone):
        return HttpResponse("<span style='color:red; font-size:12px;'>该手机号已注册！</span>")
    else:
        return HttpResponse("<span style='color:green; font-size:12px;'>手机号可用!</span>")


def check_captcha(request):
    captcha = request.POST.get('captcha')
    # print(captcha)
    if captcha.lower() == request.session.get('code').lower():
        del request.session['code']
        return HttpResponse("<span style='color:green; font-size:12px;'>&nbsp;验证码输入正确</span>")
    elif captcha == '':
        return HttpResponse("<span style='color:red; font-size:12px;'></span>")
    else:
        return HttpResponse("<span style='color:red; font-size:12px;'>&nbsp;验证码错误，请重新输入</span>")


def send_email_msg(request):
    # print(time.time())
    # if not request.session.get('sendCodeTime'):
    try:
        if not redis.get('emailCode'):
            request.session['sendCodeTime'] = time.time()
            email = request.POST.get('email')
            emailCode = random.sample(string.ascii_letters + string.digits, 4)
            emailCode = ''.join(emailCode)
            # request.session['emailCode'] = emailCode
            status = send_mail(
                '这是一封注册邮件',  # 邮件的主题
                '验证码是： {} ，此验证码有效期为15分钟！'.format(emailCode),  # 邮件内容
                '773426798@qq.com',  # 邮件的发送方，需要与配置中的一致
                [email],  # 邮件的接收方  可以写多个
            )
            # print(status)
            if status:
                redis.set('emailCode', emailCode, 900)
                request.session['email' + emailCode.lower()] = email
                return HttpResponse("发送成功！请在15分钟内使用")
            else:
                return HttpResponse("发送失败！")
        else:
            # print(request.session.get('sendCodeTime'), type(request.session.get('sendCodeTime')))
            if request.session.get('sendCodeTime') + 60 <= time.time():
                request.session['sendCodeTime'] = time.time()
                email = request.POST.get('email')
                if redis.get('emailCode'):
                    emailCode = redis.get('emailCode').decode()
                else:
                    emailCode = random.sample(string.ascii_letters + string.digits, 4)
                    emailCode = ''.join(emailCode)
                    # request.session['emailCode'] = emailCode
                    redis.set('emailCode', emailCode, 900)
                status = send_mail(
                    '这是一封注册邮件',  # 邮件的主题
                    '验证码是： {} ，此验证码剩余有效期为{}分钟！'.format(emailCode, int(redis.ttl('emailCode')/60)+1),  # 邮件内容
                    '773426798@qq.com',  # 邮件的发送方，需要与配置中的一致
                    [email],  # 邮件的接收方  可以写多个
                )
                # print(status)
                if status:
                    request.session['email' + emailCode.lower()] = email
                    return HttpResponse("发送成功！该验证码还可以在{}分钟内使用".format(int(redis.ttl('emailCode')/60)+1))
                else:
                    return HttpResponse("发送失败！")
            else:
                return HttpResponse(
                    "60秒内只能发送一封，请在{}秒后获取！".format(int(request.session.get('sendCodeTime') + 60 - time.time())))
    except Exception as e:
        print(e)
        redis.delete('emailCode')
        del request.session['sendCodeTime']
        return redirect('/send_email_msg/')


def check_email_code(request):
    emailCode = request.POST.get('emailCode')
    email = request.POST.get('email')
    if not redis.get('emailCode'):
        return HttpResponse("<span style='color:red; font-size:12px;'>&nbsp;请发送验证码！</span>")
    if request.session.get('email' + emailCode.lower()) == email:
        if redis.get('emailCode').decode().lower() == emailCode.lower():
            return HttpResponse("<span style='color:green; font-size:12px;'>&nbsp;输入正确！</span>")
        else:
            return HttpResponse("<span style='color:red; font-size:12px;'>&nbsp;输入错误！</span>")
    else:
        return HttpResponse("<span style='color:red; font-size:12px;'>&nbsp;请发送验证码！</span>")
