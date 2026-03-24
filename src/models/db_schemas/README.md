## Run Alembic Migrations

### configuration

```bash
$ cp alembic.ini.example alembic.ini    
```

- update the `alembic.ini` with you database credentials `sqlalchemy.url`

### (optional) create a new migration

```bash
alembic revision --autogenerate -m "ADD ..."
```

### Upgrade the database

```bash
alembic upgrade head
```