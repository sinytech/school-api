# schools api

## Docker run

```
docker compose -f 'docker-compose.yml' up -d --build 
```

### List docker ENVIRONMENT variables set to the container

Run from the OS terminal
```
docker inspect -f \
    '{{range $index, $value := .Config.Env}}{{println $value}}{{end}}' \
    container_name
```



## ENVIRONMENT variables

Need to set everything in docker-compose.yml file for security reasons.

```
DATABASE_HOSTNAME = <docker-database-name>
DATABASE_PORT = 5432
DATABASE_PASSWORD = <password>
DATABASE_NAME = <db>
DATABASE_USERNAME = <user>
SECRET_KEY = 01c467dd1e55dc862fcbc0be6cc7393abd4af5e29c12f182737fb3e449ebbedc 
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7
```



## SECRET_KEY
SECRET_KEY = 01c467dd1e55dc862fcbc0be6cc7393abd4af5e29c12f182737fb3e449ebbedc 

To generate run command
```
openssl rand -hex 32
```


## Alembic

This is database revision manager. Run it in the server docker side in /app root project folder.

### Create new revision

- 1. Define/update model/entity
- 2. Create new revision and name with hunman name
```
alembic revision --autogenerate -m "Create user"

Note: --autogenerate - auto check the models/entities for a changes
```

- 3. Apply it to sync the database

```
alembic upgrade head
```




## GitHub mirroring
```
git push --mirror <URL_GITHUB_REPO>
```



