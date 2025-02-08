import logging
from fastapi import FastAPI, HTTPException, status, Depends
from src.api.schemas.query import Query
from src.rag.retrivier import Retrivier
from src.rag.generator import Generator
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


retrivier = Retrivier()
generator = Generator()


app = FastAPI(lifespan=lifespan)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='./bot.log',
    filemode='a'
)
logger = logging.getLogger('api')


@app.get('/')
async def main():
    return {"Trauma"}


@app.post('/query')
async def query_answer(query: Query = Depends()):
    try:
        context = await retrivier.get_context(query.question)
        answer = await generator.generate_answer(
            question=query.question,
            context=context
        )
        return {'answer': answer}
    except Exception as e:
        logger.log(msg=f'Error processing request: {str(e)}', level=logging.ERROR)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Interval Server Error')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
