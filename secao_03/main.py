from typing import List, Optional, Any, Dict
from fastapi import FastAPI
# tratando erros
from fastapi import HTTPException
from fastapi import status
from fastapi import Response
from fastapi import Path
from fastapi import Query
from fastapi import Header
from fastapi import Depends
# utilizando o model
from models.curso import Curso
from models.curso import cursos
# Imports diversos
from time import sleep
import asyncio


# FastAPi Chama Await automaticamente ao usar depends
async def fake_db():
    try:
        print("Abrindo conexao com o banco de dados...")
        await asyncio.sleep(1)
    finally:
        print("fecahndo Conexão com o Banco de Dados")
        await asyncio.sleep(1)


app = FastAPI(
    title="API de Cursos da Geek University",
    version="0.0.1",
    description="Uma API Para Estudo do FastAPI"
)


@app.get('/', description="Retorna a Rota Riz da API", summary="Exemplo de Summary")
async def root():
    return {
        "Message": "Hello World!"
    }


@app.get('/cursos',
         description="Retorna Todos os Cursos ou uma lista vazia",
         summary="Retorna Todos os Cursos",
         response_model=List[Curso],
         response_description="Cursos Encontrados com Sucesso!.")
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos


@app.get('/cursos/{curso_id}',
         description="Retorna um Cursos com ID especifico ou vazio",
         summary="Retorna um curso com Id especifico",
         response_model=Curso)
async def get_curso(curso_id: int = Path(default=None, title='Id do Curso', description='Deve ser entre 1 e 2', gt=0, lt=3), db: Any = Depends(fake_db)):
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(status_code=404, detail="Curso nao encontraddo")


@app.post('/cursos', status_code=201,
          description="Cria um Cursos com novo ID",
          summary="Cria um novo Curso",
          response_model=Curso,
          response_description="Curso Criado com Sucesso!.")
async def post_curso(curso: Curso, db: Any = Depends(fake_db)):
    if curso.id not in cursos:
        next_id: int = len(cursos) + 1
        curso.id = next_id
        cursos.append(curso)
        return curso
    else:
        raise HTTPException(
            status_code=409, detail=f"Ja existe um curso com o Id {curso.id}")


@app.put('/cursos/{curso_id}',
         description="Edita recursos de um Curso com ID especifico",
         summary="Editar um Curso",
         response_model=Curso,
         response_description="Curso Editado com Sucesso!.")
async def put_curso(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        cursos[curso_id] = curso
        del curso.id
        return curso
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Não existe um curso com o ID {curso_id}"
        )


@app.delete('/cursos/{curso_id}',
            description="Deleta um Curso com ID especifico",
            summary="deletar um Curso",
            response_description="Curso Deletado com Sucesso!.")
async def delete_curso(curso_id: int, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        del cursos[curso_id]
        return Response(status_code=204)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Curso com ID {curso_id} não encontrado"
        )


# Exemplo de query parameters
@app.get('/calculadora')
async def calculadora(a: int = Query(default=None, gt=5), b: int = Query(default=None, gt=10), x_geek: str = Header(default=None), c: Optional[int] = None):
    if c:
        soma = a + b + c
    else:
        soma = a + b
    print(f"X-geek: {x_geek}")
    return {"Resultado": soma}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                log_level="info", reload=True)
