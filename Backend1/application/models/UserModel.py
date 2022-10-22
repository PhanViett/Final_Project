import uuid
import datetime
# from datetime import datetime
from application.models import db, pwd_context
from application.utils.helpers.string_processing_helper import clean_string
from ..app import bcrypt

from marshmallow import fields, Schema

from .PredictModel import PredictSchema


class UserModel(db.Model):
	__tablename__ = 'users'
	
	created_at = db.Column(db.BigInteger, default=int(datetime.datetime.utcnow().timestamp()), nullable=True)
	updated_at = db.Column(db.BigInteger, default=int(datetime.datetime.utcnow().timestamp()), nullable=True)
	deactive_at = db.Column(db.BigInteger, nullable=True)
	delete_at = db.Column(db.BigInteger, nullable=True)

	id = db.Column(db.Integer, primary_key=True)
	# tai_khoan_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tai_khoan.id"), nullable=True)
	ho = db.Column(db.String(80), nullable=True)
	ten = db.Column(db.String(80), nullable=True)
	ho_ten = db.Column(db.String(80), nullable=True)
	ten_khong_dau = db.Column(db.String(80), nullable=True)
	avatar_url = db.Column(db.String, nullable=True)
	ngay_sinh = db.Column(db.BigInteger, nullable=True)
	gioi_tinh = db.Column(db.String, nullable=True)
	dien_thoai = db.Column(db.String(12), nullable=True)
	ma_cong_dan = db.Column(db.String(80), nullable=True)
	ngay_cap = db.Column(db.BigInteger, nullable=True)
	noi_cap = db.Column(db.String(80), nullable=True)
	email = db.Column(db.String(80), nullable=True)

	dia_chi = db.Column(db.String, nullable=True)
	so_nha = db.Column(db.String, nullable=True)
	# tinh_thanh_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tinh_thanh.id"), nullable=True)
	# quan_huyen_id = db.Column(UUID(as_uuid=True), db.ForeignKey("quan_huyen.id"), nullable=True)
	# xa_phuong_id = db.Column(UUID(as_uuid=True), db.ForeignKey("xa_phuong.id"), nullable=True)

	vai_tro = db.Column(db.String, nullable=False)
	tai_khoan = db.Column(db.String, nullable=True)
	password = db.Column(db.String, nullable=True)
	active = db.Column(db.Boolean, default=True, nullable=False)

	predicts = db.relationship('PredictModel', backref='users', lazy=True)


def __init__(self, tai_khoan=None, password=None, ho=None, ten=None, avatar_url=None, ngay_sinh=None, gioi_tinh=None, dien_thoai=None, ma_cong_dan=None, email=None, active=None,
                ngay_cap=None, noi_cap=None, dia_chi=None, so_nha=None, tinh_thanh_id=None, quan_huyen_id=None, xa_phuong_id=None, vai_tro=None):
	self.id = uuid.uuid4()
	self.tai_khoan = tai_khoan
	self.password = self.__generate_hash(password)
	self.ho = ho
	self.ten = ten
	self.ho_ten = " ".join(filter(None, [ho, ten]))
	self.ten_khong_dau = clean_string(self.ho_ten)
	self.avatar_url = avatar_url
	self.ngay_sinh = ngay_sinh
	self.gioi_tinh = gioi_tinh
	self.dien_thoai = dien_thoai
	self.ma_cong_dan = ma_cong_dan
	self.email = email
	self.ngay_cap = ngay_cap
	self.noi_cap = noi_cap

	self.dia_chi = dia_chi
	self.so_nha = so_nha
	self.tinh_thanh_id = tinh_thanh_id
	self.quan_huyen_id = quan_huyen_id
	self.xa_phuong_id = xa_phuong_id

	self.vai_tro = vai_tro
	self.active = active

def __generate_hash(self, password):
	return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

def check_hash(self, password):
	return bcrypt.check_password_hash(self.password, password)

def save(self):
	db.session.add(self)
	db.session.commit()

def update(self, data):
	for key, item in data.items():
		if key == 'password': # add this new line
			self.password = self.__generate_hash(item) # add this new line
		setattr(self, key, item)
	self.updated_at = int(datetime.datetime.utcnow().timestamp())
	db.session.commit()

def delete(self):
	db.session.delete(self)
	db.session.commit()



@staticmethod
def get_all_users():
	return UserModel.query.all()

@staticmethod
def get_one_user(id):
	return UserModel.query.get(id)

def __repr(self):
	return '<id {}>'.format(self.id)


class UserSchema(Schema):
	"""
	User Schema
	"""
	id = fields.Int(dump_only=True)
	ten = fields.Str(required=True)
	email = fields.Email(required=True)
	password = fields.Str(required=True)
	created_at = fields.Int(dump_only=True)
	update_at = fields.Int(dump_only=True)
	predicts = fields.Nested(PredictSchema, many=True)