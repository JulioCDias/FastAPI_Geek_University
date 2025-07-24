from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def root():
    return {
        "message": "Hello World!"
    }


@app.get('/msg')
async def menssagem():
    return {
        "message": "Rota de menssagem"
    }


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                log_level="info", reload=True)
