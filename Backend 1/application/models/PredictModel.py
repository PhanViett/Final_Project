import datetime
# from datetime import datetime
from marshmallow import fields, Schema
from . import db

class PredictModel(db.Model):
  __tablename__ = 'predicts'

  created_at = db.Column(db.BigInteger, default=int(datetime.datetime.utcnow().timestamp()), nullable=True)
  updated_at = db.Column(db.BigInteger, default=int(datetime.datetime.utcnow().timestamp()), nullable=True)
	
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

  result = db.Column(db.Boolean, nullable=True)

  def __init__(self, user_id=None, result=None):
    self.user_id = user_id
    self.result = result

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      setattr(self, key, item)
    self.updated_at = int(datetime.datetime.utcnow().timestamp())
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  @staticmethod
  def get_all_predicts():
    return PredictModel.query.all()
  
  @staticmethod
  def get_one_predict(id):
    return PredictModel.query.get(id)

  def __repr__(self):
    return '<id {}>'.format(self.id)


class PredictSchema(Schema):
  id = fields.Int(dump_only=True)
  user_id = fields.Int(required=True)
  created_at = fields.Int(dump_only=True)
  updated_at = fields.Int(dump_only=True)
