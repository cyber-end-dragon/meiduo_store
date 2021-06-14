import re

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django import http

from users.models import User
from meiduo_mall.utils.response_code import RETCODE
from django.db import DatabaseError
from django.contrib.auth import login
# Create your views here.


class UsernameCountView(View):

    def get(self, request, username):

        count = User.objects.filter(username=username).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})



class RegisterView(View):

    def get(self, request):

        return render(request, 'register.html')

    def post(self,request):

        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        allow = request.POST.get('allow')

        if not all([username,password,password2,mobile,allow]):
            return http.HttpResponseForbidden('缺少参数 Missing Parameter')
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        if not re.match(r'^1[3-9]\d{9}$',mobile):
            return http.HttpResponseForbidden('您输入的手机号格式不正确')
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')

        # return render(request, 'register.html', {'register_errmsg': '注册失败'})

        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg':'注册失败'})

        login(request,user)

        # return http.HttpResponse('注册成功')
        return redirect(reverse('contents:index'))

