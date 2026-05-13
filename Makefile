DC = docker-compose
EXEC = docker exec -it
LOGS = docker logs
APP = docker/app.yml
APP_SERVICE = app
ENV = --env-file .env


# ------------------------------------------

.PHONY: app
app:
	${DC} -f ${APP} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP} down

.PHONY: app-logs
app-logs:
	${DC} -f ${APP} logs -f ${APP_SERVICE}

# ------------------------------------------