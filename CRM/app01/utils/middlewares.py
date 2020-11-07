from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render,HttpResponse,redirect
class LoginMiddleWaer(MiddlewareMixin):

    def process_request(self,request):
        if request.path in ['/login/','/reg/','/get_valid_img/']:
            return None

        if not request.user.id:

            return redirect('/login/')
