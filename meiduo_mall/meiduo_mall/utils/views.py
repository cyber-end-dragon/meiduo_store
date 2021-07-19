from django.contrib.auth.mixins import LoginRequiredMixin
from django import http
from meiduo_mall.utils.response_code import RETCODE

class LoginRequiredJsonMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        return http.JsonResponse({'code': RETCODE.SESSIONERR, 'errmsg': '用户未登录'})