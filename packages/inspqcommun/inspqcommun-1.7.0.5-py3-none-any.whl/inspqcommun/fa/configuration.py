import os
from inspqcommun.identity.keycloak_tools import KeycloakEnvironment

DEFAULT_LOG_LEVEL: str = "INFO"
DEFAULT_FILES_PATH: str = None
DEFAULT_FA_BASE_URL: str = 'http://localhost:8089'
DEFAULT_FA_BASE_URI: str = '/fa-services'
DEFAULT_KEYCLOAK_URL: str = 'http://keycloak.url/auth'
DEFAULT_KEYCLOAK_AUTH_REALM: str = 'msss'
DEFAULT_KEYCLOAK_AUTH_USER: str = 'PERMISSIONS'

class Configuration:

    def get_log_level(self, default_value=DEFAULT_LOG_LEVEL) -> str:
        return os.environ.get("LOG_LEVEL", default_value)

    def get_files_path(self, default_value=DEFAULT_FILES_PATH) -> str:
        return os.environ.get("FILES_PATH", default_value)

    def get_fonctions_allegees_url(self, default_value=DEFAULT_FA_BASE_URL) -> str:
        return os.environ.get("FA_BASE_URL", default_value)

    def get_fonctions_allegees_uri(self, default_value=DEFAULT_FA_BASE_URI) -> str:
        return os.environ.get("FA_BASE_URI", default_value)
    
    def get_keycloak_base_url(self, default_value=DEFAULT_KEYCLOAK_URL) -> str:
        url = os.environ.get("KEYCLOAK_BASE_URL", default_value) 
        return url if url.endswith("/auth") else url + "/auth"
        
    def get_keycloak_auth_realm(self, default_value=DEFAULT_KEYCLOAK_AUTH_REALM) -> str:
        return os.environ.get("KEYCLOAK_AUTH_REALM", default_value)
    
    def get_keycloak_auth_user(self, default_value=DEFAULT_KEYCLOAK_AUTH_USER) -> str:
        return os.environ.get("KEYCLOAK_AUTH_USER", default_value)

    def get_authorization_header(self) -> str:
        kcenv = KeycloakEnvironment(defaultAuthRealm=self.get_keycloak_auth_realm(), defaultAuthUser=self.get_keycloak_auth_user(), baseKeycloakUrl=self.get_keycloak_url(), keycloakEnabled=False)
        headers = kcenv.authenticate()
        return headers.get('Authorization')