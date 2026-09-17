from pydantic import BaseModel


class CofreCriar(BaseModel):
    nome: str
    senha_mestra: str


class SegredoCriar(BaseModel):
    titulo: str
    usuario: str | None = None
    url: str | None = None
    senha: str


class SegredoResposta(BaseModel):
    id: str
    titulo: str
    usuario: str | None = None
    url: str | None = None
    senha: str


class SegredoLista(BaseModel):
    id: str
    titulo: str
    usuario: str | None = None
    url: str | None = None