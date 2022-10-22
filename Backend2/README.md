# How to run project

pip3 install -r requirements.txt

python3 -m flask run

# Apt document

http://127.0.0.1:5000/swagger-ui

# flask-migrate ( update table - add columms)

flask db merge heads

flask db stamp head

flask db migrate -m "Update data table"

flask db upgrade

# FUNCTION SEARCH

search user information by First Name and Phone Number

# Validate

last_name - max 80 characters

first_name - max 80 characters

phone - max 11 characters

address - max 300 characters


Cách sử dụng tags

https://youtu.be/tlSagaeB0JY?t=1337

#debug dev

xem log service
http://10.14.141.23:9009/#!/auth
admin/123456

#minio
10.14.141.23:9001
minio
minio123

#flask run port 
flask run --host=0.0.0.0 --port=7778


#RabbitMQ 
http://10.14.141.23:15672
admin
123456

https://learnk8s.io/scaling-celery-rabbitmq-kubernetes