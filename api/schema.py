from pydantic import BaseModel


class ProcessoInputDTO(BaseModel):
    numero: str
