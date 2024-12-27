## to build docker 
docker-compose up --build

## to stop compose 
docker-compose down -v

---
## create env
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