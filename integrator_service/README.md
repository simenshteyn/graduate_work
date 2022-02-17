## Integrator Service


OpenAPI: [http://localhost/api/v1/docs](http://localhost/api/v1/docs)

**Setup**
1. Create .env file with sample:

`$ cp env.sample .env`

`$ vi .env`

**Run project without tests**

`$ docker-compose up --build -d`

**Testing**

`$ docker-compose --profile=testing up --build`

 - Clear docker containers with all data:
 
`$ docker-compose down -v`

**Celery Flower**:

Monitoring app at [http://localhost:5555](http://localhost:5555) (username: user, password: test).