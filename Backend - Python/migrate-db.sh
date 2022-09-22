python3.10 -m flask db merge heads

python3.10 -m flask db stamp head

python3.10 -m flask db migrate -m "Update data table"

python3.10 -m flask db upgrade
