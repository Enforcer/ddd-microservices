# Setting up

## Prerequisites

- [docker](https://docs.docker.com/desktop/) or compatible tool (like [podman](https://podman.io/) or [colima](https://github.com/abiosoft/colima))
- [uv](https://docs.astral.sh/uv/) and Python 3.13 for local work without containers

## Build base image

First we build base image used by all the microservices:

```bash
docker compose build shell
```

NOTE: This is a convenience for the workshop. Normally, each microservice would have a separate image and dependencies.

## Pull the rest of images

```bash
docker compose pull tempo grafana tempo-init rabbitmq mongodb postgresdb prometheus mongo-express apicurio-registry apicurio-registry-ui
```

# Resetting

If you need to start fresh, remove all the containers with volumes:

```bash
<CTRL+C> / <CMD + C> (in running docker compose)
docker compose down -v
docker compose up
```
