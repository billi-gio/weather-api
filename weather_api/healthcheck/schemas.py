from pydantic import BaseModel


class ServiceHealthcheck(BaseModel):
    service: str
    environment: str
