# Configure .env file
Write your bot token, server url and DB url
```shell
cp app/.env_template app/.env
vim app/.env
```
# Docker-compose
*Docker compose V1:*
```shell
docker-compose build
docker-compose up
```
*Docker compose V2:*
```shell
docker compose build
docker compose up
```