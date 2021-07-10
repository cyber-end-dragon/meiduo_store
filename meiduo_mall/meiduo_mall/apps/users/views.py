import re

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django import http
from django_redis import get_redis_connection

from users.models import User
from meiduo_mall.utils.response_code import RETCODE
from django.db import DatabaseError
from django.contrib.auth import login, authenticate
# Create your views here.


class LoginView(View):

    # 提供用户登陆页面
    def get(self, request):

        return render(request, 'login.html')

    # 实现用户登陆逻辑
    def post(self, request):
        # 接收参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')

        # 校验参数
        if not all([username, password]):
            return http.HttpResponseForbidden('缺少参数')
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 认证用户
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'login.html', {'account_errmsg': '账号或密码错误'})
        # 状态保持
        login(request, user)
        if remembered != 'on':
            # 没有记住登陆： 状态保持在浏览器会话结束后销毁
            request.session.set_expiry(0)
        else:
            # 记住登陆： 状态默认保持周期为两周
            request.session.set_expiry(None)
        # 响应结果
        return redirect(reverse('contents:index'))
        pass


class MobileCountView(View):
    # 手机号重复注册
    def get(self, request, mobile):

        count = User.objects.filter(mobile=mobile).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})


class UsernameCountView(View):
    # 用户名重复注册
    def get(self, request, username):

        count = User.objects.filter(username=username).count()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'count': count})


class RegisterView(View):

    def get(self, request):

        return render(request, 'register.html')

    def post(self, request):

        # 接收参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        sms_code_client = request.POST.get('sms_code')
        allow = request.POST.get('allow')

        # 校验参数
        if not all([username, password, password2, mobile, allow]):
            return http.HttpResponseForbidden('缺少参数 Missing Parameter')
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('您输入的手机号格式不正确')
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')

        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if sms_code_server is None:
            return render(request, 'register.html', {'sms_code_errmsg': '短信验证码失效'})
        if sms_code_client != sms_code_server.decode():
            return render(request, 'register.html', {'sms_code_errmsg': '输入短信验证码有误'})

        # return render(request, 'register.html', {'register_errmsg': '注册失败'})

        # 保存数据,实现状态保持
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': '注册失败'})
        login(request, user)

        # return http.HttpResponse('注册成功')
        return redirect(reverse('contents:index'))
