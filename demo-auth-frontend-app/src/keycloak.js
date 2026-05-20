import Keycloak from "keycloak-js";

const keycloak = new Keycloak({
  url: import.meta.env.VITE_KC_BASE_URL,
  realm: import.meta.env.VITE_KC_REALM,
  clientId: import.meta.env.VITE_KC_APP_CLIENT_ID,
});

export default keycloak;