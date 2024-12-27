## Build docker 
docker-compose up --build

##  Stop compose 
docker-compose down -v

---
## Create env
POSTGRES_PORT=5432
POSTGRES_PASSWORD=1234
POSTGRES_USER=admin
POSTGRES_DB=iot_events
RABBITMQ_USER=user
RABBITMQ_PASSWORD=guest
REDIS_HOST=redis
REDIS_PORT=6379
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672

### If there is a 403 user connection error, follow this guide.
https://docs.google.com/document/d/1uHlzu-p2eFq4PlwV05WQcxa274rIzSV63dcXWCC4xrE/edit?usp=sharing