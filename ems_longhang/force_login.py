from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class MyMiddleWare(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        print('init强制登录！')

    def process_request(self, request):
        # 某些视图不需要强制登录，直接放行即可
        pass_url = ['/login/', '/check/', '/register/', '/insert/', '/', '/get_captcha/', '/check_email/',
                    '/check_captcha/', '/send_email_msg/', '/check_email_code/', '/check_phone/']
        # 如果你请求的路径，在放行的url列表中，不需要登录标识，直接可以访问
        if request.path in pass_url:
            pass
        elif 'static' in request.path:
            # print(request.path)
            pass
        else:
            # print(request.path)
            login_check = request.session.get('check_login')
            if login_check:
                pass
            else:
                request.session['info'] = '请先进行登录！'
                return redirect('/')
