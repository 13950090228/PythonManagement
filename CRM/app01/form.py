from django.core.exceptions import ValidationError
from django import forms
from django.forms import widgets
from app01.models import UserInfo
import re

class UserForm(forms.Form):
    user = forms.CharField(min_length=2,max_length=15,
                           label='用户名',
                           widget=widgets.TextInput(),
                           error_messages = {"required": "该字段不能为空","min_length":"不能少于5个字符"},
                           )
    gender = forms.ChoiceField(choices=((1, "男"),(0, "女")),
                                label='性别',

                                )
    pwd = forms.CharField(min_length=5, max_length=15,
                          label='密码',
                          widget=widgets.PasswordInput(),
                          error_messages={"required": "该字段不能为空","min_length":"不能少于5个字符"},
                          )
    r_pwd = forms.CharField(min_length=5, max_length=15,
                            label='确认密码',
                            widget=widgets.PasswordInput(),
                            error_messages={"required": "该字段不能为空","min_length":"不能少于5个字符"},
                            )
    email = forms.EmailField(min_length=5,
                             label='邮箱',
                             error_messages={"invalid": "输入正确的邮箱格式！","required": "该字段不能为空","min_length":"不能少于5个字符"},
                             )

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for filed in self.fields.values():
            filed.widget.attrs.update({"class":"form-control"})

    def clean_user(self):
        val = self.cleaned_data.get("user")
        user = UserInfo.objects.filter(username=val).first()
        if user:
            raise ValidationError("用户已存在!")
        else:
            return val

    def clean_pwd(self):
        val = self.cleaned_data.get("pwd")
        if val.isdigit():
            raise ValidationError("密码不能为纯数字!")
        else:
            return val

    def clean_r_pwd(self):
        r_val = self.cleaned_data.get("r_pwd")
        val = self.cleaned_data.get("pwd")
        if r_val and val and r_val!=val:
            # raise ValidationError("两次密码不一致!")
            self.add_error('r_pwd',ValidationError("两次密码不一致!"))
        else:

            return val

    def clean_email(self):
        val = self.cleaned_data.get("email")
        if re.search("\w+@163.com", val):
            return val
        else:
            raise ValidationError("邮箱必须是163邮箱！")

