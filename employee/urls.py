from django.urls import path

from employee import views
urlpatterns = [
    path('emplist/', views.emplist),
    path('del_data/', views.del_data),
    path('addemp/', views.add_emp),
    path('add/', views.add),
    path('update/', views.update),
    path('update_data/', views.update_data),
]
