from django.shortcuts import render,HttpResponse,redirect
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO
import random
from django.urls import reverse
from django import forms
from django.http import JsonResponse
from django.contrib import auth
from app01.models import UserInfo,Customer,ConsultRecord
from django.core.exceptions import ValidationError
from django.forms import widgets
import re
import django
from django.db.models import Q,F
from app01.form import UserForm
from app01.utils.page import Pagination
from django.contrib.auth.decorators import login_required
import copy
from django.views import View
# Create your views here.


class Customers(View):

    def get(self,request):

        if reverse("customers_list") == request.path:
            label = "全部客户"
            from django.utils.functional import SimpleLazyObject

            if (isinstance(request.user, SimpleLazyObject)) and str(request.user) == 'lyq':
                customers_list = Customer.objects.all()
            else:

                customers_list = Customer.objects.filter(consultant__isnull=True)
        else:
            label = "我的客户"
            customers_list = Customer.objects.filter(consultant=request.user)

            # search过滤
        val = request.GET.get('val')
        file = request.GET.get('file')
        if val:
            ret = Q()
            ret.children.append((file + "__contains", val))
            customers_list = customers_list.filter(ret)
            # customers_list=customers_list.filter(Q(name__contains=val)|Q(qq__contains=val)|Q(phone__contains=val))

        current_page_num = request.GET.get("page")
        pagination = Pagination(current_page_num, customers_list.count(), request, per_page_num=10)
        customers_list = customers_list[pagination.start:pagination.end]

        path = request.path

        next = "?next=%s"%(path)

        return render(request, "customers_list.html", locals())

    def post(self,request):
        data = request.POST.getlist('select_pk_list')
        func_str = request.POST.get("action")

        if not hasattr(self,func_str):
            return HttpResponse("非法输入")
        else:
            func = getattr(self,func_str)
            func(request,data)
            ret = self.get(request)
        return ret

    def patch_delete(self,request,data):
        Customer.objects.filter(pk__in=data).delete()

    def Public_to_private(self,request,data):
        Customer.objects.filter(pk__in=data).update(consultant=request.user)

    def Private_to_public(self,request,data):
        Customer.objects.filter(pk__in=data).update(consultant=None)


class CustomerModelForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields="__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from multiselectfield.forms.fields import MultiSelectFormField
        for filed in self.fields.values():
            if not isinstance(filed,MultiSelectFormField):
                filed.widget.attrs.update({"class": "form-control"})
            # filed.error_messages = {"required": "此项不能为空"}

