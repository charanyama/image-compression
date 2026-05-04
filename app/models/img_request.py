from pydantic import BaseModel


class CompressionParams(BaseModel):
    clusters: int = 5
