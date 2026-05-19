# AuthDemoApp 

В этом репо представлено демо работы приложения с keycloak


## Источники

- https://www.keycloak.org/server/containers
- https://habr.com/ru/companies/amvera/articles/907990/
- https://slurm.io/blog/keycloak-chto-ehto-i-kak-rabotaet
- https://worksolutions.ru/blog/keycloak-nastrojka-mnogourovnevoj-autentifikaczii/



```shell
# export real and users

docker exec -it docker-keycloak-1 /opt/keycloak/bin/kc.sh export --dir /tmp/export --realm auth-demo-realm --users realm_file

docker cp docker-keycloak-1:/tmp/export ./assets
```