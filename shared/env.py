from os import environ


def get_env_var(var_name: str) -> str:
    return environ[var_name]
