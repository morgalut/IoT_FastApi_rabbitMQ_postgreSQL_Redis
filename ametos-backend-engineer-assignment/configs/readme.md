


## Build docker 
docker-compose up --build -d

##  Stop compose 
docker-compose down -v


## If you can't ping
```
docker-compose exec postgres apt-get update && apt-get install -y iputils-ping

docker-compose exec postgres ping redis

docker-compose exec postgres bash -c "apt-get update && apt-get install -y iputils-ping"

docker-compose exec postgres ping redis

```
## Use cmd admin to run and install 
```choco install redis-64```
## Check Redis
```docker run -it --network=container:configs-redis-1 redis redis-cli -h redis```
```PING```
```
SET mykey "Hello"
GET mykey
```
---
## Create .env
```
POSTGRES_PORT=5432
POSTGRES_PASSWORD=newer_password
POSTGRES_USER=new_admin
POSTGRES_DB=iot_events
RABBITMQ_USER=user
RABBITMQ_PASSWORD=guest
REDIS_HOST=redis
REDIS_PORT=6379
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672 
```

### If there is a 403 user connection error, follow this guide.
https://docs.google.com/document/d/1uHlzu-p2eFq4PlwV05WQcxa274rIzSV63dcXWCC4xrE/edit?usp=sharing