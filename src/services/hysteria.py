import logging
from pathlib import Path
from typing import Any, Dict

import docker
from docker.errors import NotFound, DockerException
from ruamel.yaml import YAML

from src.core.config import settings

logger = logging.getLogger(__name__)


class HysteriaConfigService:
    def __init__(self, config_path: Path = settings.hysteria.config_path):
        self.config_path = config_path
        self.yaml = YAML()
        self.yaml.preserve_quotes = True
        self.yaml.indent(mapping=2, sequence=4, offset=2)
        self.docker_client = None
        try:
            self.docker_client = docker.from_env()
        except DockerException as e:
            logger.warning(f"Could not connect to Docker daemon: {e}")
        
        self._ensure_config_exists()

    def _ensure_config_exists(self) -> None:
        """Create default config if it doesn't exist or is empty."""
        if not self.config_path.exists() or self.config_path.stat().st_size == 0:
            logger.info(f"Config file not found or empty at {self.config_path}, creating default...")
            default_config = {
                "listen": settings.hysteria.listen_port,
                "acme": {
                    "domains": [settings.hysteria.acme_domain],
                    "email": settings.hysteria.acme_email
                },
                "auth": {
                    "type": "userpass",
                    "userpass": {}
                },
                "masquerade": {
                    "type": "proxy",
                    "proxy": {
                        "url": settings.hysteria.masquerade_url,
                        "rewriteHost": True
                    }
                }
            }
            self._save_config(default_config)

    def _reload_service(self) -> None:
        """Restart the Hysteria container to apply changes."""
        if not self.docker_client:
            logger.warning("Docker client not initialized, skipping reload")
            return

        container_name = settings.hysteria.container_name
        try:
            container = self.docker_client.containers.get(container_name)
            # Hysteria 2 supports hot reload via SIGHUP? 
            # Docs say: "Send SIGHUP to the process to reload the config file."
            # Let's try SIGHUP first, fallback to restart if needed.
            # But for simplicity and robustness, restart is often safer if connections drop anyway.
            # Let's use restart for now as it's guaranteed to work.
            container.restart()
            logger.info(f"Container {container_name} restarted successfully")
        except NotFound:
            logger.error(f"Container {container_name} not found")
        except Exception as e:
            logger.error(f"Failed to restart container {container_name}: {e}")

    def _load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found at {self.config_path}")
            
        with open(self.config_path, "r", encoding="utf-8") as f:
            return self.yaml.load(f) or {}

    def _save_config(self, config: Dict[str, Any]) -> None:
        with open(self.config_path, "w", encoding="utf-8") as f:
            self.yaml.dump(config, f)

    def get_users(self) -> Dict[str, str]:
        config = self._load_config()
        auth = config.get("auth", {})
        if not auth:
            return {}
        return auth.get("userpass") or {}

    def add_user(self, username: str, password: str) -> None:
        config = self._load_config()
        
        # Ensure structure exists
        if "auth" not in config:
            config["auth"] = {"type": "userpass", "userpass": {}}
        
        if config["auth"] is None:
             config["auth"] = {"type": "userpass", "userpass": {}}

        if "userpass" not in config["auth"] or config["auth"]["userpass"] is None:
            config["auth"]["userpass"] = {}

        config["auth"]["userpass"][username] = password
        self._save_config(config)
        self._reload_service()

    def remove_user(self, username: str) -> bool:
        config = self._load_config()
        auth = config.get("auth", {})
        userpass = auth.get("userpass")
        
        if userpass and username in userpass:
            del userpass[username]
            self._save_config(config)
            self._reload_service()
            return True
        return False

    def get_connection_uri(self, username: str) -> str:
        config = self._load_config()
        auth: dict = config.get("auth", {})
        userpass: list = auth.get("userpass", {})
        
        if not userpass or username not in userpass:
            raise ValueError(f"User {username} not found")
            
        password: str = userpass[username]
        
        # Determine SNI
        sni = "google.com"
        if "acme" in config and "domains" in config["acme"] and config["acme"]["domains"]:
             sni: str = config["acme"]["domains"][0]
        elif "tls" in config and "sni" in config["tls"]:
             sni: str = config["tls"]["sni"]
             
        host = settings.hysteria.public_host
        port = settings.hysteria.public_port
        
        uri = f"hy2://{username}:{password}@{host}:{port}/?sni={sni}"
        
        if host in ["127.0.0.1", "localhost"]:
            uri += "&insecure=1"
            
        return uri

hysteria_service = HysteriaConfigService()
