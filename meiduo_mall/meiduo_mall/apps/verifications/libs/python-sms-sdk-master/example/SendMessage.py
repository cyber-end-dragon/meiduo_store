from ronglian_sms_sdk import SmsSDK

accId = '8a216da879f05833017a097b097e054f'
accToken = '93872037560749d7b870f5fc6e3983f4'
appId = '8a216da879f05833017a097b0a6e0556'

def send_message():
    sdk = SmsSDK(accId, accToken, appId)
    tid = '登录验证模板'
    mobile = '15750972731'
    datas = ('1374', '30s')
    resp = sdk.sendMessage(tid, mobile, datas)
    print(resp)

resp = send_message()
print(resp)
