from django.urls import path

from ajax import views

app_name = 'ajax'
urlpatterns = [
    path('check_email/', views.check_email, name='email'),
    path('check_phone/', views.check_phone, name='checkPhone'),
    path('send_email_msg/', views.send_email_msg, name='sendEmail'),
    path('check_email_code/', views.check_email_code, name='checkEmailCode'),
    path('check_captcha/', views.check_captcha, name='captcha'),
]
