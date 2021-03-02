# coding exercise

## Environment

Ubuntu 18.04
Python 3.7
Flask 1.1.2
uWSGI 2.0.19.1
MySQL 8.0.23

## Quick Start

Build and start containers for api server:

```bash
docker-compose up --build -d
```

Chech if server is alive:

```bash
curl http://localhost:5000/tasks/
```

## Testing

Run unit tests:

```bash
docker exec -it flask_ct flask test
```
