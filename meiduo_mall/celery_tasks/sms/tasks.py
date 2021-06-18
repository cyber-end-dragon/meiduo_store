from celery_tasks.sms.python_sms_sdk import SendMessage
from . import constants
from celery_tasks.main import celery_app


# 定义任务
@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    # 发送短信验证码的异步任务
    message_data = (sms_code, constants.SMS_CODE_REDIS_EXPIRES//60)
    send_ret = SendMessage.CCP().send_sms(constants.SEND_SMS_TEMPLATE_ID, mobile, message_data)
    return send_ret
