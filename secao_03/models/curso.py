from typing import Optional
from pydantic import BaseModel, validator


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int

    @validator('titulo')
    def validar_titulo(cls, value):
        palavras = value.split(' ')
        if len(palavras) < 3:
            raise ValueError("O titulo dev ter pelo menos 3 palavras")
        return value

    @validator('aulas')
    def validar_aulas(cls, value):
        quantidade = value
        if quantidade < 12:
            raise ValueError("A Quantidade de Aulas deve ser Maior do que 3.")
        return value

    @validator('horas')
    def validar_horas(cls, value):
        quantidade = value
        if quantidade < 10:
            raise ValueError("A Quantidade de horas deve ser Maior do que 3.")
        return value


cursos = [
    Curso(id=1, titulo="Programação para Leigos", aulas=190, horas=89),
    Curso(id=2, titulo="Algoritimos e Logica de Programação", aulas=52, horas=66),

]
