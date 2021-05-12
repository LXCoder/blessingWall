from . import api
from flask import current_app,request,jsonify,session
from blessingWall import db,constants
from blessingWall.models import Bless,JsapiTicket,AccessToken
from blessingWall.utils.response_code import RET
from blessingWall.utils.commons import login_required,createNonceStr,getJsApiTicket

import hashlib,time,json

# 登录功能
@api.route("/sessions",methods=['POST'])
def login():

    # 获取请求的json数据，返回字典
    req_dict = request.get_json()

    username = req_dict.get("username")
    password = req_dict.get("password")
    # 校验参数
    if not all([username,password]):
        return jsonify(errno=RET.PARAMERR, errmsg="用户名或密码不能为空")
    
     # 登陆成功，创建一个session，并跳转到后台首页
    if username == "admin" and password == "admin":
        session['user_id'] = 'admin'
        session.permanent = True
    else:
        return jsonify(errno=RET.LOGINERR, errmsg="用户名或密码错误")

    # 返回结果
    return jsonify(errno=RET.OK, errmsg="登陆成功")

# 退出系统
@api.route("/session", methods=["DELETE"])
def logout():
    """登出"""
    # 清除session数据
    csrf_token = session.get("csrf_token")
    session.clear()
    session["csrf_token"] = csrf_token
    return jsonify(errno=RET.OK, errmsg="OK")

# 留言功能
@api.route("/blessing",methods=['POST'])
def blessing():

    # 获取请求的json数据，返回字典
    req_dict = request.get_json()

    name = req_dict.get("name").strip()
    banji = req_dict.get("banji").strip()
    comment = req_dict.get("comment").strip()
    # 校验参数
    if not comment:
        return jsonify(errno=RET.PARAMERR, errmsg="祝福语不能为空")
    
    if len(comment) == 0:
        return jsonify(errno=RET.PARAMERR, errmsg="祝福语不能为空")

    bless = Bless(bless=comment)
    if name:
        bless.name = name
    if banji:
        bless.banji = banji
    # 查询该祝福语是否存在
    _bless = Bless.query.filter(Bless.bless == comment).first()
    
    if _bless:  # 若存在的话
        if _bless.state == 2:       # 它的状态为屏蔽，返回错误
            return jsonify(errno=RET.PARAMERR, errmsg="祝福语含有敏感词汇")
        elif _bless.state == 1:     # 它的状态为通过，修改将要插入的祝福语状态并提交到数据库
            bless.state = 1
    try:
        db.session.add(bless)
        db.session.commit()
    except Exception as e:
        # 数据库操作错误后的回滚
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="插入数据库异常")

    # 返回结果
    return jsonify(errno=RET.OK, errmsg="祝福成功")

# 获得祝福语
@api.route("/blesses")
@login_required
def getBless():
    # 获取参数
    state = request.args.get("state")
    page = request.args.get("page")

    # 若没有这些参数，取默认值
    if not state:
        state = 0
    
    if not page:
        page = 1
    
    state = int(state)
    page = int(page)

    try:
        paginate = Bless.query.filter(Bless.state == state).order_by(Bless.time.desc()).paginate(page=page,per_page=constants.PER_PAGE,error_out=False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据库异常")
    

    # 获取页面数据
    bless_li = paginate.items
    blesses = []
    for bless in bless_li:
        blesses.append(bless.to_basic_dict())
    
    # 获取总页数
    total_page = paginate.pages
    has_prev  = paginate.has_prev
    has_next = paginate.has_next
    page_li = list(paginate.iter_pages(2,2,3,2))

    return jsonify(errno=RET.OK, errmsg="OK", data={
        "total_page": total_page, 
        "current_page": page,
        "has_prev": has_prev,
        "has_next": has_next,
        "state": state,
        "blesses": blesses, 
        "page_li":page_li
    })
    

# 批处理通过、屏蔽祝福语状态
@api.route("/blesses",methods=["PUT"])
@login_required
def changeState():
    req_dict = request.get_json()

    state = req_dict.get("state")
    ids = req_dict.get("ids")

    if not all([state,ids]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    
    state = int(state)

    try:
        Bless.query.filter(Bless.id.in_(ids)).update({"state":state})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="更改数据异常")

    return jsonify(errno=RET.OK, errmsg="OK")

# 删除祝福语
@api.route("/blesses", methods=["DELETE"])
@login_required
def deleteBless():
    req_dict = request.get_json()
    ids = req_dict.get("ids")

    if ids is None:
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    try:
        Bless.query.filter(Bless.id.in_(ids)).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="删除数据异常")

    return jsonify(errno=RET.OK, errmsg="OK")

# 获取微信公众号平台的数字签名算法
@api.route('/signpackage',methods=["POST"])
def signpackage() :
    #获得jsapi_ticket
    jsapiTicket = getJsApiTicket()
 
    # 注意 URL 一定要动态获取，不能 hardcode.
    #获取当前页面的url
    req_dict = request.get_json()
    url = req_dict.get("url")

    #获取timestamp（时间戳）
    timestamp = int(time.time())
    #获取noncestr（随机字符串）
    nonceStr = createNonceStr()
 
    #这里参数的顺序要按照 key 值 ASCII 码升序排序
    #得到signature
    #$signature = hashlib.sha1(string).hexdigest();
    ret = {
        'nonceStr': nonceStr,
        'jsapi_ticket': jsapiTicket,
        'timestamp': timestamp,
        'url': url
     }
 
    string = '&'.join(['%s=%s' % (key.lower(), ret[key]) for key in sorted(ret)])
    signature = hashlib.sha1(string.encode("utf8")).hexdigest()
 
    signPackage = {
        "appId": constants.WX_APPID,
        "nonceStr":nonceStr,
        "timestamp":timestamp,
        "url":url,
        "signature":signature,
        "rawString":string
    }
    return json.dumps(signPackage, sort_keys=True)
 



