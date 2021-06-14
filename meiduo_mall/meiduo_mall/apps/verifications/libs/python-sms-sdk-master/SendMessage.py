from ronglian_sms_sdk import SmsSDK

accId = '8a216da879f05833017a097b097e054f'
accToken = '93872037560749d7b870f5fc6e3983f4'
appId = '8a216da879f05833017a097b0a6e0556'


# def send_message(tid, mobile, datas):
#     sdk = SmsSDK(accId, accToken, appId)
#     tid = tid
#     # mobile = '15750972731'
#     # datas = ('1375', '30s')
#     mobile = mobile
#     datas = datas
#     resp = sdk.sendMessage(tid, mobile, datas)
#     print(resp)

class CCP(object):

    def __new__(cls, *args, **kwargs):

        if not hasattr(cls, '_instance'):

            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            cls._instance.sdk = SmsSDK(accId, accToken, appId)

        return cls._instance

    def send_sms(self, tid, mobile, datas):

        result = self.sdk.sendMessage(tid, mobile, datas)
        print(result)

# datas = ('1376', '30s')
# CCP().send_sms('1', '15750972731', datas)