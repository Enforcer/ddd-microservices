# Set up

## Prerequisites

To work with the repo one needs to have:
- docker (updated so `docker compose` is available)
- favourite code editor
- (optionally) Python 3.11 locally to work with code without containers

## Build base image

First we build base image used for all the microservices.
```bash
docker compose build shell
```

NOTE: This is a convenience for the workshop. Normally, each microservice would have separate image and dependencies.

## Pull the rest of images
```bash
docker compose pull mongodb redis postgresdb rabbitmq mongo-express zipkin prometheus grafana
```

# Start everything up
(all code is autoreloaded on changes)
```bash
docker compose up
```

# Resetting

If you need to start fresh, remove all the containers with volumes:

```bash
<CTRL+C> / <CMD + C> (in running docker compose)
docker compose down -v
docker compose up
```

# Running services

```bash
docker compose up <service>
```
where service is one of `availability`, `items`, `negotiations`

## Accessing services

### Items
`http://localhost:8100/docs`

### Negotiations
`http://localhost:8200/docs`

### Availability
`http://localhost:8300/docs`

# Running tests

```bash
docker compose run <service> pytest
```
where service is one of `availability`, `items`, `negotiations`

