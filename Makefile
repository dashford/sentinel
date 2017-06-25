all : up

up :
	docker-compose up -d

down :
	docker-compose down

app :
	docker-compose run --rm --no-deps python python /home/sentinel/sentinel.py

pip :
	docker-compose run --rm --no-deps python pip install -r /home/sentinel/requirements.txt
