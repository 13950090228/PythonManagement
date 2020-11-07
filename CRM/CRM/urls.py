"""CRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from app01 import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('get_valid_img/',views.get_valid_img),
    path('reg/', views.reg),
    path('', views.index),
    path('customers/list/', views.Customers.as_view(),name='customers_list'),
    path('mycustomers/', views.Customers.as_view(),name="mycustomers"),
    path('logout/', views.logout),
    path('customer/add/', views.AddCustomers.as_view(),name='addcustomer'),
    path('consult_record/',views.ConsultRecordView.as_view(),name='consultrecord'),
    re_path('customer/edit/(\d+)', views.EditCustomers.as_view(),name='editcustomer'),
    path('consult_record/add/',views.AddConsultRecord.as_view(),name='addconsultrecord'),
#

]
