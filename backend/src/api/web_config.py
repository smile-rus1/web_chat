from dataclasses import dataclass


@dataclass
class WebConfig:
    host: str
    port: int
    debug: bool
    api_v1_str: str
