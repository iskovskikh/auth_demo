DC = docker-compose
EXEC = docker exec -it
LOGS = docker logs
APP = docker/app.yaml
KC = docker/keycloak.yaml
FRONTEND_APP_SERVICE = frontend
BACKEND_APP_SERVICE = backend
KC_SERVICE = keycloak
ENV = --env-file demo-auth-backend-app/.env

# ------------------------------------------

.PHONY: app
app:
	${DC} -f ${APP} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP} down

.PHONY: app-logs
app-logs:
	${DC} -f ${APP} logs -f ${BACKEND_APP_SERVICE}

.PHONY: app-frontend-logs
app-frontend-logs:
	${DC} -f ${APP} logs -f ${FRONTEND_APP_SERVICE}

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