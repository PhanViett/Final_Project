import pytz
from datetime import datetime
from marshmallow import pre_dump, validate, fields


def convert_timestamp(date):
    if isinstance(date, fields.DateTime):
        date = str(date)
        datetime_object = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    elif isinstance(date, str):
        date: str = date
        datetime_object = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
    millisec = datetime_object.timestamp() * 1000

    return int(millisec)


def convert_milisec(milisec):
    if isinstance(milisec, int):
        date = datetime.datetime.fromtimestamp(milisec/1000.0)


def get_current_time(type):
    tzHCM = pytz.timezone("Asia/Ho_Chi_Minh")
    timeInHCM = datetime.now(tzHCM)
    timeInHCM_str = timeInHCM.strftime("%Y-%m-%d %H:%M:%S")
    timeInHCM_int = datetime.strptime(timeInHCM_str, "%Y-%m-%d %H:%M:%S")

    if type == "str":
        return timeInHCM_str
    else:
        return round(timeInHCM_int.timestamp() * 1000)
