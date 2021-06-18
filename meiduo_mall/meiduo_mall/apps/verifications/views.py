from django.shortcuts import render
from django.views import View
from django import http
from django_redis import get_redis_connection
import random, logging

from verifications.libs.captcha.captcha import captcha
from verifications.libs.python_sms_sdk import SendMessage
from meiduo_mall.utils.response_code import RETCODE
from . import constants
# Create your views here.

# Create log
logger = logging.getLogger('django')


class SMSCodeView(View):

    def get(self, request, mobile):

        # 接收参数
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('uuid')

        # 校验参数
        if not all([image_code_client, uuid]):
            return http.HttpResponseForbidden('缺少参数')

        # 创建redis对象
        redis_conn = get_redis_connection('verify_code')
        # 判断用户是否频繁发送短信验证码
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return http.JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '发送短信过于频繁'})

        # 提取图形验证码
        # redis_conn = get_redis_connection('verify_code')
        image_code_server = redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码失效'})

        # 删除图形验证码
        redis_conn.delete('img_%s' % uuid)

        # 对比图形验证码
        image_code_server = image_code_server.decode()
        if image_code_server.lower() != image_code_client.lower():
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '输入图形验证码有误'})

        # 生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)

        # 输出日志, 记录验证码
        logger.info(sms_code)

        # 保存短信验证码
        redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        redis_conn.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)

        # 发送短信验证码
        message_data = (sms_code, constants.SMS_CODE_REDIS_EXPIRES//60)
        SendMessage.CCP().send_sms(constants.SEND_SMS_TEMPLATE_ID, mobile, message_data)

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '发送短信成功'})




class ImageCodeView(View):

    def get(self, request, uuid):

        # 生成图形验证码
        text, image = captcha.generate_captcha()

        # 保存图形验证码
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_%s' % uuid, constants.IMAGE_CODE_REDIS_EXPIRES, text)

        # 响应图形验证码
        return http.HttpResponse(image, content_type='image/jpg')
