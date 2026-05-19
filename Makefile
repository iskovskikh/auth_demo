DC = docker-compose
EXEC = docker exec -it
LOGS = docker logs
APP = docker/app.yaml
KC = docker/keycloak.yaml
APP_SERVICE = app
KC_SERVICE = keycloak
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

# Keycloak Docker compose target
# Run Keycloak container defined in docker/keycloak.yaml

.PHONY: keycloak
keycloak:
	${DC} -f ${KC} up --build -d

.PHONY: keycloak-down
keycloak-down:
	${DC} -f ${KC} down


.PHONY: keycloak-logs
keycloak-logs:
	${DC} -f ${KC} logs -f ${KC_SERVICE}