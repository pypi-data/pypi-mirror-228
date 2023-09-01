import typer
from pathlib import Path
import json

from pydantic_settings import BaseSettings
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    nas_ip: str = "192.168.1.1"
    nas_port: str = "8080"
    nas_username: str = ""
    nas_password: str = ""
    nas_prefix: str = ""

    console_endpoint: str = ""
    console_token: str = ""

    model_config = SettingsConfigDict(
        env_file="env", env_file_encoding="utf-8")


APP_NAME = "v360-console-utility"


def init_settings():
    """
    Read settings from the config file
    """
    app_dir = typer.get_app_dir(APP_NAME)
    config_path: Path = Path(app_dir) / "config.json"
    if not config_path.is_file():
        typer.echo(f"Config file doesn't exists at {config_path}")
        raise typer.Exit()
    # parse config

    with open(config_path) as f:
        state = json.load(f)

    settings = Settings(nas_ip=state['nas']['ip'], nas_port=state['nas']['port'], nas_username=state['nas']['username'], nas_password=state['nas']
                        ['password'], nas_prefix=state['nas']['prefix'], console_endpoint=state['console']['endpoint'], console_token=state['console']['token'])
    return settings


settings = init_settings()
