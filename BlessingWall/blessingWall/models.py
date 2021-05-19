from datetime import datetime
from blessingWall import db

class Bless(db.Model):
    # 定义表名
    __tablename__ = 'blessings'
    # 定义字段
    id = db.Column(db.Integer, primary_key = True,autoincrement=True)
    bless = db.Column(db.String(255),default = '',nullable=False)
    state = db.Column(db.Integer,default = 0,nullable=False)
    time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)
    name = db.Column(db.String(10),default = '',nullable=False)
    banji = db.Column(db.String(20),default = '')

    #repr()方法显示一个可读字符串
    def __repr__(self):
        return '<Bless: %s %s %s %s %s %s>' % (self.id, self.bless, self.state, self.time,self.name,self.banji)

    def to_basic_dict(self):
        """将基本信息转换为字典数据"""
        bless_dict = {
            "id": self.id,
            "bless": self.bless,
            "state": self.state,
            "name": self.name,
            "banji": self.banji,
            "time": self.time.strftime('%Y-%m-%d %H:%M:%S')
        }
        return bless_dict

class AccessToken(db.Model):
    # 定义表名
    __tablename__ = 'accesstokens'
    # 定义字段
    id = db.Column(db.Integer, primary_key = True,autoincrement=True)
    token = db.Column(db.String(255),default = '',nullable=False)
    lifetime = db.Column(db.DateTime,default=datetime.now)

    #repr()方法显示一个可读字符串
    def __repr__(self):
        return '<Bless: %s %s %s>' % (self.id, self.token, self.lifetime)

    def get_date(self):
        delta = datetime.now() - self.lifetime
        if delta.total_seconds() < 6000:
            return True
        else:
            return False

class JsapiTicket(db.Model):
    # 定义表名
    __tablename__ = 'jsapitickets'
    # 定义字段
    id = db.Column(db.Integer, primary_key = True,autoincrement=True)
    token = db.Column(db.String(255),default = '',nullable=False)
    lifetime = db.Column(db.DateTime,default=datetime.now)

    #repr()方法显示一个可读字符串
    def __repr__(self):
        return '<Bless: %s %s %s>' % (self.id, self.token, self.lifetime)

    def get_date(self):
        delta = datetime.now() - self.lifetime
        if delta.total_seconds() < 6000:
            return True
        else:
            return False