class ConsultRecordModelForm(forms.ModelForm):
    class Meta:
        model=ConsultRecord
        fields="__all__"
        exclude = ["delete_status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.forms.fields import BooleanField
        for filed in self.fields.values():

            if not isinstance(filed,BooleanField):
                filed.widget.attrs.update({"class": "form-control"})

class AddCustomers(View):
    def get(self,request):
        form = CustomerModelForm()
        return render(request,"customer_add.html",locals())

    def post(self,request):
        form = CustomerModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/customers/list/')
        else:
            return render(request, "customer_add.html", locals())

class EditCustomers(View):

    def get(self,request,id):

        edit_obj = Customer.objects.filter(pk=id)[0]
        form = CustomerModelForm(instance=edit_obj)
        return render(request,"customer_add.html",locals())

    def post(self,request,id):
        edit_obj = Customer.objects.filter(pk=id)[0]

        form = CustomerModelForm(request.POST,instance=edit_obj)
        if form.is_valid():
            form.save()

            return redirect(request.GET.get("next"))
        else:
            return render(request, "customer_edit.html", locals())

class ConsultRecordView(View):
    def get(self,request):
        pk = request.GET.get("customer_id")
        print(pk)
        # consult_list = ConsultRecord.objects.all()
        consult_list = ConsultRecord.objects.filter(consultant=request.user)
        if pk:
            consult_list = consult_list.filter(customer_id=pk)


        path = request.path

        next = "?next=%s" % (path)
        return render(request,'consultrecord.html',locals())

class AddConsultRecord(View):
    def get(self,request):
        form = ConsultRecordModelForm()
        return render(request, "consultrecord_add.html", locals())

    def post(selfself,request):

        form = ConsultRecordModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/consult_record/')
        else:
            return render(request, "consultrecord_add.html", locals())

def login(request):
    if request.is_ajax():
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        validcode = request.POST.get("validcode")
        response = {"user":None,"error_msg":""}


        if validcode.upper() == request.session.get("keep_char").upper():
            user_obj = auth.authenticate(username=user, password=pwd)

            if user_obj:
                auth.login(request,user_obj)
                response["user"] = user

                return JsonResponse(response)
            else:

                response["error_msg"] = "用户名或密码错误"
                return JsonResponse(response)
        else:

            response["error_msg"]="验证码错误"
            return JsonResponse(response)

    else:

        return render(request,"login.html")

def get_valid_img(request):
    #方式一 获取指定图片
    # with open("static/img/1107.jpg","rb") as f:
    #     data = f.read()

    #方式二 获取验证码
    def get_random_color():
        import random
        return(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    # img = Image.new("RGB",(150,35),get_random_color())
    #
    # f = open('static/img/vaild.png','wb')
    # img.save(f,'png')
    # with open("static/img/vaild.png","rb") as f:
    #     data = f.read()

    #方式三
    # img = Image.new("RGB", (150, 35), get_random_color())
    # f=BytesIO()
    # img.save(f," png")
    # data = f.getvalue()

    #方式四 完善文本
    #
    # img = Image.new("RGB", (150, 35), get_random_color())
    # draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype("static/font/kumo.ttf",32)
    # draw.text((25,0),"python",get_random_color(),font=font)
    # f=BytesIO()
    # img.save(f,"png")
    # data = f.getvalue()

    #方式五
    img = Image.new("RGB", (120, 35), get_random_color())
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("static/font/kumo.ttf",32)


    keep_char=""
    for i in range(4):
        random_num = str(random.randint(0,9))
        random_lowalf = chr(random.randint(97,122))
        random_upperalf = chr(random.randint(65,90))
        random_char = random.choice([random_num,random_lowalf,random_upperalf])
        draw.text((i*28,0),random_char,get_random_color(),font=font)
        keep_char+=random_char

    width=120
    height=35
    for i in range(8):
        x1=random.randint(0,width)
        x2=random.randint(0,width)
        y1=random.randint(0,height)
        y2=random.randint(0,height)
        draw.line((x1,y1,x2,y2),fill=get_random_color())

    for i in range(30):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    print(keep_char)
    f=BytesIO()
    img.save(f,"png")
    data = f.getvalue()

    request.session['keep_char']=keep_char
    return HttpResponse(data)

def reg(request):
    if request.is_ajax():
        print(request.POST)
        res = {"user":None,"err_msg":None}
        form = UserForm(request.POST)

        if form.is_valid():
            res["user"] = form.cleaned_data.get("user")
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            gender = form.cleaned_data.get("gender")
            UserInfo.objects.create_user(username=user,password=pwd,email=email,gender=gender)
            print("正确数据：",form.cleaned_data)
        else:
            res["err_msg"] = form.errors

        return JsonResponse(res)
    else:
        form = UserForm()
        return render(request,"reg.html",locals())



# def loginrequest(func):
#     def inner(request):
#         if not request.user.id:
#             return redirect('/login/')
#         else:
#
#             return func(request)
#     return inner

# @login_required
def index(request):

    return render(request,"index.html")

# @loginrequest
def customers(request):
    print(copy.deepcopy(request.GET))
    if reverse("customers_list") == request.path:
        customers_list = Customer.objects.all()
    else:
        customers_list = Customer.objects.filter(consultant=request.user)

    #search过滤
    val = request.GET.get('val')
    file = request.GET.get('file')
    if val:
        ret = Q()
        ret.children.append((file+"__contains",val))
        customers_list = customers_list.filter(ret)
        # customers_list=customers_list.filter(Q(name__contains=val)|Q(qq__contains=val)|Q(phone__contains=val))

    current_page_num = request.GET.get("page")
    pagination = Pagination(current_page_num,customers_list.count(),request,per_page_num=10)
    customers_list = customers_list[pagination.start:pagination.end]

    return render(request,"customers_list.html",locals())

def logout(request):
    auth.logout(request)

    return redirect('/login/')