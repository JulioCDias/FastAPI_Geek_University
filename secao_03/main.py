from typing import List, Optional
from fastapi import FastAPI
# tratando erros
from fastapi import HTTPException
from fastapi import status
from fastapi import Response
# utilizando o model
from models.curso import Curso


app = FastAPI()

cursos = {
    1: {
        "titulo": "Programação para leigos",
        "aulas": 112,
        "horas": 58
    },
    2: {
        "titulo": "Algoritimo e Logica de Programação",
        "aulas": 87,
        "horas": 67
    }
}


@app.get('/')
async def root():
    return {
        "Message": "Hello World!"
    }


@app.get('/cursos')
async def get_cursos():
    return cursos


@app.get('/cursos/{curso_id}')
async def get_curso(curso_id: int):
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(status_code=404, detail="Curso nao encontraddo")


@app.post('/cursos', status_code=201)
async def post_curso(curso: Curso):
    if curso.id not in cursos:
        next_id: int = len(cursos) + 1
        cursos[next_id] = curso
        del curso.id
        return curso
    else:
        raise HTTPException(
            status_code=409, detail=f"Ja existe um curso com o Id {curso.id}")


@app.put('/cursos/{curso_id}')
async def put_curso(curso_id: int, curso: Curso):
    if id in cursos:
        cursos[curso_id] = curso
        del curso.id
        return curso
    else:
        raise HTTPException(
            status_code=404, detail=f"Não exixte um curso com o Id {id}")


@app.delete('/cursos/{curso_id}')
async def delete_curso(curso_id: int):
    if curso_id in cursos:
        del cursos[curso_id]
        return Response(status_code=204)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Curso com ID {curso_id} não encontrado"
        )

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                log_level="info", reload=True)
