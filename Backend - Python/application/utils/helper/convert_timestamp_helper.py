from datetime import datetime, timedelta, date
from marshmallow import pre_dump, validate, fields
import time

def convert_timestamp(date):
    if isinstance(date, fields.DateTime):
        date = str(date)
        datetime_object = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    elif isinstance(date, str):
        date: str = date
        datetime_object = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
    millisec = datetime_object.timestamp() * 1000

    return int(millisec)

def current_milli_time():
    return round(time.time() * 1000)

def plus_time(time_day):
    end_date = datetime.now() + timedelta(days=time_day)
    millisec = end_date.timestamp() * 1000

    return millisec


def convert_milisec(milisec):
    if isinstance(milisec, int):
        date = datetime.datetime.fromtimestamp(milisec/1000.0)
