from werkzeug.routing import BaseConverter
from flask import session,jsonify,current_app
from blessingWall import constants
from blessingWall.utils.response_code import RET
from functools import wraps

import json,string,urllib,random

# 定义正则转换器
class ReConverter(BaseConverter):

    def __init__(self,url_map,regex):
        # 调用父类的初始化方法
        super(ReConverter,self).__init__(url_map)
        # 保存正则表达式
        self.regex = regex

# 定义的验证登录状态的装饰器
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            return jsonify(errno=RET.SESSIONERR,errmsg="用户未登录")
    return wrapper

# 获得随机字符串
def createNonceStr(length = 16):
    #获取noncestr（随机字符串）
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

# 获得jsapi_ticket
def getJsApiTicket():
    
    #获得jsapi_ticket之后，就可以生成JS-SDK权限验证的签名了
    #获取access_token
    from blessingWall.models import JsapiTicket
    try:
        ticket = JsapiTicket.query.order_by(JsapiTicket.lifetime.desc()).first()
        # 判断ticket是否为空和是否在有效期内
        if ticket and ticket.get_date():
            return ticket.token
    except Exception as e:
        current_app.logger.error(e)
 
    accessToken = accesstokens()
 
    #获取jsapi_ticket
    url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type=jsapi".format(accessToken)
    req = urllib.request.Request(url)
    res_data = urllib.request.urlopen(req)
    res = res_data.read().decode(encoding='utf-8')
    res = json.loads(res)
    # 插入新的ticket到数据库中
    _ticket = JsapiTicket(token = res['ticket'])

    from blessingWall import db

    try:
        db.session.add(_ticket)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
 
    return res['ticket']
 
# 获得accesstoken
def accesstokens():
    from blessingWall.models import AccessToken
    try:
        accesstoken = AccessToken.query.order_by(AccessToken.lifetime.desc()).first()
        # 判断token是否为空和是否在有效期内
        if accesstoken and accesstoken.get_date():
            return accesstoken.token
    except Exception as e:
        current_app.logger.error(e)

    url= 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(constants.WX_APPID,constants.WX_SECRET)
 
    req = urllib.request.Request(url)
    data = urllib.request.urlopen(req)
    res = data.read().decode(encoding='utf-8')
    res = json.loads(res)

    accessToken = res['access_token']
    
    token = AccessToken(token=accessToken)

    from blessingWall import db

    try:
        db.session.add(token)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)

    return accessToken