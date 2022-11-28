from application.commons.pagination import paginate
from application.extensions import db
from application.models.record import Records
from application.schemas.record import RecordSchema
from application.utils.resource.http_code import HttpCode
from flask import jsonify, request
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource

import numpy as np
import pickle


class RecordGetList(Resource):
    @ jwt_required()
    def post(self):
        schema = RecordSchema(many=True)
        query = Records.query.order_by(Records.created_at.desc())
        data = request.json
        
        if not data:
            return paginate(query, schema), HttpCode.OK

        if data.get("status"):
            query = query.filter(Records.result == data.get("status"))

        if data.get("id"):
            query = query.filter(Records.user_id == data.get("id"))

        query = query
        res = paginate(query, schema)

        if len(res["results"]) < 1:
            return {
                "msg": "Người dùng này không có lịch sử chẩn đoán!!"
            }, HttpCode.OK
        elif len(res["results"]) >= 1:
            for x in res["results"]:
                a = Records.query.filter(Records.id == x["id"]).first()
                x["created_at"] = a.created_at

        return res, HttpCode.OK


class RecordCreate(Resource):
    @jwt_required()
    def post(self):
        req = {
            "tuoi": request.json.get("tuoi"),
            "gioi_tinh": request.json.get("gioi_tinh"),
            "height": request.json.get("height"),
            "weight": request.json.get("weight"),
            "ap_hi": request.json.get("ap_hi"),
            "ap_lo": request.json.get("ap_lo"),
            "chol": request.json.get("chol"),
            "gluc": request.json.get("gluc"),
            "smoke": request.json.get("smoke"),
            "alco": request.json.get("alco"),
            "active": request.json.get("active"),
            "result": request.json.get("result")
        }

        record = Records( tuoi=req["tuoi"], gioi_tinh=req["gioi_tinh"], height=req["height"], 
                          weight=req["weight"], ap_hi=req["ap_hi"], ap_lo=req["ap_lo"], 
                          chol=req["chol"], gluc=req["gluc"], smoke=req["smoke"], alco=req["alco"], 
                          active=req["active"], result=req["result"])
        
        record.user_id = current_user.id

        db.session.add(record)
        db.session.commit()
        
        return jsonify({"status": "SUCCESS", "msg": "Thông tin chẩn đoán được lưu trữ thành công"})


class RecordDelete(Resource):
    def delete(self, id):
        record = Records.query.filter(Records.id == id).first()

        if record is None:
            return jsonify({"status": "FAILED", "msg": "Thông tin chẩn đoán không tồn tại trong hệ thống"}), HttpCode.BadRequest
        
        db.session.delete(record)
        db.session.commit()

        return {"msg": "Xóa thông tin chẩn đoán thành công!"}, HttpCode.OK


class RecordPredict(Resource):
    @jwt_required()
    def post(self):
        model = pickle.load(open('model.pkl', 'rb'))

        features = [float(i) for i in request.form.values()]

        array_features = [np.array(features)]
        
        prediction = model.predict(array_features)

        output = prediction
        req = {
            "tuoi": request.form.get("age"),
            "gioi_tinh": request.form.get("gender"),
            "height": request.form.get("height"),
            "weight": request.form.get("weight"),
            "ap_hi": request.form.get("ap_hi"),
            "ap_lo": request.form.get("ap_lo"),
            "chol": request.form.get("chol"),
            "gluc": request.form.get("gluc"),
            "smoke": request.form.get("smoke"),
            "alco": request.form.get("alco"),
            "active": request.form.get("active"),
        }

        record = Records( tuoi=req["tuoi"], gioi_tinh=req["gioi_tinh"], height=req["height"], 
                          weight=req["weight"], ap_hi=req["ap_hi"], ap_lo=req["ap_lo"], 
                          chol=req["chol"], gluc=req["gluc"], smoke=req["smoke"], alco=req["alco"], 
                          active=req["active"], result=int(output[0]))
        
        record.user_id = current_user.id

        db.session.add(record)
        db.session.commit()

        if output == 1:
            return ({'result':'Sức khỏe của bạn rất bình thường.'})
        else:
            return ({'result':'Bạn có nguy cơ gặp vấn đề liên quan đến bệnh tim.'})
