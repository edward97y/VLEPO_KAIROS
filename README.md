# VLEPO KAIROS

## Requirements
- Python 3.12.3
### Create New Environment
1) python -m venv vlepo
2) activate the env using: 
```bash
$ source vlepo/bin/activate
```
## Installation 


### if you are linux user you must do this first

```bash
$ sudo apt update
$ sudo apt install libpq-dev gcc python3-dev
```
### Install the required packages
```bash
$ pip install -r requirements.txt
```
# install postgresql  by using 
```bash
$ sudo apt install postgresql
```
### setup the environment variable
```bash
$ cp .env.example .env
```

## Run the FastAPI Server
```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
## Run Docker Compose Services
```bash
$ cd docker
$ cp .env.example .env
```
## update .env with your credentials
```bash
$ docker compose -f 'docker/docker-compose.yml' up -d --build
```
