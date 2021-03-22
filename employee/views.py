import os
import uuid

from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect

# Create your views here.
from employee.models import Employee, Department


def emplist(request):
    info = None
    if request.session.get('info'):
        info = request.session.get('info')
        del request.session['info']
    name = request.session.get('name')
    data = Employee.objects.all()
    number = int(request.GET.get('number', 1))
    # TODO 由于数据过多，我们对数据进行分页展示
    # 1.初始化一个分页对象
    paginator = Paginator(object_list=data, per_page=5)
    # print(paginator.per_page)  # 获取所有页面的对象总数，也就是data的个数
    # print(paginator.num_pages)  # 获取总页数
    # print(paginator.page_range)  # 返回页面可以遍历的范围

    # 2.分页器对象的方法
    page = paginator.page(number)  # 调用page方法，获取某一页面的对象
    # print(page.object_list)  # 返回页面的所有对象
    # print(page.number)  # 页码
    # print(page.paginator)
    return render(request, 'emplist.html', {'info': info, 'name': name, 'page': page})


def del_data(request):
    number = request.GET.get('number')
    # print(number)
    if request.GET.get('id'):
        # 在删除数据库时对图片进行删除
        os.remove(
            os.getcwd() + '/media/' + list(Employee.objects.filter(id=request.GET.get('id')).values('head_pic'))[0][
                'head_pic'])
        Employee.objects.get(id=request.GET.get('id')).delete()
    return redirect('/emplist/?number=' + number)


def add_emp(request):
    number = request.GET.get('number')
    info = None
    if request.session.get('info'):
        info = request.session.get('info')
        del request.session['info']
    dept_list = Department.objects.all()
    return render(request, 'addEmp.html', {'info': info, 'department': dept_list, 'number': number})


def add(request):
    number = request.GET.get('number')
    try:
        id = Employee.objects.values('id').last()['id']
    except:
        id = 0
    name = request.POST.get('name')
    salary = request.POST.get('salary')
    age = request.POST.get('age')
    sex = request.POST.get('sex')
    birthday = request.POST.get('birthday')
    dept_id = request.POST.get('department')
    image = request.FILES.get('image')
    # 获取拓展名
    extend = os.path.splitext(image.name)[1]
    # 对上传图像的名字进行唯一化
    image.name = str(uuid.uuid4()) + extend
    try:
        with transaction.atomic():
            add = Employee.objects.create(id=id + 1, name=name, salary=salary, age=age, sex=sex, birthday=birthday,
                                          head_pic=image, depart_id=dept_id)
            if add:
                request.session['info'] = '添加成功'
                return redirect('/emplist/?number=' + number)
            else:
                request.session['info'] = '添加失败'
                return redirect('/addemp/')
    except Exception as e:
        print(e)
        request.session['info'] = '注册失败！'
        return redirect('/addemp/')


# 数据更新页面视图
def update(request):
    number = request.GET.get('number')
    info = None
    if request.session.get('info'):
        info = request.session.get('info')
        del request.session['info']
    # 获取前端需要更新的id
    id = request.GET.get('id')
    dept_list = Department.objects.all()
    data = Employee.objects.filter(id=id)[0]
    return render(request, 'updateEmp.html', {'department': dept_list, 'data': data, 'info': info, 'number': number})


# 数据更新视图
def update_data(request):
    number = request.GET.get('number')
    # print(number)
    id = request.POST.get('id')
    name = request.POST.get('name')
    salary = request.POST.get('salary')
    age = request.POST.get('age')
    sex = request.POST.get('sex')
    birthday = request.POST.get('birthday')
    dept_id = request.POST.get('department')
    image = request.FILES.get('image')
    # print(id, name, salary, age, image, birthday)
    # 获取游标
    emp = Employee.objects.get(id=id)
    # 对比数据有无更新
    if emp.name == name and emp.salary == float(
            salary) and emp.age == age and image is None and emp.sex == sex and birthday == '' and emp.depart_id == int(dept_id):
        request.session['info'] = '您没有进行修改！'
        # return redirect('/emplist/')
        return redirect('/emplist/?number=' + number)
    else:
        try:
            with transaction.atomic():
                emp.name = name
                emp.salary = salary
                emp.age = age
                emp.sex = sex
                if birthday:
                    emp.birthday = birthday
                emp.depart_id = dept_id
                # image不为空时
                if image:
                    # 获取拓展名
                    extend = os.path.splitext(image.name)[1]
                    # 对上传图像的名字进行唯一化
                    image.name = str(uuid.uuid4()) + extend
                    # 如果有上传图片，则删除服务器原来的图片
                    os.remove(
                        os.getcwd() + '/media/' +
                        list(Employee.objects.filter(id=request.POST.get('id')).values('head_pic'))[0][
                            'head_pic'])
                    emp.head_pic = image
                # 保存以上修改数据
                emp.save()
                request.session['info'] = '修改成功！'
                # return redirect('/emplist/')
                return redirect('/emplist/?number=' + number)
        except Exception as e:
            print(e)
            request.session['info'] = '修改失败！'
            return redirect('/update/')
